# ml_model.py
# Trains a Linear Regression model on synthetic data to predict total CO2 emissions.
# The model learns the same emission relationships as the rule-based calculator,
# but can generalize to unseen input combinations.

import random
import pickle
import os
import numpy as np
import shap
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error

# Human-readable names for each feature (used in SHAP output)
FEATURE_NAMES = [
    "electricity_units",
    "fuel_litres",
    "lpg_cylinders",
    "transport_type",
    "shopping_level",
]

# --- Encoding maps (categorical → numeric) ---
# These must stay consistent between training and prediction.
TRANSPORT_ENCODING = {"bike": 0, "public_transport": 1, "car": 2}
SHOPPING_ENCODING  = {"low": 0, "medium": 1, "high": 2}

# Path to save/load the trained model
MODEL_PATH = "greenscore_model.pkl"


# ------------------------------------------------------------------ #
# STEP 1: Generate Synthetic Dataset
# ------------------------------------------------------------------ #

def generate_dataset(n_samples: int = 1000) -> tuple:
    """
    Creates a synthetic dataset of n_samples users.
    Features are randomly sampled within realistic monthly usage ranges.
    Target (total_emissions) is calculated using the same emission factors
    as calculator.py — this is what the model will learn to predict.

    Returns:
        X: list of feature rows  [electricity, petrol, lpg, transport_enc, shopping_enc]
        y: list of total emission values
    """
    # Emission factors (must match calculator.py)
    ELEC_FACTOR      = 0.82
    PETROL_FACTOR    = 2.30
    LPG_FACTOR       = 42.0
    TRANSPORT_VALUES = [0.0, 2.5, 41.0]   # bike, public_transport, car
    SHOPPING_VALUES  = [10.0, 30.0, 60.0] # low, medium, high

    X, y = [], []

    for _ in range(n_samples):
        elec      = random.uniform(0, 300)    # kWh
        petrol    = random.uniform(0, 100)    # litres
        lpg       = random.uniform(0, 5)      # cylinders
        transport = random.randint(0, 2)      # 0=bike, 1=public, 2=car
        shopping  = random.randint(0, 2)      # 0=low, 1=medium, 2=high

        # Calculate total emissions (same formula as calculator.py)
        total = (
            elec    * ELEC_FACTOR +
            petrol  * PETROL_FACTOR +
            lpg     * LPG_FACTOR +
            TRANSPORT_VALUES[transport] +
            SHOPPING_VALUES[shopping]
        )

        X.append([elec, petrol, lpg, transport, shopping])
        y.append(round(total, 2))

    return X, y


# ------------------------------------------------------------------ #
# STEP 2: Train the Model
# ------------------------------------------------------------------ #

def train_model() -> LinearRegression:
    """
    Generates synthetic data, trains a Linear Regression model,
    prints evaluation metrics, and saves the model to disk.

    Returns:
        Trained LinearRegression model
    """
    print("Generating synthetic dataset...")
    X, y = generate_dataset(n_samples=1000)

    # Split into 80% training, 20% testing
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )

    # Train Linear Regression
    model = LinearRegression()
    model.fit(X_train, y_train)

    # Evaluate on test set
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print(f"Model trained. Mean Absolute Error on test set: {mae:.2f} kg CO2")

    # Save model to disk so it doesn't retrain every run
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"Model saved to {MODEL_PATH}")

    # Save a sample of training data as SHAP background dataset
    # SHAP uses this to compute baseline (expected) feature contributions
    background = np.array(X_train[:100])
    with open("greenscore_background.pkl", "wb") as f:
        pickle.dump(background, f)

    return model


def load_model() -> LinearRegression:
    """
    Loads the trained model from disk.
    If no saved model exists, trains a new one first.
    """
    if not os.path.exists(MODEL_PATH):
        print("No saved model found. Training now...")
        return train_model()

    with open(MODEL_PATH, "rb") as f:
        model = pickle.load(f)
    return model


# ------------------------------------------------------------------ #
# STEP 3: Predict Function
# ------------------------------------------------------------------ #

def predict_emissions(inputs: dict) -> float:
    """
    Predicts total monthly CO2 emissions using the trained ML model.

    Args:
        inputs: dict with keys:
            electricity_units (float)
            petrol_litres     (float)
            lpg_cylinders     (float)
            transport_type    (str: "bike" | "car" | "public_transport")
            shopping_habit    (str: "low" | "medium" | "high")

    Returns:
        Predicted total emissions in kg CO2 (float)
    """
    model = load_model()

    # Encode categorical inputs to numbers
    transport_enc = TRANSPORT_ENCODING.get(inputs["transport_type"], 0)
    shopping_enc  = SHOPPING_ENCODING.get(inputs["shopping_habit"], 0)

    # Build feature row — order must match training data
    features = [[
        inputs["electricity_units"],
        inputs["petrol_litres"],
        inputs["lpg_cylinders"],
        transport_enc,
        shopping_enc,
    ]]

    prediction = model.predict(features)[0]
    return round(max(0.0, prediction), 2)  # clamp to non-negative


# ------------------------------------------------------------------ #
# STEP 4: Explainability with SHAP
# ------------------------------------------------------------------ #

def explain_prediction(inputs: dict) -> dict:
    """
    Uses SHAP to explain how much each feature contributed to the
    predicted emission value for a given user input.

    SHAP (SHapley Additive exPlanations) assigns each feature a value
    that represents its contribution to the prediction relative to
    the average prediction across the background dataset.

    Args:
        inputs: same dict used by predict_emissions()

    Returns:
        {
            "contributions": { feature_name: shap_value, ... },
            "top_contributor": "feature_name"
        }
    """
    model = load_model()

    # Load background dataset (saved during training)
    bg_path = "greenscore_background.pkl"
    if not os.path.exists(bg_path):
        # If background not found, retrain to generate it
        train_model()
    with open(bg_path, "rb") as f:
        background = pickle.load(f)

    # Encode categorical inputs
    transport_enc = TRANSPORT_ENCODING.get(inputs["transport_type"], 0)
    shopping_enc  = SHOPPING_ENCODING.get(inputs["shopping_habit"], 0)

    # Build feature row as numpy array
    feature_row = np.array([[
        inputs["electricity_units"],
        inputs["petrol_litres"],
        inputs["lpg_cylinders"],
        transport_enc,
        shopping_enc,
    ]])

    # Create SHAP explainer using the background dataset
    # KernelExplainer works with any model — simple and model-agnostic
    explainer   = shap.KernelExplainer(model.predict, background)
    shap_values = explainer.shap_values(feature_row, silent=True)

    # Map feature names to their SHAP contribution values
    contributions = {
        name: round(float(val), 4)
        for name, val in zip(FEATURE_NAMES, shap_values[0])
    }

    # Identify the feature with the highest absolute contribution
    top_contributor = max(contributions, key=lambda k: abs(contributions[k]))

    return {
        "contributions": contributions,
        "top_contributor": top_contributor,
    }


# ------------------------------------------------------------------ #
# Run standalone to train and test
# ------------------------------------------------------------------ #
if __name__ == "__main__":
    train_model()

    sample = {
        "electricity_units": 120,
        "petrol_litres":      30,
        "lpg_cylinders":       2,
        "transport_type":   "car",
        "shopping_habit":  "medium",
    }

    result = predict_emissions(sample)
    print(f"\nSample prediction: {result} kg CO2")

    explanation = explain_prediction(sample)
    print(f"\nSHAP Contributions: {explanation['contributions']}")
    print(f"Top contributor:    {explanation['top_contributor']}")

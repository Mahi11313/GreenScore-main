# main.py
# Entry point for GreenScore — runs both rule-based and ML-based pipelines.

import json
from calculator import calculate_emissions
from scorer import calculate_green_score, get_score_label
from recommender import generate_recommendations
from ml_model import predict_emissions, explain_prediction

# --- User Inputs (hardcoded for Phase 3) ---
user_inputs = {
    "electricity_units": 120,
    "petrol_litres":      30,
    "lpg_cylinders":       2,
    "transport_type":   "car",
    "shopping_habit":  "medium",
}


def run_greenscore(inputs: dict) -> dict:
    """
    Runs the full GreenScore pipeline using both:
    - Rule-based calculation (exact, from calculator.py)
    - ML prediction (learned estimate, from ml_model.py)
    """
    # --- Rule-based path ---
    breakdown    = calculate_emissions(inputs)
    score        = calculate_green_score(breakdown["total"])
    label        = get_score_label(score)
    tips         = generate_recommendations(inputs, breakdown)

    # --- ML prediction path ---
    ml_predicted = predict_emissions(inputs)
    ml_score     = calculate_green_score(ml_predicted)
    ml_label     = get_score_label(ml_score)

    # --- XAI: SHAP explanation ---
    explanation  = explain_prediction(inputs)

    return {
        "rule_based": {
            "total_emissions": breakdown["total"],
            "green_score":     score,
            "score_label":     label,
            "breakdown": {
                "electricity_kg": breakdown["electricity"],
                "petrol_kg":      breakdown["petrol"],
                "lpg_kg":         breakdown["lpg"],
                "transport_kg":   breakdown["transport"],
                "shopping_kg":    breakdown["shopping"],
            },
            "recommendations": tips,
        },
        "ml_predicted": {
            "total_emissions": ml_predicted,
            "green_score":     ml_score,
            "score_label":     ml_label,
        },
        "explainability": {
            "feature_contributions": explanation["contributions"],
            "top_contributor":       explanation["top_contributor"],
        }
    }


if __name__ == "__main__":
    result = run_greenscore(user_inputs)
    print(json.dumps(result, indent=2))

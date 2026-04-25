# api.py
# FastAPI backend — exposes GreenScore logic as an HTTP endpoint.
# Run with: uvicorn api:app --reload

from fastapi import FastAPI
from pydantic import BaseModel
from typing import Literal

from calculator import calculate_emissions
from scorer import calculate_green_score, get_score_label
from recommender import generate_recommendations

app = FastAPI(title="GreenScore API", version="2.0.0")


# --- Request Schema ---
class UserInputRequest(BaseModel):
    electricity_units: float
    petrol_litres:     float
    lpg_cylinders:     float
    transport_type:    Literal["bike", "car", "public_transport"]
    shopping_habit:    Literal["low", "medium", "high"]


# --- Main Endpoint ---
@app.post("/calculate")
def calculate(user: UserInputRequest):
    """Accepts user inputs and returns emissions, score, and recommendations."""
    inputs = user.model_dump()

    breakdown      = calculate_emissions(inputs)
    score          = calculate_green_score(breakdown["total"])
    label          = get_score_label(score)
    recommendations = generate_recommendations(inputs, breakdown)

    return {
        "total_emissions": breakdown["total"],
        "green_score": score,
        "score_label": label,
        "breakdown": {
            "electricity_kg": breakdown["electricity"],
            "petrol_kg":      breakdown["petrol"],
            "lpg_kg":         breakdown["lpg"],
            "transport_kg":   breakdown["transport"],
            "shopping_kg":    breakdown["shopping"],
        },
        "recommendations": recommendations,
    }


@app.get("/health")
def health():
    return {"status": "ok"}

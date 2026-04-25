# storage.py
# Handles saving user inputs and results to a CSV file for history tracking.
# Each run appends a new row — existing data is never overwritten.

import csv
import os
from datetime import datetime

HISTORY_FILE = "history.csv"

# Column headers for the CSV file
HEADERS = [
    "timestamp",
    "mode",
    "electricity_units",
    "petrol_litres",
    "lpg_cylinders",
    "transport_type",
    "shopping_habit",
    "total_emissions_kg",
    "green_score",
    "score_label",
]


def save_result(inputs: dict, total_emissions: float, score: int, label: str, mode: str):
    """
    Appends one row of user inputs + results to history.csv.
    Creates the file with headers if it doesn't exist yet.

    Args:
        inputs          : user input dictionary
        total_emissions : calculated or predicted total CO2 (kg)
        score           : Green Score (300–850)
        label           : score label string
        mode            : "Rule-Based" or "ML-Based"
    """
    file_exists = os.path.exists(HISTORY_FILE)

    with open(HISTORY_FILE, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=HEADERS)

        # Write header only when creating the file for the first time
        if not file_exists:
            writer.writeheader()

        writer.writerow({
            "timestamp":          datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "mode":               mode,
            "electricity_units":  inputs["electricity_units"],
            "petrol_litres":      inputs["petrol_litres"],
            "lpg_cylinders":      inputs["lpg_cylinders"],
            "transport_type":     inputs["transport_type"],
            "shopping_habit":     inputs["shopping_habit"],
            "total_emissions_kg": total_emissions,
            "green_score":        score,
            "score_label":        label,
        })


def load_history() -> list:
    """
    Reads all past entries from history.csv.

    Returns:
        List of dicts, one per saved entry. Empty list if no history yet.
    """
    if not os.path.exists(HISTORY_FILE):
        return []

    with open(HISTORY_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        return list(reader)

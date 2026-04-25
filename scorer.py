# scorer.py
# Converts total CO2 emissions into a Green Score (300–850).
# Higher score = lower emissions = better for the environment.

# Score boundaries
MIN_SCORE = 300
MAX_SCORE = 850

# Emission ceiling — anyone at or above this gets the minimum score
MAX_EMISSIONS = 500  # kg CO2 per month


def calculate_green_score(total_emissions: float) -> int:
    """
    Maps total monthly emissions (kg CO2) to a score between 300 and 850.

    Formula:
        score = 850 - (emissions / 500) * 550
        clamped between 300 and 850
    """
    score = MAX_SCORE - (total_emissions / MAX_EMISSIONS) * (MAX_SCORE - MIN_SCORE)
    return int(max(MIN_SCORE, min(MAX_SCORE, score)))


def get_score_label(score: int) -> str:
    """Returns a human-readable label for the given Green Score."""
    if score >= 700:
        return "Excellent"
    elif score >= 550:
        return "Moderate"
    elif score >= 400:
        return "Needs Improvement"
    else:
        return "Critical"

# recommender.py
# Generates practical, rule-based recommendations based on emission breakdown.


def generate_recommendations(inputs: dict, breakdown: dict) -> list:
    """
    Analyzes the emission breakdown and user inputs to suggest improvements.

    Args:
        inputs   : original user input dictionary
        breakdown: emission breakdown from calculator.py

    Returns:
        A list of recommendation strings.
    """
    tips = []

    # --- Electricity ---
    if breakdown["electricity"] > 100:
        tips.append(
            "Your electricity usage is high. "
            "Switch to LED bulbs, use energy-efficient appliances, and unplug idle devices."
        )

    # --- Petrol / Fuel ---
    if breakdown["petrol"] > 50:
        tips.append(
            "Your fuel consumption is high. "
            "Consider carpooling, combining trips, or switching to an electric/hybrid vehicle."
        )

    # --- LPG ---
    if breakdown["lpg"] > 84:  # more than 2 cylinders per month
        tips.append(
            "You are using a lot of LPG. "
            "Try energy-efficient cookware, pressure cookers, or an induction stove."
        )

    # --- Transport ---
    if inputs.get("transport_type") == "car":
        tips.append(
            "You rely on a car for transport. "
            "Try public transport or cycling for short distances to cut emissions."
        )

    # --- Shopping ---
    if inputs.get("shopping_habit") == "high":
        tips.append(
            "Your shopping habits contribute to higher emissions. "
            "Buy only what you need and prefer sustainable or second-hand products."
        )

    # --- All good ---
    if not tips:
        tips.append("Great job! Your carbon footprint is low. Keep up the sustainable habits.")

    return tips

# calculator.py
# Handles all carbon emission calculations using standard emission factors.

# --- Emission Factors ---
ELECTRICITY_FACTOR = 0.82   # kg CO2 per kWh unit
PETROL_FACTOR      = 2.30   # kg CO2 per litre
LPG_FACTOR         = 42.00  # kg CO2 per cylinder

# Transport and shopping are flat monthly estimates (kg CO2)
TRANSPORT_EMISSIONS = {
    "bike":             0.0,
    "public_transport": 2.5,
    "car":             41.0,
}

SHOPPING_EMISSIONS = {
    "low":    10.0,
    "medium": 30.0,
    "high":   60.0,
}


def electricity_emissions(units: float) -> float:
    """Calculate CO2 emissions from electricity usage."""
    return round(units * ELECTRICITY_FACTOR, 2)


def fuel_emissions(litres: float) -> float:
    """Calculate CO2 emissions from petrol/fuel usage."""
    return round(litres * PETROL_FACTOR, 2)


def lpg_emissions(cylinders: float) -> float:
    """Calculate CO2 emissions from LPG cylinder usage."""
    return round(cylinders * LPG_FACTOR, 2)


def transport_emissions(transport_type: str) -> float:
    """Return flat monthly CO2 estimate based on transport type."""
    return TRANSPORT_EMISSIONS.get(transport_type, 0.0)


def shopping_emissions(shopping_habit: str) -> float:
    """Return flat monthly CO2 estimate based on shopping habit."""
    return SHOPPING_EMISSIONS.get(shopping_habit, 0.0)


def calculate_emissions(inputs: dict) -> dict:
    """
    Takes a user input dictionary and returns a full emission breakdown.

    Expected keys in inputs:
        electricity_units, petrol_litres, lpg_cylinders,
        transport_type, shopping_habit
    """
    breakdown = {
        "electricity": electricity_emissions(inputs["electricity_units"]),
        "petrol":      fuel_emissions(inputs["petrol_litres"]),
        "lpg":         lpg_emissions(inputs["lpg_cylinders"]),
        "transport":   transport_emissions(inputs["transport_type"]),
        "shopping":    shopping_emissions(inputs["shopping_habit"]),
    }
    breakdown["total"] = round(sum(breakdown.values()), 2)
    return breakdown

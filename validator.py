# validator.py
# Validates user inputs before passing them to the calculation pipeline.
# Returns a list of error messages (empty list = all inputs are valid).

# Reasonable upper limits for monthly usage
LIMITS = {
    "electricity_units": (0, 2000),   # kWh
    "petrol_litres":     (0, 500),    # litres
    "lpg_cylinders":     (0, 20),     # cylinders
}


def validate_inputs(inputs: dict) -> list:
    """
    Checks inputs against defined limits.

    Args:
        inputs: user input dictionary

    Returns:
        List of error strings. Empty list means inputs are valid.
    """
    errors = []

    for field, (min_val, max_val) in LIMITS.items():
        value = inputs.get(field, 0)
        label = field.replace('_', ' ').title()
        if value < 0:
            # Explicit negative check — number_input min_value=0 prevents this in UI,
            # but we guard here for API / direct calls too
            errors.append(f"{label} cannot be negative. Please enter 0 or above.")
        elif value > max_val:
            errors.append(
                f"{label} value of {value} seems too high "
                f"(max allowed: {max_val}). Please double-check your entry."
            )

    return errors

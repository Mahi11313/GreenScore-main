from dataclasses import dataclass
from typing import Literal


@dataclass
class UserInput:
    electricity_units: float                          # kWh per month
    petrol_litres: float                              # litres per month
    lpg_cylinders: float                              # cylinders per month
    transport_type: Literal["bike", "car", "public_transport"]
    shopping_habit: Literal["low", "medium", "high"]

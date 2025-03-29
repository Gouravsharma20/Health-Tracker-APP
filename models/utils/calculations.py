# Utility functions for BMI and MDR calculations

# Function to calculate BMI
def calculate_bmi(weight: float, height: float) -> float:
    return weight / (height ** 2)

# Function to calculate Minimum Daily Requirement (MDR)
def calculate_mdr(weight: float, activity_level: float) -> float:
    return weight * activity_level * 1.2

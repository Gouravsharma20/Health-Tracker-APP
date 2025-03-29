# Utility functions for BMI calculations

def calculate_bmi(weight_kg: float, height_m: float) -> float:
    """Calculates Body Mass Index (BMI)."""
    return round(weight_kg / (height_m ** 2), 2)

def determine_bmi_category(bmi: float) -> str:
    """Determines the BMI category based on the BMI value."""
    if bmi < 18.5:
        return "🍃 Light as a Feather (Underweight)"
    elif 18.5 <= bmi < 24.9:
        return "💪 Peak Performance (Normal Range)"
    elif 25 <= bmi < 29.9:
        return "🍔 Enjoying Life (Overweight)"
    else:
        return "⚠️ Extra Cushioning (Obese)"

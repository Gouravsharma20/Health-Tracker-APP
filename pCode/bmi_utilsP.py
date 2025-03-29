from models import ClientType



def classify_client(weight: float, height: float) ->str:
    bmi = weight / (height ** 2)  # Calculate BMI
    
    if bmi < 16.0:
        return "🦴 Skeleton Mode Activated (Severely Underweight)"
    elif 16.0 <= bmi < 18.5:
        return "🍃 Light as a Feather (Underweight)"
    elif 18.5 <= bmi < 25.0:
        return "💪 Peak Performance (Normal Range)"
    elif 25.0 <= bmi < 30.0:
        return "🍔 Enjoying Life (Overweight)"
    elif 30.0 <= bmi < 35.0:
        return "⚠️ Extra Cushioning (Obesity Class 1)"
    elif 35.0 <= bmi < 40.0:
        return "🔥 Heavyweight Champ (Obesity Class 2)"
    else:
        return "🚀 Big Boss Level (Obesity Class 3)"


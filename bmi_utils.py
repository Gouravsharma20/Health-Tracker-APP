from models import ClientType



def classify_client(weight: float, height: float) -> ClientType:
    bmi = weight / (height ** 2)  # Calculate BMI
    
    if bmi < 16.0:
        return ClientType.SEVERELY_UNDERWEIGHT
    elif 16.0 <= bmi < 18.5:
        return ClientType.UNDERWEIGHT
    elif 18.5 <= bmi < 25.0:
        return ClientType.NORMAL
    elif 25.0 <= bmi < 30.0:
        return ClientType.OVERWEIGHT
    elif 30.0 <= bmi < 35.0:
        return ClientType.OBESITY_CLASS1
    elif 35.0 <= bmi < 40.0:
        return ClientType.OBESITY_CLASS2
    else:
        return ClientType.OBESITY_CLASS3


from enum import Enum

# Enum for Trainer Specializations
class SpecializationEnum(str, Enum):
    CARDIO = "Cardio"
    STRENGTH = "Strength Training"
    YOGA = "Yoga"
    PILATES = "Pilates"
    CROSSFIT = "CrossFit"
    ZUMBA = "Zumba"
    HIIT = "HIIT"
    FUNCTIONAL = "Functional Training"
    REHAB = "Rehabilitation"

    def __str__(self):
        return self.value

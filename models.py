from sqlalchemy import Boolean,Column,Integer,String,Enum,Date
from pydantic import BaseModel
import enum
from datetime import date

from database import Base

class GenderEnum(str,enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class MembershipTypeEnum(str,enum.Enum):
    TRIAL = "Trial"
    MONTHLY = "Monthly"
    QUARTERLY = "Quarterly"
    HALFYEARLY = "HalfYearly"
    ANNUALLY = "Annually"

class DietTypeEnum(str,enum.Enum):
    VEG = "Veg"
    NONVEG = "Nonveg"
    EGG = "Egg"
    VEGAN = "Vegan"
    ALL = "All"

class DaysEnum(str, enum.Enum):
    MONDAY = "Monday"
    TUESDAY = "Tuesday"
    WEDNESDAY = "Wednesday"
    THURSDAY = "Thursday"
    FRIDAY = "Friday"
    SATURDAY = "Saturday"
    SUNDAY = "Sunday"
    
class ClientType(str, enum.Enum):
    SEVERELYUNDERWEIGHT = "SeverelyUnderweight"
    UNDERWEIGHT = "Underweight"
    NORMAL = "Normal"
    OVERWEIGHT = "Overweight"
    OBESITY_CLASS1 = "ObesityClass1"
    OBESITY_CLASS2 = "ObesityClass2"
    OBESITY_CLASS3 = "ObesityClass3"

class WorkoutPlanEnum(str, enum.Enum):
    WEIGHT_LOSS = "Weight Loss"
    MUSCLE_GAIN = "Muscle Gain"
    GENERAL_FITNESS = "General Fitness"
    CARDIO_ONLY = "Cardio Only"
    




class Client(Base):
    __tablename__ = "Clients"
    client_id = Column(Integer,primary_key=True,index=True)
    client_name = Column(String)
    client_username = Column(String(50),unique = True)
    client_phonenumber = Column(String(10),unique = True)
    client_gender = Column(Enum(GenderEnum),nullable=False)
    client_dob = Column(Date)
    client_join_date = Column(Date,nullable=False)
    client_diet_type = Column(Enum(DietTypeEnum), nullable=False)  # Default diet preference
    client_nonveg_days = Column(String, nullable=True)
    client_last_payment_date = Column(Date, nullable=True)
    client_membership_active = Column(Boolean, default=True)  # Membership status
    client_weight = Column(Integer, nullable=True)  # Weight in kg
    client_height = Column(Integer, nullable=True)  # Height in cm
    client_membership_expiry_date = Column(Date, nullable=True)  # Expiry date
    client_workout_plan = Column(Enum(WorkoutPlanEnum), nullable=True)  # Assigned workout plan
    client_trainer_id = Column(Integer, nullable=True)  # Assigned trainer ID
    client_email = Column(String(100), unique=True, nullable=True)  # Email
    client_emergency_contact = Column(String(10), nullable=True)  # Emergency contact
    client_goal = Column(String, nullable=True)  # Fitness goal
    client_workout_time = Column(String, nullable=True)  # Preferred workout timing
    client_referred_by = Column(Integer, nullable=True)  # Referral ID
    client_medical_conditions = Column(String, nullable=True)  # Medical conditions






from sqlalchemy import Boolean, Column, Integer, String, Enum, Date, ForeignKey, Float, Time
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from pydantic import BaseModel
import enum
from datetime import date
from database import Base

class GenderEnum(str, enum.Enum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

class MembershipTypeEnum(str, enum.Enum):
    TRIAL = "Trial"
    MONTHLY = "Monthly"
    QUARTERLY = "Quarterly"
    HALFYEARLY = "HalfYearly"
    ANNUALLY = "Annually"

class DietTypeEnum(str, enum.Enum):
    VEG = "Veg"
    NONVEG = "Nonveg"
    EGG = "Egg"
    VEGAN = "Vegan"
    ALL = "All"

class WorkoutPlanEnum(str, enum.Enum):
    WEIGHT_LOSS = "Weight Loss"
    MUSCLE_GAIN = "Muscle Gain"
    GENERAL_FITNESS = "General Fitness"
    CARDIO_ONLY = "Cardio Only"

    
class ClientType(str, enum.Enum):
    SEVERELYUNDERWEIGHT = "Severely Underweight"
    UNDERWEIGHT = "Underweight"
    NORMAL = "Normal"
    OVERWEIGHT = "Overweight"
    OBESITY_CLASS1 = "Obesity Class 1"
    OBESITY_CLASS2 = "Obesity Class 2"
    OBESITY_CLASS3 = "Obesity Class 3"


class Trainers(Base):
    __tablename__ = "Trainers"
    trainer_id = Column(Integer, primary_key=True, index=True)
    # other columns...



class Client(Base):
    __tablename__ = "Clients"

    client_id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(50), nullable=False)
    client_username = Column(String(50), unique=True, index=True, nullable=False)
    client_phonenumber = Column(String(10), unique=True, index=True, nullable=False)
    client_gender = Column(Enum(GenderEnum), nullable=False)
    client_dob = Column(Date, nullable=False)
    client_join_date = Column(Date, nullable=False, default=date.today)
    client_diet_type = Column(Enum(DietTypeEnum), nullable=False)
    client_nonveg_days = Column(JSON, nullable=True)  # JSON column for multiple days
    client_last_payment_date = Column(Date, nullable=True)
    client_membership_active = Column(Boolean, default=True)
    client_weight = Column(Float, nullable=True)
    client_height = Column(Float, nullable=True)
    client_membership_expiry_date = Column(Date, nullable=True)
    client_workout_plan = Column(Enum(WorkoutPlanEnum), nullable=True)
    
    # Foreign Keys
    client_trainer_id = Column(Integer, ForeignKey("Trainers.trainer_id"), nullable=True)
    client_referred_by = Column(Integer, ForeignKey("Clients.client_id"), nullable=True)

    # Additional Fields
    client_email = Column(String(100), unique=True, nullable=True, index=True)
    client_emergency_contact = Column(String(10), nullable=True)
    client_goal = Column(String(200), nullable=True)
    client_workout_time = Column(Time, nullable=True)  # Stores HH:MM:SS format
    client_medical_conditions = Column(String(200), nullable=True)

    # Relationships
    trainer = relationship("Trainer", back_populates="clients")
    referred_by_client = relationship("Client", remote_side=[client_id])  # Self-referencing relationship

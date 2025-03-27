from sqlalchemy import Boolean, Column, Integer, String, Enum, Date, ForeignKey, Float, Time , Table
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import JSON
from pydantic import BaseModel
import enum
from datetime import date
from database import Base
from sqlalchemy.ext.hybrid import hybrid_property

# Used Int instead of string (Space-Management) 
class GenderEnum(enum.Enum):
    MALE = 1
    FEMALE = 2
    OTHER = 3

class MembershipTypeEnum(enum.Enum):
    TRIAL = 1
    MONTHLY = 2
    QUARTERLY = 3
    HALFYEARLY = 4
    ANNUALLY = 5

class DietTypeEnum(enum.Enum):
    VEGAN = 1
    VEG = 2
    NONVEG = 3
    EGG = 4
    ALL = 5

class WorkoutPlanEnum(enum.Enum):
    GENERAL_FITNESS = 1
    WEIGHT_LOSS = 2
    MUSCLE_GAIN = 3
    CARDIO_ONLY = 4

    
class ClientType(enum.Enum):
    SEVERELY_UNDERWEIGHT = 1
    UNDERWEIGHT = 2
    NORMAL = 3
    OVERWEIGHT = 4
    OBESITY_CLASS1 = 5
    OBESITY_CLASS2 = 6
    OBESITY_CLASS3 = 7


# Association Tables for Many-to-Many Relations
client_workout_association = Table(
    "client_workout_association",
    Base.metadata,
    Column("client_id", Integer, ForeignKey("clients.client_id")),
    Column("workout_id", Integer, ForeignKey("workouts.workout_id")),
)

client_diet_association = Table(
    "client_diet_association",
    Base.metadata,
    Column("client_id", Integer, ForeignKey("clients.client_id")),
    Column("diet_id", Integer, ForeignKey("diets.diet_id")),
)

# Trainers Table
class Trainer(Base):
    __tablename__ = "trainers"

    trainer_id = Column(Integer, primary_key=True, index=True)
    trainer_name = Column(String(50), nullable=False)
    specialization = Column(String(100), nullable=True)  # e.g., "Strength Training, Cardio"
    experience_years = Column(Integer, nullable=True)
    clients = relationship("Client", back_populates="trainer")




# Clients Table
class Client(Base):
    __tablename__ = "clients"

    client_id = Column(Integer, primary_key=True, index=True)
    client_name = Column(String(50), nullable=False)
    client_username = Column(String(50), unique=True, index=True, nullable=False)
    client_email = Column(String(100), unique=True, nullable=False, index=True)
    client_phonenumber = Column(String(15), unique=True, index=True, nullable=False)
    client_gender = Column(Enum(GenderEnum), nullable=False)
    client_dob = Column(Date, nullable=False)
    client_join_date = Column(Date, nullable=False, default=date.today)

    client_height = Column(Float, nullable=True)
    client_weight = Column(Float, nullable=True)

    # Foreign Keys
    client_trainer_id = Column(Integer, ForeignKey("trainers.trainer_id", ondelete="SET NULL"), nullable=True)
    
    # Relationships
    trainer = relationship("Trainer", back_populates="clients")
    memberships = relationship("Membership", back_populates="client")
    payments = relationship("Payment", back_populates="client")
    workouts = relationship("Workout", secondary=client_workout_association, back_populates="clients")
    diets = relationship("Diet", secondary=client_diet_association, back_populates="clients")

    @hybrid_property
    def client_BMI(self):
        if self.client_height and self.client_weight:
            return round(self.client_weight / ((self.client_height / 100) ** 2), 2)
        return None
    
    

# Payments Table
class Payment(Base):
    __tablename__ = "payments"

    payment_id = Column(Integer, primary_key=True, index=True)
    client_id = Column(Integer, ForeignKey("clients.client_id", ondelete="CASCADE"), nullable=False)
    amount = Column(Float, nullable=False)
    payment_date = Column(Date, nullable=False, default=date.today)
    payment_method = Column(String(50), nullable=False)  # e.g., "Credit Card", "UPI", "Cash"

    client = relationship("Client", back_populates="payments")


# Workouts Table
class Workout(Base):
    __tablename__ = "workouts"

    workout_id = Column(Integer, primary_key=True, index=True)
    workout_name = Column(String(50), nullable=False)
    difficulty_level = Column(String(50), nullable=False)  # e.g., "Beginner", "Intermediate", "Advanced"
    duration_minutes = Column(Integer, nullable=False)  # Workout duration

    clients = relationship("Client", secondary=client_workout_association, back_populates="workouts")

# Diets Table
class Diet(Base):
    __tablename__ = "diets"

    diet_id = Column(Integer, primary_key=True, index=True)
    diet_type = Column(Enum(DietTypeEnum), nullable=False)
    meal_plan = Column(String(200), nullable=False)  # e.g., "Breakfast: Oats, Lunch: Rice & Chicken"

    clients = relationship("Client", secondary=client_diet_association, back_populates="diets")
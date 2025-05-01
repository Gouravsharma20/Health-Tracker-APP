# models/trainer/trainer.py

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from database import Base
from models.trainer.specialization_enum import SpecializationEnum  # ✅ Import shared enum

# ORM Model for Trainer table
class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, index=True)  # Unique trainer ID
    name = Column(String(25), nullable=False, index=True)  # Trainer name
    email = Column(String(100), unique=True, nullable=False, index=True)  # Unique enforced here
    hashed_password = Column(String(255), nullable=False)  # ✅ Updated for security best practices
    age = Column(Integer,nullable=False)
    experience_years = Column(Integer,nullable=False)
    specialization = Column(Enum(SpecializationEnum), nullable=False)  # Specialization (enum)
    workouts = relationship("Workout", back_populates="trainer")  # Relationship to workouts


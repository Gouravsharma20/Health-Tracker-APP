# Trainer model for gym trainers and their specializations
from sqlalchemy import Column, Integer, String, Enum
from database import Base
from enum import Enum as PyEnum

# Specialization types for trainers
class SpecializationEnum(str, PyEnum):
    STRENGTH = "Strength Training"
    CARDIO = "Cardio"
    YOGA = "Yoga"

# ORM Model for Trainer table
class Trainer(Base):
    __tablename__ = "trainers"

    id = Column(Integer, primary_key=True, index=True)  # Unique trainer ID
    name = Column(String(25), nullable=False)  # Trainer name
    specialization = Column(Enum(SpecializationEnum), nullable=False)  # Specialization field

# Workout model for managing trainer-assigned workouts
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# ORM Model for Workout table
class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)  # Unique workout ID
    trainer_id = Column(Integer, ForeignKey("trainers.id"))  # Assigned trainer
    workout_type = Column(String, nullable=False)  # Type of workout

    # Relationship with Trainer model
    trainer = relationship("Trainer", back_populates="workouts")

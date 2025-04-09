# models/trainer/workout.py

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from models.utils.client_workout_association import clientWorkoutAssociation_table

# ORM Model for Workout table
class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)  # Unique workout ID
    trainer_id = Column(Integer, ForeignKey("trainers.id"), nullable=False)  # Assigned trainer
    workout_type = Column(String(50), nullable=False)  # Increased length for flexibility

    # Relationship with Trainer model
    trainer = relationship("Trainer", back_populates="workouts")

    # Relationship with Clients via association table
    clients = relationship(
        "Client",
        secondary=clientWorkoutAssociation_table,
        back_populates="workouts"
    )

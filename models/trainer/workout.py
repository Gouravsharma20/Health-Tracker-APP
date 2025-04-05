# Workout model for managing trainer-assigned workouts
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from models.customer.client import Client

from models.utils.client_workout_association import clientWorkoutAssociation_table
from models.trainer.trainer import Trainer

# ORM Model for Workout table
class Workout(Base):
    __tablename__ = "workouts"

    id = Column(Integer, primary_key=True, index=True)  # Unique workout ID
    trainer_id = Column(Integer, ForeignKey("trainers.id"))  # Assigned trainer
    workout_type = Column(String(20), nullable=False)  # Type of workout

    # Relationship with Trainer model
    trainer = relationship("Trainer", back_populates="workouts")
    clients = relationship("Client",secondary=clientWorkoutAssociation_table,back_populates="workouts")
    
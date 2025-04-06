# models/owner/owner_model.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)  # Hash this in real apps

    # Relationship to gym images
    gym_images = relationship("GymImage", back_populates="owner",cascade="all, delete-orphan")   

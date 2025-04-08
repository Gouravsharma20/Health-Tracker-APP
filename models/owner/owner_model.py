# models/owner/owner_model.py

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base
from models.customer.membership import Membership
from models.owner.gym_image_model import GymImage

class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=False, nullable=False, index=True)
    password = Column(String(255), nullable=False)  # Hash this in real apps
    memberships = relationship("Membership", back_populates="owner",cascade="all, delete-orphan")

    # Relationship to gym images
    gym_images = relationship("GymImage", back_populates="owner",cascade="all, delete-orphan")   

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

# Owner model representing gym owners
class Owner(Base):
    __tablename__ = "owners"

    id = Column(Integer, primary_key=True, index=True)  # Unique owner ID
    name = Column(String(100), nullable=False)  # Owner's name
    email = Column(String(100), nullable=False, index=True)  # Owner's email
    password = Column(String(255), nullable=False)  # Hashed password (store securely)

    # One-to-many relationship with memberships
    memberships = relationship(
        "Membership",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

    # One-to-many relationship with uploaded gym images
    gym_images = relationship(
        "GymImage",
        back_populates="owner",
        cascade="all, delete-orphan"
    )

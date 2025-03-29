from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from database import Base

# ORM Model for Membership table
class Membership(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)  # Unique membership ID
    type = Column(String(50), nullable=False)  # Specify a length for VARCHAR
    price = Column(Integer, nullable=False)  # Membership price

    # Relationship with Client model
    clients = relationship("Client", back_populates="membership")

from sqlalchemy import Column, Integer, String, ForeignKey, JSON
from sqlalchemy.orm import relationship
from database import Base

# ORM Model for Memberships
class Membership(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)  # Unique membership ID
    membership_type = Column(String(50), nullable=False)  # Type (e.g., Gold, Platinum)
    price = Column(Integer, nullable=False)  # Membership price
    benefits = Column(JSON, nullable=False, default=list)  # Benefits stored as JSON list

    owner_id = Column(Integer, ForeignKey("owners.id"))  # Link to the gym owner
    owner = relationship("Owner", back_populates="memberships")

    # Relationship with clients (many clients can share one membership type)
    clients = relationship("Client", back_populates="membership")

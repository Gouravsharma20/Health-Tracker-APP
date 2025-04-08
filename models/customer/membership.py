from sqlalchemy import Column, Integer, String ,ForeignKey ,JSON 
from sqlalchemy.orm import relationship 
from database import Base
from typing import Optional,List

# ORM Model for Membership table
class Membership(Base):
    __tablename__ = "memberships"

    id = Column(Integer, primary_key=True, index=True)  # Unique membership ID
    membership_type = Column(String(50), nullable=False)  # Specify a length for VARCHAR
    price = Column(Integer, nullable=False)  # Membership price
    benefits = Column(JSON,nullable=False,default=List)  # Membership benefits
    owner_id = Column(Integer,ForeignKey("owners.id"))
    owner = relationship("Owner",back_populates="memberships")

    # Relationship with Client model
    clients = relationship("Client", back_populates="membership")

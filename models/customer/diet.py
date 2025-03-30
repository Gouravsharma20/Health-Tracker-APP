# Diet model for managing client diet plans
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# ORM Model for Diet table
class Diet(Base):
    __tablename__ = "diets"

    id = Column(Integer, primary_key=True, index=True)  # Unique diet ID
    client_id = Column(Integer, ForeignKey("clients.id"))  # Foreign key for client
    diet_plan = Column(String(12), nullable=False)  # Diet plan details

    # Relationship with Client model
    client = relationship("Client", back_populates="diet")

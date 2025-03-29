# Finance model for tracking gym revenue and expenses
from sqlalchemy import Column, Integer, String
from database import Base

# ORM Model for Finance table
class Finance(Base):
    __tablename__ = "finances"

    id = Column(Integer, primary_key=True, index=True)  # Unique finance ID
    revenue = Column(Integer, nullable=False)  # Total revenue
    expenses = Column(Integer, nullable=False)  # Total expenses
    profit = Column(Integer, nullable=False)  # Net profit

# Finance model for tracking gym revenue and expenses
from sqlalchemy import Column, Integer
from database import Base

# ORM Model for Finance table
class Finance(Base):
    __tablename__ = "finances"

    id = Column(Integer, primary_key=True, index=True)  # Unique finance record ID
    revenue = Column(Integer, nullable=False)  # Total revenue
    expenses = Column(Integer, nullable=False)  # Total expenses
    profit = Column(Integer, nullable=False)  # Net profit

"""from sqlalchemy import Column, Integer, String, Date, Float, Enum
from database import Base

class Owner(Base):
    __tablename__ = "owners"  # Table for gym owners

    owner_id = Column(Integer, primary_key=True, index=True)
    owner_name = Column(String, nullable=False)
    owner_username = Column(String(50), unique=True, nullable=False)
    owner_password = Column(String, nullable=False)  # Hashed password
    owner_phone = Column(String(10), unique=True, nullable=False)
    owner_email = Column(String, unique=True, nullable=False)

    gym_name = Column(String, nullable=False)
    gym_address = Column(String, nullable=False)
    gym_contact_number = Column(String(10), nullable=False)
    gym_registration_number = Column(String, unique=True, nullable=True)

    subscription_plan = Column(String, nullable=False)  # Monthly, Yearly, etc.
    subscription_start_date = Column(Date, nullable=False)
    subscription_end_date = Column(Date, nullable=False)
    
    total_revenue = Column(Float, default=0.0)  # Earnings
    pending_payments = Column(Float, default=0.0)  # Unpaid fees

    total_clients = Column(Integer, default=0)  # Number of active clients
    total_trainers = Column(Integer, default=0)  # Number of trainers
    
    gym_opening_time = Column(String, nullable=False)  # Example: "06:00 AM"
    gym_closing_time = Column(String, nullable=False)  # Example: "10:00 PM" """

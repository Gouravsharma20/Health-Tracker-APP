# Client model representing gym members
from sqlalchemy import Column, Integer, String, ForeignKey , Float 
from sqlalchemy.orm import relationship
from sqlalchemy import Enum as SqlEnum
from enum import Enum as PyEnum
from database import Base
from models.utils.bmi_utils import calculate_bmi, determine_bmi_category
from models.customer.diet import clientDietAssociation_table
from models.utils.client_workout_association import clientWorkoutAssociation_table


# Gender enumeration for clients
class GenderEnum(str, PyEnum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"
    def __str__(self):
        return self.value  # ✅ Ensure correct Enum conversion

# ORM Model for Client table
class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)  # Unique client ID
    name = Column(String(25), nullable=False)  # Client name
    age = Column(Integer, nullable=False)  # Client age
    weight = Column(Float, nullable=False) # Client weight
    height = Column(Float, nullable=False) # Client height
    diets = relationship("Diet", secondary=clientDietAssociation_table, back_populates="clients")


    def get_bmi(self) -> float:
        """Returns the calculated BMI for the client."""
        return calculate_bmi(self.weight, self.height)

    def get_bmi_category(self) -> str:
        """Returns the BMI category for the client."""
        return determine_bmi_category(self.get_bmi())

    gender = Column(SqlEnum(GenderEnum), nullable=False)  # Client gender
    membership_id = Column(Integer, ForeignKey("memberships.id"))  # Foreign key for membership

    # Establishing relationship with Membership model
    membership = relationship("Membership", back_populates="clients")

    diets = relationship("Diet", secondary=clientDietAssociation_table, back_populates="clients")
    workouts = relationship("Workout",secondary=clientWorkoutAssociation_table,back_populates="clients")


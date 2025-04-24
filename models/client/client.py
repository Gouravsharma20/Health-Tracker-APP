from enum import Enum as PyEnum
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Enum as SqlEnum
from sqlalchemy.orm import relationship
from database import Base
from pydantic import BaseModel,Field
from models.client.diet import clientDietAssociation_table
from models.utils.client_workout_association import clientWorkoutAssociation_table
from models.utils.bmi_utils import calculate_bmi, determine_bmi_category
from models.utils.client_diet_association import clientDietAssociation_table


# Gender enumeration
class GenderEnum(str, PyEnum):
    MALE = "Male"
    FEMALE = "Female"
    OTHER = "Other"

    def __str__(self):
        return self.value
    
class ClientCreate(BaseModel):
    name: str
    age: int
    weight: float
    height: float
    email: str
    gender: GenderEnum
    password:str = Field(min_length=8)

    class Config:
        orm_mode = True
    
class ClientResponse(BaseModel):
    id: int
    name: str
    age: int
    weight: float
    height: float
    email: str
    gender: GenderEnum

    class Config:
        orm_mode = True



class Client(Base):
    __tablename__ = "clients"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)
    height = Column(Float, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    gender = Column(SqlEnum(GenderEnum), nullable=False)

    # Relationships
    membership_id = Column(Integer, ForeignKey("memberships.id"))
    membership = relationship("Membership", back_populates="clients")

    diets = relationship(
        "Diet",
        secondary=clientDietAssociation_table,
        back_populates="clients",
        cascade="all, delete"
    )

    workouts = relationship(
        "Workout",
        secondary=clientWorkoutAssociation_table,
        back_populates="clients",
        cascade="all, delete"
    )

    def get_bmi(self) -> float:
        return calculate_bmi(self.weight, self.height)

    def get_bmi_category(self) -> str:
        return determine_bmi_category(self.get_bmi())

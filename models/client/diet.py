# models/client/diet.py

from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum as PyEnum
from models.utils.client_diet_association import clientDietAssociation_table

class diettypeEnum(str, PyEnum):
    VEGAN = "Vegan"
    VEGETARIAN = "Vegetarian"
    NON_VEGETARIAN = "Non-Vegetarian"
    EGGITARIAN = "Eggitarian"
    MEDITERRANEAN = "Mediterranean"

    def __str__(self):
        return self.value

class Diet(Base):
    __tablename__ = "diets"

    id = Column(Integer, primary_key=True, index=True)
    diet_type = Column(Enum(diettypeEnum), nullable=False)
    diet_plan = Column(String(255), default="General Plan", nullable=False)

    clients = relationship("Client", secondary=clientDietAssociation_table, back_populates="diets")

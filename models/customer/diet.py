# Diet model for managing client diet plans
from sqlalchemy import Column, Integer, String, ForeignKey,Enum,Table
from sqlalchemy.orm import relationship
from database import Base
from enum import Enum as PyEnum

class diettypeEnum(str, PyEnum):
    VEGAN = "Vegan"
    VEGETARIAN = "Vegetarian"
    NON_VEGETARIAN = "Non-Vegetarian"
    Eggitarian = "Eggitarian"
    MEDITERRANEAN = "Mediterranean"

    def __str__(self):
        return self.value  # Ensure correct Enum conversion


clientDietAssociation_table = Table(
    'client_diet',
    Base.metadata,
    Column('client_id', Integer, ForeignKey('clients.id')),
    Column('diet_id', Integer, ForeignKey('diets.id'))
)


# ORM Model for Diet table
class Diet(Base):
    __tablename__ = "diets"

    id = Column(Integer, primary_key=True, index=True)  # Unique diet ID
    diet_type = Column(Enum(diettypeEnum), nullable=False)  # Diet type (e.g., Vegan, Vegetarian)

    # Relationship with Client model
    clients = relationship("Client", secondary= clientDietAssociation_table, back_populates="diets")

from pydantic import BaseModel, Field
from typing import Optional
from models.customer.client import GenderEnum
from models.customer.diet import diettypeEnum

class ClientCreate(BaseModel):
    name: str = Field(..., max_length=25)
    age: int
    weight: float
    height: float
    gender: GenderEnum
    membership_id: int
    diets: list[diettypeEnum] = []

class ClientUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=25)
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    gender: Optional[GenderEnum] = None
    membership_id: Optional[int] = None

class ClientResponse(ClientCreate):
    id: int

    class Config:
        from_attributes = True

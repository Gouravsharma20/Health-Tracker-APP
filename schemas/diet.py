from models.customer.diet import diettypeEnum
from pydantic import BaseModel
from models.customer.diet import diettypeEnum

class DietResponse(BaseModel):
    id: int
    diet_type: diettypeEnum

    class Config:
        from_attributes = True

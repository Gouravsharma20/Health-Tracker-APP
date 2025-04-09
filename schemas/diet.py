from models.client.diet import diettypeEnum
from pydantic import BaseModel
from models.client.diet import diettypeEnum

class DietResponse(BaseModel):
    id: int
    diet_type: diettypeEnum

    model_config = {
    "from_attributes": True
}


from pydantic import BaseModel, Field
from models.customer.client import GenderEnum
from typing import Optional,Literal
from models.trainer.trainer import SpecializationEnum


# ✅ Schema for Trainer model
class TrainerCreate(BaseModel):
    name: str = Field(..., max_length=100)
    specialization: SpecializationEnum

# ✅ Schema for creating a new Client
class ClientCreate(BaseModel):
    name: str = Field(..., max_length=25)
    age: int
    weight: float
    height: float
    gender: GenderEnum
    membership_id: int

# ✅ Schema for updating a Client
class ClientUpdate(BaseModel):
    name:Optional[str] = Field(None, max_length=25)
    age:Optional[int] = None
    weight:Optional[float] = None
    height:Optional[float] = None
    gender:Optional[GenderEnum] = None
    membership_id:Optional[int] = None

# ✅ Schema for returning a Client response
class ClientResponse(ClientCreate):
    id: int

    class Config:
        from_attributes = True  # Allows ORM compatibility

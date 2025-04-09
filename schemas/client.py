from pydantic import BaseModel, Field, EmailStr
from typing import Optional, List
from models.client.client import GenderEnum
from models.client.diet import diettypeEnum
from schemas.membership import MembershipResponse
from schemas.diet import DietResponse

# ✅ Shared base class for reusability
class ClientBase(BaseModel):
    name: str = Field(..., max_length=25)
    age: int
    weight: float
    height: float
    gender: GenderEnum
    membership_id: int
    diets: List[diettypeEnum] = []

# ✅ Used in registration
class ClientCreate(ClientBase):
    email: EmailStr
    password: str  # ✅ Include password in creation

# ✅ Used for PATCH/PUT
class ClientUpdate(BaseModel):
    name: Optional[str] = Field(None, max_length=25)
    age: Optional[int] = None
    weight: Optional[float] = None
    height: Optional[float] = None
    gender: Optional[GenderEnum] = None
    membership_id: Optional[int] = None
    diets: Optional[List[diettypeEnum]] = None

# ✅ Used in GET /client/{id} or /me
class ClientResponse(ClientBase):
    id: int
    email: EmailStr
    membership: Optional[MembershipResponse]
    diets: List[DietResponse]  # Full objects

    class Config:
        orm_mode = True
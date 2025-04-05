from pydantic import BaseModel, Field
from typing import Optional

# ✅ Schema to create a membership
class MembershipCreate(BaseModel):
    type: str = Field(..., max_length=50)
    price: int

# ✅ Schema to update a membership
class MembershipUpdate(BaseModel):
    type: Optional[str] = Field(None, max_length=50)
    price: Optional[int]

# ✅ Schema to return membership data
class MembershipResponse(MembershipCreate):
    id: int

    class Config:
        from_attributes = True

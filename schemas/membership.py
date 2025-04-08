from pydantic import BaseModel
from typing import Optional,List

class MembershipBase(BaseModel):
    membership_type: str
    price: int
    benefits: List[str]

class MembershipCreate(MembershipBase):
    pass

class MembershipUpdate(BaseModel):
    membership_type:Optional[str] = None
    price: Optional[int] = None
    benefits: Optional[List[str]] = None

class MembershipResponse(MembershipBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True

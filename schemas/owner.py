from pydantic import BaseModel, EmailStr


class OwnerBase(BaseModel):
    name: str
    email: EmailStr


class OwnerCreate(OwnerBase):
    password: str


class OwnerResponse(OwnerBase):
    email: EmailStr
    id: int

    model_config = {
        "from_attributes": True  # For Pydantic v2 (replaces orm_mode=True)
    }


class OwnerSignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

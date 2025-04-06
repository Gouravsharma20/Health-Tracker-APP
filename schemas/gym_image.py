from pydantic import BaseModel, HttpUrl
from typing import Optional

class GymImageCreate(BaseModel):
    caption: Optional[str] = None

class GymImageResponse(GymImageCreate):
    id: int
    image_url: HttpUrl

    class Config:
        from_attributes = True  # Pydantic v2 equivalent of orm_mode

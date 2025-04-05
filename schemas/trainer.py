from pydantic import BaseModel, Field
from models.trainer.trainer import SpecializationEnum

class TrainerCreate(BaseModel):
    name: str = Field(..., max_length=100)
    specialization: SpecializationEnum

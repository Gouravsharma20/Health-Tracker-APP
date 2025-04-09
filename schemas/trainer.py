from pydantic import BaseModel, Field, EmailStr
from models.trainer.trainer import SpecializationEnum

class TrainerCreate(BaseModel):
    name: str = Field(..., max_length=100)
    email: EmailStr
    password: str
    age: int
    experience_years: int
    specialization: SpecializationEnum

class TrainerResponse(BaseModel):
    id: int
    name: str
    email: EmailStr
    age: int
    experience_years: int
    specialization: SpecializationEnum

    class Config:
        from_attributes = True 

# Workout Response Schema
class WorkoutResponse(BaseModel):
    id: int
    name: str
    description: str
    duration_minutes: int
    intensity: str  
    workout_type: str  
    class Config:
        from_attributes = True  

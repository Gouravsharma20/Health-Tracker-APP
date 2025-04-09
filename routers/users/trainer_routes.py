from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from auth.trainer_auth_utils import get_current_trainer
from models.trainer.trainer import Trainer, SpecializationEnum
from models.trainer.workout import Workout
from schemas.trainer import TrainerResponse, WorkoutResponse

router = APIRouter(
    prefix="/trainers",
    tags=["Trainers"]
)

# ✅ Authenticated route to get logged-in trainer profile
@router.get("/me", response_model=TrainerResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_trainer: Trainer = Depends(get_current_trainer)
):
    trainer = db.query(Trainer).filter(Trainer.id == current_trainer.id).first()
    if not trainer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Trainer not found.")
    return trainer


# ✅ Public route to get all trainers (optionally filter by specialization)
@router.get("/", response_model=List[TrainerResponse])
def get_all_trainers(
    specialization: Optional[SpecializationEnum] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Trainer)
    if specialization:
        query = query.filter(Trainer.specialization == specialization)
    return query.all()


# ✅ Public route to get all workouts
@router.get("/workouts", response_model=List[WorkoutResponse])
def get_all_workouts(db: Session = Depends(get_db)):
    return db.query(Workout).all()

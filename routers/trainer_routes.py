from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from models.trainer.trainer import Trainer
from models.trainer.workout import Workout
from models.schemas import TrainerCreate
from models.trainer.trainer import SpecializationEnum

router = APIRouter()

@router.get("/trainers/")
def get_trainers(db: Session = Depends(get_db)):
    return db.query(Trainer).all()

@router.get("/workouts/")
def get_workouts(db: Session = Depends(get_db)):
    return db.query(Workout).all()

@router.post("/trainers/")
def create_trainer(trainer: TrainerCreate , db: Session = Depends(get_db)):
    new_trainer = Trainer(
        name=trainer.name,
        specialization= SpecializationEnum(trainer.specialization)
        )
    
    db.add(new_trainer)
    db.commit()
    db.refresh(new_trainer)
    return new_trainer

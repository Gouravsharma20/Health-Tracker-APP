
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from models.trainer.trainer import Trainer
from models.trainer.workout import Workout
from schemas.trainer import TrainerCreate
from models.trainer.trainer import SpecializationEnum

router = APIRouter(
    prefix="/trainer",
    tags=["Trainer"]
)

@router.get("/")
def get_trainers(db: Session = Depends(get_db)):
    return db.query(Trainer).all()

@router.post("/")
def create_trainer(trainer: TrainerCreate , db: Session = Depends(get_db)):
    new_trainer = Trainer(
        name=trainer.name,
        specialization= SpecializationEnum(trainer.specialization)
        )
    db.add(new_trainer)
    db.commit()
    db.refresh(new_trainer)
    return new_trainer
router.get("/")
def get_workouts(db: Session = Depends(get_db)):
    return db.query(Workout).all()

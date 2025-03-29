from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from models.trainer.trainer import Trainer
from models.trainer.workout import Workout

router = APIRouter()

@router.get("/trainers/")
def get_trainers(db: Session = Depends(get_db)):
    return db.query(Trainer).all()

@router.get("/workouts/")
def get_workouts(db: Session = Depends(get_db)):
    return db.query(Workout).all()

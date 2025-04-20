from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from models.trainer.workout import Workout
from models.trainer.trainer import Trainer
from dependencies import get_db

router = APIRouter(
    prefix="/workout",
    tags=["Workout"]
)

@router.post("/")
def create_workout(workout_type: str, trainer_id: int, db: Session = Depends(get_db)):
    # Check if the trainer exists
    trainer = db.query(Trainer).filter(Trainer.id == trainer_id).first()
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")

    # Create a new workout for the trainer
    new_workout = Workout(
        workout_type=workout_type,
        trainer_id=trainer_id
    )
    db.add(new_workout)
    db.commit()
    db.refresh(new_workout)
    return new_workout

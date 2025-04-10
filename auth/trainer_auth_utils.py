from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from auth.auth import get_current_trainer  # ✅ Verifies role = trainer
from dependencies import get_db
from models.trainer.trainer import Trainer
from auth.password_utils import verify_password  # ✅ Make sure this exists


# ✅ Used in login
def authenticate_trainer(db: Session, email: str, password: str):
    trainer = db.query(Trainer).filter(Trainer.email == email).first()
    if not trainer or not verify_password(password, trainer.hashed_password):
        return None
    return trainer


# ✅ Used in /me route — returns actual Trainer object from DB
def get_current_trainer_user(
    payload: dict = Depends(get_current_trainer), db: Session = Depends(get_db)
) -> Trainer:
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    trainer = db.query(Trainer).filter(Trainer.email == email).first()
    if not trainer:
        raise HTTPException(status_code=404, detail="Trainer not found")

    return trainer

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from models.owner.finance import Finance

router = APIRouter()

@router.get("/finances/")
def get_finances(db: Session = Depends(get_db)):
    return db.query(Finance).all()

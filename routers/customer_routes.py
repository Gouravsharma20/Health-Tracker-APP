from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from models.customer.client import Client
from models.customer.diet import Diet
from models.customer.membership import Membership

router = APIRouter()

@router.get("/clients/")
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()

@router.get("/diets/")
def get_diets(db: Session = Depends(get_db)):
    return db.query(Diet).all()

@router.get("/memberships/")
def get_memberships(db: Session = Depends(get_db)):
    return db.query(Membership).all()

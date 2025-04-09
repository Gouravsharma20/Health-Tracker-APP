from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from typing import List
from models.client.client import Client
from models.client.diet import Diet
from models.client.membership import Membership
from schemas.client import ClientResponse
from auth.client_auth_utils import get_current_client

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)


@router.get("/me", response_model=ClientResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_client: Client = Depends(get_current_client)
):
    client = db.query(Client).filter(Client.id == current_client.id).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Client not found.")
    return client


@router.get("/diets", response_model=List[dict])
def get_all_diets(
    db: Session = Depends(get_db),
    current_client: Client = Depends(get_current_client)
):
    return db.query(Diet).all()


@router.get("/memberships", response_model=List[dict])
def get_all_memberships(
    db: Session = Depends(get_db),
    current_client: Client = Depends(get_current_client)
):
    return db.query(Membership).all()

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from auth.auth import get_current_client  # ✅ Already decodes and checks role
from dependencies import get_db
from models.client.client import Client
from auth.password_utils import verify_password  # ✅ make sure this exists


# ✅ Used in login route
def authenticate_client(db: Session, email: str, password: str):
    client = db.query(Client).filter(Client.email == email).first()
    if not client or not verify_password(password, client.hashed_password):
        return None
    return client


# ✅ Used in /me route – now returns full Client instance from DB
def get_current_client_user(
    payload: dict = Depends(get_current_client), db: Session = Depends(get_db)
) -> Client:
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    client = db.query(Client).filter(Client.email == email).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    return client

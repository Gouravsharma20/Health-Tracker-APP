# auth/auth.py
from pydantic import BaseModel, EmailStr
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from auth.jwt_utils import decode_token
from dependencies import get_db, redis_client
from sqlalchemy.orm import Session
from models.client.client import Client
from models.trainer.trainer import Trainer
from models.owner.owner import Owner

# 🔑 Role-specific OAuth2 schemes
client_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/client/login")
trainer_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/trainer/login")
owner_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/owner/login")

# ✅ Default alias used in some shared routes (e.g. legacy or client-only)
oauth2_scheme = client_oauth2_scheme

# 🧰 Generic current client fetcher (used in some routes)
def get_current_user(token: str = Depends(client_oauth2_scheme), db: Session = Depends(get_db)) -> Client:
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        jti = payload.get("jti")

        if not email or not jti:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

        if redis_client.get(jti):
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token has been blacklisted")

        user = db.query(Client).filter(Client.email == email).first()
        if user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")

        return user

    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# 🧾 Shared schema for signup
class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

# auth/auth.py
from pydantic import BaseModel, EmailStr
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from auth.jwt_utils import decode_token
from dependencies import get_db
from sqlalchemy.orm import Session
from models.customer import Client

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> Client:
    """
    Dependency that returns the currently authenticated user based on the JWT token.
    Also checks if the token is blacklisted.
    """
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        jti = payload.get("jti")

        if not email or not jti:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token",
            )

        # Optional: Redis blacklist check
        from dependencies import redis_client
        if redis_client.get(jti):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token has been blacklisted",
            )

        user = db.query(Client).filter(Client.email == email).first()
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        return user

    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token",
        )





class SignupRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

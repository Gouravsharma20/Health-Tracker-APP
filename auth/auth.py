from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from typing import Optional
from redis import Redis
import os
from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

# Load env variables
load_dotenv()

# Load your secret key and algorithm from environment
SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Redis setup for token blacklisting
redis_client = Redis(host="localhost", port=6379, db=0, decode_responses=True)

# Role-specific OAuth2 schemes (used in Swagger and route protection)
client_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/client/login")
trainer_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/trainer/login")
owner_oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/owner/login")

# Decode and validate JWT token
def verify_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti: Optional[str] = payload.get("jti")

        if not jti:
            raise HTTPException(status_code=401, detail="Invalid token: no jti")

        if redis_client.get(jti):
            raise HTTPException(status_code=401, detail="Token is blacklisted")

        return payload
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

# Universal get_current_user
def get_current_user(token: str = Depends(client_oauth2_scheme)):
    return verify_token(token)

# Role-based token checkers
def get_current_client(token: str = Depends(client_oauth2_scheme)):
    payload = verify_token(token)
    if payload.get("role") != "client":
        raise HTTPException(status_code=403, detail="Only clients allowed")
    return payload

def get_current_trainer(token: str = Depends(trainer_oauth2_scheme)):
    payload = verify_token(token)
    if payload.get("role") != "trainer":
        raise HTTPException(status_code=403, detail="Only trainers allowed")
    return payload

def get_current_owner(token: str = Depends(owner_oauth2_scheme)):
    payload = verify_token(token)
    if payload.get("role") != "owner":
        raise HTTPException(status_code=403, detail="Only owners allowed")
    return payload

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException, status
from jose import jwt, JWTError
from redis import Redis
from dotenv import load_dotenv
import os
from dependencies import redis_client
load_dotenv()

# OAuth2 schemes for different roles
oauth2_scheme_client = OAuth2PasswordBearer(tokenUrl="/auth/client/login")
oauth2_scheme_trainer = OAuth2PasswordBearer(tokenUrl="/auth/trainer/login")
oauth2_scheme_owner = OAuth2PasswordBearer(tokenUrl="/auth/owner/login")

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"

# Redis setup for token blacklist
redis = Redis(host="localhost", port=6379, db=0)

def get_current_user(token: str = Depends(oauth2_scheme_client)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")

        if jti is None:
            raise HTTPException(status_code=401, detail="Missing JTI in token")

        if redis.get(jti):
            raise HTTPException(status_code=401, detail="Token is blacklisted")

        return payload  # Contains sub, role, exp, etc.
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

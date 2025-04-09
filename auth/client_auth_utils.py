# auth/client_auth_utils.py
from fastapi import Depends, HTTPException
from jose import JWTError
from sqlalchemy.orm import Session
from auth.jwt_utils import decode_token
from dependencies import get_db, redis_client
from models.client.client import Client
from routers.auth.auth_base import oauth2_scheme_client

def get_current_client(token: str = Depends(oauth2_scheme_client), db: Session = Depends(get_db)) -> Client:
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        role = payload.get("role")
        jti = payload.get("jti")

        if not email or role != "client":
            raise HTTPException(status_code=401, detail="Invalid client token")

        if redis_client.get(jti):
            raise HTTPException(status_code=401, detail="Token blacklisted")

        client = db.query(Client).filter(Client.email == email).first()
        if not client:
            raise HTTPException(status_code=404, detail="Client not found")

        return client

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

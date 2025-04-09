# auth/owner_auth_utils.py
from fastapi import Depends, HTTPException
from jose import JWTError
from sqlalchemy.orm import Session
from auth.jwt_utils import decode_token
from dependencies import get_db, redis_client
from models.owner.owner import Owner
from routers.auth.auth_base import oauth2_scheme_owner

def get_current_owner(token: str = Depends(oauth2_scheme_owner), db: Session = Depends(get_db)) -> Owner:
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        role = payload.get("role")
        jti = payload.get("jti")

        if not email or role != "owner":
            raise HTTPException(status_code=401, detail="Invalid owner token")

        if redis_client.get(jti):
            raise HTTPException(status_code=401, detail="Token blacklisted")

        owner = db.query(Owner).filter(Owner.email == email).first()
        if not owner:
            raise HTTPException(status_code=404, detail="Owner not found")

        return owner

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

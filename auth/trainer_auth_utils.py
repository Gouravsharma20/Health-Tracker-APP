# auth/trainer_auth_utils.py
from fastapi import Depends, HTTPException
from jose import JWTError
from sqlalchemy.orm import Session
from auth.jwt_utils import decode_token
from dependencies import get_db, redis_client
from models.trainer.trainer import Trainer
from routers.auth.auth_base import oauth2_scheme_trainer

def get_current_trainer(token: str = Depends(oauth2_scheme_trainer), db: Session = Depends(get_db)) -> Trainer:
    try:
        payload = decode_token(token)
        email = payload.get("sub")
        role = payload.get("role")
        jti = payload.get("jti")

        if not email or role != "trainer":
            raise HTTPException(status_code=401, detail="Invalid trainer token")

        if redis_client.get(jti):
            raise HTTPException(status_code=401, detail="Token blacklisted")

        trainer = db.query(Trainer).filter(Trainer.email == email).first()
        if not trainer:
            raise HTTPException(status_code=404, detail="Trainer not found")

        return trainer

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

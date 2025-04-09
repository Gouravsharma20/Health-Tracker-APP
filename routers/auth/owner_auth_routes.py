from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from schemas.owner import OwnerCreate, OwnerResponse
from models.owner.owner import Owner
from auth.password_utils import hash_password, verify_password
from auth.jwt_utils import create_access_token, decode_token
from dependencies import get_db, redis_client
from jose import JWTError
from datetime import datetime
from routers.auth.auth_base import oauth2_scheme_owner
from auth.owner_auth_utils import get_current_owner

router = APIRouter(prefix="/auth/owner", tags=["Owner Auth"])

@router.post("/signup")
def owner_signup(payload: OwnerCreate, db: Session = Depends(get_db)):
    existing = db.query(Owner).filter(Owner.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_owner = Owner(
        name=payload.name,
        email=payload.email,
        password=hash_password(payload.password)
    )
    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)
    return {"msg": "Owner registered successfully"}

@router.post("/login")
def owner_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.email == form_data.username).first()
    if not owner:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    is_valid, needs_rehash = verify_password(form_data.password, owner.password)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if needs_rehash:
        owner.password = hash_password(form_data.password)
        db.commit()

    token_data = {"sub": owner.email, "role": "owner"}
    token, jti = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}


@router.post("/logout")
def owner_logout(token: str = Depends(oauth2_scheme_owner)):
    try:
        payload = decode_token(token)
        jti = payload.get("jti")
        exp = payload.get("exp")
        ttl = exp - int(datetime.utcnow().timestamp())
        if jti and ttl > 0:
            redis_client.setex(jti, ttl, "blacklisted")
            return {"msg": "Successfully logged out"}
        raise HTTPException(status_code=400, detail="Token expired or invalid")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@router.get("/me", response_model=OwnerResponse)
def get_owner_profile(current_owner: Owner = Depends(get_current_owner)):
    return current_owner

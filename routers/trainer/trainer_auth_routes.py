from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime
from jose import JWTError
from schemas.trainer import TrainerResponse, TrainerCreate
from models.trainer.trainer import Trainer
from dependencies import get_db, redis_client
from auth.password_utils import hash_password, verify_password
from auth.jwt_utils import create_access_token, decode_token
from auth.trainer_auth_utils import get_current_trainer_user

# ✅ This is correct usage now
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/trainer/login")

trainer_auth_router = APIRouter(
    prefix="/auth/trainer",
      tags=["Trainer"]
    )

@trainer_auth_router.post("/signup")
async def trainer_signup(payload: TrainerCreate, db: Session = Depends(get_db)):
    existing = db.query(Trainer).filter(Trainer.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")
    new_trainer = Trainer(    
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        age=payload.age,
        experience_years=payload.experience_years,
        specialization=payload.specialization
    )
    
    db.add(new_trainer)
    db.commit()
    db.refresh(new_trainer)
    return {"msg": "Trainer registered successfully"}

    

@trainer_auth_router.post("/login")
async def trainer_login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    trainer = db.query(Trainer).filter(Trainer.email == form_data.username).first()
    if not trainer:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    is_valid, needs_rehash = verify_password(form_data.password, trainer.hashed_password)
    if not is_valid:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    if needs_rehash:
        trainer.hashed_password = hash_password(form_data.password)
        db.commit()

    # ✅ Add role to token!
    token_data = {"sub": trainer.email, "role": "trainer"}
    token, jti = create_access_token(token_data)
    return {"access_token": token, "token_type": "bearer"}

@trainer_auth_router.post("/logout")
async def trainer_logout(token: str = Depends(oauth2_scheme)):  # ✅ use `oauth2_scheme` not oauth2_scheme_trainer unless it's defined elsewhere
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
    
@trainer_auth_router.get("/me", response_model=TrainerResponse)
async def get_trainer_profile(current_trainer: Trainer = Depends(get_current_trainer_user)):
    return current_trainer

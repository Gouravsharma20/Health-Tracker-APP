# routers/auth_routes.py or routers/user_routes.py

from fastapi import APIRouter, Depends
from auth.auth import oauth2_scheme
from auth.jwt_utils import decode_token
from dependencies import redis_client
from jose import JWTError
from fastapi import HTTPException,Depends
from datetime import timedelta,datetime
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from models.customer import Client
from auth.password_utils import verify_password, hash_password
from auth.jwt_utils import create_access_token, decode_token
from dependencies import get_db
from auth.auth import SignupRequest,get_current_user


router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup")
def signup(payload: SignupRequest, db: Session = Depends(get_db)):
    existing = db.query(Client).filter(Client.email == payload.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already exists")

    new_client = Client(
        name=payload.name,
        email=payload.email,
        hashed_password=hash_password(payload.password),
        age=25,
        height=170,
        weight=70,
        gender="Male"
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return {"msg": "User registered successfully"}

@router.post("/login")
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(Client).filter(Client.email == form_data.username).first()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token, jti = create_access_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
    """
    Logs out the user by blacklisting the JWT using its unique identifier (jti).
    """
    try:
        payload = decode_token(token)
        jti = payload.get("jti")
        exp = payload.get("exp")  # ✅ Extract expiration timestamp from JWT
        if jti and exp:
            # ✅ Calculate remaining TTL
            current_time = int(datetime.now(current_time).timestamp())
            ttl = exp - current_time
            if ttl > 0:
                redis_client.setex(jti, ttl, "blacklisted")
                return {"msg": "Successfully logged out"}
            else:
                raise HTTPException(status_code=400, detail="Token already expired")
        raise HTTPException(status_code=400, detail="Token jti or exp missing")
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/me")
def get_profile(current_user = Depends(get_current_user)):
    return {
        "name": current_user.name,
        "email": current_user.email
    }
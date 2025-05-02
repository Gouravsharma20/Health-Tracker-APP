from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.client_auth_utils import authenticate_client
from auth.jwt_utils import create_access_token, decode_token, blacklist_token
from dependencies import redis_client
from models.client.client import ClientCreate,ClientResponse
from models.client.client import Client
from sqlalchemy.orm import Session
from database import get_db
from auth.client_auth_utils import get_current_client_user
from auth.password_utils import hash_password,verify_password
from dependencies import redis_client,get_db
import traceback
import mysql.connector
import os

client_auth_router = APIRouter(prefix="/auth/client", tags=["Client"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/client/login")  # ✅ Swagger will work

@client_auth_router.post("/signup", response_model=ClientResponse)
async def signup(
    data: ClientCreate,
    db: Session = Depends(get_db),
    request: Request = None
):
    existing_user = db.query(Client).filter(Client.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = Client(
        name = data.name,
        age = data.age,
        weight = data.weight,
        height = data.height,
        gender = data.gender,
        email = data.email,
        hashed_password = hash_password(data.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@client_auth_router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.email == form_data.username).first()
    if not client:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")
    
    is_valid, needs_rehash = verify_password(form_data.password,client.hashed_password)
    if not is_valid:
        raise HTTPException(status_code=401,detail="Invalid Credentials")
    
    if needs_rehash:
        client.hashed_password = hash_password(form_data.password)
        db.commit()

    token_data = {"sub": client.email, "role": "client"}
    token, jti = create_access_token(token_data)
    redis_client.set(jti, "active")

    return {"access_token": token, "token_type": "bearer"}

@client_auth_router.post("/logout")
async def logout(token: str = Depends(oauth2_scheme)):
    try:
        payload = decode_token(token)
        jti = payload.get("jti")
        if jti:
            blacklist_token(jti)
            return {"msg": "Logout successful"}
        else:
            raise HTTPException(status_code=400, detail="Token missing jti")
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@client_auth_router.get("/me", response_model=ClientResponse)
async def read_clients_me(current_user: Client = Depends(get_current_client_user)):
    return current_user

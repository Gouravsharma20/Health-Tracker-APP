from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from auth.client_auth_utils import authenticate_client
from auth.jwt_utils import create_access_token, decode_token, blacklist_token
from dependencies import redis_client
from models.client.client import ClientCreate,ClientResponse
from models.client.client import Client
from sqlalchemy.orm import Session
from database import get_db
from auth.client_auth_utils import get_current_client_user

router = APIRouter(prefix="/auth/client", tags=["Client Auth"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/client/login")  # ✅ Swagger will work

@router.post("/signup", response_model=ClientResponse)
def signup(data: ClientCreate, db: Session = Depends(get_db)):
    existing_user = db.query(Client).filter(Client.email == data.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    new_user = Client(
        name=data.name,
        email=data.email,
        hashed_password=data.hashed_password,
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_client(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    token_data = {"sub": user.email, "role": "client"}
    token, jti = create_access_token(token_data)
    redis_client.set(jti, "active")

    return {"access_token": token, "token_type": "bearer"}

@router.post("/logout")
def logout(token: str = Depends(oauth2_scheme)):
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

@router.get("/me", response_model=ClientResponse)
def read_clients_me(current_user: Client = Depends(get_current_client_user)):
    return current_user

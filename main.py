from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, EmailStr
import models
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Client, Trainer , MembershipTypeEnum , GenderEnum
from datetime import date
from bmi_utils import classify_client
from utils import calculate_discounted_price



app = FastAPI()
models.Base.metadata.create_all(bind=engine)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Depends(get_db)

# Request Model for Discount Calculation
class DiscountRequest(BaseModel):
    base_price: float = Field(..., gt=0, description="Base price must be greater than 0")
    membership_type: MembershipTypeEnum
    gender: GenderEnum


# Request model for creating a client
class ClientCreate(BaseModel):
    client_name: str
    client_username: str
    client_email: str
    client_phonenumber: str
    client_gender: GenderEnum
    client_dob: date
    client_height: float
    client_weight: float
    client_trainer_id: Optional[int] = None  # Optional foreign key
    client_type: Optional[str] = None

    class Config:
        orm_mode = True  # Needed to convert SQLAlchemy objects into Pydantic models

# Request model for creating a trainer
class TrainerCreate(BaseModel):
    trainer_name: str
    specialization: models.WorkoutPlanEnum
    experience_years: int

    class Config:
        orm_mode = True

# Get all clients
@app.get("/clients/", response_model=List[ClientCreate])
def get_clients(db: Session = db_dependency):
    clients = db.query(Client).all()
    return clients

# Create a new client
@app.post("/clients/", response_model=ClientCreate)
def create_client(client: ClientCreate, db: Session = db_dependency):
    existing_client = db.query(Client).filter(Client.client_email == client.client_email).first() # prevent duplicate emailid usage
    if existing_client:
        raise HTTPException(status_code=400, detail="Client with this email already exists")

    client_type = classify_client(client.client_weight,client.client_height)
    db_client = Client(
        client_name=client.client_name,
        client_username=client.client_username,
        client_email=client.client_email,
        client_phonenumber=client.client_phonenumber,
        client_gender=client.client_gender,
        client_dob=client.client_dob,
        client_height=client.client_height,
        client_weight=client.client_weight,
        client_trainer_id=client.client_trainer_id,
        client_goal = 
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# Get all trainers
@app.get("/trainers/", response_model=List[TrainerCreate])
def get_trainers(db: Session = db_dependency):
    trainers = db.query(Trainer).all()
    return trainers

# Create a new trainer
@app.post("/trainers/", response_model=TrainerCreate)
def create_trainer(trainer: TrainerCreate, db: Session = Depends(get_db)):
    db_trainer = Trainer(**trainer.model_dump)
    db.add(db_trainer)
    db.commit()
    db.refresh(db_trainer)
    return db_trainer

@app.post("/membership/discount/")
def get_discounted_price(request: DiscountRequest):
    try:
        discounted_price = calculate_discounted_price(request.base_price, request.membership_type, request.gender)
        return {
            "original_price": request.base_price,
            "discounted_price": round(discounted_price, 2),
            "membership_type": request.membership_type.value,
            "gender": request.gender.value,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error calculating discount: {str(e)}")

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Fitness Management API!"}



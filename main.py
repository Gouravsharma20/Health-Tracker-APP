from typing import Optional, List
from fastapi import FastAPI, HTTPException, Depends
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Client, Trainer  # Importing models
from datetime import date

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

# Request model for creating a client
class ClientCreate(BaseModel):
    client_name: str
    client_username: str
    client_email: str
    client_phonenumber: str
    client_gender: int
    client_dob: date
    client_height: float
    client_weight: float
    client_trainer_id: Optional[int] = None  # Optional foreign key

    class Config:
        orm_mode = True  # Needed to convert SQLAlchemy objects into Pydantic models

# Request model for creating a trainer
class TrainerCreate(BaseModel):
    trainer_name: str
    specialization: str
    experience_years: int

    class Config:
        orm_mode = True

# Get all clients
@app.get("/clients/", response_model=List[ClientCreate])
def get_clients(db: Session = Depends(get_db)):
    clients = db.query(Client).all()
    return clients

# Create a new client
@app.post("/clients/", response_model=ClientCreate)
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    db_client = Client(**client.dict())
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

# Get all trainers
@app.get("/trainers/", response_model=List[TrainerCreate])
def get_trainers(db: Session = Depends(get_db)):
    trainers = db.query(Trainer).all()
    return trainers

# Create a new trainer
@app.post("/trainers/", response_model=TrainerCreate)
def create_trainer(trainer: TrainerCreate, db: Session = Depends(get_db)):
    db_trainer = Trainer(**trainer.dict())
    db.add(db_trainer)
    db.commit()
    db.refresh(db_trainer)
    return db_trainer

# Root endpoint
@app.get("/")
def root():
    return {"message": "Welcome to the Fitness Management API!"}

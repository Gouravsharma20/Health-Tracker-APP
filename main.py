from typing import Union,Optional,List
from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel,Field,EmailStr
from typing import Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from bmi_utils import classify_client
from datetime import date,time
from sqlalchemy.orm import Session




app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class BMICalculation(BaseModel):
    weight:float = Field(...,gt=0,description="Weight should be greater than 0")
    height:float = Field(...,ge=0,le=300,description = "Height must be between 30cm to 300cm")


class ClientCreate(BaseModel):
    client_name: str = Field(..., min_length=2, max_length=50)
    client_username: str = Field(..., min_length=3, max_length=50)
    client_phonenumber: int = None
    client_gender: models.GenderEnum
    client_dob: Optional[date] = None
    client_join_date: Optional[date] = date.today()
    client_diet_type: Optional[models.DietTypeEnum] = None
    client_nonveg_days: Optional[dict] = None
    client_last_payment_date: Optional[date] = None
    client_membership_active: Optional[bool] = True
    client_weight: Optional[float] = None
    client_height: Optional[float] = None
    client_membership_expiry_date: Optional[date] = None
    client_workout_plan: Optional[models.WorkoutPlanEnum] = None
    client_BMI: Optional[float] = None
    client_Bmi_Category: Optional[models.ClientType] = None
    client_trainer_id: Optional[int] = None
    client_referred_by: Optional[int] = None
    client_email: Optional[EmailStr] = None
    client_emergency_contact: Optional[str] = None
    client_goal: Optional[str] = None
    client_workout_time: Optional[time] = None
    client_medical_conditions: Optional[str] = None



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session , Depends(get_db)]


""" @app.post("/Clients",status_code=status.HTTP_201_CREATED)
async def Calculate_BMI(Client_data:BMICalculation,db:db_dependency):

    height_in_meter = Client_data.height/100
    Client_height = height_in_meter

    bmi = Client_data.weight / (Client_height ** 2 )
    bmi = round(bmi, 2)

    bmi_category = classify_client(Client_data.weight,Client_data.height)

    new_client = models.Client(
        client_weight = Client_data.weight,
        client_height = height_in_meter,
        client_BMI = bmi,
        client_Bmi_Category = bmi_category
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
"""

"""@app.post("/Clients",status_code=status.HTTP_201_CREATED)
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    print(client)  # Debugging step
    new_client = models.Client(client_name = client.client_name)
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client"""


@app.post("/clients/", status_code=status.HTTP_201_CREATED, response_model=ClientCreate)
async def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client = models.Client(**client.dict())  # Convert Pydantic model to dictionary
    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client


@app.get("/clients/", response_model=List[ClientCreate])
async def get_all_clients(db: Session = Depends(get_db)):
    clients = db.query(models.Client).all()
    return clients


@app.get("/clients/{client_id}", response_model=ClientCreate)
async def get_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.client_id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")
    return client


@app.put("/clients/{client_id}", response_model=ClientCreate)
async def update_client(client_id: int, updated_data: ClientCreate, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.client_id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    for key, value in updated_data.dict().items():
        if value is not None:
            setattr(client, key, value)

    db.commit()
    db.refresh(client)
    return client


@app.delete("/clients/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(client_id: int, db: Session = Depends(get_db)):
    client = db.query(models.Client).filter(models.Client.client_id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    db.delete(client)
    db.commit()
    return {"message": "Client deleted successfully"}


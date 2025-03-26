from typing import Union
from fastapi import FastAPI,HTTPException,Depends,status
from pydantic import BaseModel,Field
from typing import Annotated
import models
from database import engine,SessionLocal
from sqlalchemy.orm import Session
from bmi_utils import classify_client

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class BMICalculation(BaseModel):
    weight:float = Field(...,gt=0,description="Weight should be greater than 0")
    height:float = Field(...,ge=30,le=300,decription = "Height must be between 30cm to 300cm")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session , Depends(get_db)]

@app.post("/Clients",status_code=status.HTTP_201_CREATED)
async def Calculate_BMI(Client_data:BMICalculation,db:db_dependency):

    height_in_meter = Client_data.height/100

    bmi = Client_data.weight / (height_in_meter ** 2 )
    bmi = round(bmi, 2)

    bmi_category = classify_client(Client_data.weight,Client_data.height)

    new_client = models.Client(
        Client_weight = Client_data.weight,
        Client_height = Client_data.height_in_meter,
        Client_BMI = bmi,
        Client_Bmi_Category = bmi_category
    )
    db.add(new_client)
    db.commit()
    db.refresh(new_client)

from fastapi import APIRouter,UploadFile,File, Depends,HTTPException
from pydantic import BaseModel,EmailStr
from sqlalchemy.orm import Session
from database import get_db
from models.utils.cloudinary_utils import upload_image_to_cloudinary
from models.owner.gym_image_model import GymImage
from models.owner.owner_model import Owner
from dependencies import get_db
from models.owner.finance import Finance
from schemas.owner import OwnerCreate, OwnerOut

router = APIRouter()

def create_owner(owner: OwnerCreate, db: Session = Depends(get_db)):
    existing_owner = db.query(Owner).filter(Owner.email == owner.email).first()
    if existing_owner:
        raise HTTPException(status_code=400, detail="Owner with this email already exists.")

    new_owner = Owner(
        name=owner.name,
        email=owner.email,
        password=owner.password  
    )
    db.add(new_owner)
    db.commit()
    db.refresh(new_owner)
    return new_owner

@router.post("/owners/", response_model=OwnerOut, tags=["Owner"])
def create_owner(owner: OwnerCreate, db: Session = Depends(get_db)):
    db_owner = Owner(**owner.dict())
    db.add(db_owner)
    db.commit()
    db.refresh(db_owner)
    return db_owner

@router.get("/finances/",tags=["Owner"])
def get_finances(db: Session = Depends(get_db)):
    return db.query(Finance).all()

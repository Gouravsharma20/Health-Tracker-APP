from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dependencies import get_db
from models.customer.client import Client
from models.customer.diet import Diet
from models.customer.membership import Membership
from models.schemas import ClientCreate, ClientUpdate, ClientResponse



router = APIRouter()

@router.get("/clients/")
def get_clients(db: Session = Depends(get_db)):
    return db.query(Client).all()




@router.get("/diets/")
def get_diets(db: Session = Depends(get_db)):
    return db.query(Diet).all()

@router.get("/memberships/")
def get_memberships(db: Session = Depends(get_db)):
    return db.query(Membership).all()


@router.post("/clients/")
def create_client(client: ClientCreate, db: Session = Depends(get_db)):
    new_client = Client(
    name=client.name,
    age=client.age,
    weight=client.weight,
    height=client.height,
    gender=client.gender.value,  # ✅ Convert Enum to string
    membership_id=client.membership_id,
)
    
    for diet_type in client.diets:
        existing_diet = db.query(Diet).filter(Diet.diet_type == diet_type).first()
        if not existing_diet:
            existing_diet = Diet(diet_type=diet_type)
        new_client.diets.append(existing_diet)



    db.add(new_client)
    db.commit()
    db.refresh(new_client)
    return new_client
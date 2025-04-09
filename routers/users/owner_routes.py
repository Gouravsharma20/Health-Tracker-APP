from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.owner.finance import Finance
from schemas.owner import OwnerResponse
from auth.owner_auth_utils import get_current_owner
from models.owner.owner import Owner

router = APIRouter(prefix="/owners", tags=["Owner"])


@router.get("/me", response_model=OwnerResponse)
def get_my_profile(
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    owner = db.query(Owner).filter(Owner.id == current_owner.id).first()
    if not owner:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Owner not found.")
    return owner


@router.get("/finances", response_model=list[dict])
def get_all_finances(
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    finances = db.query(Finance).all()
    return [f.__dict__ for f in finances]

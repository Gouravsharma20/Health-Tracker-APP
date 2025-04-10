from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session

from auth.auth import get_current_owner  # ✅ Token + role verified
from dependencies import get_db
from models.owner.owner import Owner
from auth.password_utils import verify_password  # ✅ Ensure this is implemented


# ✅ Used in login
def authenticate_owner(db: Session, email: str, password: str):
    owner = db.query(Owner).filter(Owner.email == email).first()
    if not owner or not verify_password(password, owner.hashed_password):
        return None
    return owner


# ✅ Used in /me route — returns full DB Owner instance
def get_current_owner_user(
    payload: dict = Depends(get_current_owner), db: Session = Depends(get_db)
) -> Owner:
    email = payload.get("sub")
    if not email:
        raise HTTPException(status_code=401, detail="Invalid token payload")

    owner = db.query(Owner).filter(Owner.email == email).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")

    return owner

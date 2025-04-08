from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.customer.membership import Membership
from models.owner.owner_model import Owner
from models.customer.client import Client
from schemas.membership import MembershipCreate, MembershipUpdate, MembershipResponse

router = APIRouter(prefix="/memberships", tags=["Memberships"])

# ✅ 1. Create membership for a specific owner
@router.post("/owners/{owner_id}/", response_model=MembershipResponse)
def create_membership_for_owner(owner_id: int, membership: MembershipCreate, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter(Owner.id == owner_id).first()
    if not owner:
        raise HTTPException(status_code=404, detail="Owner not found")

    new_membership = Membership(**membership.dict(), owner_id=owner_id)
    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)
    return new_membership

# ✅ 2. Get all memberships for a specific owner
@router.get("/owners/{owner_id}/", response_model=list[MembershipResponse])
def get_memberships_by_owner(owner_id: int, db: Session = Depends(get_db)):
    return db.query(Membership).filter(Membership.owner_id == owner_id).all()

# ✅ 3. Get all memberships (global list)
@router.get("/", response_model=list[MembershipResponse])
def get_all_memberships(db: Session = Depends(get_db)):
    return db.query(Membership).all()

# ✅ 4. Get a specific membership by ID
@router.get("/{membership_id}", response_model=MembershipResponse)
def get_membership(membership_id: int, db: Session = Depends(get_db)):
    membership = db.query(Membership).filter(Membership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    return membership

# ✅ 5. Update a membership
@router.put("/{membership_id}", response_model=MembershipResponse)
def update_membership(membership_id: int, updated: MembershipUpdate, db: Session = Depends(get_db)):
    membership = db.query(Membership).filter(Membership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    for field, value in updated.dict(exclude_unset=True).items():
        setattr(membership, field, value)
    db.commit()
    db.refresh(membership)
    return membership

# ✅ 6. Delete a membership
@router.delete("/{membership_id}")
def delete_membership(membership_id: int, db: Session = Depends(get_db)):
    membership = db.query(Membership).filter(Membership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    db.delete(membership)
    db.commit()
    return {"message": "Membership deleted successfully"}

# ✅ 7. Assign membership to client
@router.post("/assign/{client_id}/{membership_id}")
def assign_membership_to_client(client_id: int, membership_id: int, db: Session = Depends(get_db)):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    membership = db.query(Membership).filter(Membership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")

    client.membership_id = membership_id
    db.commit()
    return {"message": f"Membership '{membership.membership_type}' assigned to client '{client.name}'"}


@router.patch("/{membership_id}", response_model=MembershipResponse)
def partial_update_membership(
    membership_id: int,
    update_data: MembershipUpdate,
    db: Session = Depends(get_db)
):
    membership = db.query(Membership).filter(Membership.id == membership_id).first()

    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")

    update_fields = update_data.dict(exclude_unset=True)

    for field, value in update_fields.items():
        setattr(membership, field, value)

    db.commit()
    db.refresh(membership)
    return membership


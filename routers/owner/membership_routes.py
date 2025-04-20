from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from database import get_db
from models.client.membership import Membership
from models.owner.owner import Owner
from models.client.client import Client
from routers.client.membership import MembershipCreate, MembershipUpdate, MembershipResponse
from auth.owner_auth_utils import get_current_owner

router = APIRouter(prefix="/memberships", tags=["Memberships"])

# ✅ 1. PUBLIC: Get all memberships (global list)
@router.get("/", response_model=list[MembershipResponse])
def get_all_memberships(db: Session = Depends(get_db)):
    return db.query(Membership).all()

# ✅ 2. PUBLIC: Get a specific membership by ID
@router.get("/{membership_id}", response_model=MembershipResponse)
def get_membership(membership_id: int, db: Session = Depends(get_db)):
    membership = db.query(Membership).filter(Membership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    return membership

# ✅ 3. OWNER-ONLY: Create membership
@router.post("/owners/{owner_id}/", response_model=MembershipResponse)
def create_membership_for_owner(
    owner_id: int,
    membership: MembershipCreate,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    if current_owner.id != owner_id:
        raise HTTPException(status_code=403, detail="Unauthorized to create membership for this owner")

    new_membership = Membership(**membership.dict(), owner_id=owner_id)
    db.add(new_membership)
    db.commit()
    db.refresh(new_membership)
    return new_membership

# ✅ 4. OWNER-ONLY: Get all memberships for a specific owner
@router.get("/owners/{owner_id}/", response_model=list[MembershipResponse])
def get_memberships_by_owner(
    owner_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    if current_owner.id != owner_id:
        raise HTTPException(status_code=403, detail="Unauthorized to view these memberships")

    return db.query(Membership).filter(Membership.owner_id == owner_id).all()

# ✅ 5. OWNER-ONLY: Update a membership
@router.put("/{membership_id}", response_model=MembershipResponse)
def update_membership(
    membership_id: int,
    updated: MembershipUpdate,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    membership = db.query(Membership).filter(Membership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    if membership.owner_id != current_owner.id:
        raise HTTPException(status_code=403, detail="Unauthorized to update this membership")

    for field, value in updated.dict(exclude_unset=True).items():
        setattr(membership, field, value)

    db.commit()
    db.refresh(membership)
    return membership

# ✅ 6. OWNER-ONLY: Partial update
@router.patch("/{membership_id}", response_model=MembershipResponse)
def partial_update_membership(
    membership_id: int,
    update_data: MembershipUpdate,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    membership = db.query(Membership).filter(Membership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    if membership.owner_id != current_owner.id:
        raise HTTPException(status_code=403, detail="Unauthorized to update this membership")

    for field, value in update_data.dict(exclude_unset=True).items():
        setattr(membership, field, value)

    db.commit()
    db.refresh(membership)
    return membership

# ✅ 7. OWNER-ONLY: Delete membership
@router.delete("/{membership_id}")
def delete_membership(
    membership_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    membership = db.query(Membership).filter(Membership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    if membership.owner_id != current_owner.id:
        raise HTTPException(status_code=403, detail="Unauthorized to delete this membership")

    db.delete(membership)
    db.commit()
    return {"message": "Membership deleted successfully"}

# ✅ 8. OWNER-ONLY: Assign membership to client
@router.post("/assign/{client_id}/{membership_id}")
def assign_membership_to_client(
    client_id: int,
    membership_id: int,
    db: Session = Depends(get_db),
    current_owner: Owner = Depends(get_current_owner)
):
    client = db.query(Client).filter(Client.id == client_id).first()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    membership = db.query(Membership).filter(Membership.id == membership_id).first()
    if not membership:
        raise HTTPException(status_code=404, detail="Membership not found")
    if membership.owner_id != current_owner.id:
        raise HTTPException(status_code=403, detail="Unauthorized to assign this membership")

    client.membership_id = membership_id
    db.commit()
    return {"message": f"Membership '{membership.membership_type}' assigned to client '{client.name}'"}

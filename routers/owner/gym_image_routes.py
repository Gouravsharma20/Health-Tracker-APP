from fastapi import APIRouter, UploadFile, File, Form, Depends
from sqlalchemy.orm import Session
from models.owner.gym_image import GymImage
from database import get_db
import cloudinary.uploader
from routers.owner.gym_image import GymImageCreate, GymImageResponse

router = APIRouter(tags=["Owner"])

@router.post("/owners/{owner_id}/upload-images", response_model=GymImageResponse)
async def upload_gym_image(
    owner_id: int,
    caption: str = Form(None),
    image: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    result = cloudinary.uploader.upload(image.file)
    image_url = result.get("secure_url")

    new_image = GymImage(owner_id=owner_id, image_url=image_url, caption=caption)
    db.add(new_image)
    db.commit()
    db.refresh(new_image)
    return new_image

@router.get("/owners/{owner_id}/upload-images", response_model=list[GymImageResponse])
def get_gym_images(owner_id: int, db: Session = Depends(get_db)):
    return db.query(GymImage).filter(GymImage.owner_id == owner_id).all()

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

# GymImage model for storing uploaded gym photos
class GymImage(Base):
    __tablename__ = "gym_images"

    id = Column(Integer, primary_key=True, index=True)  # Unique image ID
    owner_id = Column(Integer, ForeignKey("owners.id"), nullable=False)  # Owner who uploaded the image
    image_url = Column(String(255), nullable=False)  # URL of the uploaded image
    caption = Column(String(255), nullable=True)  # Optional caption for the image

    # Relationship to the Owner model
    owner = relationship("Owner", back_populates="gym_images")

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class GymImage(Base):
    __tablename__ = "gym_images"

    id = Column(Integer, primary_key=True, index=True)
    owner_id = Column(Integer, ForeignKey("owners.id"))
    image_url = Column(String(255), nullable=False)
    caption = Column(String(255), nullable=True)

    owner = relationship("Owner", back_populates="gym_images")

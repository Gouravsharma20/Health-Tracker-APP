# utils/cloudinary_utils.py
import os
import cloudinary
import cloudinary.uploader
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# Configure Cloudinary
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME"),
    api_key=os.getenv("CLOUDINARY_API_KEY"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET"),
    secure=True
)

def upload_image_to_cloudinary(file_path: str, public_id: str = None):
    try:
        upload_result = cloudinary.uploader.upload(file_path, public_id=public_id)
        return upload_result.get("secure_url")
    except Exception as e:
        print(f"Error uploading to Cloudinary: {e}")
        return None

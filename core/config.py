import os
from dotenv import load_dotenv

load_dotenv()

JWT_SECRET_KEY = os.getenv("SECRET_KEY")
JWT_ALGORITHM = os.getenv("ALGORITHM")
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Database connection string
DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./gym.db")

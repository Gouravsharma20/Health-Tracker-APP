from fastapi import FastAPI
from dotenv import load_dotenv

from database import engine, Base
from routers import router as main_router  # Centralized router

# Load environment variables from .env
load_dotenv()

# Create all tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI(
    title="Health Tracker API",
    version="1.0.0",
    description="API for managing clients, trainers, memberships, and workouts in a health tracking system."
)

# Register all routes via centralized router
app.include_router(main_router)

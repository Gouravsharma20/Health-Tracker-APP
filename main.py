from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
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

# Serve static assets and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Custom HTML landing page at "/"
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Register all API routes
app.include_router(main_router)

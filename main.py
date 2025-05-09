from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from models.client.client import Client
from models.client.diet import Diet
from models.client.membership import Membership
from models.owner.owner import Owner
from models.owner.finance import Finance
from models.owner.gym_image import GymImage
from models.trainer.trainer import Trainer
from models.trainer.workout import Workout
from routers import test_db
#from routers.owner.owner_auth_routes import router as owner_auth_routes
from routers.client.client_auth_routes import client_auth_router
from routers.owner.gym_image_routes import gym_image_router
from routers.owner.membership_routes import membership_router
from routers.owner.owner_auth_routes import owner_auth_router
from routers.trainer.trainer_auth_routes import trainer_auth_router
from routers.trainer.workout_routes import workout_router


from database import engine, Base



# Load environment variables from .env
load_dotenv()

# Create all tables


# Initialize FastAPI app
app = FastAPI(
    title="Health Tracker API",
    version="1.0.0",
    description="API for managing clients, trainers, memberships, and workouts in a health tracking system."
)

#app.include_router(owner_auth_routes)
app.include_router(test_db.router)
app.include_router(client_auth_router)
app.include_router(gym_image_router)
app.include_router(membership_router)
app.include_router(owner_auth_router)
app.include_router(trainer_auth_router)
app.include_router(workout_router)

# Serve static assets and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Custom HTML landing page at "/"
@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Register all API routes
Base.metadata.create_all(bind=engine)
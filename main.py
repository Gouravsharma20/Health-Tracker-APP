from fastapi import FastAPI
from database import engine, Base
from dotenv import load_dotenv
from routers import (
    trainer_routes,
    workout_routes,
    membership_routes,
    customer_routes,
    gym_image_routes,
    owner_routes,
    auth_routes,
    general_routes
)

load_dotenv()
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Register routers
app.include_router(auth_routes.router)
app.include_router(owner_routes.router)
app.include_router(trainer_routes.router)
app.include_router(customer_routes.router)
app.include_router(membership_routes.router)
app.include_router(workout_routes.router)
app.include_router(gym_image_routes.router)

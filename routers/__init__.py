from fastapi import APIRouter
from routers.customer_routes import router as customer_router
from routers.trainer_routes import router as trainer_router
from routers.owner_routes import router as owner_router
from routers.workout_routes import router as workout_router

# Create the main router
router = APIRouter()

# Include all routers
router.include_router(customer_router, prefix="/customers", tags=["Customers"])
router.include_router(trainer_router, prefix="/trainers", tags=["Trainers"])
router.include_router(owner_router, prefix="/owners", tags=["Owners"])
router.include_router(workout_router, prefix="/workouts", tags=["Workouts"])

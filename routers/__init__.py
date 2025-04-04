from fastapi import APIRouter
from routes.customer_routes import router as customer_router
from routes.trainer_routes import router as trainer_router
from routes.owner_routes import router as owner_router
from routes.workout_routes import router as workout_router
from routes.auth_routes import router as auth_router
from routes.admin_routes import router as admin_router

# Create the main router
router = APIRouter()

# Include all routers
router.include_router(customer_router, prefix="/customers", tags=["Customers"])
router.include_router(trainer_router, prefix="/trainers", tags=["Trainers"])
router.include_router(owner_router, prefix="/owners", tags=["Owners"])
router.include_router(workout_router, prefix="/workouts", tags=["Workouts"])
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(admin_router, prefix="/admin", tags=["Admin"])

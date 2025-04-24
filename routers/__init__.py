from fastapi import APIRouter
from routers.client.client_auth_routes import client_auth_router  
from routers.trainer.trainer_auth_routes import trainer_auth_router
from routers.owner.owner_auth_routes import  owner_auth_router
from routers.owner.membership_routes import membership_router
from routers.owner.gym_image_routes import gym_image_router    
from routers.trainer.workout_routes import  workout_router    
from routers.trainer.trainer_auth_routes import trainer_auth_router
# Create the main router
router = APIRouter()

# Include user routers
router.include_router(client_auth_router, prefix="/clients", tags=["Clients"])
router.include_router(trainer_auth_router, prefix="/trainers", tags=["Trainers"])
router.include_router(owner_auth_router, prefix="/owners", tags=["Owners"])

# Include auth routers
router.include_router(client_auth_router, prefix="/auth/client", tags=["Client Auth"])
router.include_router(trainer_auth_router, prefix="/auth/trainer", tags=["Trainer Auth"])
router.include_router(owner_auth_router, prefix="/auth/owner", tags=["Owner Auth"])

# Include core domain routers
router.include_router(workout_router, prefix="/workouts", tags=["Workouts"])
router.include_router(membership_router, prefix="/memberships", tags=["Memberships"])

# Include general-purpose routers
router.include_router(gym_image_router, prefix="/gyms", tags=["Gym Images"])

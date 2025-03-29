from fastapi import FastAPI
from routers import customer_routes, trainer_routes, owner_routes
from database import engine, Base

# Creating all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Including routers for API endpoint
app.include_router(customer_routes.router, prefix="/customer", tags=["Customer"])
app.include_router(trainer_routes.router, prefix="/trainer", tags=["Trainer"])
app.include_router(owner_routes.router, prefix="/owner", tags=["Owner"])

@app.get("/")
def home():
    return {"message": "Welcome to the Fitness Management System"}


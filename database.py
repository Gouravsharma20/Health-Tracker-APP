# database.py
import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Read the database URL from the environment variable set in docker-compose.yml
# Fallback to localhost only if the env var isn't set (useful for running outside docker)
DATABASE_URL = os.getenv("DATABASE_URL", "mysql+pymysql://root:Gourav12345@localhost:3306/healthTrackerApp")

print(f"--- Connecting to Database URL: {DATABASE_URL} ---") # Optional: Add for debugging

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
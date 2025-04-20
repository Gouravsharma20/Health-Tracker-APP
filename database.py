import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from dotenv import load_dotenv
import pymysql

# ✅ Load env variables from .env
load_dotenv()

# Check if running in Docker (optional)
IS_DOCKER = os.getenv("RUNNING_IN_DOCKER", "false").lower() == "true"

# ✅ Use values from environment
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASSWORD")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"




print(f"--- Connecting to Database: {DATABASE_URL} ---")

# SQLAlchemy setup
Base = declarative_base()

# Retry connection
MAX_RETRIES = 5
for attempt in range(MAX_RETRIES):
    try:
        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        print("✅ Database connection successful!")
        break
    except Exception as e:
        print(f"⚠️ Database connection failed: {e}")
        if attempt < MAX_RETRIES - 1:
            wait_time = 2 ** attempt
            print(f"🔄 Retrying in {wait_time} seconds...")
            time.sleep(wait_time)
        else:
            print("❌ Failed to connect after multiple attempts. Exiting.")
            raise ConnectionError("Unable to connect to the database after multiple attempts.")

# FastAPI dependency
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

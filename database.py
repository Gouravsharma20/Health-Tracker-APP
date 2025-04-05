import os
import time
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker ,Session

# Detect if running inside Docker
IS_DOCKER = os.getenv("RUNNING_IN_DOCKER", "false").lower() == "true"

# Use Docker hostname if inside a container, otherwise fallback to localhost
DB_HOST = "mysql-db" if IS_DOCKER else "localhost"
DB_NAME = "healthTrackerApp"
DB_USER = "root"
DB_PASS = "Gourav12345"

DATABASE_URL = "mysql+pymysql://root:Gourav12345@localhost:3306/healthTrackerApp"


print(f"--- Connecting to Database: {DATABASE_URL} ---")
Base = declarative_base()

# Retry mechanism for connecting to MySQL
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
            print("🔄 Retrying in 5 seconds...")
            time.sleep(5)
        else:
            print("❌ Failed to connect after multiple attempts. Exiting.")
            exit(1)
def get_db():
    db: Session = SessionLocal()
    try:
        yield db
    finally:
        db.close()

"""# Database configuration and session management
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# SQLite database URL
DATABASE_URL = "sqlite:///./test.db"

# Creating database engine
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Creating a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for models
Base = declarative_base()
"""
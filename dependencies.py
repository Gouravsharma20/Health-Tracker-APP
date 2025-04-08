# Dependency to get the database session
from database import SessionLocal
import redis

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

redis_client = redis.StrictRedis(host="localhost", port=6379, db=0, decode_responses=True)

# Dependency to get the database session
from database import SessionLocal
import redis
import os

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

redis_client = redis.StrictRedis(
    host=os.getenv("REDIS_HOST","localhost"),
    port=int(os.getenv("REDIS_PORT",6379)),
    db=int(os.getenv("REDIS_DB",0)),
    decode_responses=True
    )

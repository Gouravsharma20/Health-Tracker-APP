from datetime import datetime, timedelta
from jose import JWTError, jwt
import uuid
import os
import redis
from dotenv import load_dotenv

load_dotenv()

# Load environment variables
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))
REDIS_HOST = os.getenv("REDIS_HOST", "localhost")
REDIS_PORT = int(os.getenv("REDIS_PORT", 6379))

# Redis client
r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)

def create_access_token(data: dict):
    to_encode = data.copy()
    jti = str(uuid.uuid4())  # Unique token ID
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    issued_at = datetime.utcnow()

    to_encode.update({
        "exp": expire,
        "iat": issued_at,
        "jti": jti
    })

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt, jti

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        jti = payload.get("jti")

        # Check Redis for blacklisted token
        if jti and r.get(jti) == "blacklisted":
            raise JWTError("Token has been blacklisted")

        return payload
    except JWTError as e:
        raise JWTError(f"Invalid or expired token: {str(e)}")

def blacklist_token(jti: str, exp: int):
    """
    Blacklists a token by storing its jti in Redis until it expires.
    """
    ttl = exp - int(datetime.utcnow().timestamp())
    if ttl > 0:
        r.setex(jti, ttl, "blacklisted")

# auth/password_utils.py

from passlib.context import CryptContext
from typing import Tuple
import os
from dotenv import load_dotenv

load_dotenv()

# Load configuration from .env
BCRYPT_ROUNDS = int(os.getenv("BCRYPT_ROUNDS", 12))  # Default to 12 if not specified
PEPPER = os.getenv("PEPPER_KEY", "")

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto",
    bcrypt__rounds=BCRYPT_ROUNDS
)

def apply_pepper(password: str) -> str:
    """
    Append a server-side secret (pepper) to the password.
    """
    return password + PEPPER

def hash_password(password: str) -> str:
    """
    Hash a password using bcrypt with pepper and rounds.
    """
    peppered = apply_pepper(password)
    return pwd_context.hash(peppered)

def verify_password(plain_password: str, hashed_password: str) -> Tuple[bool, bool]:
    """
    Verify a password against a hashed one. Returns a tuple:
    (is_valid, needs_rehash)
    """
    peppered = apply_pepper(plain_password)
    is_valid = pwd_context.verify(peppered, hashed_password)
    needs_rehash = is_valid and pwd_context.needs_update(hashed_password)

    # Optional: Log or handle rehashing event
    # if needs_rehash:
    #     print("[INFO] Password needs rehashing.")

    return is_valid, needs_rehash

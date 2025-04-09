from pydantic import BaseModel
from typing import Optional

class Token(BaseModel):
    access_token: str
    token_type: str  # typically 'bearer'
    expires_in: Optional[int] = None  # in seconds
    refresh_token: Optional[str] = None  # if implementing refresh logic

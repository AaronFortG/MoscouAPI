from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    firebase_uid: str
    name: Optional[str] = None
    email: Optional[str] = None
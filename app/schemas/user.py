from pydantic import BaseModel
from typing import Optional

class UserResponse(BaseModel):
    firebase_uid: str
    name: Optional[str] = None
    email: Optional[str] = None

    class Config:
        schema_extra = {
            "example": {
                "firebase_uid": "abc123",
                "name": "John Doe",
                "email": "johndoe@example.com"
            }
        }
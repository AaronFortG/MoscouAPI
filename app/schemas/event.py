from datetime import datetime
from pydantic import BaseModel, validator
from typing import Optional


class EventSchema(BaseModel):
    event_id: Optional[int] = None
    name: str
    price: float
    description: Optional[str] = None
    image_url: Optional[str] = None
    event_date: datetime
    created_at: datetime

    class Config:
        # Use a custom JSON encoder to ensure datetime fields are in ISO format with a 'Z'
        json_encoders = {
            datetime: lambda dt: dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if dt else None
        }

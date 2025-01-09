from datetime import datetime
from pydantic import BaseModel, validator
from typing import Optional

class EventCreate(BaseModel):
    name: str
    price: float
    image_url: Optional[str] = None
    event_date: datetime

    @validator('event_date', pre=True)
    def strip_timezone(cls, value):
        if isinstance(value, str):
            value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        if value.tzinfo is not None:
            value = value.astimezone(tz=None).replace(tzinfo=None)
        return value
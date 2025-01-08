from pydantic import BaseModel
from typing import Optional

class EventCreate(BaseModel):
    name: str
    price: float
    image_url: Optional[str] = None
    event_date: str

from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TicketCreate(BaseModel):
    user_id: str
    event_id: int
    qr_code: str


class TicketValidate(BaseModel):
    validator_id: str

class TicketResponse(BaseModel):
    ticket_id: int
    user_id: str
    user_name: str
    event_id: int
    qr_code: str
    validated: bool
    validator_id: Optional[str] = None
    validator_name: Optional[str] = None
    validated_date: Optional[datetime] = None
    purchased_at: datetime

    class Config:
        # Use a custom JSON encoder to ensure datetime fields are in ISO format with a 'Z'
        json_encoders = {
            datetime: lambda dt: dt.strftime("%Y-%m-%dT%H:%M:%S.%fZ") if dt else None
        }
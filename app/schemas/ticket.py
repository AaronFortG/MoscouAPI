from pydantic import BaseModel


class TicketCreate(BaseModel):
    user_id: str
    event_id: int
    qr_code: str


class TicketValidate(BaseModel):
    validator_id: str

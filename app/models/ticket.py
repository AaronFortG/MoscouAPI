from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from app.database import Base
from sqlalchemy.sql import func

class TicketModel(Base):
    __tablename__ = "tickets"
    ticket_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(String(128), ForeignKey("users.firebase_uid"), nullable=False)
    validator_id = Column(String(128), ForeignKey("users.firebase_uid"), nullable=True)
    event_id = Column(Integer, ForeignKey("events.event_id"), nullable=False)
    validated = Column(Boolean, default=False)
    qr_code = Column(String, nullable=True)
    validated_date = Column(DateTime, nullable=True)
    purchased_at = Column(DateTime, default=func.now())

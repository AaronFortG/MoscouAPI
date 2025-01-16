from sqlalchemy import Column, Integer, Float, DateTime, Text, String
from app.database import Base
from sqlalchemy.sql import func

class Event(Base):
    __tablename__ = "events"
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    description = Column(Text, nullable=True)
    image_url = Column(Text, nullable=True)
    event_date = Column(DateTime(timezone=True), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default="CURRENT_TIMESTAMP")

from sqlalchemy import Column, Integer, String, Float, DateTime
from app.database import Base
from sqlalchemy.sql import func

class Event(Base):
    __tablename__ = "events"
    event_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    price = Column(Float, nullable=False)
    image_url = Column(String, nullable=True)
    event_date = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=func.now())

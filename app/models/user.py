from sqlalchemy import Column, String
from app.database import Base

class User(Base):
    __tablename__ = "users"
    firebase_uid = Column(String(128), primary_key=True)
    name = Column(String(100), nullable=True)
    email = Column(String(100), nullable=True)

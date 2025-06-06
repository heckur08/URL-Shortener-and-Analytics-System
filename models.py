from sqlalchemy import Column, Integer, String, Text, DateTime, func
from database import Base

class URL(Base):
    __tablename__ = "urls"
    id = Column(Integer, primary_key=True, index=True)
    long_url = Column(Text, nullable=False)
    short_code = Column(String(10), unique=True, nullable=False)
    created_at = Column(DateTime, default=func.now())

class Click(Base):
    __tablename__ = "clicks"
    id = Column(Integer, primary_key=True)
    short_code = Column(String(10))
    timestamp = Column(DateTime, default=func.now())
    ip_address = Column(String(45))
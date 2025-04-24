from sqlalchemy import Column, Integer, String, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Quote(Base):
    __tablename__ = "quotes"
    id = Column(Integer, primary_key=True, index=True)
    platform = Column(String, index=True)
    event_id = Column(String, index=True)
    market_id = Column(String, index=True)
    outcomes = Column(JSON)
    timestamp = Column(DateTime)

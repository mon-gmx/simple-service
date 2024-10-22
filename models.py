import datetime
from dataclasses import dataclass

from sqlalchemy import Column, DateTime, Integer, String
from sqlalchemy.orm import declarative_base

Base = declarative_base()


@dataclass
class RequestLog(Base):
    __tablename__ = "requests"

    id: int
    ip_address: str
    endpoint: str
    method: str
    response_code: int
    timestamp: datetime

    id = Column(Integer, primary_key=True)
    ip_address = Column(String, nullable=False)
    endpoint = Column(String, nullable=False)
    method = Column(String, nullable=False)
    response_code = Column(Integer, nullable=False)
    timestamp = Column(DateTime, nullable=False)

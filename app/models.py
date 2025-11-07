from sqlalchemy import Column, Integer, String, DateTime
from sqlalchemy.sql import func
from .database import Base

class Link(Base):
    __tablename__ = "links"

    id = Column(Integer, primary_key=True, index=True)
    shortCode = Column(String, unique=True, index=True)
    longUrl = Column(String, nullable=False)
    createdAt  = Column(DateTime(timezone=True), server_default=func.now())
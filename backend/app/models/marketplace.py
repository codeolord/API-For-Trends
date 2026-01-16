from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from app.database import Base


class Marketplace(Base):
    __tablename__ = "marketplaces"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)  # amazon, etsy, shopify, printful
    last_scraped = Column(DateTime, nullable=True)
    next_scrape = Column(DateTime, nullable=True)
    status = Column(String(50), default="active")  # active, paused, error
    error_message = Column(String(500), nullable=True)
    
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, ForeignKey, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    marketplace = Column(String(50), index=True)  # amazon, etsy, shopify, etc
    external_id = Column(String(255), unique=True, index=True)
    title = Column(String(500))
    description = Column(Text)
    category = Column(String(200), index=True)
    price = Column(Float)
    rating = Column(Float, nullable=True)
    reviews_count = Column(Integer, default=0)
    sales_count = Column(Integer, nullable=True)
    image_url = Column(String(500))
    product_url = Column(String(500), unique=True)
    
    # Metadata
    tags = Column(JSON)  # ["tag1", "tag2", ...]
    keywords = Column(JSON)
    raw_data = Column(JSON)  # Store original scrape data
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    last_scraped = Column(DateTime, nullable=True)
    
    # Relationships
    trend_id = Column(Integer, ForeignKey("trends.id"), nullable=True)
    trend = relationship("Trend", back_populates="products")
    
    __table_args__ = (
        Index("idx_marketplace_category", "marketplace", "category"),
        Index("idx_created_at", "created_at"),
    )

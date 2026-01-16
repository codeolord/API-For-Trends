from sqlalchemy import Column, Integer, String, Float, DateTime, Text, JSON, Index
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Trend(Base):
    __tablename__ = "trends"

    id = Column(Integer, primary_key=True, index=True)
    niche = Column(String(200), index=True)
    category = Column(String(200), index=True)
    
    # Trend scoring
    demand_score = Column(Float)  # 0-100
    competition_score = Column(Float)  # 0-100
    growth_score = Column(Float)  # 0-100
    profitability_score = Column(Float)  # 0-100
    overall_score = Column(Float)  # Weighted average
    
    # Market data
    marketplace_counts = Column(JSON)  # {"amazon": 150, "etsy": 200, ...}
    avg_price = Column(Float)
    price_range = Column(JSON)  # {"min": 10, "max": 50}
    total_reviews = Column(Integer)
    avg_rating = Column(Float)
    
    # Analysis
    target_audience = Column(JSON)  # {demographics, interests, pain points}
    style_patterns = Column(JSON)  # [{color: "", material: "", design_type: ""}, ...]
    growth_indicators = Column(JSON)
    season_trend = Column(String(50))  # evergreen, seasonal, trending, declining
    
    # Description
    summary = Column(Text)
    insights = Column(JSON)  # Key insights about this trend
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    next_analysis = Column(DateTime, nullable=True)
    
    # Relationships
    products = relationship("Product", back_populates="trend")
    designs = relationship("Design", back_populates="trend")
    
    __table_args__ = (
        Index("idx_niche_category", "niche", "category"),
        Index("idx_overall_score", "overall_score"),
    )

from sqlalchemy import Column, Integer, String, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base


class Design(Base):
    __tablename__ = "designs"

    id = Column(Integer, primary_key=True, index=True)
    trend_id = Column(Integer, ForeignKey("trends.id"), index=True)
    
    title = Column(String(300))
    description = Column(Text)
    
    # Design data
    design_prompt = Column(Text)
    design_metadata = Column(JSON)  # style, colors, elements, etc
    
    # Generated assets
    image_url = Column(String(500))
    mockup_urls = Column(JSON)  # URLs for different product mockups
    
    # Print-on-demand data
    printful_template_id = Column(String(100), nullable=True)
    print_specifications = Column(JSON)  # {size, colors, placement, etc}
    
    # Status
    status = Column(String(50), default="draft")  # draft, ready, published
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow, index=True)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    trend = relationship("Trend", back_populates="designs")

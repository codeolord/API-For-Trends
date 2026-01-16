from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict, Any


class ProductCreate(BaseModel):
    marketplace: str
    external_id: str
    title: str
    description: Optional[str] = None
    category: str
    price: float
    rating: Optional[float] = None
    reviews_count: int = 0
    sales_count: Optional[int] = None
    image_url: str
    product_url: str
    tags: Optional[List[str]] = None
    keywords: Optional[List[str]] = None
    raw_data: Optional[Dict[str, Any]] = None


class ProductResponse(ProductCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    last_scraped: Optional[datetime] = None
    trend_id: Optional[int] = None

    class Config:
        from_attributes = True

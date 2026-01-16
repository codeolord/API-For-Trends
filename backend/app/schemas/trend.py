from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict, Any


class TrendCreate(BaseModel):
    niche: str
    category: str
    demand_score: float
    competition_score: float
    growth_score: float
    profitability_score: float
    overall_score: float
    marketplace_counts: Dict[str, int]
    avg_price: float
    price_range: Dict[str, float]
    total_reviews: int
    avg_rating: float
    target_audience: Optional[Dict[str, Any]] = None
    style_patterns: Optional[List[Dict[str, Any]]] = None
    growth_indicators: Optional[Dict[str, Any]] = None
    season_trend: Optional[str] = "evergreen"
    summary: Optional[str] = None
    insights: Optional[List[str]] = None


class TrendResponse(TrendCreate):
    id: int
    created_at: datetime
    updated_at: datetime
    next_analysis: Optional[datetime] = None

    class Config:
        from_attributes = True

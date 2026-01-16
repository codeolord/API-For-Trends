from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models import Trend
from app.schemas.trend import TrendResponse, TrendCreate
from typing import List

router = APIRouter()


@router.get("", response_model=List[TrendResponse])
def list_trends(
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    niche: str = Query(None),
    category: str = Query(None),
    min_score: float = Query(0, ge=0, le=100),
    db: Session = Depends(get_db),
):
    """List all trends with optional filters"""
    query = db.query(Trend)
    
    if niche:
        query = query.filter(Trend.niche.ilike(f"%{niche}%"))
    if category:
        query = query.filter(Trend.category.ilike(f"%{category}%"))
    if min_score:
        query = query.filter(Trend.overall_score >= min_score)
    
    trends = query.order_by(desc(Trend.overall_score)).offset(skip).limit(limit).all()
    return trends


@router.get("/{trend_id}", response_model=TrendResponse)
def get_trend(trend_id: int, db: Session = Depends(get_db)):
    """Get a specific trend by ID"""
    trend = db.query(Trend).filter(Trend.id == trend_id).first()
    if not trend:
        raise HTTPException(status_code=404, detail="Trend not found")
    return trend


@router.post("", response_model=TrendResponse)
def create_trend(trend_data: TrendCreate, db: Session = Depends(get_db)):
    """Create a new trend"""
    trend = Trend(**trend_data.dict())
    db.add(trend)
    db.commit()
    db.refresh(trend)
    return trend

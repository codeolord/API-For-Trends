from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models import Design
from app.schemas.design import DesignResponse, DesignCreate
from typing import List

router = APIRouter()


@router.get("", response_model=List[DesignResponse])
def list_designs(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    trend_id: int = Query(None),
    status: str = Query(None),
    db: Session = Depends(get_db),
):
    """List designs with optional filters"""
    query = db.query(Design)
    
    if trend_id:
        query = query.filter(Design.trend_id == trend_id)
    if status:
        query = query.filter(Design.status == status)
    
    designs = query.order_by(desc(Design.created_at)).offset(skip).limit(limit).all()
    return designs


@router.get("/{design_id}", response_model=DesignResponse)
def get_design(design_id: int, db: Session = Depends(get_db)):
    """Get a specific design by ID"""
    design = db.query(Design).filter(Design.id == design_id).first()
    if not design:
        raise HTTPException(status_code=404, detail="Design not found")
    return design


@router.post("", response_model=DesignResponse)
def create_design(design_data: DesignCreate, db: Session = Depends(get_db)):
    """Create a new design"""
    design = Design(**design_data.dict())
    db.add(design)
    db.commit()
    db.refresh(design)
    return design

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.database import get_db
from app.models import Product
from app.schemas.product import ProductResponse, ProductCreate
from typing import List

router = APIRouter()


@router.get("", response_model=List[ProductResponse])
def list_products(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    marketplace: str = Query(None),
    category: str = Query(None),
    min_rating: float = Query(0, ge=0, le=5),
    db: Session = Depends(get_db),
):
    """List products with optional filters"""
    query = db.query(Product)
    
    if marketplace:
        query = query.filter(Product.marketplace == marketplace)
    if category:
        query = query.filter(Product.category.ilike(f"%{category}%"))
    if min_rating:
        query = query.filter(Product.rating >= min_rating)
    
    products = query.order_by(desc(Product.created_at)).offset(skip).limit(limit).all()
    return products


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Get a specific product by ID"""
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@router.post("", response_model=ProductResponse)
def create_product(product_data: ProductCreate, db: Session = Depends(get_db)):
    """Create a new product record"""
    product = Product(**product_data.dict())
    db.add(product)
    db.commit()
    db.refresh(product)
    return product

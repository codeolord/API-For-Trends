from fastapi import APIRouter
from app.api import trends, products, designs

api_router = APIRouter(prefix="/api/v1")

api_router.include_router(trends.router, prefix="/trends", tags=["trends"])
api_router.include_router(products.router, prefix="/products", tags=["products"])
api_router.include_router(designs.router, prefix="/designs", tags=["designs"])

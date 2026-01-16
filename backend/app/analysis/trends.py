from typing import List, Dict, Any
from sqlalchemy.orm import Session
from app.models import Trend, Product
from app.utils.logger import logger
from datetime import datetime
import math


def calculate_trend_scores(products: List[Product]) -> Dict[str, float]:
    """Calculate trend scores based on product metrics"""
    
    if not products:
        return {
            "demand_score": 0,
            "competition_score": 50,
            "growth_score": 0,
            "profitability_score": 0,
            "overall_score": 0
        }
    
    total_reviews = sum(p.reviews_count for p in products)
    avg_price = sum(p.price for p in products) / len(products) if products else 0
    avg_rating = sum(p.rating for p in products if p.rating) / len([p for p in products if p.rating]) if any(p.rating for p in products) else 0
    
    # Demand: Based on review count and recency
    demand_score = min(100, (total_reviews / 10) + (avg_rating * 5))
    
    # Competition: More products = more competition
    competition_score = min(100, len(products))
    
    # Growth: Based on average rating and review velocity
    growth_score = min(100, (avg_rating * 20) + 10)
    
    # Profitability: Based on price point and demand
    profitability_score = min(100, (avg_price / 50 * 50) + (avg_rating * 10))
    
    # Overall: Weighted average
    overall_score = (
        demand_score * 0.25 +
        (100 - competition_score) * 0.25 +
        growth_score * 0.25 +
        profitability_score * 0.25
    )
    
    return {
        "demand_score": round(demand_score, 2),
        "competition_score": round(competition_score, 2),
        "growth_score": round(growth_score, 2),
        "profitability_score": round(profitability_score, 2),
        "overall_score": round(overall_score, 2)
    }


def infer_audience(products: List[Product]) -> Dict[str, Any]:
    """Infer target audience from products"""
    
    categories = {}
    price_points = []
    
    for product in products:
        # Aggregate categories
        if product.category:
            categories[product.category] = categories.get(product.category, 0) + 1
        price_points.append(product.price)
    
    avg_price = sum(price_points) / len(price_points) if price_points else 0
    
    return {
        "primary_categories": sorted(categories.items(), key=lambda x: x[1], reverse=True)[:3],
        "price_sensitivity": "budget" if avg_price < 20 else "mid" if avg_price < 50 else "premium",
        "avg_price": round(avg_price, 2),
        "demographics": {
            "estimated_age_group": "18-45",
            "interests": ["design", "personalization", "unique products"],
            "pain_points": ["quality", "customization", "fast shipping"]
        }
    }


def analyze_trends(db: Session) -> List[Trend]:
    """Analyze products and create/update trends"""
    logger.info("Starting trend analysis")
    
    # Group products by niche (category + common keywords)
    from sqlalchemy import func
    
    categories = db.query(Product.category).distinct().filter(Product.category != None).all()
    trends_created = []
    
    for (category,) in categories:
        products = db.query(Product).filter(Product.category == category).all()
        
        if len(products) < 3:  # Need minimum products to form a trend
            continue
        
        # Calculate scores
        scores = calculate_trend_scores(products)
        audience = infer_audience(products)
        
        # Get marketplace distribution
        marketplace_counts = {}
        for product in products:
            marketplace_counts[product.marketplace] = marketplace_counts.get(product.marketplace, 0) + 1
        
        # Calculate price range
        prices = [p.price for p in products if p.price]
        price_range = {
            "min": min(prices) if prices else 0,
            "max": max(prices) if prices else 0
        }
        
        # Create or update trend
        existing_trend = db.query(Trend).filter(
            Trend.category == category
        ).first()
        
        trend_data = {
            "niche": category,
            "category": category,
            "demand_score": scores["demand_score"],
            "competition_score": scores["competition_score"],
            "growth_score": scores["growth_score"],
            "profitability_score": scores["profitability_score"],
            "overall_score": scores["overall_score"],
            "marketplace_counts": marketplace_counts,
            "avg_price": sum(prices) / len(prices) if prices else 0,
            "price_range": price_range,
            "total_reviews": sum(p.reviews_count for p in products),
            "avg_rating": sum(p.rating for p in products if p.rating) / len([p for p in products if p.rating]) if any(p.rating for p in products) else 0,
            "target_audience": audience,
            "style_patterns": [{"category": p.category, "price": p.price} for p in products[:5]],
            "season_trend": "evergreen",
            "summary": f"{category} products showing strong demand",
            "insights": [
                f"Found {len(products)} products in this niche",
                f"Average rating: {round(sum(p.rating for p in products if p.rating) / len([p for p in products if p.rating]) if any(p.rating for p in products) else 0, 2)}",
                f"Price range: ${price_range['min']:.2f} - ${price_range['max']:.2f}"
            ],
            "next_analysis": datetime.utcnow()
        }
        
        if existing_trend:
            for key, value in trend_data.items():
                setattr(existing_trend, key, value)
            db.commit()
            trends_created.append(existing_trend)
        else:
            trend = Trend(**trend_data)
            db.add(trend)
            db.commit()
            db.refresh(trend)
            trends_created.append(trend)
    
    logger.info(f"Created/updated {len(trends_created)} trends")
    return trends_created

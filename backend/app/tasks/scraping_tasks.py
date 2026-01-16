from celery import shared_task
from app.utils.logger import logger
from app.database import SessionLocal
from app.analysis.trends import analyze_trends
import logging

logger_task = logging.getLogger("pod_trends.tasks")


@shared_task
def scrape_marketplace(marketplace: str):
    """Scrape a marketplace for products"""
    logger_task.info(f"Starting scrape for {marketplace}")
    try:
        from app.scrapers import scrapers
        scraper = scrapers.get_scraper(marketplace)
        products = scraper.scrape()
        logger_task.info(f"Scraped {len(products)} products from {marketplace}")
        return {"status": "success", "count": len(products)}
    except Exception as e:
        logger_task.error(f"Error scraping {marketplace}: {str(e)}")
        return {"status": "error", "message": str(e)}


@shared_task
def analyze_trends_task():
    """Analyze trends from collected products"""
    logger_task.info("Starting trend analysis")
    db = SessionLocal()
    try:
        trends = analyze_trends(db)
        logger_task.info(f"Analyzed {len(trends)} trends")
        return {"status": "success", "trend_count": len(trends)}
    except Exception as e:
        logger_task.error(f"Error analyzing trends: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()


@shared_task
def generate_designs_task(trend_id: int):
    """Generate designs for a specific trend"""
    logger_task.info(f"Generating designs for trend {trend_id}")
    db = SessionLocal()
    try:
        from app.ai.design_generator import DesignGenerator
        generator = DesignGenerator()
        designs = generator.generate_for_trend(trend_id, db)
        logger_task.info(f"Generated {len(designs)} designs for trend {trend_id}")
        return {"status": "success", "design_count": len(designs)}
    except Exception as e:
        logger_task.error(f"Error generating designs: {str(e)}")
        return {"status": "error", "message": str(e)}
    finally:
        db.close()

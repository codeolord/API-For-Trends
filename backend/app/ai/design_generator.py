from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models import Design, Trend
from app.config import get_settings
from app.utils.logger import logger
import json
import re

settings = get_settings()


class DesignGenerator:
    """Generate AI-powered designs for trends"""
    
    def __init__(self):
        self.logger = logger
        self.client = self._init_client()
    
    def _init_client(self):
        """Initialize OpenAI or Anthropic client"""
        if settings.openai_api_key:
            import openai
            return openai.OpenAI(api_key=settings.openai_api_key)
        elif settings.anthropic_api_key:
            import anthropic
            return anthropic.Anthropic(api_key=settings.anthropic_api_key)
        else:
            self.logger.warning("No AI API key configured")
            return None
    
    def generate_for_trend(self, trend_id: int, db: Session) -> List[Design]:
        """Generate multiple designs for a trend"""
        trend = db.query(Trend).filter(Trend.id == trend_id).first()
        if not trend:
            self.logger.error(f"Trend {trend_id} not found")
            return []
        
        self.logger.info(f"Generating designs for trend: {trend.niche}")
        designs = []
        
        # Generate 3 different design prompts
        for i in range(3):
            prompt = self._create_design_prompt(trend, i)
            design = self._create_design(trend, prompt, db)
            if design:
                designs.append(design)
        
        return designs
    
    def _create_design_prompt(self, trend: Trend, variant: int) -> str:
        """Create a design prompt for a trend"""
        variants = [
            f"Modern minimalist design for {trend.niche} with clean lines and trending colors",
            f"Bold and colorful design for {trend.niche} with eye-catching typography",
            f"Vintage-inspired design for {trend.niche} with nostalgic elements"
        ]
        
        return variants[variant % len(variants)]
    
    def _create_design(self, trend: Trend, prompt: str, db: Session) -> Optional[Design]:
        """Create a design record for a trend"""
        try:
            design = Design(
                trend_id=trend.id,
                title=f"{trend.niche} Design - Variant",
                description=f"AI-generated design for the {trend.niche} trend",
                design_prompt=prompt,
                design_metadata={
                    "trend_niche": trend.niche,
                    "target_audience": trend.target_audience,
                    "colors": ["#FF6B6B", "#4ECDC4", "#45B7D1"],
                    "style": "modern"
                },
                print_specifications={
                    "size": "A4",
                    "colors": "4C",
                    "material": "100% cotton",
                    "placement": "front"
                },
                status="draft"
            )
            db.add(design)
            db.commit()
            db.refresh(design)
            self.logger.info(f"Created design: {design.id}")
            return design
        except Exception as e:
            self.logger.error(f"Error creating design: {str(e)}")
            db.rollback()
            return None
    
    def generate_image(self, prompt: str) -> Optional[str]:
        """Generate an image using Stable Diffusion or similar"""
        if not self.client:
            self.logger.warning("No AI client available")
            return None
        
        try:
            # This is a placeholder - actual implementation would call image generation API
            self.logger.info(f"Generating image for prompt: {prompt}")
            return "https://placeholder-image-url.com/image.jpg"
        except Exception as e:
            self.logger.error(f"Error generating image: {str(e)}")
            return None
    
    def create_mockups(self, design_id: int, image_url: str, db: Session) -> List[str]:
        """Create product mockups for a design"""
        mockup_urls = []
        
        product_types = ["t-shirt", "hoodie", "mug", "poster"]
        
        for product_type in product_types:
            mockup_url = f"https://mockup-generator.example.com/{product_type}/{design_id}.jpg"
            mockup_urls.append(mockup_url)
        
        return mockup_urls

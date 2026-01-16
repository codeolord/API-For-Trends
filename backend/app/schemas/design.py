from pydantic import BaseModel
from datetime import datetime
from typing import Optional, Dict, Any, List


class DesignCreate(BaseModel):
    trend_id: int
    title: str
    description: Optional[str] = None
    design_prompt: str
    design_metadata: Optional[Dict[str, Any]] = None
    image_url: Optional[str] = None
    mockup_urls: Optional[List[str]] = None
    print_specifications: Optional[Dict[str, Any]] = None


class DesignResponse(DesignCreate):
    id: int
    status: str
    created_at: datetime
    updated_at: datetime
    printful_template_id: Optional[str] = None

    class Config:
        from_attributes = True

from typing import Optional
from app.config import get_settings
from app.utils.logger import logger

settings = get_settings()


class PrintfulClient:
    """Printful API client for managing print-on-demand products"""
    
    def __init__(self):
        self.api_key = settings.printful_api_key
        self.base_url = "https://api.printful.com"
        self.logger = logger
    
    def create_product(self, design_id: int, title: str, description: str) -> Optional[dict]:
        """Create a product in Printful"""
        self.logger.info(f"Creating Printful product: {title}")
        
        if not self.api_key:
            self.logger.warning("Printful API key not configured")
            return None
        
        try:
            # Placeholder for actual Printful API call
            product_data = {
                "external_id": f"design_{design_id}",
                "name": title,
                "description": description,
                "sync_product": {
                    "name": title,
                    "description": description,
                    "variants": [
                        {
                            "name": "T-Shirt - White",
                            "sku": f"design_{design_id}_tshirt_white",
                            "price": 14.99
                        }
                    ]
                }
            }
            
            self.logger.info(f"Product created in Printful: {product_data}")
            return product_data
        except Exception as e:
            self.logger.error(f"Error creating Printful product: {str(e)}")
            return None


class ShopifyClient:
    """Shopify API client for managing products"""
    
    def __init__(self):
        self.access_token = settings.shopify_access_token
        self.store_name = settings.shopify_store_name
        self.base_url = f"https://{self.store_name}.myshopify.com/admin/api/2023-10"
        self.logger = logger
    
    def create_draft_product(self, title: str, description: str, image_url: str, 
                            price: float) -> Optional[dict]:
        """Create a draft product in Shopify"""
        self.logger.info(f"Creating Shopify draft product: {title}")
        
        if not self.access_token:
            self.logger.warning("Shopify access token not configured")
            return None
        
        try:
            # Placeholder for actual Shopify API call
            product_data = {
                "product": {
                    "title": title,
                    "body_html": description,
                    "product_type": "Print-on-Demand",
                    "status": "draft",
                    "images": [
                        {
                            "src": image_url
                        }
                    ],
                    "variants": [
                        {
                            "price": price,
                            "sku": f"POD-{title.replace(' ', '-').lower()}"
                        }
                    ]
                }
            }
            
            self.logger.info(f"Draft product created in Shopify: {product_data}")
            return product_data
        except Exception as e:
            self.logger.error(f"Error creating Shopify draft product: {str(e)}")
            return None

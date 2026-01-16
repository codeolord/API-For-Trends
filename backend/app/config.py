from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # App
    app_name: str = "POD Trends Platform"
    environment: str = "development"
    debug: bool = True
    secret_key: str = "your-secret-key"

    # Database
    database_url: str = "postgresql://user:password@localhost:5432/pod_trends"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # API Keys
    openai_api_key: str = ""
    anthropic_api_key: str = ""
    
    # Third Party APIs
    printful_api_key: str = ""
    shopify_access_token: str = ""
    shopify_store_name: str = ""
    
    # Celery
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    
    # Image Generation
    stable_diffusion_api_key: str = ""
    
    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()

import os
from typing import Optional
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # MongoDB Configuration
    mongodb_url: str = "mongodb://localhost:27017"
    database_name: str = "fastapi_celery_demo"
    
    # Redis Configuration
    redis_url: str = "redis://localhost:6379/0"
    
    # Celery Configuration
    celery_broker_url: str = "redis://localhost:6379/0"
    celery_result_backend: str = "redis://localhost:6379/0"
    
    # Application Configuration
    app_host: str = "0.0.0.0"
    app_port: int = 8000
    debug: bool = True
    
    # Railway Configuration
    port: int = 8000
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Use Railway's PORT environment variable if available
        if "PORT" in os.environ:
            self.app_port = int(os.environ["PORT"])
            self.port = int(os.environ["PORT"])
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Create settings instance
settings = Settings() 
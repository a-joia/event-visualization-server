import os
from typing import List

class Settings:
    """Application settings"""
    
    # API Settings
    API_TITLE: str = "Dashboard API"
    API_DESCRIPTION: str = "API for the dashboard application"
    API_VERSION: str = "1.0.0"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["*"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Database Settings
    DATABASE_URL: str = f"sqlite+aiosqlite:///{os.path.join(os.path.dirname(__file__), 'events.db')}"
    
    # Pagination Settings
    DEFAULT_PAGE_SIZE: int = 20
    MAX_PAGE_SIZE: int = 100
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"

# Create settings instance
settings = Settings() 
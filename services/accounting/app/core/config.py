"""
Конфигурация приложения
"""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Основные настройки
    APP_NAME: str = "TW Accounting Service"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # База данных
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/tw_accounting"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # Безопасность
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Email настройки
    MAIL_USERNAME: str = ""
    MAIL_PASSWORD: str = ""
    MAIL_FROM: str = ""
    MAIL_PORT: int = 587
    MAIL_SERVER: str = ""
    MAIL_TLS: bool = True
    MAIL_SSL: bool = False
    
    # Валюты
    DEFAULT_CURRENCY: str = "USD"
    SUPPORTED_CURRENCIES: List[str] = ["USD", "USDT", "TRX"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Создание экземпляра настроек
settings = Settings()

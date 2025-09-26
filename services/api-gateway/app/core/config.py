"""
Конфигурация API Gateway
"""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Основные настройки
    APP_NAME: str = "TW API Gateway"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # URL сервисов
    ACCOUNTING_SERVICE_URL: str = "http://accounting:8000"
    TRAFFIC_ANALYTICS_SERVICE_URL: str = "http://traffic-analytics:8000"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Кэширование
    REDIS_URL: str = "redis://localhost:6379"
    CACHE_TTL: int = 300  # 5 минут
    
    # Timeout для запросов к сервисам
    SERVICE_TIMEOUT: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Создание экземпляра настроек
settings = Settings()

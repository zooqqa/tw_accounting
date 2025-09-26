"""
Конфигурация Traffic Analytics Service
"""

from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Настройки приложения"""
    
    # Основные настройки
    APP_NAME: str = "TW Traffic Analytics Service"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    
    # База данных
    DATABASE_URL: str = "postgresql://postgres:postgres@localhost:5432/tw_accounting"
    
    # Redis
    REDIS_URL: str = "redis://localhost:6379"
    
    # CORS
    ALLOWED_HOSTS: List[str] = ["*"]
    
    # Celery
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    
    # Файлы
    UPLOAD_DIR: str = "/app/uploads"
    MAX_FILE_SIZE: int = 100 * 1024 * 1024  # 100MB
    
    # Аналитика
    DEFAULT_TIMEZONE: str = "UTC"
    CACHE_TTL: int = 3600  # 1 час
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Создание экземпляра настроек
settings = Settings()

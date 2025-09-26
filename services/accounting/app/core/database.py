"""
Настройки базы данных
"""

from sqlmodel import SQLModel, create_engine, Session
from app.core.config import settings

# Создание движка базы данных
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Логирование SQL запросов в debug режиме
    pool_pre_ping=True,   # Проверка соединения перед использованием
    pool_recycle=300,     # Переподключение каждые 5 минут
)

def get_session():
    """Получение сессии базы данных"""
    with Session(engine) as session:
        yield session

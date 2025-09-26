"""
Настройки базы данных
"""

from typing import AsyncGenerator
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

# Создание синхронного движка базы данных (для создания таблиц)
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,  # Логирование SQL запросов в debug режиме
    pool_pre_ping=True,   # Проверка соединения перед использованием
    pool_recycle=300,     # Переподключение каждые 5 минут
)

# Создание асинхронного движка для FastAPI-Users
async_database_url = settings.DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")
async_engine = create_async_engine(async_database_url, echo=settings.DEBUG)
async_session_maker = sessionmaker(async_engine, class_=AsyncSession, expire_on_commit=False)


def get_session():
    """Получение синхронной сессии базы данных"""
    with Session(engine) as session:
        yield session


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Получение асинхронной сессии базы данных"""
    async with async_session_maker() as session:
        yield session

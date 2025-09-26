"""
Скрипт для инициализации базы данных
"""

from sqlmodel import SQLModel
from app.core.database import engine
from app.models import Base

def init_db():
    """Создание всех таблиц в базе данных"""
    print("Creating database tables...")
    SQLModel.metadata.create_all(engine)
    print("Database tables created successfully!")

if __name__ == "__main__":
    init_db()

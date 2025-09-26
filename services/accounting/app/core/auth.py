"""
Настройки аутентификации с FastAPI-Users
"""

from datetime import timedelta
from typing import Optional

from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase

from app.core.config import settings
from app.core.database import engine
from app.models.users import User

# Создание транспорта для JWT токенов
bearer_transport = BearerTransport(tokenUrl="auth/jwt/login")

# Создание стратегии JWT
def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )

# Создание бэкенда аутентификации
auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

# Создание адаптера базы данных
def get_user_db():
    yield SQLAlchemyUserDatabase(User, engine)

# Создание FastAPI Users
fastapi_users = FastAPIUsers[User, int](get_user_db, [auth_backend])

# Получение текущего пользователя
current_active_user = fastapi_users.current_user(active=True)
current_superuser = fastapi_users.current_user(active=True, superuser=True)

"""
TW Accounting Service
Основной модуль FastAPI приложения для учета финансов
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import settings
from app.core.database import engine
from app.models import Base

# Создание таблиц
Base.create_all(bind=engine)

# Создание FastAPI приложения
app = FastAPI(
    title="TW Accounting Service",
    description="Сервис бухгалтерии для учета финансов и транзакций",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Настройка CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_HOSTS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Настройка TrustedHost
app.add_middleware(
    TrustedHostMiddleware,
    allowed_hosts=settings.ALLOWED_HOSTS
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """Проверка состояния сервиса"""
    return {
        "status": "healthy",
        "service": "accounting",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": "TW Accounting Service",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Импорт API роутов
from app.api import auth
# from app.api import accounts, projects, categories, counterparties

# Включение роутов
app.include_router(auth.router, prefix="/api", tags=["authentication"])
# app.include_router(accounts.router, prefix="/api/accounts", tags=["accounts"])
# app.include_router(projects.router, prefix="/api/projects", tags=["projects"])
# app.include_router(categories.router, prefix="/api/categories", tags=["categories"])
# app.include_router(counterparties.router, prefix="/api/counterparties", tags=["counterparties"])

"""
TW Traffic Analytics Service
Основной модуль FastAPI приложения для аналитики трафика
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware

from app.core.config import settings

# Создание FastAPI приложения
app = FastAPI(
    title="TW Traffic Analytics Service",
    description="Сервис аналитики трафика для обработки данных из партнерских программ",
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
        "service": "traffic-analytics",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": "TW Traffic Analytics Service",
        "version": "1.0.0",
        "docs": "/docs"
    }

# Импорт API роутов (будут добавлены позже)
# from app.api import analytics, import_data, campaigns

# app.include_router(analytics.router, prefix="/api/analytics", tags=["analytics"])
# app.include_router(import_data.router, prefix="/api/import", tags=["import"])
# app.include_router(campaigns.router, prefix="/api/campaigns", tags=["campaigns"])

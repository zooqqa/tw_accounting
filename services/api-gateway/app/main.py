"""
TW API Gateway
Основной модуль FastAPI приложения для API Gateway
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.responses import JSONResponse
import httpx

from app.core.config import settings

# Создание FastAPI приложения
app = FastAPI(
    title="TW API Gateway",
    description="API Gateway для объединения сервисов бухгалтерии и аналитики",
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
    """Проверка состояния API Gateway"""
    return {
        "status": "healthy",
        "service": "api-gateway",
        "version": "1.0.0"
    }

# Root endpoint
@app.get("/")
async def root():
    """Корневой endpoint"""
    return {
        "message": "TW API Gateway",
        "version": "1.0.0",
        "docs": "/docs",
        "services": {
            "accounting": "/api/accounting",
            "traffic-analytics": "/api/traffic-analytics"
        }
    }

# Проксирование запросов к Accounting Service
@app.api_route("/api/accounting/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_accounting(request: Request, path: str):
    """Проксирование запросов к Accounting Service"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.ACCOUNTING_SERVICE_URL}/api/{path}"
            response = await client.request(
                method=request.method,
                url=url,
                headers=request.headers,
                params=request.query_params,
                content=await request.body()
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
                headers=dict(response.headers)
            )
    except httpx.RequestError as e:
        return JSONResponse(
            content={"error": f"Accounting service unavailable: {str(e)}"},
            status_code=503
        )

# Проксирование запросов к Traffic Analytics Service
@app.api_route("/api/traffic-analytics/{path:path}", methods=["GET", "POST", "PUT", "DELETE"])
async def proxy_traffic_analytics(request: Request, path: str):
    """Проксирование запросов к Traffic Analytics Service"""
    try:
        async with httpx.AsyncClient() as client:
            url = f"{settings.TRAFFIC_ANALYTICS_SERVICE_URL}/api/{path}"
            response = await client.request(
                method=request.method,
                url=url,
                headers=request.headers,
                params=request.query_params,
                content=await request.body()
            )
            return JSONResponse(
                content=response.json(),
                status_code=response.status_code,
                headers=dict(response.headers)
            )
    except httpx.RequestError as e:
        return JSONResponse(
            content={"error": f"Traffic Analytics service unavailable: {str(e)}"},
            status_code=503
        )

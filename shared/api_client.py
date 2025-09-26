"""
Общий HTTP клиент для взаимодействия между сервисами
"""

import httpx
from typing import Dict, Any, Optional
from pydantic import BaseModel


class APIClient:
    """HTTP клиент для взаимодействия с API"""
    
    def __init__(self, base_url: str, timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.timeout = timeout
    
    async def get(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """GET запрос"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}{endpoint}", params=params)
            response.raise_for_status()
            return response.json()
    
    async def post(self, endpoint: str, data: Optional[Dict] = None, json: Optional[BaseModel] = None) -> Dict[str, Any]:
        """POST запрос"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            if json:
                response = await client.post(f"{self.base_url}{endpoint}", json=json.dict())
            else:
                response = await client.post(f"{self.base_url}{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
    
    async def put(self, endpoint: str, data: Optional[Dict] = None, json: Optional[BaseModel] = None) -> Dict[str, Any]:
        """PUT запрос"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            if json:
                response = await client.put(f"{self.base_url}{endpoint}", json=json.dict())
            else:
                response = await client.put(f"{self.base_url}{endpoint}", json=data)
            response.raise_for_status()
            return response.json()
    
    async def delete(self, endpoint: str) -> Dict[str, Any]:
        """DELETE запрос"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.delete(f"{self.base_url}{endpoint}")
            response.raise_for_status()
            return response.json()


class AccountingServiceClient(APIClient):
    """Клиент для Accounting Service"""
    
    def __init__(self, base_url: str = "http://accounting:8000"):
        super().__init__(base_url)
    
    async def get_accounts(self) -> Dict[str, Any]:
        """Получение списка счетов"""
        return await self.get("/api/accounts")
    
    async def get_projects(self) -> Dict[str, Any]:
        """Получение списка проектов"""
        return await self.get("/api/projects")
    
    async def create_transaction(self, transaction_data: Dict) -> Dict[str, Any]:
        """Создание транзакции"""
        return await self.post("/api/transactions", data=transaction_data)


class TrafficAnalyticsServiceClient(APIClient):
    """Клиент для Traffic Analytics Service"""
    
    def __init__(self, base_url: str = "http://traffic-analytics:8000"):
        super().__init__(base_url)
    
    async def get_analytics(self) -> Dict[str, Any]:
        """Получение аналитики"""
        return await self.get("/api/analytics")
    
    async def import_csv(self, file_data: bytes, filename: str) -> Dict[str, Any]:
        """Импорт CSV файла"""
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            files = {"file": (filename, file_data, "text/csv")}
            response = await client.post(f"{self.base_url}/api/import/csv", files=files)
            response.raise_for_status()
            return response.json()

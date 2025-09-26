"""
Сервис для работы с криптовалютами
"""

import httpx
from decimal import Decimal
from datetime import datetime
from typing import Optional, Dict, Any
from sqlmodel import Session
from fastapi import HTTPException, status

from app.core.config import settings
from app.models.transactions import (
    Transaction, CryptoTransactionDetail, TransactionType, TransactionStatus
)
from app.models.accounts import Account
from app.services.transactions import TransactionService


class CryptoService:
    """Сервис для работы с криптовалютными операциями"""
    
    def __init__(self, db: Session):
        self.db = db
        self.transaction_service = TransactionService(db)
    
    async def get_trx_to_usd_rate(self) -> Decimal:
        """Получение курса TRX к USD"""
        try:
            async with httpx.AsyncClient() as client:
                # Используем CoinGecko API для получения курса
                response = await client.get(
                    "https://api.coingecko.com/api/v3/simple/price",
                    params={"ids": "tron", "vs_currencies": "usd"}
                )
                data = response.json()
                rate = Decimal(str(data["tron"]["usd"]))
                return rate
        except Exception as e:
            # В случае ошибки используем фиксированный курс
            return Decimal("0.10")  # Примерный курс TRX/USD
    
    async def get_usdt_to_usd_rate(self) -> Decimal:
        """Получение курса USDT к USD (обычно ~1.0)"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    "https://api.coingecko.com/api/v3/simple/price",
                    params={"ids": "tether", "vs_currencies": "usd"}
                )
                data = response.json()
                rate = Decimal(str(data["tether"]["usd"]))
                return rate
        except Exception as e:
            return Decimal("1.0")  # USDT стабильная монета
    
    async def validate_tron_transaction(self, tx_hash: str) -> Optional[Dict[str, Any]]:
        """Валидация TRON транзакции через TronScan API"""
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(
                    f"https://apilist.tronscan.org/api/transaction-info",
                    params={"hash": tx_hash}
                )
                
                if response.status_code == 200:
                    data = response.json()
                    if data.get("contractRet") == "SUCCESS":
                        return {
                            "hash": tx_hash,
                            "success": True,
                            "block_number": data.get("blockNumber"),
                            "timestamp": data.get("timestamp"),
                            "from_address": data.get("ownerAddress"),
                            "to_address": data.get("toAddress"),
                            "amount": data.get("amount", 0),
                            "fee": data.get("cost", {}).get("net_fee", 0),
                            "confirmations": data.get("confirmed", False)
                        }
                return None
        except Exception as e:
            print(f"Error validating TRON transaction: {e}")
            return None
    
    async def create_crypto_income_transaction(
        self,
        amount_crypto: Decimal,
        currency: str,  # "TRX" или "USDT"
        description: str,
        crypto_account_id: int,
        usd_account_id: int,
        tx_hash: Optional[str] = None,
        wallet_from: Optional[str] = None,
        wallet_to: Optional[str] = None,
        project_id: Optional[int] = None,
        category_id: Optional[int] = None,
        counterparty_id: Optional[int] = None
    ) -> Transaction:
        """
        Создание транзакции прихода криптовалюты с конвертацией в USD
        """
        # Получаем курс валюты
        if currency.upper() == "TRX":
            rate = await self.get_trx_to_usd_rate()
        elif currency.upper() == "USDT":
            rate = await self.get_usdt_to_usd_rate()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported currency: {currency}"
            )
        
        # Рассчитываем сумму в USD
        amount_usd = amount_crypto * rate
        
        # Валидируем транзакцию, если предоставлен хеш
        tron_data = None
        if tx_hash:
            tron_data = await self.validate_tron_transaction(tx_hash)
            if not tron_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or unconfirmed TRON transaction"
                )
        
        # Создаем основную транзакцию
        transaction = self.transaction_service.create_income_transaction(
            amount=amount_usd,
            description=f"{description} ({amount_crypto} {currency.upper()})",
            income_account_id=crypto_account_id,
            bank_account_id=usd_account_id,
            project_id=project_id,
            category_id=category_id,
            counterparty_id=counterparty_id
        )
        
        # Создаем детали криптовалютной транзакции
        crypto_detail = CryptoTransactionDetail(
            transaction_id=transaction.id,
            currency=currency.upper(),
            amount_crypto=amount_crypto,
            rate_to_usd=rate,
            tx_hash=tx_hash,
            wallet_from=wallet_from,
            wallet_to=wallet_to,
            block_number=tron_data.get("block_number") if tron_data else None,
            confirmation_count=1 if tron_data and tron_data.get("confirmations") else 0
        )
        
        self.db.add(crypto_detail)
        self.db.commit()
        self.db.refresh(crypto_detail)
        
        return transaction
    
    async def create_crypto_expense_transaction(
        self,
        amount_crypto: Decimal,
        currency: str,  # "TRX" или "USDT"
        description: str,
        crypto_account_id: int,
        usd_account_id: int,
        tx_hash: Optional[str] = None,
        wallet_from: Optional[str] = None,
        wallet_to: Optional[str] = None,
        fee_crypto: Optional[Decimal] = None,
        project_id: Optional[int] = None,
        category_id: Optional[int] = None,
        counterparty_id: Optional[int] = None
    ) -> Transaction:
        """
        Создание транзакции расхода криптовалюты с конвертацией в USD
        """
        # Получаем курс валюты
        if currency.upper() == "TRX":
            rate = await self.get_trx_to_usd_rate()
        elif currency.upper() == "USDT":
            rate = await self.get_usdt_to_usd_rate()
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Unsupported currency: {currency}"
            )
        
        # Рассчитываем сумму в USD (включая комиссию)
        total_crypto = amount_crypto + (fee_crypto or Decimal('0'))
        amount_usd = total_crypto * rate
        
        # Валидируем транзакцию, если предоставлен хеш
        tron_data = None
        if tx_hash:
            tron_data = await self.validate_tron_transaction(tx_hash)
            if not tron_data:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Invalid or unconfirmed TRON transaction"
                )
        
        # Создаем основную транзакцию
        transaction = self.transaction_service.create_expense_transaction(
            amount=amount_usd,
            description=f"{description} ({amount_crypto} {currency.upper()})",
            expense_account_id=crypto_account_id,
            bank_account_id=usd_account_id,
            project_id=project_id,
            category_id=category_id,
            counterparty_id=counterparty_id
        )
        
        # Создаем детали криптовалютной транзакции
        crypto_detail = CryptoTransactionDetail(
            transaction_id=transaction.id,
            currency=currency.upper(),
            amount_crypto=amount_crypto,
            rate_to_usd=rate,
            tx_hash=tx_hash,
            wallet_from=wallet_from,
            wallet_to=wallet_to,
            fee=fee_crypto,
            block_number=tron_data.get("block_number") if tron_data else None,
            confirmation_count=1 if tron_data and tron_data.get("confirmations") else 0
        )
        
        self.db.add(crypto_detail)
        self.db.commit()
        self.db.refresh(crypto_detail)
        
        return transaction
    
    def get_crypto_transaction_details(self, transaction_id: int) -> Optional[CryptoTransactionDetail]:
        """Получение деталей криптовалютной транзакции"""
        from sqlmodel import select
        statement = select(CryptoTransactionDetail).where(
            CryptoTransactionDetail.transaction_id == transaction_id
        )
        return self.db.exec(statement).first()
    
    async def update_crypto_rates(self) -> Dict[str, Decimal]:
        """Обновление курсов криптовалют"""
        rates = {
            "TRX": await self.get_trx_to_usd_rate(),
            "USDT": await self.get_usdt_to_usd_rate()
        }
        return rates
    
    def get_crypto_balance_summary(self, account_id: int) -> Dict[str, Any]:
        """Получение сводки по криптовалютному счету"""
        account = self.db.get(Account, account_id)
        if not account:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Account not found"
            )
        
        # Получаем все криптовалютные транзакции для этого счета
        from sqlmodel import select
        statement = select(CryptoTransactionDetail).join(Transaction).where(
            (Transaction.project_id == account_id) |  # Временно используем project_id
            (Transaction.category_id == account_id)   # как связь с криптосчетом
        )
        
        crypto_details = self.db.exec(statement).all()
        
        summary = {
            "account_name": account.name,
            "usd_balance": account.balance,
            "currencies": {}
        }
        
        # Группируем по валютам
        for detail in crypto_details:
            currency = detail.currency
            if currency not in summary["currencies"]:
                summary["currencies"][currency] = {
                    "total_crypto": Decimal('0'),
                    "transactions_count": 0
                }
            
            # Здесь нужна более сложная логика для подсчета crypto-баланса
            # на основе входящих и исходящих транзакций
            summary["currencies"][currency]["transactions_count"] += 1
        
        return summary

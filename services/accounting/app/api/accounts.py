"""
API роуты для управления счетами
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.auth import current_active_user
from app.models.users import User
from app.models.accounts import Account, AccountCreate, AccountUpdate, AccountRead

router = APIRouter()

@router.get("/", response_model=List[AccountRead])
async def get_accounts(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Получение списка счетов"""
    statement = select(Account).offset(skip).limit(limit)
    accounts = db.exec(statement).all()
    return accounts

@router.get("/{account_id}", response_model=AccountRead)
async def get_account(
    account_id: int,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Получение счета по ID"""
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    return account

@router.post("/", response_model=AccountRead)
async def create_account(
    account_data: AccountCreate,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Создание нового счета"""
    account = Account(**account_data.dict())
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

@router.put("/{account_id}", response_model=AccountRead)
async def update_account(
    account_id: int,
    account_data: AccountUpdate,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Обновление счета"""
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    for field, value in account_data.dict(exclude_unset=True).items():
        setattr(account, field, value)
    
    db.add(account)
    db.commit()
    db.refresh(account)
    return account

@router.delete("/{account_id}")
async def delete_account(
    account_id: int,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Удаление счета"""
    account = db.get(Account, account_id)
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Account not found"
        )
    
    db.delete(account)
    db.commit()
    return {"message": "Account deleted successfully"}

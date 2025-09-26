"""
API роуты для управления контрагентами
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.auth import current_active_user
from app.models.users import User
from app.models.counterparties import Counterparty, CounterpartyCreate, CounterpartyUpdate, CounterpartyRead

router = APIRouter()

@router.get("/", response_model=List[CounterpartyRead])
async def get_counterparties(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Получение списка контрагентов"""
    statement = select(Counterparty).offset(skip).limit(limit)
    counterparties = db.exec(statement).all()
    return counterparties

@router.get("/{counterparty_id}", response_model=CounterpartyRead)
async def get_counterparty(
    counterparty_id: int,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Получение контрагента по ID"""
    counterparty = db.get(Counterparty, counterparty_id)
    if not counterparty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Counterparty not found"
        )
    return counterparty

@router.post("/", response_model=CounterpartyRead)
async def create_counterparty(
    counterparty_data: CounterpartyCreate,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Создание нового контрагента"""
    counterparty = Counterparty(**counterparty_data.dict())
    db.add(counterparty)
    db.commit()
    db.refresh(counterparty)
    return counterparty

@router.put("/{counterparty_id}", response_model=CounterpartyRead)
async def update_counterparty(
    counterparty_id: int,
    counterparty_data: CounterpartyUpdate,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Обновление контрагента"""
    counterparty = db.get(Counterparty, counterparty_id)
    if not counterparty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Counterparty not found"
        )
    
    for field, value in counterparty_data.dict(exclude_unset=True).items():
        setattr(counterparty, field, value)
    
    db.add(counterparty)
    db.commit()
    db.refresh(counterparty)
    return counterparty

@router.delete("/{counterparty_id}")
async def delete_counterparty(
    counterparty_id: int,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Удаление контрагента"""
    counterparty = db.get(Counterparty, counterparty_id)
    if not counterparty:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Counterparty not found"
        )
    
    db.delete(counterparty)
    db.commit()
    return {"message": "Counterparty deleted successfully"}

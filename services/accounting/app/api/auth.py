"""
API роуты для аутентификации
"""

from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select

from app.core.auth import (
    authenticate_user, create_access_token, get_password_hash,
    current_active_user, current_superuser
)
from app.core.config import settings
from app.core.database import get_session
from app.models.users import User, UserCreate, UserRead, UserUpdate, UserLogin, Token

router = APIRouter()


@router.post("/auth/register", response_model=UserRead)
def register(user_data: UserCreate, db: Session = Depends(get_session)):
    """Регистрация нового пользователя"""
    # Проверяем, не существует ли пользователь с таким email
    statement = select(User).where(User.email == user_data.email)
    existing_user = db.exec(statement).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    
    # Создаем нового пользователя
    hashed_password = get_password_hash(user_data.password)
    
    db_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        first_name=user_data.first_name,
        last_name=user_data.last_name,
        phone=user_data.phone
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    
    return db_user


@router.post("/auth/login", response_model=Token)
def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_session)):
    """Вход пользователя"""
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/auth/me", response_model=UserRead)
def get_me(current_user: User = Depends(current_active_user)):
    """Получение информации о текущем пользователе"""
    return current_user


@router.patch("/auth/me", response_model=UserRead)
def update_me(
    user_update: UserUpdate,
    current_user: User = Depends(current_active_user),
    db: Session = Depends(get_session)
):
    """Обновление информации о текущем пользователе"""
    for field, value in user_update.model_dump(exclude_unset=True).items():
        setattr(current_user, field, value)
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    
    return current_user


@router.get("/users", response_model=list[UserRead])
def list_users(
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(current_superuser),
    db: Session = Depends(get_session)
):
    """Получение списка пользователей (только для суперпользователей)"""
    statement = select(User).offset(skip).limit(limit)
    users = db.exec(statement).all()
    return users


@router.get("/users/{user_id}", response_model=UserRead)
def get_user(
    user_id: int,
    current_user: User = Depends(current_superuser),
    db: Session = Depends(get_session)
):
    """Получение пользователя по ID (только для суперпользователей)"""
    statement = select(User).where(User.id == user_id)
    user = db.exec(statement).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user

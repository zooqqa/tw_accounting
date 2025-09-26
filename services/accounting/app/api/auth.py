"""
API роуты для аутентификации
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.auth import fastapi_users, current_active_user, current_superuser
from app.core.database import get_session
from app.models.users import User, UserCreate, UserRead, UserUpdate

router = APIRouter()

# Включение роутов FastAPI Users
router.include_router(
    fastapi_users.get_auth_router(auth_backend=fastapi_users.auth_backends[0]),
    prefix="/auth/jwt",
    tags=["authentication"]
)

router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["authentication"]
)

router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["authentication"]
)

router.include_router(
    fastapi_users.get_verify_router(UserRead),
    prefix="/auth",
    tags=["authentication"]
)

router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["users"]
)

# Дополнительные эндпоинты
@router.get("/me", response_model=UserRead)
async def get_me(user: User = Depends(current_active_user)):
    """Получение информации о текущем пользователе"""
    return user

@router.patch("/me", response_model=UserRead)
async def update_me(
    user_update: UserUpdate,
    user: User = Depends(current_active_user),
    db: Session = Depends(get_session)
):
    """Обновление информации о текущем пользователе"""
    for field, value in user_update.dict(exclude_unset=True).items():
        setattr(user, field, value)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    return user

@router.delete("/me")
async def delete_me(
    user: User = Depends(current_active_user),
    db: Session = Depends(get_session)
):
    """Удаление аккаунта текущего пользователя"""
    db.delete(user)
    db.commit()
    
    return {"message": "Account deleted successfully"}

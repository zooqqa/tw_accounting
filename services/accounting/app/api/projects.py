"""
API роуты для управления проектами
"""

from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.core.database import get_session
from app.core.auth import current_active_user
from app.models.users import User
from app.models.projects import Project, ProjectCreate, ProjectUpdate, ProjectRead

router = APIRouter()

@router.get("/", response_model=List[ProjectRead])
async def get_projects(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Получение списка проектов"""
    statement = select(Project).offset(skip).limit(limit)
    projects = db.exec(statement).all()
    return projects

@router.get("/{project_id}", response_model=ProjectRead)
async def get_project(
    project_id: int,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Получение проекта по ID"""
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    return project

@router.post("/", response_model=ProjectRead)
async def create_project(
    project_data: ProjectCreate,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Создание нового проекта"""
    project = Project(**project_data.dict())
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.put("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: int,
    project_data: ProjectUpdate,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Обновление проекта"""
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    for field, value in project_data.dict(exclude_unset=True).items():
        setattr(project, field, value)
    
    db.add(project)
    db.commit()
    db.refresh(project)
    return project

@router.delete("/{project_id}")
async def delete_project(
    project_id: int,
    db: Session = Depends(get_session),
    user: User = Depends(current_active_user)
):
    """Удаление проекта"""
    project = db.get(Project, project_id)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found"
        )
    
    db.delete(project)
    db.commit()
    return {"message": "Project deleted successfully"}

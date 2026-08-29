from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.schemas.auth import LoginRequest, Token, UserCreate, UserRead
from app.domain.auth.service import authenticate_user, create_user
from app.core.security import create_access_token
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
async def login(payload: LoginRequest, db: AsyncSession = Depends(get_db)):
    user = await authenticate_user(db, payload.email, payload.password)
    role_name = user.role.name if user.role else "VIEWER"
    token_str = create_access_token(subject=user.id, role=role_name)
    return Token(
        access_token=token_str,
        token_type="bearer",
        user_id=user.id,
        email=user.email,
        role=role_name,
        full_name=user.full_name
    )


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(payload: UserCreate, db: AsyncSession = Depends(get_db)):
    user = await create_user(db, payload)
    return UserRead(
        id=user.id,
        email=user.email,
        full_name=user.full_name,
        role_id=user.role_id,
        role_name=user.role.name if user.role else "VIEWER",
        is_active=user.is_active,
        is_superuser=user.is_superuser,
        created_at=user.created_at
    )


@router.get("/me", response_model=UserRead)
async def get_me(current_user: User = Depends(get_current_user)):
    return UserRead(
        id=current_user.id,
        email=current_user.email,
        full_name=current_user.full_name,
        role_id=current_user.role_id,
        role_name=current_user.role.name if current_user.role else "VIEWER",
        is_active=current_user.is_active,
        is_superuser=current_user.is_superuser,
        created_at=current_user.created_at
    )

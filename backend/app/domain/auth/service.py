from typing import Optional, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.user import User, Role, RoleEnum
from app.schemas.auth import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password, create_access_token
from app.core.exceptions import AuthenticationError, ResourceNotFoundError


async def seed_initial_roles(db: AsyncSession) -> None:
    """Ensure all default system roles exist in database."""
    role_descriptions = {
        RoleEnum.SUPER_ADMIN: "Full system control and administrative privileges.",
        RoleEnum.ADMIN: "Administrative access to pipelines, users, and connections.",
        RoleEnum.DATA_ENGINEER: "Create, configure, execute, and maintain data pipelines.",
        RoleEnum.DATA_ANALYST: "Execute pipelines, analyze data quality, and view analytics.",
        RoleEnum.DEVELOPER: "Develop and test data pipelines and transformation operators.",
        RoleEnum.VIEWER: "Read-only access to pipeline status and monitoring dashboards.",
    }

    for role_enum, description in role_descriptions.items():
        result = await db.execute(select(Role).where(Role.name == role_enum))
        existing_role = result.scalars().first()
        if not existing_role:
            new_role = Role(name=role_enum, description=description)
            db.add(new_role)
    await db.commit()


async def authenticate_user(db: AsyncSession, email: str, password: str) -> User:
    result = await db.execute(select(User).where(User.email == email))
    user = result.scalars().first()
    if not user:
        raise AuthenticationError("Invalid email or password.")
    if not verify_password(password, user.hashed_password):
        raise AuthenticationError("Invalid email or password.")
    if not user.is_active:
        raise AuthenticationError("User account is deactivated.")
    return user


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalars().first():
        raise AuthenticationError("User with this email already exists.")

    role_result = await db.execute(select(Role).where(Role.id == user_in.role_id))
    role = role_result.scalars().first()
    if not role:
        # Fallback to VIEWER role
        v_result = await db.execute(select(Role).where(Role.name == RoleEnum.VIEWER))
        role = v_result.scalars().first()

    hashed_pw = get_password_hash(user_in.password)
    new_user = User(
        email=user_in.email,
        full_name=user_in.full_name,
        hashed_password=hashed_pw,
        role_id=role.id if role else 1,
        is_active=True,
        is_superuser=(role.name == RoleEnum.SUPER_ADMIN if role else False)
    )
    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)
    return new_user


async def get_user_by_id(db: AsyncSession, user_id: int) -> User:
    result = await db.execute(select(User).where(User.id == user_id))
    user = result.scalars().first()
    if not user:
        raise ResourceNotFoundError("User", str(user_id))
    return user

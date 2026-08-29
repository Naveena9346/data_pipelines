from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.connection import (
    DataSourceCreate, DataSourceRead, TestConnectionRequest, TestConnectionResponse
)
from app.domain.connections.service import (
    create_data_source, test_connection_service, get_data_sources
)

router = APIRouter(prefix="/sources", tags=["Data Sources"])


@router.get("", response_model=List[DataSourceRead])
async def list_sources(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sources = await get_data_sources(db)
    return sources


@router.post("", response_model=DataSourceRead, status_code=status.HTTP_201_CREATED)
async def create_source(
    payload: DataSourceCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    source = await create_data_source(db, payload, current_user.id)
    return source


@router.post("/test", response_model=TestConnectionResponse)
async def test_connection(
    payload: TestConnectionRequest,
    current_user: User = Depends(get_current_user)
):
    res = await test_connection_service(payload)
    return res

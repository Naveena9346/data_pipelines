import json
from typing import List, Dict, Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.models.connection import DataSource, Dataset, SourceTypeEnum
from app.schemas.connection import DataSourceCreate, TestConnectionRequest, TestConnectionResponse
from app.core.security import encrypt_sensitive_string, decrypt_sensitive_string
from app.core.exceptions import ResourceNotFoundError
from app.domain.connections.connectors import get_connector


async def create_data_source(
    db: AsyncSession,
    source_in: DataSourceCreate,
    user_id: int
) -> DataSource:
    encrypted_json = encrypt_sensitive_string(json.dumps(source_in.config))
    data_source = DataSource(
        name=source_in.name,
        description=source_in.description,
        source_type=source_in.source_type,
        encrypted_config=encrypted_json,
        created_by_id=user_id,
        is_active=True
    )
    db.add(data_source)
    await db.commit()
    await db.refresh(data_source)
    return data_source


async def test_connection_service(payload: TestConnectionRequest) -> TestConnectionResponse:
    connector = get_connector(payload.source_type, payload.config)
    res = connector.test_connection()
    return TestConnectionResponse(
        success=res["success"],
        message=res["message"],
        latency_ms=res.get("latency_ms")
    )


async def get_data_sources(db: AsyncSession) -> List[DataSource]:
    result = await db.execute(select(DataSource).where(DataSource.is_active == True))
    return list(result.scalars().all())


async def get_data_source_by_id(db: AsyncSession, source_id: int) -> DataSource:
    result = await db.execute(select(DataSource).where(DataSource.id == source_id))
    ds = result.scalars().first()
    if not ds:
        raise ResourceNotFoundError("DataSource", str(source_id))
    return ds

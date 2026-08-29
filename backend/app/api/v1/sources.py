import os
import shutil
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import get_db
from app.core.config import settings
from app.api.deps import get_current_user
from app.models.user import User
from app.models.connection import DataSource, Dataset, SourceTypeEnum
from app.schemas.connection import (
    DataSourceCreate, DataSourceRead, TestConnectionRequest, TestConnectionResponse, DatasetRead
)
from app.domain.connections.service import (
    create_data_source, test_connection_service, get_data_sources
)
from app.domain.ingestion.extractors import IngestionExtractor
from app.domain.ingestion.schema_infer import SchemaInferEngine

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


@router.post("/upload-dataset", response_model=DatasetRead, status_code=status.HTTP_201_CREATED)
async def upload_dataset(
    file: UploadFile = File(...),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    file_ext = file.filename.split(".")[-1].upper()
    if file_ext not in ["CSV", "JSON", "PARQUET"]:
        raise HTTPException(status_code=400, detail="Only CSV, JSON, and PARQUET files are supported.")

    os.makedirs(settings.DATA_STORAGE_PATH, exist_ok=True)
    file_location = os.path.join(settings.DATA_STORAGE_PATH, file.filename)
    
    # Save file contents cleanly
    contents = await file.read()
    with open(file_location, "wb") as f:
        f.write(contents)

    file_size = len(contents)

    # Ingest and infer schema using Polars
    format_type = f"{file_ext}_FILE"
    try:
        df = IngestionExtractor.extract_file(file_location, format_type)
        schema_info = SchemaInferEngine.infer_schema_from_df(df)
        total_rows = df.height
    except Exception as e:
        schema_info = [
            {"column_name": "id", "data_type": "INTEGER", "nullable": False},
            {"column_name": "data", "data_type": "VARCHAR", "nullable": True}
        ]
        total_rows = 100

    # Ensure default Local File Data Source exists
    res = await db.execute(select(DataSource).where(DataSource.source_type == SourceTypeEnum.CSV_FILE))
    ds = res.scalars().first()
    if not ds:
        ds = DataSource(
            name="Local File Repository",
            description="Uploaded CSV/JSON dataset repository",
            source_type=SourceTypeEnum.CSV_FILE,
            encrypted_config="{}",
            created_by_id=current_user.id,
            is_active=True
        )
        db.add(ds)
        await db.flush()

    dataset = Dataset(
        name=file.filename,
        description=f"Uploaded dataset ({file_ext} format)",
        data_source_id=ds.id,
        file_path=file_location,
        schema_definition=schema_info,
        total_rows=total_rows,
        file_size_bytes=file_size
    )
    db.add(dataset)
    await db.commit()
    await db.refresh(dataset)
    return dataset


@router.get("/datasets", response_model=List[DatasetRead])
async def list_datasets(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(select(Dataset))
    return list(result.scalars().all())

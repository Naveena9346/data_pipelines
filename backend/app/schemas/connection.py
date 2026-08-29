from datetime import datetime
from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict
from app.models.connection import SourceTypeEnum


class DataSourceCreate(BaseModel):
    name: str
    description: Optional[str] = None
    source_type: SourceTypeEnum
    config: Dict[str, Any]  # Unencrypted parameters from client


class DataSourceRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    source_type: SourceTypeEnum
    is_active: bool
    created_by_id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class TestConnectionRequest(BaseModel):
    source_type: SourceTypeEnum
    config: Dict[str, Any]


class TestConnectionResponse(BaseModel):
    success: bool
    message: str
    latency_ms: Optional[float] = None


class DatasetCreate(BaseModel):
    name: str
    description: Optional[str] = None
    data_source_id: int
    file_path: Optional[str] = None
    table_name: Optional[str] = None
    schema_definition: Optional[List[Dict[str, Any]]] = None


class DatasetRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    data_source_id: int
    file_path: Optional[str] = None
    table_name: Optional[str] = None
    schema_definition: Optional[List[Dict[str, Any]]] = None
    total_rows: int
    file_size_bytes: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)

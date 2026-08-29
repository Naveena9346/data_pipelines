import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum, JSON, BigInteger
from sqlalchemy.orm import relationship
from app.core.db import Base


class SourceTypeEnum(str, enum.Enum):
    POSTGRES = "POSTGRES"
    MYSQL = "MYSQL"
    SQLITE = "SQLITE"
    SNOWFLAKE = "SNOWFLAKE"
    CSV_FILE = "CSV_FILE"
    JSON_FILE = "JSON_FILE"
    PARQUET_FILE = "PARQUET_FILE"
    EXCEL_FILE = "EXCEL_FILE"
    S3_BUCKET = "S3_BUCKET"
    REST_API = "REST_API"


class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    source_type = Column(Enum(SourceTypeEnum), nullable=False)
    encrypted_config = Column(Text, nullable=False)  # Encrypted JSON connection parameters
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    creator = relationship("User", back_populates="data_sources")
    datasets = relationship("Dataset", back_populates="data_source", cascade="all, delete-orphan")


class Dataset(Base):
    __tablename__ = "datasets"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    data_source_id = Column(Integer, ForeignKey("data_sources.id", ondelete="CASCADE"), nullable=False)
    file_path = Column(String(512), nullable=True)
    table_name = Column(String(255), nullable=True)
    schema_definition = Column(JSON, nullable=True)  # List of {column_name, data_type, nullable}
    total_rows = Column(BigInteger, default=0)
    file_size_bytes = Column(BigInteger, default=0)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    data_source = relationship("DataSource", back_populates="datasets")

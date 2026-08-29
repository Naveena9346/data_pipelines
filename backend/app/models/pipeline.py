import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey, Enum, JSON, Float
from sqlalchemy.orm import relationship
from app.core.db import Base


class NodeTypeEnum(str, enum.Enum):
    EXTRACTOR_DB = "EXTRACTOR_DB"
    EXTRACTOR_FILE = "EXTRACTOR_FILE"
    EXTRACTOR_API = "EXTRACTOR_API"
    TRANSFORM_POLARS = "TRANSFORM_POLARS"
    TRANSFORM_DUCKDB = "TRANSFORM_DUCKDB"
    TRANSFORM_SQL = "TRANSFORM_SQL"
    VALIDATOR_SCHEMA = "VALIDATOR_SCHEMA"
    VALIDATOR_QUALITY = "VALIDATOR_QUALITY"
    LOADER_DB = "LOADER_DB"
    LOADER_FILE = "LOADER_FILE"
    ALERT_NOTIFICATION = "ALERT_NOTIFICATION"


class Pipeline(Base):
    __tablename__ = "pipelines"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    cron_schedule = Column(String(100), nullable=True)  # e.g., '0 * * * *'
    is_active = Column(Boolean, default=True)
    max_retries = Column(Integer, default=3)
    retry_delay_seconds = Column(Integer, default=60)
    timeout_seconds = Column(Integer, default=3600)
    created_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))

    creator = relationship("User", back_populates="pipelines")
    nodes = relationship("PipelineNode", back_populates="pipeline", cascade="all, delete-orphan")
    edges = relationship("PipelineEdge", back_populates="pipeline", cascade="all, delete-orphan")
    executions = relationship("PipelineExecution", back_populates="pipeline", cascade="all, delete-orphan")


class PipelineNode(Base):
    __tablename__ = "pipeline_nodes"

    id = Column(Integer, primary_key=True, index=True)
    pipeline_id = Column(Integer, ForeignKey("pipelines.id", ondelete="CASCADE"), nullable=False)
    node_key = Column(String(100), nullable=False, index=True)  # Canvas unique identifier
    name = Column(String(255), nullable=False)
    node_type = Column(Enum(NodeTypeEnum), nullable=False)
    config_json = Column(JSON, nullable=False, default={})
    position_x = Column(Float, default=0.0)
    position_y = Column(Float, default=0.0)

    pipeline = relationship("Pipeline", back_populates="nodes")


class PipelineEdge(Base):
    __tablename__ = "pipeline_edges"

    id = Column(Integer, primary_key=True, index=True)
    pipeline_id = Column(Integer, ForeignKey("pipelines.id", ondelete="CASCADE"), nullable=False)
    edge_key = Column(String(100), nullable=False)
    source_node_key = Column(String(100), nullable=False)
    target_node_key = Column(String(100), nullable=False)
    condition_expression = Column(Text, nullable=True)

    pipeline = relationship("Pipeline", back_populates="edges")

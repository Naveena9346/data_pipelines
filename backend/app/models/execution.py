import enum
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Enum, BigInteger, JSON
from sqlalchemy.orm import relationship
from app.core.db import Base


class ExecutionStatusEnum(str, enum.Enum):
    PENDING = "PENDING"
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    CANCELLED = "CANCELLED"


class PipelineExecution(Base):
    __tablename__ = "pipeline_executions"

    id = Column(Integer, primary_key=True, index=True)
    pipeline_id = Column(Integer, ForeignKey("pipelines.id", ondelete="CASCADE"), nullable=False)
    status = Column(Enum(ExecutionStatusEnum), default=ExecutionStatusEnum.PENDING, index=True)
    trigger_type = Column(String(50), default="MANUAL")  # MANUAL, SCHEDULED, API
    triggered_by_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)
    duration_seconds = Column(Integer, default=0)
    total_records_processed = Column(BigInteger, default=0)
    error_summary = Column(Text, nullable=True)

    pipeline = relationship("Pipeline", back_populates="executions")
    task_executions = relationship("TaskExecution", back_populates="execution", cascade="all, delete-orphan")
    quality_reports = relationship("DataQualityReport", back_populates="execution", cascade="all, delete-orphan")


class TaskExecution(Base):
    __tablename__ = "task_executions"

    id = Column(Integer, primary_key=True, index=True)
    execution_id = Column(Integer, ForeignKey("pipeline_executions.id", ondelete="CASCADE"), nullable=False)
    node_key = Column(String(100), nullable=False)
    node_name = Column(String(255), nullable=False)
    status = Column(Enum(ExecutionStatusEnum), default=ExecutionStatusEnum.PENDING)
    input_rows = Column(BigInteger, default=0)
    output_rows = Column(BigInteger, default=0)
    retry_count = Column(Integer, default=0)
    error_message = Column(Text, nullable=True)
    started_at = Column(DateTime(timezone=True), nullable=True)
    finished_at = Column(DateTime(timezone=True), nullable=True)

    execution = relationship("PipelineExecution", back_populates="task_executions")
    logs = relationship("ExecutionLog", back_populates="task_execution", cascade="all, delete-orphan")


class ExecutionLog(Base):
    __tablename__ = "execution_logs"

    id = Column(Integer, primary_key=True, index=True)
    task_execution_id = Column(Integer, ForeignKey("task_executions.id", ondelete="CASCADE"), nullable=False)
    log_level = Column(String(20), default="INFO")
    message = Column(Text, nullable=False)
    timestamp = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

    task_execution = relationship("TaskExecution", back_populates="logs")

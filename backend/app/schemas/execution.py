from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
from app.models.execution import ExecutionStatusEnum


class ExecutionTriggerRequest(BaseModel):
    trigger_type: str = "MANUAL"
    override_params: Optional[Dict[str, Any]] = None


class ExecutionLogRead(BaseModel):
    id: int
    task_execution_id: int
    log_level: str
    message: str
    timestamp: datetime

    model_config = ConfigDict(from_attributes=True)


class TaskExecutionRead(BaseModel):
    id: int
    execution_id: int
    node_key: str
    node_name: str
    status: ExecutionStatusEnum
    input_rows: int
    output_rows: int
    retry_count: int
    error_message: Optional[str] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    logs: List[ExecutionLogRead] = []

    model_config = ConfigDict(from_attributes=True)


class PipelineExecutionRead(BaseModel):
    id: int
    pipeline_id: int
    status: ExecutionStatusEnum
    trigger_type: str
    triggered_by_id: Optional[int] = None
    started_at: Optional[datetime] = None
    finished_at: Optional[datetime] = None
    duration_seconds: int
    total_records_processed: int
    error_summary: Optional[str] = None
    task_executions: List[TaskExecutionRead] = []

    model_config = ConfigDict(from_attributes=True)

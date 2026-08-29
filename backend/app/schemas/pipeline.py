from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict
from app.models.pipeline import NodeTypeEnum


class PipelineNodeBase(BaseModel):
    node_key: str
    name: str
    node_type: NodeTypeEnum
    config_json: Dict[str, Any] = {}
    position_x: float = 0.0
    position_y: float = 0.0


class PipelineNodeCreate(PipelineNodeBase):
    pass


class PipelineNodeRead(PipelineNodeBase):
    id: int
    pipeline_id: int

    model_config = ConfigDict(from_attributes=True)


class PipelineEdgeBase(BaseModel):
    edge_key: str
    source_node_key: str
    target_node_key: str
    condition_expression: Optional[str] = None


class PipelineEdgeCreate(PipelineEdgeBase):
    pass


class PipelineEdgeRead(PipelineEdgeBase):
    id: int
    pipeline_id: int

    model_config = ConfigDict(from_attributes=True)


class PipelineCreate(BaseModel):
    name: str
    description: Optional[str] = None
    cron_schedule: Optional[str] = None
    max_retries: int = 3
    retry_delay_seconds: int = 60
    timeout_seconds: int = 3600
    nodes: List[PipelineNodeCreate] = []
    edges: List[PipelineEdgeCreate] = []


class PipelineUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    cron_schedule: Optional[str] = None
    is_active: Optional[bool] = None
    max_retries: Optional[int] = None
    retry_delay_seconds: Optional[int] = None
    timeout_seconds: Optional[int] = None
    nodes: Optional[List[PipelineNodeCreate]] = None
    edges: Optional[List[PipelineEdgeCreate]] = None


class PipelineRead(BaseModel):
    id: int
    name: str
    description: Optional[str] = None
    cron_schedule: Optional[str] = None
    is_active: bool
    max_retries: int
    retry_delay_seconds: int
    timeout_seconds: int
    created_by_id: int
    created_at: datetime
    updated_at: datetime
    nodes: List[PipelineNodeRead] = []
    edges: List[PipelineEdgeRead] = []

    model_config = ConfigDict(from_attributes=True)


class ValidateDAGResponse(BaseModel):
    is_valid: bool
    message: str
    node_count: int
    edge_count: int
    execution_order: List[str] = []

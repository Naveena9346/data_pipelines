from datetime import datetime
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, ConfigDict


class DataQualityReportRead(BaseModel):
    id: int
    execution_id: int
    node_key: str
    total_rules: int
    passed_rules: int
    failed_rules: int
    rules_summary: List[Dict[str, Any]] = []
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AuditLogRead(BaseModel):
    id: int
    user_id: Optional[int] = None
    action: str
    resource_type: str
    resource_id: Optional[str] = None
    details: Optional[Dict[str, Any]] = None
    ip_address: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class SystemDashboardMetrics(BaseModel):
    total_pipelines: int
    running_pipelines: int
    successful_pipelines: int
    failed_pipelines: int
    total_records_processed: int
    average_execution_time_seconds: float
    overall_error_rate_percentage: float
    active_data_sources: int
    data_quality_pass_rate_percentage: float
    recent_executions: List[Dict[str, Any]] = []

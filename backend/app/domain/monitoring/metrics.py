from typing import Dict, Any, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from app.models.pipeline import Pipeline
from app.models.execution import PipelineExecution, ExecutionStatusEnum
from app.models.connection import DataSource
from app.models.monitoring import DataQualityReport
from app.schemas.monitoring import SystemDashboardMetrics


async def calculate_system_dashboard_metrics(db: AsyncSession) -> SystemDashboardMetrics:
    # 1. Total Pipelines
    total_pipes_res = await db.execute(select(func.count(Pipeline.id)))
    total_pipelines = total_pipes_res.scalar() or 0

    # 2. Pipeline Execution Status Counts
    running_res = await db.execute(select(func.count(PipelineExecution.id)).where(PipelineExecution.status == ExecutionStatusEnum.RUNNING))
    running_pipelines = running_res.scalar() or 0

    success_res = await db.execute(select(func.count(PipelineExecution.id)).where(PipelineExecution.status == ExecutionStatusEnum.SUCCESS))
    successful_pipelines = success_res.scalar() or 0

    failed_res = await db.execute(select(func.count(PipelineExecution.id)).where(PipelineExecution.status == ExecutionStatusEnum.FAILED))
    failed_pipelines = failed_res.scalar() or 0

    # 3. Total Records Processed
    records_res = await db.execute(select(func.sum(PipelineExecution.total_records_processed)))
    total_records_processed = records_res.scalar() or 0

    # 4. Average Duration
    duration_res = await db.execute(select(func.avg(PipelineExecution.duration_seconds)))
    avg_duration = round(float(duration_res.scalar() or 0.0), 2)

    # 5. Calculate Error Rate Percentage
    total_execs = successful_pipelines + failed_pipelines
    error_rate = round((failed_pipelines / total_execs * 100), 2) if total_execs > 0 else 0.0

    # 6. Active Data Sources
    sources_res = await db.execute(select(func.count(DataSource.id)).where(DataSource.is_active == True))
    active_data_sources = sources_res.scalar() or 0

    # 7. Quality Pass Rate
    passed_rules_res = await db.execute(select(func.sum(DataQualityReport.passed_rules)))
    total_rules_res = await db.execute(select(func.sum(DataQualityReport.total_rules)))
    passed_r = passed_rules_res.scalar() or 0
    total_r = total_rules_res.scalar() or 0
    quality_pass_rate = round((passed_r / total_r * 100), 2) if total_r > 0 else 100.0

    return SystemDashboardMetrics(
        total_pipelines=total_pipelines,
        running_pipelines=running_pipelines,
        successful_pipelines=successful_pipelines,
        failed_pipelines=failed_pipelines,
        total_records_processed=total_records_processed,
        average_execution_time_seconds=avg_duration,
        overall_error_rate_percentage=error_rate,
        active_data_sources=active_data_sources,
        data_quality_pass_rate_percentage=quality_pass_rate,
        recent_executions=[]
    )

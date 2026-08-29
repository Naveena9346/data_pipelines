from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.execution import PipelineExecution, TaskExecution, ExecutionLog
from app.schemas.execution import PipelineExecutionRead, TaskExecutionRead, ExecutionLogRead

router = APIRouter(prefix="/executions", tags=["Pipeline Executions"])


@router.get("", response_model=List[PipelineExecutionRead])
async def list_executions(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(PipelineExecution)
        .options(
            selectinload(PipelineExecution.task_executions).selectinload(TaskExecution.logs)
        )
        .order_by(PipelineExecution.id.desc())
    )
    return list(result.scalars().all())


@router.get("/{execution_id}", response_model=PipelineExecutionRead)
async def get_execution_detail(
    execution_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(PipelineExecution)
        .where(PipelineExecution.id == execution_id)
        .options(
            selectinload(PipelineExecution.task_executions).selectinload(TaskExecution.logs)
        )
    )
    execution = result.scalars().first()
    if not execution:
        raise HTTPException(status_code=404, detail="Execution record not found")
    return execution


@router.get("/{execution_id}/logs", response_model=List[ExecutionLogRead])
async def get_execution_logs(
    execution_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(ExecutionLog)
        .join(TaskExecution)
        .where(TaskExecution.execution_id == execution_id)
        .order_by(ExecutionLog.timestamp.asc())
    )
    return list(result.scalars().all())

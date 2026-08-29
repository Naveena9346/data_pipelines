from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.models.pipeline import Pipeline, PipelineNode, PipelineEdge
from app.schemas.pipeline import (
    PipelineCreate, PipelineRead, ValidateDAGResponse
)
from app.domain.orchestration.dag_compiler import DAGCompiler
from app.domain.orchestration.executor import PipelineExecutor

router = APIRouter(prefix="/pipelines", tags=["Pipelines"])


@router.get("", response_model=List[PipelineRead])
async def list_pipelines(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    result = await db.execute(
        select(Pipeline).options(selectinload(Pipeline.nodes), selectinload(Pipeline.edges))
    )
    return list(result.scalars().all())


@router.post("", response_model=PipelineRead, status_code=status.HTTP_201_CREATED)
async def create_pipeline(
    payload: PipelineCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Validate DAG before saving
    node_dicts = [n.model_dump() for n in payload.nodes]
    edge_dicts = [e.model_dump() for e in payload.edges]
    DAGCompiler.compile_and_toposort(node_dicts, edge_dicts)

    pipeline = Pipeline(
        name=payload.name,
        description=payload.description,
        cron_schedule=payload.cron_schedule,
        max_retries=payload.max_retries,
        retry_delay_seconds=payload.retry_delay_seconds,
        timeout_seconds=payload.timeout_seconds,
        created_by_id=current_user.id
    )
    db.add(pipeline)
    await db.flush()

    for node_in in payload.nodes:
        db.add(PipelineNode(
            pipeline_id=pipeline.id,
            node_key=node_in.node_key,
            name=node_in.name,
            node_type=node_in.node_type,
            config_json=node_in.config_json,
            position_x=node_in.position_x,
            position_y=node_in.position_y
        ))

    for edge_in in payload.edges:
        db.add(PipelineEdge(
            pipeline_id=pipeline.id,
            edge_key=edge_in.edge_key,
            source_node_key=edge_in.source_node_key,
            target_node_key=edge_in.target_node_key,
            condition_expression=edge_in.condition_expression
        ))

    await db.commit()
    
    # Reload with relationships
    res = await db.execute(
        select(Pipeline).where(Pipeline.id == pipeline.id).options(
            selectinload(Pipeline.nodes), selectinload(Pipeline.edges)
        )
    )
    return res.scalars().first()


@router.post("/{pipeline_id}/validate", response_model=ValidateDAGResponse)
async def validate_pipeline(
    pipeline_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    res = await db.execute(
        select(Pipeline).where(Pipeline.id == pipeline_id).options(
            selectinload(Pipeline.nodes), selectinload(Pipeline.edges)
        )
    )
    pipeline = res.scalars().first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    nodes = [{"node_key": n.node_key, "name": n.name} for n in pipeline.nodes]
    edges = [{"source_node_key": e.source_node_key, "target_node_key": e.target_node_key} for e in pipeline.edges]

    try:
        toposort = DAGCompiler.compile_and_toposort(nodes, edges)
        return ValidateDAGResponse(
            is_valid=True,
            message="DAG topology is valid and acyclic.",
            node_count=len(nodes),
            edge_count=len(edges),
            execution_order=toposort
        )
    except Exception as e:
        return ValidateDAGResponse(
            is_valid=False,
            message=str(e),
            node_count=len(nodes),
            edge_count=len(edges),
            execution_order=[]
        )


@router.post("/{pipeline_id}/execute")
async def execute_pipeline(
    pipeline_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    res = await db.execute(
        select(Pipeline).where(Pipeline.id == pipeline_id).options(
            selectinload(Pipeline.nodes), selectinload(Pipeline.edges)
        )
    )
    pipeline = res.scalars().first()
    if not pipeline:
        raise HTTPException(status_code=404, detail="Pipeline not found")

    node_dicts = [
        {"node_key": n.node_key, "name": n.name, "node_type": n.node_type, "config_json": n.config_json}
        for n in pipeline.nodes
    ]
    edge_dicts = [
        {"source_node_key": e.source_node_key, "target_node_key": e.target_node_key}
        for e in pipeline.edges
    ]

    exec_result = PipelineExecutor.execute_pipeline_dag(node_dicts, edge_dicts)
    return {
        "pipeline_id": pipeline_id,
        "execution_status": exec_result["status"],
        "total_records_processed": exec_result["total_records_processed"],
        "node_results": exec_result["node_results"]
    }

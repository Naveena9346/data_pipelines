from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.db import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.monitoring import SystemDashboardMetrics
from app.domain.monitoring.metrics import calculate_system_dashboard_metrics

router = APIRouter(prefix="/monitoring", tags=["Monitoring & Analytics"])


@router.get("/metrics", response_model=SystemDashboardMetrics)
async def get_dashboard_metrics(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    metrics = await calculate_system_dashboard_metrics(db)
    return metrics

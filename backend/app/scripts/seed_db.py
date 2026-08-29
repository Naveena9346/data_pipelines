import asyncio
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.db import AsyncSessionLocal, async_engine, Base
from app.models.user import User, Role, RoleEnum
from app.models.connection import DataSource, Dataset, SourceTypeEnum
from app.models.pipeline import Pipeline, PipelineNode, PipelineEdge, NodeTypeEnum
from app.models.execution import PipelineExecution, TaskExecution, ExecutionLog, ExecutionStatusEnum
from app.models.monitoring import DataQualityReport, AuditLog
from app.domain.auth.service import seed_initial_roles
from app.core.security import get_password_hash


async def seed_data():
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as session:
        await seed_initial_roles(session)

        # 1. Seed Super Admin & Lead Data Engineer
        res_admin = await session.execute(select(User).where(User.email == "admin@dataforge.io"))
        admin_user = res_admin.scalars().first()
        if not admin_user:
            res_role = await session.execute(select(Role).where(Role.name == RoleEnum.SUPER_ADMIN))
            admin_role = res_role.scalars().first()
            admin_user = User(
                email="admin@dataforge.io",
                full_name="Lead Data Engineer",
                hashed_password=get_password_hash("password123"),
                role_id=admin_role.id,
                is_active=True,
                is_superuser=True
            )
            session.add(admin_user)
            await session.flush()

        # 2. Seed Data Sources
        res_ds = await session.execute(select(DataSource))
        existing_ds = res_ds.scalars().all()
        if not existing_ds:
            ds1 = DataSource(
                name="Main Analytics PostgreSQL",
                description="Production relational analytics data store",
                source_type=SourceTypeEnum.POSTGRES,
                encrypted_config="{}",
                created_by_id=admin_user.id,
                is_active=True
            )
            ds2 = DataSource(
                name="Local CSV Order Repository",
                description="High-speed CSV batch ingestion storage",
                source_type=SourceTypeEnum.CSV_FILE,
                encrypted_config="{}",
                created_by_id=admin_user.id,
                is_active=True
            )
            session.add_all([ds1, ds2])
            await session.flush()

            # Seed Dataset
            dataset1 = Dataset(
                name="customer_orders_2026.csv",
                description="Daily transaction records",
                data_source_id=ds2.id,
                file_path="./data_storage/customer_orders_2026.csv",
                schema_definition=[
                    {"column_name": "order_id", "data_type": "INTEGER", "nullable": False},
                    {"column_name": "customer", "data_type": "VARCHAR", "nullable": True},
                    {"column_name": "amount", "data_type": "FLOAT", "nullable": True},
                    {"column_name": "status", "data_type": "VARCHAR", "nullable": True}
                ],
                total_rows=42500,
                file_size_bytes=1048576
            )
            session.add(dataset1)

        # 3. Seed Sample Pipelines
        res_pipe = await session.execute(select(Pipeline))
        existing_pipes = res_pipe.scalars().all()
        if not existing_pipes:
            p1 = Pipeline(
                name="Customer Orders ETL Pipeline",
                description="Ingests CSV order logs, applies Polars filter & schema validation, loads to PostgreSQL",
                cron_schedule="0 * * * *",
                is_active=True,
                max_retries=3,
                retry_delay_seconds=60,
                timeout_seconds=3600,
                created_by_id=admin_user.id
            )
            session.add(p1)
            await session.flush()

            # Nodes for p1
            n1 = PipelineNode(
                pipeline_id=p1.id,
                node_key="n1",
                name="Extract Orders CSV",
                node_type=NodeTypeEnum.EXTRACTOR_FILE,
                config_json={"file_path": "./data_storage/customer_orders_2026.csv", "format_type": "CSV"},
                position_x=100.0,
                position_y=200.0
            )
            n2 = PipelineNode(
                pipeline_id=p1.id,
                node_key="n2",
                name="Polars Filter Tech Orders",
                node_type=NodeTypeEnum.TRANSFORM_POLARS,
                config_json={"operator_type": "FILTER", "column": "status", "operator": "==", "value": "ACTIVE"},
                position_x=350.0,
                position_y=200.0
            )
            n3 = PipelineNode(
                pipeline_id=p1.id,
                node_key="n3",
                name="Schema & Quality Validator",
                node_type=NodeTypeEnum.VALIDATOR_QUALITY,
                config_json={"rules": [{"rule_type": "NOT_NULL", "column": "order_id"}]},
                position_x=600.0,
                position_y=200.0
            )
            n4 = PipelineNode(
                pipeline_id=p1.id,
                node_key="n4",
                name="Load to PostgreSQL Lake",
                node_type=NodeTypeEnum.LOADER_DB,
                config_json={},
                position_x=850.0,
                position_y=200.0
            )
            session.add_all([n1, n2, n3, n4])

            # Edges for p1
            e1 = PipelineEdge(pipeline_id=p1.id, edge_key="e1", source_node_key="n1", target_node_key="n2")
            e2 = PipelineEdge(pipeline_id=p1.id, edge_key="e2", source_node_key="n2", target_node_key="n3")
            e3 = PipelineEdge(pipeline_id=p1.id, edge_key="e3", source_node_key="n3", target_node_key="n4")
            session.add_all([e1, e2, e3])

            # Seed Execution History
            exec1 = PipelineExecution(
                pipeline_id=p1.id,
                status=ExecutionStatusEnum.SUCCESS,
                trigger_type="CRON",
                triggered_by_id=admin_user.id,
                started_at=datetime.now(timezone.utc),
                finished_at=datetime.now(timezone.utc),
                duration_seconds=4,
                total_records_processed=42500
            )
            session.add(exec1)
            await session.flush()

            # Task executions
            t1 = TaskExecution(
                execution_id=exec1.id,
                node_key="n1",
                node_name="Extract Orders CSV",
                status=ExecutionStatusEnum.SUCCESS,
                input_rows=0,
                output_rows=42500,
                started_at=datetime.now(timezone.utc),
                finished_at=datetime.now(timezone.utc)
            )
            session.add(t1)
            await session.flush()

            l1 = ExecutionLog(
                task_execution_id=t1.id,
                log_level="INFO",
                message="Successfully ingested 42,500 records from CSV file."
            )
            session.add(l1)

            # Quality report
            qr1 = DataQualityReport(
                execution_id=exec1.id,
                node_key="n3",
                total_rules=5,
                passed_rules=5,
                failed_rules=0,
                rules_summary=[{"rule": "NOT_NULL", "column": "order_id", "passed": True}]
            )
            session.add(qr1)

            # Audit log
            al1 = AuditLog(
                user_id=admin_user.id,
                action="PIPELINE_EXECUTED",
                resource_type="PIPELINE",
                resource_id=str(p1.id),
                details={"execution_id": exec1.id, "status": "SUCCESS"}
            )
            session.add(al1)

        await session.commit()

if __name__ == "__main__":
    asyncio.run(seed_data())

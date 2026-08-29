from typing import List, Dict, Set
from app.models.user import RoleEnum
from app.core.exceptions import PermissionDeniedError

# Define standard RBAC permissions across system domains
PERMISSIONS: Dict[str, str] = {
    # User Management
    "user:create": "Create new user accounts",
    "user:read": "View user profiles and roles",
    "user:update": "Modify user settings and roles",
    "user:delete": "Delete user accounts",

    # Data Sources & Datasets
    "datasource:create": "Create new data source connections",
    "datasource:read": "View data sources and connection details",
    "datasource:test": "Test connectivity to data sources",
    "datasource:delete": "Remove data sources",

    # Pipelines & DAG Builder
    "pipeline:create": "Create new pipeline DAGs",
    "pipeline:read": "View pipeline topologies and settings",
    "pipeline:update": "Modify existing pipeline DAGs",
    "pipeline:delete": "Delete data pipelines",
    "pipeline:execute": "Trigger manual pipeline execution",
    "pipeline:schedule": "Configure pipeline schedules and retries",

    # Monitoring & Quality
    "monitoring:read": "View system performance and dashboards",
    "audit:read": "View system audit logs",
    "quality:read": "View data quality reports",
}

ROLE_PERMISSIONS_MAPPING: Dict[RoleEnum, Set[str]] = {
    RoleEnum.SUPER_ADMIN: set(PERMISSIONS.keys()),
    RoleEnum.ADMIN: set(PERMISSIONS.keys()),
    RoleEnum.DATA_ENGINEER: {
        "user:read",
        "datasource:create", "datasource:read", "datasource:test", "datasource:delete",
        "pipeline:create", "pipeline:read", "pipeline:update", "pipeline:delete", "pipeline:execute", "pipeline:schedule",
        "monitoring:read", "audit:read", "quality:read",
    },
    RoleEnum.DATA_ANALYST: {
        "user:read",
        "datasource:read", "datasource:test",
        "pipeline:read", "pipeline:execute",
        "monitoring:read", "quality:read",
    },
    RoleEnum.DEVELOPER: {
        "user:read",
        "datasource:read", "datasource:test",
        "pipeline:create", "pipeline:read", "pipeline:update", "pipeline:execute",
        "monitoring:read", "quality:read",
    },
    RoleEnum.VIEWER: {
        "user:read",
        "datasource:read",
        "pipeline:read",
        "monitoring:read", "quality:read",
    },
}


def check_permission(role_name: str, required_permission: str) -> None:
    try:
        role_enum = RoleEnum(role_name)
    except ValueError:
        raise PermissionDeniedError(f"Invalid role '{role_name}'")

    allowed_permissions = ROLE_PERMISSIONS_MAPPING.get(role_enum, set())
    if required_permission not in allowed_permissions:
        raise PermissionDeniedError(
            f"Role '{role_name}' lacks permission '{required_permission}' for this operation."
        )

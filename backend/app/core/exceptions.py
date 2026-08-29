class DataForgeException(Exception):
    """Base exception class for DataForge application errors."""
    def __init__(self, message: str, code: str = "INTERNAL_ERROR"):
        self.message = message
        self.code = code
        super().__init__(self.message)


class AuthenticationError(DataForgeException):
    def __init__(self, message: str = "Invalid credentials or expired session."):
        super().__init__(message, code="AUTHENTICATION_ERROR")


class PermissionDeniedError(DataForgeException):
    def __init__(self, message: str = "User does not possess required role permissions."):
        super().__init__(message, code="PERMISSION_DENIED")


class ResourceNotFoundError(DataForgeException):
    def __init__(self, resource: str, identifier: str):
        super().__init__(f"{resource} with ID/key '{identifier}' was not found.", code="NOT_FOUND")


class ValidationError(DataForgeException):
    def __init__(self, message: str):
        super().__init__(message, code="VALIDATION_ERROR")


class PipelineExecutionError(DataForgeException):
    def __init__(self, pipeline_id: str, details: str):
        super().__init__(f"Pipeline '{pipeline_id}' execution failed: {details}", code="EXECUTION_FAILED")


class DAGCycleError(DataForgeException):
    def __init__(self, details: str):
        super().__init__(f"DAG Graph Cycle Error: {details}", code="DAG_CYCLE_DETECTED")

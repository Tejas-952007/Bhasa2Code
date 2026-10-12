"""Pydantic schemas and enums for safe code sandbox execution."""

from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class ExecutionStatus(str, Enum):
    """Execution status outcomes for isolated code execution."""

    SUCCESS = "SUCCESS"
    RUNTIME_ERROR = "RUNTIME_ERROR"
    TIMEOUT = "TIMEOUT"
    RESOURCE_LIMIT = "RESOURCE_LIMIT"
    VALIDATION_FAILED = "VALIDATION_FAILED"
    UNSUPPORTED = "UNSUPPORTED"
    SANDBOX_ERROR = "SANDBOX_ERROR"
    OUTPUT_LIMIT = "OUTPUT_LIMIT"
    DEPENDENCY_ERROR = "DEPENDENCY_ERROR"


class SandboxResult(BaseModel):
    """Structured result returned from isolated sandbox execution."""

    status: ExecutionStatus
    language: str
    stdout: str = ""
    stderr: str = ""
    exit_code: Optional[int] = None
    duration_ms: Optional[float] = None
    timed_out: bool = False
    output_truncated: bool = False
    diagnostics: List[str] = Field(default_factory=list)

    @property
    def is_success(self) -> bool:
        """Convenience property for success checking."""
        return self.status == ExecutionStatus.SUCCESS


class ExecutionRequest(BaseModel):
    """Request specification for code execution."""

    language: str
    code: str
    stdin: str = ""
    timeout_seconds: Optional[float] = None
    memory_limit_mb: Optional[int] = None
    bypass_validation: bool = False

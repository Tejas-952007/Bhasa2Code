"""Pydantic schemas for response and code validation."""

from enum import Enum
from typing import Any, Dict, List, Optional
from pydantic import BaseModel, Field


class ValidationStatus(str, Enum):
    """Validation outcome status for a code block or overall response."""

    VALID = "VALID"
    INVALID = "INVALID"
    UNSUPPORTED = "UNSUPPORTED"
    NOT_VALIDATED = "NOT_VALIDATED"
    INCOMPLETE = "INCOMPLETE"


class ValidationDiagnostic(BaseModel):
    """Structured diagnostic message (error, warning, or info) from validation."""

    severity: str = "ERROR"  # "ERROR", "WARNING", "INFO"
    message: str
    line: Optional[int] = None
    column: Optional[int] = None
    code: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        """Convert diagnostic to dictionary."""
        return self.model_dump()


class CodeBlock(BaseModel):
    """Raw extracted code block from Markdown text."""

    block_id: int
    declared_language: Optional[str] = None
    resolved_language: Optional[str] = None
    code: str
    start_char: int = 0
    end_char: int = 0
    is_fenced: bool = True


class CodeValidationResult(BaseModel):
    """Validation result for an individual code block."""

    block_id: int
    language: Optional[str] = None
    status: ValidationStatus
    code: str
    diagnostics: List[ValidationDiagnostic] = Field(default_factory=list)
    validator: Optional[str] = None

    @property
    def is_valid(self) -> bool:
        return self.status == ValidationStatus.VALID

    @property
    def has_errors(self) -> bool:
        return any(d.severity.upper() == "ERROR" for d in self.diagnostics)


class ResponseValidationResult(BaseModel):
    """Aggregated validation result for an assistant response."""

    status: ValidationStatus
    original_response: str
    code_blocks: List[CodeValidationResult] = Field(default_factory=list)
    diagnostics: List[ValidationDiagnostic] = Field(default_factory=list)
    has_code: bool = False

    @property
    def is_valid(self) -> bool:
        return self.status == ValidationStatus.VALID

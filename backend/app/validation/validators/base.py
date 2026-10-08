"""Base validator interface and common utilities for code validation."""

from abc import ABC, abstractmethod
from typing import List, Optional
from backend.app.validation.schemas import CodeValidationResult, ValidationDiagnostic, ValidationStatus


class BaseCodeValidator(ABC):
    """Abstract base validator for language-specific syntax validation."""

    language: str

    @abstractmethod
    def validate(self, code: str, block_id: int = 1) -> CodeValidationResult:
        """Validate code syntax without executing it.

        Args:
            code: Source code string to validate.
            block_id: Sequential identifier of the code block.

        Returns:
            CodeValidationResult indicating VALID, INVALID, or UNSUPPORTED.
        """
        pass

    def create_result(
        self,
        block_id: int,
        status: ValidationStatus,
        code: str,
        diagnostics: Optional[List[ValidationDiagnostic]] = None,
        validator_name: Optional[str] = None,
    ) -> CodeValidationResult:
        """Helper to construct CodeValidationResult."""
        return CodeValidationResult(
            block_id=block_id,
            language=self.language,
            status=status,
            code=code,
            diagnostics=diagnostics or [],
            validator=validator_name or self.__class__.__name__,
        )

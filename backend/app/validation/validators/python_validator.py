"""Python syntax validator using stdlib ast.parse."""

import ast
from backend.app.validation.schemas import CodeValidationResult, ValidationDiagnostic, ValidationStatus
from backend.app.validation.validators.base import BaseCodeValidator


class PythonValidator(BaseCodeValidator):
    """Validates Python syntax statically using standard library AST parser."""

    language = "python"

    def validate(self, code: str, block_id: int = 1) -> CodeValidationResult:
        """Parse Python source code using ast.parse without executing any statements."""
        if not code or not code.strip():
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.VALID,
                code=code,
                diagnostics=[],
            )

        try:
            # ast.parse does not execute code; it purely builds the syntax tree
            ast.parse(code)
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.VALID,
                code=code,
                diagnostics=[],
            )
        except (SyntaxError, IndentationError) as err:
            diagnostic = ValidationDiagnostic(
                severity="ERROR",
                message=err.msg or str(err),
                line=err.lineno,
                column=err.offset,
                code=err.text.strip() if err.text else None,
            )
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.INVALID,
                code=code,
                diagnostics=[diagnostic],
            )
        except Exception as err:
            diagnostic = ValidationDiagnostic(
                severity="ERROR",
                message=f"Parser error: {err}",
            )
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.INVALID,
                code=code,
                diagnostics=[diagnostic],
            )

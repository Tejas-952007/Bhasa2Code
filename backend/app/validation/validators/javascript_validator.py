"""JavaScript syntax validator using node --check without execution."""

import os
import re
import shutil
import subprocess
import tempfile
from typing import List, Optional

from backend.app.validation.schemas import CodeValidationResult, ValidationDiagnostic, ValidationStatus
from backend.app.validation.validators.base import BaseCodeValidator


class JavaScriptValidator(BaseCodeValidator):
    """Validates JavaScript syntax using node --check without executing code."""

    language = "javascript"

    def __init__(self, timeout_seconds: float = 5.0, node_path: Optional[str] = None) -> None:
        self.timeout_seconds = timeout_seconds
        self.node_path = node_path or shutil.which("node")

    def is_available(self) -> bool:
        """Check whether the node executable exists on the system."""
        if not self.node_path:
            return False
        return bool(shutil.which(self.node_path) or os.path.exists(self.node_path))

    def validate(self, code: str, block_id: int = 1) -> CodeValidationResult:
        """Validate JavaScript syntax using node --check in an isolated temporary file."""
        if not self.is_available():
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.UNSUPPORTED,
                code=code,
                diagnostics=[
                    ValidationDiagnostic(
                        severity="INFO",
                        message="Node.js runtime not found on host system. JavaScript syntax validation unsupported.",
                    )
                ],
            )

        if not code or not code.strip():
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.VALID,
                code=code,
                diagnostics=[],
            )

        temp_path = None
        try:
            with tempfile.NamedTemporaryFile("w", suffix=".js", delete=False, encoding="utf-8") as tf:
                tf.write(code)
                temp_path = tf.name

            # node --check verifies script syntax without execution
            proc = subprocess.run(
                [self.node_path, "--check", temp_path],
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                shell=False,
            )

            diagnostics = self._parse_node_output(proc.stderr, temp_path)

            if proc.returncode == 0:
                return self.create_result(
                    block_id=block_id,
                    status=ValidationStatus.VALID,
                    code=code,
                    diagnostics=diagnostics,
                )
            else:
                return self.create_result(
                    block_id=block_id,
                    status=ValidationStatus.INVALID,
                    code=code,
                    diagnostics=diagnostics or [
                        ValidationDiagnostic(
                            severity="ERROR",
                            message=proc.stderr.strip() or "JavaScript syntax error.",
                        )
                    ],
                )

        except FileNotFoundError:
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.UNSUPPORTED,
                code=code,
                diagnostics=[
                    ValidationDiagnostic(
                        severity="INFO",
                        message="Node.js executable not found.",
                    )
                ],
            )
        except subprocess.TimeoutExpired:
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.INVALID,
                code=code,
                diagnostics=[
                    ValidationDiagnostic(
                        severity="ERROR",
                        message=f"JavaScript syntax check timed out after {self.timeout_seconds} seconds.",
                    )
                ],
            )
        except Exception as err:
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.INVALID,
                code=code,
                diagnostics=[
                    ValidationDiagnostic(
                        severity="ERROR",
                        message=f"Execution error invoking node: {err}",
                    )
                ],
            )
        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass

    def _parse_node_output(self, output: str, filename: str) -> List[ValidationDiagnostic]:
        """Extract diagnostics from node --check stderr."""
        diagnostics: List[ValidationDiagnostic] = []
        if not output:
            return diagnostics

        # Matches lines like: /tmp/...js:1
        # followed by SyntaxError: Unexpected token ';'
        line_num = None
        line_match = re.search(rf"{re.escape(filename)}:(\d+)", output)
        if line_match:
            line_num = int(line_match.group(1))

        error_match = re.search(r"SyntaxError:\s*(.*)", output)
        if error_match:
            msg = error_match.group(1).strip()
            diagnostics.append(
                ValidationDiagnostic(
                    severity="ERROR",
                    message=f"SyntaxError: {msg}",
                    line=line_num,
                )
            )

        return diagnostics

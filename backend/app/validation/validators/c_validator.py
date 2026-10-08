"""C code syntax validator using gcc -fsyntax-only."""

import os
import re
import shutil
import subprocess
import tempfile
from typing import List, Optional

from backend.app.validation.schemas import CodeValidationResult, ValidationDiagnostic, ValidationStatus
from backend.app.validation.validators.base import BaseCodeValidator


class CValidator(BaseCodeValidator):
    """Validates C syntax without compilation or execution via gcc -fsyntax-only."""

    language = "c"

    def __init__(self, timeout_seconds: float = 5.0, gcc_path: Optional[str] = None) -> None:
        self.timeout_seconds = timeout_seconds
        self.gcc_path = gcc_path or shutil.which("gcc")

    def is_available(self) -> bool:
        """Check whether the gcc executable exists on the system."""
        if not self.gcc_path:
            return False
        return bool(shutil.which(self.gcc_path) or os.path.exists(self.gcc_path))

    def validate(self, code: str, block_id: int = 1) -> CodeValidationResult:
        """Validate C syntax using gcc -fsyntax-only in an isolated subprocess."""
        if not self.is_available():
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.UNSUPPORTED,
                code=code,
                diagnostics=[
                    ValidationDiagnostic(
                        severity="INFO",
                        message="GCC compiler not found on host system. Syntax validation unsupported.",
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
            with tempfile.NamedTemporaryFile("w", suffix=".c", delete=False) as tf:
                tf.write(code)
                temp_path = tf.name

            proc = subprocess.run(
                [self.gcc_path, "-fsyntax-only", temp_path],
                capture_output=True,
                text=True,
                timeout=self.timeout_seconds,
                shell=False,
            )

            diagnostics = self._parse_compiler_output(proc.stderr, temp_path)

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
                            message=proc.stderr.strip() or "Syntax compilation failed.",
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
                        message="GCC compiler executable not found.",
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
                        message=f"GCC syntax check timed out after {self.timeout_seconds} seconds.",
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
                        message=f"Execution error invoking gcc: {err}",
                    )
                ],
            )
        finally:
            if temp_path and os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except OSError:
                    pass

    def _parse_compiler_output(self, output: str, filename: str) -> List[ValidationDiagnostic]:
        """Extract diagnostics from gcc output."""
        diagnostics: List[ValidationDiagnostic] = []
        if not output:
            return diagnostics

        # Matches lines like: /tmp/file.c:4:12: error: expected ';' before 'return'
        line_pattern = re.compile(
            rf"{re.escape(filename)}:(\d+):(?:(\d+):)?\s*(error|warning|fatal error):\s*(.*)",
            re.IGNORECASE,
        )

        for line in output.splitlines():
            match = line_pattern.search(line)
            if match:
                line_no = int(match.group(1))
                col_no = int(match.group(2)) if match.group(2) else None
                kind = match.group(3).upper()
                msg = match.group(4).strip()
                severity = "ERROR" if "ERROR" in kind else "WARNING"
                diagnostics.append(
                    ValidationDiagnostic(
                        severity=severity,
                        message=msg,
                        line=line_no,
                        column=col_no,
                    )
                )

        return diagnostics

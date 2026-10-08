"""Java code syntax validator using javac compile checking."""

import os
import re
import shutil
import subprocess
import tempfile
from typing import List, Optional

from backend.app.validation.schemas import CodeValidationResult, ValidationDiagnostic, ValidationStatus
from backend.app.validation.validators.base import BaseCodeValidator


class JavaValidator(BaseCodeValidator):
    """Validates Java syntax using javac compile checking without execution."""

    language = "java"

    def __init__(self, timeout_seconds: float = 5.0, javac_path: Optional[str] = None) -> None:
        self.timeout_seconds = timeout_seconds
        self.javac_path = javac_path or shutil.which("javac")

    def is_available(self) -> bool:
        """Check whether the javac executable exists on the system."""
        if not self.javac_path:
            return False
        return bool(shutil.which(self.javac_path) or os.path.exists(self.javac_path))

    def validate(self, code: str, block_id: int = 1) -> CodeValidationResult:
        """Validate Java syntax in a temporary directory using javac."""
        if not self.is_available():
            return self.create_result(
                block_id=block_id,
                status=ValidationStatus.UNSUPPORTED,
                code=code,
                diagnostics=[
                    ValidationDiagnostic(
                        severity="INFO",
                        message="Java compiler (javac) not found on host system. Syntax validation unsupported.",
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

        # Resolve primary class name
        class_name = self._extract_class_name(code)

        try:
            with tempfile.TemporaryDirectory() as tmpdir:
                src_path = os.path.join(tmpdir, f"{class_name}.java")
                with open(src_path, "w", encoding="utf-8") as f:
                    f.write(code)

                # javac compile checking: compile into tmpdir (never run classes)
                proc = subprocess.run(
                    [self.javac_path, "-d", tmpdir, src_path],
                    capture_output=True,
                    text=True,
                    timeout=self.timeout_seconds,
                    shell=False,
                )

                diagnostics = self._parse_compiler_output(proc.stderr, src_path)

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
                                message=proc.stderr.strip() or "Java compilation syntax error.",
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
                        message="Java compiler executable not found.",
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
                        message=f"Java syntax check timed out after {self.timeout_seconds} seconds.",
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
                        message=f"Execution error invoking javac: {err}",
                    )
                ],
            )

    def _extract_class_name(self, code: str) -> str:
        """Find the public class name or first declared class in code."""
        pub_match = re.search(r"\bpublic\s+(?:final\s+|abstract\s+)?class\s+([A-Za-z0-9_$]+)", code)
        if pub_match:
            return pub_match.group(1)

        class_match = re.search(r"\bclass\s+([A-Za-z0-9_$]+)", code)
        if class_match:
            return class_match.group(1)

        return "Main"

    def _parse_compiler_output(self, output: str, filename: str) -> List[ValidationDiagnostic]:
        """Extract diagnostics from javac compiler output."""
        diagnostics: List[ValidationDiagnostic] = []
        if not output:
            return diagnostics

        # Matches lines like: /tmp/.../Main.java:3: error: ';' expected
        line_pattern = re.compile(
            rf"{re.escape(filename)}:(\d+):\s*(error|warning):\s*(.*)",
            re.IGNORECASE,
        )

        for line in output.splitlines():
            match = line_pattern.search(line)
            if match:
                line_no = int(match.group(1))
                kind = match.group(2).upper()
                msg = match.group(3).strip()
                severity = "ERROR" if "ERROR" in kind else "WARNING"
                diagnostics.append(
                    ValidationDiagnostic(
                        severity=severity,
                        message=msg,
                        line=line_no,
                    )
                )

        return diagnostics

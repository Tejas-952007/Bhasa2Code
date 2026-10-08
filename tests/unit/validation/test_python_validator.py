"""Unit tests for PythonValidator and AST safety."""

import os
from backend.app.validation.schemas import ValidationStatus
from backend.app.validation.validators.python_validator import PythonValidator


def test_python_valid_syntax():
    validator = PythonValidator()
    code = (
        "def add(a: int, b: int) -> int:\n"
        "    \"\"\"Docstring\"\"\"\n"
        "    return a + b\n\n"
        "class Calculator:\n"
        "    def __init__(self):\n"
        "        self.val = 0\n"
    )
    result = validator.validate(code, block_id=1)
    assert result.status == ValidationStatus.VALID
    assert result.is_valid is True
    assert len(result.diagnostics) == 0


def test_python_invalid_syntax_missing_colon():
    validator = PythonValidator()
    code = (
        "def add(a, b)\n"
        "    return a + b\n"
    )
    result = validator.validate(code, block_id=1)
    assert result.status == ValidationStatus.INVALID
    assert result.is_valid is False
    assert len(result.diagnostics) == 1
    diag = result.diagnostics[0]
    assert diag.severity == "ERROR"
    assert diag.line == 1
    assert "expected ':'" in diag.message.lower() or "syntax" in diag.message.lower()


def test_python_indentation_error():
    validator = PythonValidator()
    code = (
        "def foo():\n"
        "print('bad indent')\n"
    )
    result = validator.validate(code, block_id=1)
    assert result.status == ValidationStatus.INVALID
    assert len(result.diagnostics) == 1
    assert "indent" in result.diagnostics[0].message.lower()


def test_python_empty_code():
    validator = PythonValidator()
    assert validator.validate("").status == ValidationStatus.VALID
    assert validator.validate("   \n\n  ").status == ValidationStatus.VALID


def test_python_security_no_execution():
    """Verify that potentially harmful code is strictly parsed, never executed."""
    validator = PythonValidator()
    sentinel_file = "/tmp/bhasha2code_test_python_exec.txt"
    if os.path.exists(sentinel_file):
        os.remove(sentinel_file)

    harmful_code = (
        "import os\n"
        f"os.system('touch {sentinel_file}')\n"
        "print('executed')\n"
    )

    # Valid syntax, but MUST NOT execute
    result = validator.validate(harmful_code, block_id=1)
    assert result.status == ValidationStatus.VALID

    # Assert sentinel file was NOT created on host
    assert not os.path.exists(sentinel_file), "Security violation: Python code was executed during validation!"

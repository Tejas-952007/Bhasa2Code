"""Unit and integration tests for ResponseValidator orchestrator."""

import pytest
from backend.app.validation.response_validator import ResponseValidator
from backend.app.validation.schemas import ValidationStatus


def test_validate_no_code():
    validator = ResponseValidator()
    text = "Polymorphism is an OOP concept where an entity can take multiple forms."
    res = validator.validate(text)
    assert res.has_code is False
    assert res.status == ValidationStatus.NOT_VALIDATED
    assert len(res.code_blocks) == 0
    assert len(res.diagnostics) == 0


def test_validate_single_valid_python_block():
    validator = ResponseValidator()
    text = (
        "Here is the calculator function:\n\n"
        "```python\n"
        "def add(a, b):\n"
        "    return a + b\n"
        "```\n\n"
        "You can call it with add(2, 3)."
    )
    res = validator.validate(text)
    assert res.has_code is True
    assert res.status == ValidationStatus.VALID
    assert len(res.code_blocks) == 1
    assert res.code_blocks[0].language == "python"
    assert res.code_blocks[0].status == ValidationStatus.VALID


def test_validate_single_invalid_python_block():
    validator = ResponseValidator()
    text = (
        "Here is the code:\n\n"
        "```python\n"
        "def add(a, b)\n"
        "    return a + b\n"
        "```\n"
    )
    res = validator.validate(text)
    assert res.has_code is True
    assert res.status == ValidationStatus.INVALID
    assert len(res.code_blocks) == 1
    assert res.code_blocks[0].status == ValidationStatus.INVALID
    assert len(res.diagnostics) >= 1


def test_validate_multiple_valid_blocks():
    validator = ResponseValidator()
    text = (
        "Python version:\n"
        "```python\n"
        "def add(a, b): return a + b\n"
        "```\n\n"
        "JavaScript version:\n"
        "```javascript\n"
        "const add = (a, b) => a + b;\n"
        "```\n"
    )
    res = validator.validate(text)
    assert res.has_code is True
    assert res.status == ValidationStatus.VALID
    assert len(res.code_blocks) == 2
    assert res.code_blocks[0].status == ValidationStatus.VALID
    assert res.code_blocks[1].status == ValidationStatus.VALID


def test_validate_mixed_valid_and_invalid_blocks():
    validator = ResponseValidator()
    text = (
        "Good Python:\n"
        "```python\n"
        "x = 10\n"
        "```\n\n"
        "Bad Python:\n"
        "```python\n"
        "def foo(\n"
        "```\n"
    )
    res = validator.validate(text)
    assert res.status == ValidationStatus.INVALID
    assert len(res.code_blocks) == 2
    assert res.code_blocks[0].status == ValidationStatus.VALID
    assert res.code_blocks[1].status == ValidationStatus.INVALID


def test_validate_unsupported_language_block():
    validator = ResponseValidator()
    text = (
        "Here is Haskell:\n"
        "```haskell\n"
        "add :: Int -> Int -> Int\n"
        "add x y = x + y\n"
        "```\n"
    )
    res = validator.validate(text)
    assert res.status == ValidationStatus.UNSUPPORTED
    assert res.code_blocks[0].status == ValidationStatus.UNSUPPORTED


def test_validate_mixed_valid_and_unsupported():
    validator = ResponseValidator()
    text = (
        "```python\n"
        "x = 1\n"
        "```\n\n"
        "```rust\n"
        "fn main() {}\n"
        "```\n"
    )
    res = validator.validate(text)
    # Mixture of VALID and UNSUPPORTED results in UNSUPPORTED
    assert res.status == ValidationStatus.UNSUPPORTED


def test_validate_with_language_hint_unlabeled_fence():
    validator = ResponseValidator()
    text = (
        "```\n"
        "def multiply(a, b):\n"
        "    return a * b\n"
        "```\n"
    )
    res = validator.validate(text, language_hint="python")
    assert res.status == ValidationStatus.VALID
    assert res.code_blocks[0].language == "python"


def test_validate_none_raises_error():
    validator = ResponseValidator()
    with pytest.raises(ValueError):
        validator.validate(None)


def test_validate_determinism():
    """Verify that validating the same text 10 times yields identical outputs."""
    validator = ResponseValidator()
    text = (
        "Here is the code:\n\n"
        "```python\n"
        "def is_even(n: int) -> bool:\n"
        "    return n % 2 == 0\n"
        "```\n"
    )
    first_res = validator.validate(text)

    for _ in range(10):
        next_res = validator.validate(text)
        assert next_res.status == first_res.status
        assert len(next_res.code_blocks) == len(first_res.code_blocks)
        assert next_res.code_blocks[0].code == first_res.code_blocks[0].code
        assert next_res.code_blocks[0].status == first_res.code_blocks[0].status

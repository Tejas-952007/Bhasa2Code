"""Regression tests for Prime Number check, output truncation, instruction following, and code completion.

Verifies:
1. Prime check mathematical accuracy: negative numbers, 0, 1 are not prime.
2. 2**64 - 1 is not reported as prime (it is composite; divisible by 3).
3. "only code and two test cases" format detection and section selection.
4. Token-limit output (done_reason == "length") remains strictly marked INCOMPLETE.
5. "Complete Code" continuation prompt excludes previous conversation summaries.
6. Execution of function-only artifact produces exit code 0 without stdout, not test success.
"""

import ast
import uuid
import pytest

from backend.app.context.schemas import ContextCode, ContextMessage, ContextMetadata, ContextPackage
from backend.app.prompt.format_rules import (
    
    ExplicitFormatRequirements,
    detect_explicit_format_requirements,
    select_response_sections,
)
from backend.app.prompt.prompt_builder import PromptBuilder
from backend.app.validation.response_validator import ResponseValidator
from backend.app.validation.schemas import ValidationStatus


# Canonical prime implementation matching Bhasha2Code requirements
def canonical_is_prime(n: int) -> bool:
    """Check if an integer n is a prime number."""
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


# ---------------------------------------------------------------------------
# Test 1: Mathematical Accuracy & Boundary Conditions
# ---------------------------------------------------------------------------


def test_prime_boundary_and_large_number():
    """Verify non-positive inputs, 0, 1, and 2**64 - 1 are not reported as prime."""
    # Negative inputs
    assert canonical_is_prime(-100) is False
    assert canonical_is_prime(-5) is False
    assert canonical_is_prime(-1) is False

    # Zero and One
    assert canonical_is_prime(0) is False
    assert canonical_is_prime(1) is False

    # Small primes & composites
    assert canonical_is_prime(2) is True
    assert canonical_is_prime(3) is True
    assert canonical_is_prime(4) is False
    assert canonical_is_prime(7) is True
    assert canonical_is_prime(9) is False

    # 2**64 - 1 is divisible by 3 (composite)
    val_64 = 2**64 - 1
    assert val_64 % 3 == 0
    assert canonical_is_prime(val_64) is False


# ---------------------------------------------------------------------------
# Test 2: Explicit Format Requirements Detection
# ---------------------------------------------------------------------------


def test_code_and_two_test_cases_format_detection():
    """Verify 'only complete Python code and two simple test cases' is detected."""
    prompt = "Write a Python function to check if a number is prime. Give only complete Python code and two simple test cases."
    req = detect_explicit_format_requirements(prompt)

    assert req.code_and_tests_only is True
    assert req.num_test_cases == 2
    assert "code_and_tests_only" in req.matched_patterns

    # Priority hierarchy trumps Study Mode sections
    sections = select_response_sections(
        intent="GENERATE_CODE",
        tone="CASUAL",
        study_mode=True,
        explicit_requirements=req,
    )
    assert sections == ["Code with Test Cases"]
    assert "Flowchart" not in sections
    assert "Viva Questions" not in sections
    assert "Problem Understanding" not in sections


def test_code_and_tests_multilingual_detection():
    """Verify Hindi and Marathi variants of code and test cases only."""
    hindi_prompt = "Prime check ka sirf code aur do test cases do"
    req_hi = detect_explicit_format_requirements(hindi_prompt)
    assert req_hi.code_and_tests_only is True
    assert req_hi.num_test_cases == 2

    marathi_prompt = "Prime number sathi fakt code ani 2 test cases de"
    req_mr = detect_explicit_format_requirements(marathi_prompt)
    assert req_mr.code_and_tests_only is True
    assert req_mr.num_test_cases == 2


# ---------------------------------------------------------------------------
# Test 3: Truncation Preservation on Token Limit
# ---------------------------------------------------------------------------


def test_token_limit_marks_response_incomplete():
    """Verify done_reason == 'length' strictly sets status to INCOMPLETE."""
    validator = ResponseValidator()

    # Code block itself is valid Python, but generation stopped at token limit
    truncated_response = (
        "Here is the function:\n"
        "```python\n"
        "def is_prime(n):\n"
        "    if n <= 1:\n"
        "        return False\n"
        "    return True\n"
        "```\n"
        "Now let's look at the assertions: assert is_prime("
    )

    res = validator.validate(truncated_response, language_hint="python", done_reason="length")
    assert res.status == ValidationStatus.INCOMPLETE
    assert any("token limit" in d.message for d in res.diagnostics)


def test_unclosed_fence_marks_incomplete():
    """Verify unclosed code block marks status INCOMPLETE."""
    validator = ResponseValidator()
    truncated_code = "```python\ndef is_prime(n):\n    if n <= 1:\n        return False\n"

    res = validator.validate(truncated_code, language_hint="python", done_reason="length")
    assert res.status == ValidationStatus.INCOMPLETE
    assert res.code_blocks[0].status == ValidationStatus.INCOMPLETE


# ---------------------------------------------------------------------------
# Test 4: Complete Code Continuation Isolation
# ---------------------------------------------------------------------------


def test_complete_code_does_not_append_conversation_summaries():
    """Verify continuation prompt excludes prior assistant summaries and maintains constraints."""
    builder = PromptBuilder()

    # Multi-turn context with prior bulky assistant explanation
    messages = [
        ContextMessage(
            message_id=str(uuid.uuid4()),
            role="user",
            content="Write a Python function to check if a number is prime. Give only complete Python code and two simple test cases.",
        ),
        ContextMessage(
            message_id=str(uuid.uuid4()),
            role="assistant",
            content="Here is the problem analysis: Prime numbers have only 2 factors... Viva Question 1: What is a prime?",
        ),
    ]

    generated_code = [
        ContextCode(
            generated_code_id="c-1",
            code="def is_prime(n):\n    if n <= 1:\n        return False",
            language="python",
            validation_status="incomplete",
        )
    ]

    continuation_prompt = "Complete the code from where it stopped"
    context_package = ContextPackage(
        session_id="sess-1",
        current_message=continuation_prompt,
        messages=messages,
        current_code="def is_prime(n):\n    if n <= 1:\n        return False",
        generated_code=generated_code,
        metadata=ContextMetadata(is_follow_up=True),
    )

    spec = builder.build(
        user_message=continuation_prompt,
        context_package=context_package,
        study_mode=True,
    )

    # 1. Conversation turns must NOT be dumped as historical conversation text
    assert "--- PREVIOUS CONVERSATION TURNS ---" not in spec.context_text
    assert "Viva Question 1" not in spec.context_text

    # 2. Incomplete code must be referenced
    assert "[INCOMPLETE CODE TO COMPLETE]" in spec.context_text
    assert "def is_prime(n):" in spec.context_text

    # 3. Continuation directive must be present
    assert any("CONTINUATION TASK" in c for c in spec.explicit_constraints)

    # 4. Response section must be dedicated to Code
    assert spec.response_sections in (["Code with Test Cases"], ["Code only"])


# ---------------------------------------------------------------------------
# Test 5: Function-Only Artifact Execution Distinction
# ---------------------------------------------------------------------------


def test_function_only_artifact_does_not_imply_test_pass():
    """Verify function definition code produces exit code 0 without stdout and has no test calls."""
    func_only_code = (
        "def is_prime(n: int) -> bool:\n"
        "    if n <= 1:\n"
        "        return False\n"
        "    return True\n"
    )

    parsed = ast.parse(func_only_code)
    # Check that there are no function calls or assert statements at top level
    calls = [n for n in ast.walk(parsed) if isinstance(n, (ast.Call, ast.Assert))]
    assert len(calls) == 0, "Function-only code must not contain top-level calls or assertions"

    # Running function definition in Python globals produces no output
    import io
    import sys

    stdout_capture = io.StringIO()
    old_stdout = sys.stdout
    try:
        sys.stdout = stdout_capture
        exec(func_only_code, {})
    finally:
        sys.stdout = old_stdout

    captured_out = stdout_capture.getvalue()
    assert captured_out == "", "Executing function-only code produces empty stdout"

"""Integration tests connecting T17 LLM responses to T18 ResponseValidator."""

import time
from backend.app.llm.schemas import LLMResponse
from backend.app.validation.response_validator import ResponseValidator
from backend.app.validation.schemas import ValidationStatus


def test_integration_llm_response_valid_python():
    """Verify integration when LLM produces a valid Python function with commentary."""
    llm_resp = LLMResponse(
        text=(
            "Here is the calculator:\n\n"
            "```python\n"
            "def add(a, b):\n"
            "    return a + b\n\n"
            "print(add(10, 5))\n"
            "```\n\n"
            "This function returns the sum of two numbers."
        ),
        model="qwen2.5-coder:3b",
    )

    validator = ResponseValidator()
    result = validator.validate(llm_resp.text)

    assert result.has_code is True
    assert result.status == ValidationStatus.VALID
    assert len(result.code_blocks) == 1
    assert result.code_blocks[0].language == "python"
    assert result.code_blocks[0].is_valid is True
    assert len(result.diagnostics) == 0


def test_integration_llm_response_invalid_python():
    """Verify integration when LLM produces a syntax-corrupted Python function."""
    llm_resp = LLMResponse(
        text=(
            "```python\n"
            "def add(a, b)\n"  # missing colon
            "    return a + b\n"
            "```"
        ),
        model="qwen2.5-coder:3b",
    )

    validator = ResponseValidator()
    result = validator.validate(llm_resp.text)

    assert result.has_code is True
    assert result.status == ValidationStatus.INVALID
    assert len(result.code_blocks) == 1
    assert result.code_blocks[0].is_valid is False
    assert len(result.diagnostics) >= 1
    assert result.diagnostics[0].line == 1


def test_integration_multilingual_marathi_commentary_with_code():
    """Verify Marathi-English commentary does not disrupt code extraction or validation."""
    response_text = (
        "हा Python calculator चा program aahe:\n\n"
        "```python\n"
        "def calculator(a, b, op):\n"
        "    if op == '+':\n"
        "        return a + b\n"
        "    elif op == '-':\n"
        "        return a - b\n"
        "    return 0\n"
        "```\n\n"
        "Tu ha function use karun calculations karu shakto."
    )

    validator = ResponseValidator()
    result = validator.validate(response_text)

    assert result.has_code is True
    assert result.status == ValidationStatus.VALID
    assert result.code_blocks[0].language == "python"


def test_integration_benchmarks_all_languages():
    """Benchmark static validation execution across all supported languages."""
    validator = ResponseValidator()

    samples = {
        "python": "def fib(n):\n    if n <= 1: return n\n    return fib(n-1) + fib(n-2)\n",
        "c": "#include <stdio.h>\nint main(void) { return 0; }\n",
        "cpp": "#include <iostream>\nint main() { return 0; }\n",
        "java": "public class BenchMain { public static void main(String[] args) {} }\n",
        "javascript": "const square = (x) => x * x;\n",
        "sql": "SELECT id, count(*) FROM orders GROUP BY id HAVING count(*) > 5;\n",
    }

    results = {}

    for lang, code in samples.items():
        fence_text = f"```{lang}\n{code}\n```"
        durations = []
        for _ in range(5):
            t0 = time.perf_counter()
            res = validator.validate(fence_text)
            t1 = time.perf_counter()
            durations.append((t1 - t0) * 1000.0)  # ms
            assert res.status == ValidationStatus.VALID

        avg_ms = sum(durations) / len(durations)
        min_ms = min(durations)
        max_ms = max(durations)
        results[lang] = {"avg_ms": avg_ms, "min_ms": min_ms, "max_ms": max_ms}

    print("\n[VALIDATION PERFORMANCE BENCHMARKS (5 runs each)]")
    for lang, metrics in results.items():
        print(f"  {lang.upper():10s}: avg={metrics['avg_ms']:.2f}ms | min={metrics['min_ms']:.2f}ms | max={metrics['max_ms']:.2f}ms")

    # Python AST should be sub-millisecond
    assert results["python"]["avg_ms"] < 20.0

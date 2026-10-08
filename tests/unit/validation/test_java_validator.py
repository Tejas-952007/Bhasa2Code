"""Unit tests for JavaValidator."""

import os
from backend.app.validation.schemas import ValidationStatus
from backend.app.validation.validators.java_validator import JavaValidator


def test_java_valid_syntax():
    validator = JavaValidator()
    code = (
        "public class Calculator {\n"
        "    public static int add(int a, int b) {\n"
        "        return a + b;\n"
        "    }\n"
        "    public static void main(String[] args) {\n"
        "        System.out.println(add(5, 10));\n"
        "    }\n"
        "}\n"
    )
    res = validator.validate(code)
    assert res.status == ValidationStatus.VALID
    assert res.is_valid is True


def test_java_invalid_syntax():
    validator = JavaValidator()
    code = (
        "public class BadJava {\n"
        "    public static void main(String[] args) {\n"
        "        System.out.println(1 + 1)\n"  # missing semicolon
        "    }\n"
        "}\n"
    )
    res = validator.validate(code)
    assert res.status == ValidationStatus.INVALID
    assert len(res.diagnostics) >= 1
    assert any(";" in d.message for d in res.diagnostics)


def test_java_compiler_unavailable():
    validator = JavaValidator(javac_path="/nonexistent/bin/javac")
    res = validator.validate("public class Test {}")
    assert res.status == ValidationStatus.UNSUPPORTED


def test_java_security_no_execution():
    """Verify that Java class is compile-checked, never run on host."""
    validator = JavaValidator()
    sentinel = "/tmp/bhasha2code_test_java_exec.txt"
    if os.path.exists(sentinel):
        os.remove(sentinel)

    harmful_code = (
        "public class EvilApp {\n"
        "    public static void main(String[] args) throws Exception {\n"
        f"        Runtime.getRuntime().exec(\"touch {sentinel}\");\n"
        "    }\n"
        "}\n"
    )

    res = validator.validate(harmful_code)
    assert res.status == ValidationStatus.VALID
    assert not os.path.exists(sentinel), "Security violation: Java code was executed during validation!"

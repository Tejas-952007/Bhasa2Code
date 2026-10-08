"""Unit tests for C and C++ syntax validators."""

import os
from backend.app.validation.schemas import ValidationStatus
from backend.app.validation.validators.c_validator import CValidator
from backend.app.validation.validators.cpp_validator import CppValidator


def test_c_valid_syntax():
    validator = CValidator()
    code = (
        "#include <stdio.h>\n"
        "int add(int a, int b) {\n"
        "    return a + b;\n"
        "}\n"
        "int main(void) {\n"
        "    printf(\"%d\\n\", add(2, 3));\n"
        "    return 0;\n"
        "}\n"
    )
    res = validator.validate(code)
    assert res.status == ValidationStatus.VALID
    assert res.is_valid is True


def test_c_invalid_syntax():
    validator = CValidator()
    code = (
        "#include <stdio.h>\n"
        "int main(void) {\n"
        "    printf(\"hello\")\n"  # missing semicolon
        "    return 0;\n"
        "}\n"
    )
    res = validator.validate(code)
    assert res.status == ValidationStatus.INVALID
    assert len(res.diagnostics) >= 1
    assert any("error" in d.severity.lower() for d in res.diagnostics)


def test_c_compiler_unavailable():
    validator = CValidator(gcc_path="/nonexistent/bin/gcc")
    res = validator.validate("int x = 1;")
    assert res.status == ValidationStatus.UNSUPPORTED
    assert "not found" in res.diagnostics[0].message.lower()


def test_cpp_valid_syntax():
    validator = CppValidator()
    code = (
        "#include <iostream>\n"
        "#include <vector>\n"
        "int main() {\n"
        "    std::vector<int> nums = {1, 2, 3};\n"
        "    std::cout << nums.size() << std::endl;\n"
        "    return 0;\n"
        "}\n"
    )
    res = validator.validate(code)
    assert res.status == ValidationStatus.VALID
    assert res.is_valid is True


def test_cpp_invalid_syntax():
    validator = CppValidator()
    code = (
        "#include <iostream>\n"
        "int main() {\n"
        "    std::cout << \"hello\"\n"  # missing semicolon
        "    return 0;\n"
        "}\n"
    )
    res = validator.validate(code)
    assert res.status == ValidationStatus.INVALID
    assert len(res.diagnostics) >= 1


def test_cpp_compiler_unavailable():
    validator = CppValidator(gpp_path="/nonexistent/bin/g++")
    res = validator.validate("int x = 1;")
    assert res.status == ValidationStatus.UNSUPPORTED


def test_c_cpp_security_no_execution():
    """Verify malicious C code is not executed during syntax check."""
    validator = CValidator()
    sentinel = "/tmp/bhasha2code_test_c_exec.txt"
    if os.path.exists(sentinel):
        os.remove(sentinel)

    harmful_code = (
        "#include <stdlib.h>\n"
        "int main() {\n"
        f"    system(\"touch {sentinel}\");\n"
        "    return 0;\n"
        "}\n"
    )

    res = validator.validate(harmful_code)
    assert res.status == ValidationStatus.VALID
    assert not os.path.exists(sentinel), "Security violation: C program was compiled/executed!"

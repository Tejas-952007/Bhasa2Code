"""Unit tests for JavaScriptValidator."""

import os
from backend.app.validation.schemas import ValidationStatus
from backend.app.validation.validators.javascript_validator import JavaScriptValidator


def test_javascript_valid_syntax():
    validator = JavaScriptValidator()
    code = (
        "function add(a, b) {\n"
        "    return a + b;\n"
        "}\n"
        "const result = add(10, 20);\n"
        "console.log(result);\n"
    )
    res = validator.validate(code)
    assert res.status == ValidationStatus.VALID
    assert res.is_valid is True


def test_javascript_invalid_syntax():
    validator = JavaScriptValidator()
    code = "const x = ;"
    res = validator.validate(code)
    assert res.status == ValidationStatus.INVALID
    assert len(res.diagnostics) >= 1
    assert any("SyntaxError" in d.message for d in res.diagnostics)


def test_javascript_node_unavailable():
    validator = JavaScriptValidator(node_path="/nonexistent/bin/node")
    res = validator.validate("const a = 1;")
    assert res.status == ValidationStatus.UNSUPPORTED


def test_javascript_security_no_execution():
    """Verify that node --check parses without running the script."""
    validator = JavaScriptValidator()
    sentinel = "/tmp/bhasha2code_test_js_exec.txt"
    if os.path.exists(sentinel):
        os.remove(sentinel)

    harmful_code = (
        "const fs = require('fs');\n"
        f"fs.writeFileSync('{sentinel}', 'pwned');\n"
    )

    res = validator.validate(harmful_code)
    assert res.status == ValidationStatus.VALID
    assert not os.path.exists(sentinel), "Security violation: JavaScript code was executed during validation!"

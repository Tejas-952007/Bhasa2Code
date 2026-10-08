"""Unit tests for language resolver and heuristics."""

from backend.app.validation.language_resolver import (
    detect_language_heuristics,
    normalize_language_name,
    resolve_language,
)


def test_normalize_language_aliases():
    assert normalize_language_name("python") == "python"
    assert normalize_language_name("py") == "python"
    assert normalize_language_name("python3") == "python"
    assert normalize_language_name("c") == "c"
    assert normalize_language_name("c++") == "cpp"
    assert normalize_language_name("cpp") == "cpp"
    assert normalize_language_name("java") == "java"
    assert normalize_language_name("js") == "javascript"
    assert normalize_language_name("javascript") == "javascript"
    assert normalize_language_name("sql") == "sql"
    assert normalize_language_name("postgresql") == "sql"
    assert normalize_language_name("unknown_lang") is None
    assert normalize_language_name(None) is None


def test_resolve_language_priority():
    # 1. Declared fence overrides hint
    code = "x = 10"
    res = resolve_language(declared_language="python", code=code, language_hint="cpp")
    assert res == "python"

    # 2. Hint used when declared language is absent
    res = resolve_language(declared_language=None, code=code, language_hint="java")
    assert res == "java"

    # 3. Heuristics used when neither is present
    python_code = "def calculate(a, b):\n    return a + b\n"
    res = resolve_language(declared_language=None, code=python_code, language_hint=None)
    assert res == "python"


def test_detect_language_heuristics():
    # Python
    py_code = "import math\ndef solve():\n    pass\n"
    assert detect_language_heuristics(py_code) == "python"

    # C++
    cpp_code = "#include <iostream>\nusing namespace std;\nint main() { cout << 1; }"
    assert detect_language_heuristics(cpp_code) == "cpp"

    # C
    c_code = "#include <stdio.h>\nint main(void) {\n    printf(\"hi\");\n}"
    assert detect_language_heuristics(c_code) == "c"

    # Java
    java_code = "public class App {\n    public static void main(String[] args) {\n        System.out.println(42);\n    }\n}"
    assert detect_language_heuristics(java_code) == "java"

    # JavaScript
    js_code = "const add = (a, b) => a + b;\nconsole.log(add(1, 2));"
    assert detect_language_heuristics(js_code) == "javascript"

    # SQL
    sql_code = "SELECT id, name FROM users WHERE active = 1;"
    assert detect_language_heuristics(sql_code) == "sql"

    # Ambiguous / Plain text
    ambiguous = "hello world this is just some text"
    assert detect_language_heuristics(ambiguous) is None

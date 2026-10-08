"""Programming language resolution and heuristic classification for code validation."""

import re
from typing import Optional


# Alias mapping normalizing user and fence names to canonical internal names
LANGUAGE_ALIASES = {
    # Python
    "python": "python",
    "python3": "python",
    "py": "python",
    # C
    "c": "c",
    # C++
    "cpp": "cpp",
    "c++": "cpp",
    "cc": "cpp",
    "cxx": "cpp",
    "hpp": "cpp",
    "h++": "cpp",
    # Java
    "java": "java",
    # JavaScript
    "javascript": "javascript",
    "js": "javascript",
    "mjs": "javascript",
    "cjs": "javascript",
    "node": "javascript",
    # SQL
    "sql": "sql",
    "mysql": "sql",
    "postgres": "sql",
    "postgresql": "sql",
    "sqlite": "sql",
    "sqlite3": "sql",
}


def normalize_language_name(name: Optional[str]) -> Optional[str]:
    """Normalize a raw language name or alias to its canonical identifier."""
    if not name:
        return None
    cleaned = name.strip().lower()
    return LANGUAGE_ALIASES.get(cleaned)


def detect_language_heuristics(code: str) -> Optional[str]:
    """Detect language using strong, deterministic static lexical heuristics.

    Returns canonical language name if strong signals match, otherwise None.
    """
    if not code or not code.strip():
        return None

    cleaned_code = code.strip()

    # 1. C++ vs C includes & keywords
    has_cpp_headers = bool(re.search(r"#include\s*<(?:iostream|vector|string|memory|algorithm|map|set)>", cleaned_code))
    has_cpp_markers = bool(re.search(r"\b(?:std::|cout\s*<<|cin\s*>>|template\s*<|namespace\s+\w+)", cleaned_code))

    if has_cpp_headers or has_cpp_markers:
        return "cpp"

    has_c_headers = bool(re.search(r"#include\s*<(?:stdio\.h|stdlib\.h|string\.h|math\.h|unistd\.h)>", cleaned_code))
    has_c_main = bool(re.search(r"\bint\s+main\s*\([^)]*\)\s*\{", cleaned_code))
    has_c_printf = bool(re.search(r"\bprintf\s*\(", cleaned_code))

    if has_c_headers or (has_c_main and has_c_printf):
        return "c"

    # 2. Java patterns
    has_java_class = bool(re.search(r"\b(?:public\s+)?(?:final\s+|abstract\s+)?class\s+\w+", cleaned_code))
    has_java_main = bool(re.search(r"\bpublic\s+static\s+void\s+main\s*\(\s*String\s*\[\s*\]", cleaned_code))
    has_java_sysout = bool(re.search(r"\bSystem\.(?:out|err)\.println\s*\(", cleaned_code))

    if (has_java_class and has_java_main) or has_java_sysout:
        return "java"

    # 3. Python patterns
    has_py_def = bool(re.search(r"^\s*def\s+\w+\s*\([^)]*\)\s*:", cleaned_code, re.MULTILINE))
    has_py_import = bool(re.search(r"^\s*(?:import\s+\w+|from\s+\w+\s+import\s+)", cleaned_code, re.MULTILINE))
    has_py_if_main = "__name__ == '__main__'" in cleaned_code or '__name__ == "__main__"' in cleaned_code
    has_py_elif = bool(re.search(r"^\s*elif\s+.*:", cleaned_code, re.MULTILINE))

    if has_py_def or has_py_import or has_py_if_main or has_py_elif:
        return "python"

    # 4. JavaScript patterns
    has_js_var = bool(re.search(r"\b(?:const|let|var)\s+\w+\s*=", cleaned_code))
    has_js_log = bool(re.search(r"\bconsole\.(?:log|error|warn)\s*\(", cleaned_code))
    has_js_arrow = bool(re.search(r"\([^)]*\)\s*=>\s*\{?", cleaned_code))
    has_js_function = bool(re.search(r"\bfunction\s+\w+\s*\(", cleaned_code))

    if (has_js_var and has_js_log) or (has_js_arrow and has_js_var) or (has_js_function and has_js_log):
        return "javascript"

    # 5. SQL patterns
    has_sql_statement = bool(
        re.search(
            r"^\s*(?:SELECT\s+.+\s+FROM|INSERT\s+INTO\s+\w+|UPDATE\s+\w+\s+SET|DELETE\s+FROM\s+\w+|CREATE\s+TABLE\s+\w+|DROP\s+TABLE\s+\w+|ALTER\s+TABLE\s+\w+)",
            cleaned_code,
            re.IGNORECASE | re.DOTALL,
        )
    )
    if has_sql_statement:
        return "sql"

    return None


def resolve_language(
    declared_language: Optional[str],
    code: str,
    language_hint: Optional[str] = None,
) -> Optional[str]:
    """Resolve programming language following strict priority rules.

    Priority:
    1. Markdown fence language (normalized)
    2. Upstream language hint (normalized)
    3. Strong deterministic code heuristics
    4. None (if unknown/unresolved)
    """
    # 1. Markdown fence language
    if declared_language:
        normalized = normalize_language_name(declared_language)
        if normalized:
            return normalized

    # 2. Upstream language hint
    if language_hint:
        normalized_hint = normalize_language_name(language_hint)
        if normalized_hint:
            return normalized_hint

    # 3. Strong code heuristics
    heuristic_lang = detect_language_heuristics(code)
    if heuristic_lang:
        return heuristic_lang

    return None

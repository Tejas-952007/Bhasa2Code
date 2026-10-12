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


NON_CODE_LANGUAGES = {
    "text",
    "txt",
    "plain",
    "plaintext",
    "ascii",
    "flowchart",
    "diagram",
    "mermaid",
    "output",
    "example",
    "markdown",
    "md",
    "none",
    "raw",
}

FLOWCHART_SIGNALS = [
    "+---",
    "+--",
    "|--",
    "/--",
    "\\--",
    "|   ",
    "+===",
    "|===",
    "+---+",
    "|---|",
    "+===+",
    "|===|",
    "-->",
    "<--",
    "==>",
    "->",
    "<-",
    "├──",
    "└──",
    "│",
    "┌",
    "┐",
    "└",
    "┘",
    "┬",
    "┴",
    "┼",
    "↓",
    "↑",
    "←",
    "→",
    "▲",
    "▼",
]


def is_flowchart_or_diagram(text: str) -> bool:
    """Identify if text is an ASCII flowchart, tree, or block diagram."""
    cleaned = text.strip()
    if not cleaned:
        return False
    # Check ASCII box / diagram markers
    marker_hits = sum(1 for m in FLOWCHART_SIGNALS if m in cleaned)
    if marker_hits >= 2:
        return True
    lines = [l.strip().lower() for l in cleaned.splitlines() if l.strip()]
    if any(re.search(r"^[vV|^│↓]\s*$", l) for l in lines) and any("-" in l or "+" in l or "|" in l for l in lines):
        return True
    flow_steps = sum(
        1
        for l in lines
        if l in ("start", "stop", "end", "input", "output", "process", "decision", "yes", "no")
        or bool(re.match(r"^\[?(?:start|end|stop|initialize|loop|midpoint|condition)\]?$", l))
    )
    if flow_steps >= 2:
        return True
    if any(re.search(r"\[.+\]\s*(?:-->|->|│|↓)\s*\[.+\]", l) for l in lines):
        return True
    return False


def is_markdown_table(text: str) -> bool:
    """Identify if text is a Markdown table."""
    cleaned = text.strip()
    if not cleaned:
        return False
    lines = [l.strip() for l in cleaned.splitlines() if l.strip()]
    table_lines = [l for l in lines if l.startswith("|") and l.endswith("|") and "|" in l[1:-1]]
    has_separator = any(re.match(r"^\|(?:\s*:?-+:?\s*\|)+$", l) for l in lines)
    if has_separator or len(table_lines) >= 2:
        return True
    return False


def has_code_signals(code: str, lang: str) -> bool:
    """Verify that a code snippet contains expected syntax signals for the target language."""
    cleaned = code.strip()
    if not cleaned:
        return False
    if lang == "python":
        return bool(
            re.search(
                r"(\bdef\s+\w+|\bimport\s+\w+|\bfrom\s+\w+\s+import|\bclass\s+\w+|\bprint\s*\(|:\s*$|\bif\b|\bfor\b|\bwhile\b|\breturn\b)",
                cleaned,
                re.MULTILINE,
            )
        )
    elif lang in ("c", "cpp"):
        return bool(re.search(r"(#include|\bint\s+main|\bvoid\s+\w+|\bprintf\s*\(|\bstd::|;|{|})", cleaned))
    elif lang == "java":
        return bool(
            re.search(
                r"(\bclass\s+\w+|\bpublic\s+static\s+void|\bSystem\.(?:out|err)\.println|;|{|})",
                cleaned,
            )
        )
    elif lang == "javascript":
        return bool(
            re.search(
                r"(\bfunction\s+\w+|\bconst\s+\w+\s*=|\blet\s+\w+\s*=|\bconsole\.(?:log|error)\(|=>|;|{|})",
                cleaned,
            )
        )
    elif lang == "sql":
        return bool(
            re.search(
                r"(\bSELECT\s+.+\s+FROM|\bINSERT\s+INTO|\bUPDATE\s+\w+\s+SET|\bDELETE\s+FROM|\bCREATE\s+TABLE)",
                cleaned,
                re.IGNORECASE,
            )
        )
    return False


def is_prose_or_explanation(text: str) -> bool:
    """Identify if text is prose/explanation rather than code."""
    cleaned = text.strip()
    if not cleaned:
        return False
    # If code contains syntax characters like brackets, assignment, semicolon, keywords, it's code
    if re.search(r"[{};=()<>\[\]]|def |class |public |const |let |var |import |SELECT |int ", cleaned):
        return False
    words = re.findall(r"\b[a-zA-Z]+\b", cleaned)
    if len(words) >= 5:
        return True
    return False


def resolve_language(
    declared_language: Optional[str],
    code: str,
    language_hint: Optional[str] = None,
) -> Optional[str]:
    """Resolve programming language following strict priority rules.

    Priority:
    1. Filter out explicit non-code declared languages (text, flowchart, ascii, etc.)
    2. Filter out ASCII diagrams and flowcharts
    3. Filter out Markdown tables
    4. Filter out Prose/explanations
    5. Markdown fence language (normalized, validated for basic code signals)
    6. Strong deterministic code heuristics
    7. Upstream language hint (normalized) only if code signals match
    8. None (if unknown/unresolved/diagram/table)
    """
    # 1. Non-code declared languages
    if declared_language and declared_language.strip().lower() in NON_CODE_LANGUAGES:
        return None

    # 2. Block diagram / flowchart content filter
    if is_flowchart_or_diagram(code):
        return None

    # 3. Markdown table filter
    if is_markdown_table(code):
        return None

    # 4. Prose or explanation filter
    if is_prose_or_explanation(code):
        return None

    # 5. Markdown fence language (normalized)
    if declared_language:
        normalized = normalize_language_name(declared_language)
        if normalized:
            if has_code_signals(code, normalized) or len(code.strip().splitlines()) <= 2:
                return normalized

    # 6. Strong code heuristics
    heuristic_lang = detect_language_heuristics(code)
    if heuristic_lang:
        return heuristic_lang

    # 7. Upstream language hint (normalized)
    if language_hint:
        normalized_hint = normalize_language_name(language_hint)
        if normalized_hint:
            return normalized_hint

    return None

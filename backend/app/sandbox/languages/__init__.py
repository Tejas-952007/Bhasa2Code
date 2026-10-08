"""Language runners registry and factory for sandbox execution."""

from typing import Dict
from backend.app.sandbox.exceptions import UnsupportedLanguageError
from backend.app.sandbox.languages.base import BaseLanguageRunner, LanguageExecutionPlan
from backend.app.sandbox.languages.c_runner import CRunner
from backend.app.sandbox.languages.cpp_runner import CppRunner
from backend.app.sandbox.languages.java_runner import JavaRunner
from backend.app.sandbox.languages.javascript_runner import JavaScriptRunner
from backend.app.sandbox.languages.python_runner import PythonRunner

LANGUAGE_ALIASES: Dict[str, str] = {
    "python": "python",
    "py": "python",
    "python3": "python",
    "c": "c",
    "cpp": "cpp",
    "c++": "cpp",
    "cc": "cpp",
    "cxx": "cpp",
    "java": "java",
    "javascript": "javascript",
    "js": "javascript",
    "node": "javascript",
    "nodejs": "javascript",
}

RUNNER_MAP: Dict[str, BaseLanguageRunner] = {
    "python": PythonRunner(),
    "c": CRunner(),
    "cpp": CppRunner(),
    "java": JavaRunner(),
    "javascript": JavaScriptRunner(),
}


def normalize_sandbox_language(language: str) -> str:
    """Normalize input language string to canonical sandbox identifier."""
    if not language:
        return ""
    clean = language.strip().lower()
    return LANGUAGE_ALIASES.get(clean, clean)


def get_language_runner(language: str) -> BaseLanguageRunner:
    """Retrieve the language runner for a given language or raise UnsupportedLanguageError."""
    canonical = normalize_sandbox_language(language)
    runner = RUNNER_MAP.get(canonical)
    if not runner:
        raise UnsupportedLanguageError(
            f"Language '{language}' has no sandbox runtime adapter in T19. "
            f"Supported languages: {sorted(RUNNER_MAP.keys())}."
        )
    return runner


__all__ = [
    "BaseLanguageRunner",
    "LanguageExecutionPlan",
    "PythonRunner",
    "CRunner",
    "CppRunner",
    "JavaRunner",
    "JavaScriptRunner",
    "get_language_runner",
    "normalize_sandbox_language",
    "RUNNER_MAP",
]

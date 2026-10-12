"""Python sandbox execution runner with dynamic ML profile and image selection."""

import ast
import re
from typing import Set

from backend.app.sandbox.config import SandboxConfig
from backend.app.sandbox.languages.base import BaseLanguageRunner, LanguageExecutionPlan

ML_MODULES: Set[str] = {"sklearn", "numpy", "scipy", "pandas"}


def is_python_ml_code(code: str) -> bool:
    """Detect whether Python code imports scientific or machine learning packages."""
    if not code:
        return False

    try:
        tree = ast.parse(code)
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                for alias in node.names:
                    root_mod = alias.name.split(".")[0]
                    if root_mod in ML_MODULES:
                        return True
            elif isinstance(node, ast.ImportFrom):
                if node.module:
                    root_mod = node.module.split(".")[0]
                    if root_mod in ML_MODULES:
                        return True
    except SyntaxError:
        pass

    # Regex fallback for incomplete snippets or inline script fragments
    pattern = re.compile(
        r"^\s*(?:import|from)\s+(sklearn|numpy|scipy|pandas)\b",
        re.MULTILINE,
    )
    return bool(pattern.search(code))


class PythonRunner(BaseLanguageRunner):
    """Executes Python code inside an isolated container with adaptive ML selection."""

    @property
    def language(self) -> str:
        return "python"

    def build_plan(self, code: str, config: SandboxConfig) -> LanguageExecutionPlan:
        is_ml = is_python_ml_code(code)

        if is_ml:
            image = config.image_tags.get("python_ml", "bhasha2code-sandbox-python-ml:1.0.0")
            timeout_seconds = config.ml_timeout_seconds
            memory_limit_mb = config.ml_memory_limit_mb
        else:
            image = config.image_tags.get("python", "bhasha2code-sandbox-python:1.0.0")
            timeout_seconds = config.timeout_seconds
            memory_limit_mb = config.memory_limit_mb

        return LanguageExecutionPlan(
            language=self.language,
            image_tag=image,
            files={"main.py": code},
            entrypoint=["python3", "-u", "main.py"],
            is_ml=is_ml,
            timeout_seconds=timeout_seconds,
            memory_limit_mb=memory_limit_mb,
        )

"""Python sandbox execution runner."""

from backend.app.sandbox.config import SandboxConfig
from backend.app.sandbox.languages.base import BaseLanguageRunner, LanguageExecutionPlan


class PythonRunner(BaseLanguageRunner):
    """Executes Python code inside an isolated container."""

    @property
    def language(self) -> str:
        return "python"

    def build_plan(self, code: str, config: SandboxConfig) -> LanguageExecutionPlan:
        image = config.image_tags.get("python", "bhasha2code-sandbox-python:1.0.0")
        return LanguageExecutionPlan(
            language=self.language,
            image_tag=image,
            files={"main.py": code},
            entrypoint=["python3", "-u", "main.py"],
        )

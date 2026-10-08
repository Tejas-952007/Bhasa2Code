"""C sandbox execution runner."""

from backend.app.sandbox.config import SandboxConfig
from backend.app.sandbox.languages.base import BaseLanguageRunner, LanguageExecutionPlan


class CRunner(BaseLanguageRunner):
    """Compiles and executes C code entirely inside an isolated container."""

    @property
    def language(self) -> str:
        return "c"

    def build_plan(self, code: str, config: SandboxConfig) -> LanguageExecutionPlan:
        image = config.image_tags.get("c", "bhasha2code-sandbox-cpp:1.0.0")
        return LanguageExecutionPlan(
            language=self.language,
            image_tag=image,
            files={"main.c": code},
            entrypoint=["sh", "-c", "gcc -O2 main.c -o /workspace/prog && /workspace/prog"],
        )

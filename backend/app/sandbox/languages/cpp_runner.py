"""C++ sandbox execution runner."""

from backend.app.sandbox.config import SandboxConfig
from backend.app.sandbox.languages.base import BaseLanguageRunner, LanguageExecutionPlan


class CppRunner(BaseLanguageRunner):
    """Compiles and executes C++ code entirely inside an isolated container."""

    @property
    def language(self) -> str:
        return "cpp"

    def build_plan(self, code: str, config: SandboxConfig) -> LanguageExecutionPlan:
        image = config.image_tags.get("cpp", "bhasha2code-sandbox-cpp:1.0.0")
        return LanguageExecutionPlan(
            language=self.language,
            image_tag=image,
            files={"main.cpp": code},
            entrypoint=["sh", "-c", "g++ -O2 -std=c++17 main.cpp -o /workspace/prog && /workspace/prog"],
        )

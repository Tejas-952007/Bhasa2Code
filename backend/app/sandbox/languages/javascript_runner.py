"""JavaScript sandbox execution runner."""

from backend.app.sandbox.config import SandboxConfig
from backend.app.sandbox.languages.base import BaseLanguageRunner, LanguageExecutionPlan


class JavaScriptRunner(BaseLanguageRunner):
    """Executes JavaScript code inside an isolated Node.js container."""

    @property
    def language(self) -> str:
        return "javascript"

    def build_plan(self, code: str, config: SandboxConfig) -> LanguageExecutionPlan:
        image = config.image_tags.get("javascript", "bhasha2code-sandbox-javascript:1.0.0")
        return LanguageExecutionPlan(
            language=self.language,
            image_tag=image,
            files={"main.js": code},
            entrypoint=["node", "main.js"],
        )

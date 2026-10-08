"""Java sandbox execution runner."""

import re
from backend.app.sandbox.config import SandboxConfig
from backend.app.sandbox.languages.base import BaseLanguageRunner, LanguageExecutionPlan


class JavaRunner(BaseLanguageRunner):
    """Compiles and executes Java code entirely inside an isolated container."""

    @property
    def language(self) -> str:
        return "java"

    def _extract_class_name(self, code: str) -> str:
        """Extract public or primary class name from Java code."""
        # Check for public class
        pub_match = re.search(r"public\s+class\s+([A-Za-z0-9_$]+)", code)
        if pub_match:
            return pub_match.group(1)

        # Fallback to any class
        any_match = re.search(r"class\s+([A-Za-z0-9_$]+)", code)
        if any_match:
            return any_match.group(1)

        return "Main"

    def build_plan(self, code: str, config: SandboxConfig) -> LanguageExecutionPlan:
        image = config.image_tags.get("java", "bhasha2code-sandbox-java:1.0.0")
        classname = self._extract_class_name(code)
        filename = f"{classname}.java"

        return LanguageExecutionPlan(
            language=self.language,
            image_tag=image,
            files={filename: code},
            entrypoint=["sh", "-c", f"javac {filename} && java {classname}"],
        )

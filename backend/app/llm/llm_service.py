"""LLM Service connecting Prompt Builder output to local Ollama inference."""

import logging
from typing import Any, Dict, List, Optional

from backend.app.llm.config import OllamaSettings, get_ollama_settings
from backend.app.llm.exceptions import OllamaModelNotFoundError
from backend.app.llm.ollama_client import OllamaClient
from backend.app.llm.schemas import HealthStatus, LLMResponse, ModelInfo
from backend.app.prompt.schemas import PromptSpecification

logger = logging.getLogger(__name__)


class LLMService:
    """Service layer coordinating PromptSpecification execution on local Ollama."""

    def __init__(
        self,
        client: Optional[OllamaClient] = None,
        settings: Optional[OllamaSettings] = None,
    ) -> None:
        self.settings = settings or get_ollama_settings()
        self.client = client or OllamaClient(settings=self.settings)

    def health_check(self, raise_for_status: bool = True) -> HealthStatus:
        """Verify Ollama reachability."""
        return self.client.health_check(raise_for_status=raise_for_status)

    def is_available(self) -> bool:
        """Check if Ollama service is reachable."""
        return self.client.is_available()

    def list_models(self) -> List[ModelInfo]:
        """List models installed on the local Ollama instance."""
        return self.client.list_models()

    def is_model_available(self, model_name: str) -> bool:
        """Verify if a specific model exists locally."""
        return self.client.is_model_available(model_name=model_name)

    def generate(
        self,
        prompt_specification: PromptSpecification,
        model: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        check_model_availability: bool = True,
    ) -> LLMResponse:
        """Generate response from local LLM using a structured PromptSpecification.

        Args:
            prompt_specification: T16 PromptSpecification with rendered prompt & policies.
            model: Optional model override (defaults to configured settings.model).
            options: Additional hyperparameters (temperature, num_ctx, etc.).
            check_model_availability: Whether to verify model existence before sending request.

        Returns:
            LLMResponse containing response text, token counts, and durations.

        Raises:
            OllamaUnavailableError: If Ollama daemon is unreachable.
            OllamaModelNotFoundError: If the configured model is not installed.
            OllamaTimeoutError: If execution exceeds configured timeout.
            OllamaGenerationError: If generation fails or yields empty output.
        """
        target_model = model or self.settings.model

        # 1. Verify model availability if requested
        if check_model_availability:
            if not self.client.is_model_available(target_model):
                logger.error("Configured model '%s' not found in local Ollama installation.", target_model)
                raise OllamaModelNotFoundError(model_name=target_model)

        # 2. Render deterministic prompt
        rendered_prompt = prompt_specification.render()

        # 3. Invoke local model via transport client
        response = self.client.generate(
            prompt=rendered_prompt,
            model=target_model,
            options=options,
        )

        return response

    def generate_text(
        self,
        prompt: str,
        model: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        check_model_availability: bool = True,
    ) -> LLMResponse:
        """Direct text generation for smoke testing and raw prompts."""
        target_model = model or self.settings.model

        if check_model_availability:
            if not self.client.is_model_available(target_model):
                raise OllamaModelNotFoundError(model_name=target_model)

        return self.client.generate(
            prompt=prompt,
            model=target_model,
            options=options,
        )

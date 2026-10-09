"""LLM Service connecting Prompt Builder output to local Ollama inference."""

import logging
from typing import Any, AsyncIterator, Dict, List, Optional

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

    def resolve_generation_options(
        self,
        prompt_specification: Optional[PromptSpecification] = None,
        override_options: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """Compute dynamic generation options based on T23 token policy and prompt context."""
        opts = self.settings.get_generation_options()

        if prompt_specification is not None:
            num_predict = 384  # NORMAL default
            meta = prompt_specification.metadata or {}
            tone = (meta.get("detected_tone") or "").upper()
            constraints = prompt_specification.explicit_constraints or []
            is_study = prompt_specification.study_mode

            if is_study:
                num_predict = 768
            elif any("ONLY raw executable code" in c or "extremely brief" in c for c in constraints) or tone == "SHORT":
                num_predict = 192
            elif any("detailed" in c or "algorithm" in c or "flowchart" in c or "viva" in c for c in constraints) or tone == "DETAILED":
                num_predict = 768
            else:
                num_predict = 384

            # Dynamic context window: short standalone requests use smaller footprint
            is_follow_up = meta.get("is_follow_up", False)
            if not is_follow_up and len(prompt_specification.context_text) < 1500:
                opts["num_ctx"] = 2048
            else:
                opts["num_ctx"] = min(self.settings.num_ctx, 4096)

            opts["num_predict"] = num_predict

        if override_options:
            opts.update(override_options)

        return opts

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

        # 3. Dynamic options
        resolved_opts = self.resolve_generation_options(prompt_specification, options)

        # 4. Invoke local model via transport client
        response = self.client.generate(
            prompt=rendered_prompt,
            model=target_model,
            options=resolved_opts,
        )

        return response

    async def generate_stream(
        self,
        prompt_specification: PromptSpecification,
        model: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
        check_model_availability: bool = True,
    ) -> AsyncIterator[Dict[str, Any]]:
        """Stream tokens from local LLM using a structured PromptSpecification.

        Yields dicts matching OllamaClient.generate_stream() protocol:
            {"done": False, "token": str}
            {"done": True, "token": str, "total_duration_ms": float, ...}

        Args:
            prompt_specification: T16 PromptSpecification with rendered prompt & policies.
            model: Optional model override.
            options: Additional hyperparameters.
            check_model_availability: Whether to verify model existence first.
        """
        target_model = model or self.settings.model

        if check_model_availability:
            if not self.client.is_model_available(target_model):
                logger.error("Streaming: model '%s' not found in Ollama.", target_model)
                raise OllamaModelNotFoundError(model_name=target_model)

        rendered_prompt = prompt_specification.render()
        resolved_opts = self.resolve_generation_options(prompt_specification, options)

        async for chunk in self.client.generate_stream(
            prompt=rendered_prompt,
            model=target_model,
            options=resolved_opts,
        ):
            yield chunk

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

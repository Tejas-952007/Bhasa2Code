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
        """Compute dynamic generation options based on request type, local CPU budget, and prompt context."""
        opts = self.settings.get_generation_options()

        if prompt_specification is not None:
            meta = prompt_specification.metadata or {}
            tone = (meta.get("detected_tone") or prompt_specification.tone_instruction or "").upper()
            intent = (meta.get("detected_intent") or prompt_specification.intent_instruction or "").upper()
            constraints = prompt_specification.explicit_constraints or []
            is_study = prompt_specification.study_mode

            is_code_intent = intent in (
                "GENERATE_CODE",
                "DEBUG_CODE",
                "MODIFY_CODE",
                "CONVERT_CODE",
                "OPTIMIZE_CODE",
                "TEST_CASE_GENERATION",
            ) or any("Code" in s for s in (prompt_specification.response_sections or []))

            # Request-type-specific token budgets scaled for local CPU inference (~7-16 tokens/sec)
            is_explicit_code = any("ONLY" in c or "CONTINUATION TASK" in c for c in constraints)
            if is_explicit_code:
                if any("CONTINUATION TASK" in c for c in constraints):
                    num_predict = 512
                elif any("simple test cases" in c for c in constraints):
                    num_predict = 448
                elif any("ONLY raw executable code" in c for c in constraints):
                    num_predict = 512
                else:
                    num_predict = 512
            # 1. Study Mode: 8 structured sections (Problem, Algo, Flowchart, Code, Viva, etc.)
            elif is_study:
                num_predict = 1024
            # 2. Detailed explanation requests or explicit algorithm/flowchart/viva constraints
            elif any("detailed" in c or "algorithm" in c or "flowchart" in c or "viva" in c for c in constraints) or tone == "DETAILED":
                num_predict = 768
            # 3. Code debugging / modification / conversion / optimization (full replacement program + fix explanation)
            elif intent in ("DEBUG_CODE", "MODIFY_CODE", "CONVERT_CODE", "OPTIMIZE_CODE"):
                num_predict = 640
            # 4. Full program code generation (complete executable program with runnable entry point)
            elif intent == "GENERATE_CODE":
                num_predict = 600
            # 5. Short code / snippets / tests
            elif intent == "TEST_CASE_GENERATION":
                num_predict = 448
            # 6. Explanations, code review, errors, concepts, best practices
            elif intent in (
                "EXPLAIN_CODE",
                "CODE_REVIEW",
                "ERROR_EXPLANATION",
                "BEST_PRACTICE",
                "APPROACH_SUGGESTION",
                "ARCHITECTURE_SUGGESTION",
                "FEATURE_SUGGESTION",
                "PERFORMANCE_ANALYSIS",
            ):
                num_predict = 384
            # 7. Simple questions, concepts, search, or concise tone
            elif intent in ("CONCEPT", "SEARCH") or tone == "SHORT" or any("extremely brief" in c for c in constraints):
                num_predict = 256 if is_code_intent else 192
            else:
                num_predict = 512 if is_code_intent else 384

            # If user explicitly configured OLLAMA_NUM_PREDICT in environment, only override for unconstrained requests
            if not is_explicit_code:
                import os
                env_predict = os.getenv("OLLAMA_NUM_PREDICT")
                if env_predict is not None and env_predict.strip():
                    try:
                        configured_val = int(env_predict)
                        if configured_val >= 0:
                            num_predict = configured_val
                    except ValueError:
                        pass

            opts["num_predict"] = num_predict

            # Dynamic context window: short standalone requests use smaller footprint to reduce TTFT on CPU
            is_follow_up = meta.get("is_follow_up", False)
            if not is_follow_up and len(prompt_specification.context_text) < 1500:
                opts["num_ctx"] = 2048
            else:
                opts["num_ctx"] = min(self.settings.num_ctx, 4096)

        if override_options:
            opts.update(override_options)

        logger.info(
            "Selected generation options: num_predict=%s num_ctx=%s temp=%.2f",
            opts.get("num_predict"),
            opts.get("num_ctx"),
            opts.get("temperature", 0.0),
        )
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

        # Safe logging of generation constraints without logging user prompt
        logger.info(
            "Generating LLM response: model=%s ml_policy=%s",
            target_model,
            prompt_specification.get_ml_policy_summary(),
        )

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

        logger.info(
            "Streaming LLM response: model=%s ml_policy=%s",
            target_model,
            prompt_specification.get_ml_policy_summary(),
        )

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

"""Transport client for local Ollama HTTP API."""

import logging
from typing import Any, Dict, List, Optional
import httpx

from backend.app.llm.config import OllamaSettings, get_ollama_settings
from backend.app.llm.exceptions import (
    OllamaGenerationError,
    OllamaModelNotFoundError,
    OllamaTimeoutError,
    OllamaUnavailableError,
)
from backend.app.llm.schemas import GenerationOptions, HealthStatus, LLMResponse, ModelInfo

logger = logging.getLogger(__name__)


class OllamaClient:
    """Isolated HTTP client for the local Ollama service."""

    def __init__(
        self,
        settings: Optional[OllamaSettings] = None,
        http_client: Optional[httpx.Client] = None,
    ) -> None:
        self.settings = settings or get_ollama_settings()
        self._custom_client = http_client is not None
        self._client = http_client or httpx.Client(
            base_url=self.settings.base_url,
            timeout=self.settings.timeout_seconds,
        )

    def close(self) -> None:
        """Close the underlying HTTP client if not externally provided."""
        if not self._custom_client:
            self._client.close()

    def __enter__(self) -> "OllamaClient":
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self.close()

    def health_check(self, raise_for_status: bool = True) -> HealthStatus:
        """Check if local Ollama daemon is reachable and responding.

        Args:
            raise_for_status: If True, raises OllamaUnavailableError on failure.

        Returns:
            HealthStatus model.
        """
        try:
            resp = self._client.get("/api/version")
            if resp.status_code == 200:
                data = resp.json()
                version = data.get("version")
                # Count installed models if possible
                models_count = None
                try:
                    tags_resp = self._client.get("/api/tags")
                    if tags_resp.status_code == 200:
                        models_count = len(tags_resp.json().get("models", []))
                except Exception:
                    pass

                return HealthStatus(
                    status="ok",
                    available=True,
                    version=version,
                    models_count=models_count,
                )
            else:
                if raise_for_status:
                    raise OllamaUnavailableError(
                        f"Ollama returned HTTP {resp.status_code} during health check."
                    )
                return HealthStatus(status="error", available=False)
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.NetworkError) as exc:
            if raise_for_status:
                raise OllamaUnavailableError(
                    "Local AI service unavailable. Please start Ollama and verify the configured model.",
                    cause=exc,
                ) from exc
            return HealthStatus(status="unavailable", available=False)
        except httpx.TimeoutException as exc:
            if raise_for_status:
                raise OllamaTimeoutError(
                    timeout_seconds=self.settings.timeout_seconds,
                    message="Ollama health check timed out.",
                    cause=exc,
                ) from exc
            return HealthStatus(status="timeout", available=False)
        except Exception as exc:
            if raise_for_status:
                raise OllamaUnavailableError(
                    f"Unexpected error while checking Ollama health: {exc}",
                    cause=exc,
                ) from exc
            return HealthStatus(status="error", available=False)

    def is_available(self) -> bool:
        """Check reachability without raising exceptions."""
        status = self.health_check(raise_for_status=False)
        return status.available

    def list_models(self) -> List[ModelInfo]:
        """Fetch list of all models locally installed in Ollama.

        Returns:
            List of ModelInfo objects.

        Raises:
            OllamaUnavailableError: If Ollama is unreachable.
            OllamaTimeoutError: If the request times out.
            OllamaGenerationError: If the server returns an unexpected error.
        """
        try:
            resp = self._client.get("/api/tags")
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.NetworkError) as exc:
            raise OllamaUnavailableError(cause=exc) from exc
        except httpx.TimeoutException as exc:
            raise OllamaTimeoutError(
                timeout_seconds=self.settings.timeout_seconds,
                cause=exc,
            ) from exc
        except Exception as exc:
            raise OllamaUnavailableError(
                f"Failed to query Ollama model list: {exc}", cause=exc
            ) from exc

        if resp.status_code != 200:
            raise OllamaGenerationError(
                f"Failed to list Ollama models. Server returned HTTP {resp.status_code}: {resp.text}",
                status_code=resp.status_code,
            )

        try:
            payload = resp.json()
        except Exception as exc:
            raise OllamaGenerationError(
                "Malformed JSON response while listing Ollama models.",
                cause=exc,
            ) from exc

        models_raw = payload.get("models", [])
        return [ModelInfo.from_api_dict(item) for item in models_raw]

    def is_model_available(self, model_name: str) -> bool:
        """Check if a specific model exists locally in Ollama.

        Matches exact name, tag-normalized name, or :latest fallback.
        """
        target = model_name.strip()
        models = self.list_models()
        installed_names = {m.name for m in models}
        installed_models = {m.model for m in models if m.model}

        if target in installed_names or target in installed_models:
            return True

        # If model requested without tag, try appending :latest
        if ":" not in target:
            latest_variant = f"{target}:latest"
            if latest_variant in installed_names or latest_variant in installed_models:
                return True
            # Also check if any installed model starts with f"{target}:"
            for name in installed_names:
                if name.startswith(f"{target}:"):
                    return True

        return False

    def generate(
        self,
        prompt: str,
        model: Optional[str] = None,
        system: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None,
    ) -> LLMResponse:
        """Execute synchronous completion request on Ollama /api/generate.

        Args:
            prompt: Text prompt to generate from.
            model: Model name override (defaults to settings.model).
            system: Optional system instruction text.
            options: Additional hyperparameters (temperature, num_ctx, etc.).

        Returns:
            LLMResponse containing generated text and execution metadata.

        Raises:
            ValueError: If prompt is empty.
            OllamaUnavailableError: If Ollama daemon is unreachable.
            OllamaModelNotFoundError: If requested model is not installed.
            OllamaTimeoutError: If generation exceeds timeout threshold.
            OllamaGenerationError: If generation returns empty or error.
        """
        if not prompt or not prompt.strip():
            raise ValueError("Prompt cannot be empty.")

        target_model = model or self.settings.model
        generation_options = self.settings.get_generation_options()
        if options:
            generation_options.update(options)

        payload: Dict[str, Any] = {
            "model": target_model,
            "prompt": prompt,
            "stream": False,
            "options": generation_options,
        }
        if system:
            payload["system"] = system

        if self.settings.debug_logging:
            logger.debug(
                "Ollama request payload: model=%s options=%s prompt_len=%d",
                target_model,
                generation_options,
                len(prompt),
            )

        try:
            resp = self._client.post("/api/generate", json=payload)
        except (httpx.ConnectError, httpx.ConnectTimeout, httpx.NetworkError) as exc:
            raise OllamaUnavailableError(cause=exc) from exc
        except httpx.TimeoutException as exc:
            raise OllamaTimeoutError(
                timeout_seconds=self.settings.timeout_seconds,
                cause=exc,
            ) from exc
        except Exception as exc:
            raise OllamaGenerationError(
                f"Unexpected transport failure calling Ollama generate: {exc}",
                cause=exc,
            ) from exc

        # Handle HTTP status codes
        if resp.status_code == 404:
            raise OllamaModelNotFoundError(model_name=target_model)
        elif resp.status_code != 200:
            raise OllamaGenerationError(
                f"Ollama returned HTTP {resp.status_code}: {resp.text}",
                status_code=resp.status_code,
            )

        try:
            data = resp.json()
        except Exception as exc:
            raise OllamaGenerationError(
                "Malformed JSON response received from Ollama generate.",
                cause=exc,
            ) from exc

        generated_text = data.get("response", "")
        if not generated_text or not generated_text.strip():
            raise OllamaGenerationError("Ollama returned an empty response.")

        # Convert nanoseconds to milliseconds
        total_duration_ns = data.get("total_duration")
        total_duration_ms = (
            float(total_duration_ns) / 1_000_000.0 if total_duration_ns is not None else None
        )

        prompt_tokens = data.get("prompt_eval_count")
        completion_tokens = data.get("eval_count")
        done = data.get("done", True)

        logger.info(
            "Ollama generation succeeded: model=%s duration_ms=%.1f prompt_tokens=%s completion_tokens=%s",
            target_model,
            total_duration_ms or 0.0,
            prompt_tokens,
            completion_tokens,
        )

        return LLMResponse(
            text=generated_text.strip(),
            model=data.get("model", target_model),
            total_duration_ms=total_duration_ms,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            done=done,
            raw_metadata={
                "load_duration_ns": data.get("load_duration"),
                "prompt_eval_duration_ns": data.get("prompt_eval_duration"),
                "eval_duration_ns": data.get("eval_duration"),
            },
        )

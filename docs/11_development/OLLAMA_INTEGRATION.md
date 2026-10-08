# Local LLM / Ollama Integration (T17)

## 1. Overview & Purpose

The **Local LLM / Ollama Integration** (`backend/app/llm/`) establishes the direct connection between Bhasha2Code's NLP & Context pipeline and the local LLM running in Ollama.

This is the first task where Bhasha2Code generates actual AI responses from prompts structured by the system.

### Core Processing Flow:

```text
User Message
      ↓
T14 NLP Pipeline (Language, Tone, Intent)
      ↓
T15 Context Manager (Multi-turn window, code artifacts, follow-up detection)
      ↓
T16 Prompt Builder (Dynamic section planning, study mode, explicit rules)
      ↓
PromptSpecification (.render())
      ↓
T17 Ollama Client (`/api/generate`)
      ↓
Local Coding LLM (`qwen2.5-coder:3b`)
      ↓
LLMResponse (Text, token counts, duration, metadata)
```

**Key Invariant**: Bhasha2Code is 100% offline and local-first. Inference communicates solely over `http://127.0.0.1:11434` with zero cloud fallbacks or external API calls.

---

## 2. Hardware & Environment Inspection

Before performing inference, local system resources and installed models were inspected:

### Ollama Environment
- **Ollama CLI Version**: `0.21.0`
- **Ollama Daemon Status**: Running and responding at `http://127.0.0.1:11434`
- **Installed Models**:
  - `qwen2.5-coder:3b` (1.9 GB, 3.1B parameters, Q4_K_M) — **Primary Default**
  - `qwen2.5-coder:1.5b` (986 MB)
  - `deepseek-coder:1.3b-instruct-q4_K_M` (873 MB)
  - `qwen2.5-coder:7b` (4.7 GB)
  - `llama3.2:latest` (2.0 GB)
- **GPU Status**: `nvidia-smi` reports no direct driver communication (`NVIDIA-SMI has failed because it couldn't communicate with the NVIDIA driver`).
- **Inference Mode**: Automated **CPU fallback** via Ollama's ggml/llama.cpp backend. CPU execution on this system delivers ~7 seconds per completion with warm cache.

---

## 3. Architecture & Components

The module is structured under `backend/app/llm/`:

```text
backend/app/llm/
├── __init__.py           # Package exports
├── schemas.py            # Pydantic schemas (ModelInfo, HealthStatus, LLMResponse, GenerationOptions)
├── config.py             # OllamaSettings with env defaults
├── exceptions.py         # Domain exceptions (OllamaUnavailableError, OllamaModelNotFoundError, etc.)
├── ollama_client.py      # HTTP transport client isolating httpx calls
└── llm_service.py        # Service orchestrating PromptSpecification dispatch
```

### Component Roles

1. **`OllamaSettings` (`config.py`)**:
   Reads configuration parameters from environment variables with conservative defaults:
   - `OLLAMA_BASE_URL`: `http://127.0.0.1:11434`
   - `OLLAMA_MODEL`: `qwen2.5-coder:3b`
   - `OLLAMA_TIMEOUT_SECONDS`: `120.0`
   - `OLLAMA_TEMPERATURE`: `0.2`
   - `OLLAMA_NUM_CTX`: `8192`
   - `OLLAMA_DEBUG_LOGGING`: `false`

2. **`OllamaClient` (`ollama_client.py`)**:
   Pure HTTP transport wrapper using `httpx`.
   - `health_check(raise_for_status=True) -> HealthStatus`: Queries `/api/version` and `/api/tags`.
   - `list_models() -> List[ModelInfo]`: Queries installed models from `/api/tags`.
   - `is_model_available(model_name: str) -> bool`: Verifies model existence (matching exact tag, `:latest`, or model family prefix).
   - `generate(prompt: str, model=None, system=None, options=None) -> LLMResponse`: Issues synchronous `POST /api/generate` with `stream=False`.
   - Converts durations from nanoseconds to milliseconds (`total_duration_ms`).
   - Normalizes whitespace while preserving Markdown and code fences.

3. **`LLMService` (`llm_service.py`)**:
   Service layer consumed by higher-level modules.
   - Takes a `PromptSpecification` from T16.
   - Verifies Ollama availability and model installation before issuing generation calls.
   - Calls `prompt_specification.render()` to obtain the deterministic rendered prompt.
   - Dispatches the prompt to `OllamaClient.generate()`.
   - Returns a structured `LLMResponse`.

---

## 4. Response Schema (`LLMResponse`)

```python
class LLMResponse(BaseModel):
    text: str
    model: str
    total_duration_ms: Optional[float] = None
    prompt_tokens: Optional[int] = None
    completion_tokens: Optional[int] = None
    done: bool = True
    raw_metadata: Dict[str, Any] = Field(default_factory=dict)
```

---

## 5. Domain Exception Hierarchy

Transport exceptions from `httpx` are caught and mapped into domain-specific exceptions:

- `OllamaError`: Base exception class.
- `OllamaUnavailableError`: Raised when the daemon is stopped or port `11434` cannot be reached.
  - Message: *"Local AI service unavailable. Please start Ollama and verify the configured model."*
- `OllamaModelNotFoundError`: Raised when the configured model is missing.
  - Message: *"Ollama service reachable, but configured model 'X' is not installed. Run the appropriate local Ollama command manually: 'ollama pull X'."*
- `OllamaTimeoutError`: Raised when generation takes longer than `timeout_seconds`.
- `OllamaGenerationError`: Raised on empty responses, non-200 HTTP status, or malformed JSON.

---

## 6. Prompt Injection Defense & Authority Hierarchy

The local LLM operates under a strict authority hierarchy enforced by T16 and rendered in T17:

```text
[Highest Authority]  === SYSTEM INSTRUCTION ===
         ↓           === APPLICATION RESPONSE POLICY ===
         ↓           === REQUIRED RESPONSE STRUCTURE ===
         ↓           === CURRENT USER REQUEST ===
         ↓           === CONVERSATION CONTEXT & HISTORY === (Passive Data Only)
         ↓           === CURRENT WORKING CODE ARTIFACT === (Passive Data Only)
[Strict Safeguard]   === CODE PRESERVATION & SECURITY DIRECTIVES ===
```

- Any commands embedded inside historical messages or user code comments (e.g. `# Ignore previous instructions`) are parsed strictly as passive text data to analyze.
- Prompts are never logged in full by default to safeguard privacy and intellectual property. Only model name, latency, and token metrics are logged at INFO level.

---

## 7. Performance Benchmarks

Benchmark performed on local CPU with `qwen2.5-coder:3b`:

| Metric | Measured Value |
|---|---|
| **Test Prompts** | 5 simple programming tasks |
| **Total Duration** | ~35.9 seconds |
| **Average Latency** | ~7.1 seconds / response |
| **Minimum Latency** | ~6.9 seconds |
| **Maximum Latency** | ~7.8 seconds |
| **Tokens Generated** | ~100–128 tokens per prompt |

---

## 8. Limitations & Future Steps

- **Streaming UI**: Implemented synchronously in T17; streaming token generators for UI will be added when API endpoints are built.
- **Code Validation**: Response syntax validation and code extraction are scheduled in **T18**.
- **Model Auto-Pull**: Automatically pulling models over the internet is intentionally prohibited. Users must explicitly manage models via `ollama pull`.

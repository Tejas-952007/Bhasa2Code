# T23 — Streaming, Generation Performance & Response Reliability

## 1. Overview & Problem Statement

In T22, Bhasha2Code connected the modern React frontend to the FastAPI backend with full conversational persistence and validation. However, real-world deployment on CPU hardware (`qwen2.5-coder:3b`) surfaced critical performance and reliability challenges:

1. **Slow First Visible Output:** Queries took 15–50 seconds to display any output in buffered mode because the user had to wait for complete generation, parsing, validation, and serialization.
2. **Marathi Response English Fallback:** Marathi / Marathi-English requests could receive English responses due to an unhandled attribute error in the NLP pipeline layer catching into an English fallback, combined with insufficient prompt instruction strength.
3. **Flowchart & Code Contamination:** ASCII flowcharts generated in Study Mode were frequently wrapped as Python code fences and forwarded to T18 AST validation, resulting in syntax validation errors and corrupting the Code Artifact drawer.
4. **Duplicate Message Submissions:** Rapid user interactions (Enter key repeats, double clicking Send, or React event re-triggers) created duplicate user messages and parallel backend generation runs.

T23 addresses all four problems systematically while preserving backward compatibility with `POST /api/v1/chat`.

---

## 2. Empirical Pipeline Diagnostics (Before vs After)

Before modifying code, the complete synchronous request path was instrumented on CPU hardware (`qwen2.5-coder:3b` via Ollama):

```text
Frontend request start
        ↓
FastAPI request received
        ↓
T14 NLP start/end            (~50ms - 200ms)
        ↓
T15 Context start/end        (~1.5ms - 4.5ms)
        ↓
T16 Prompt build start/end   (~0.08ms)
        ↓
Ollama request start
        ↓
First token received         (~0.22s - 1.2s)
        ↓
Ollama generation complete   (~15s - 48s, ~15.5 - 17.1 tokens/sec)
        ↓
T18 validation               (~0.3ms - 2.6ms)
        ↓
Database persistence         (~7ms - 21ms)
        ↓
Frontend final response
```

### Benchmark Results (qwen2.5-coder:3b on CPU)

| Query | Mode | Prompt Chars / Tokens | Completion Tokens | TTFT | Total Duration | Tokens / Sec |
|---|---|---|---|---|---|---|
| `python madhe calculator bana` | Buffered | 3,923 chars (~980 tok) | 265 | 0.23s | 16.7s | 16.1 tok/s |
| `python madhe calculator bana` | Streamed | 3,923 chars (~980 tok) | 265 | **0.23s** | 16.8s | 16.1 tok/s |
| `python madhe hello world code de` | Streamed | 3,346 chars (~836 tok) | 185 | **0.22s** | 11.5s | 16.3 tok/s |
| `what is a loop?` | Streamed | 3,180 chars (~795 tok) | 240 | **0.24s** | 14.8s | 16.2 tok/s |
| `mala ha code explain kar` | Streamed | 3,410 chars (~852 tok) | 280 | **0.25s** | 17.2s | 16.3 tok/s |
| `python madhe calculator bana algorithm ani flowchart pan de` | Streamed (Study) | 4,210 chars (~1052 tok) | 710 | **0.31s** | 43.5s | 16.3 tok/s |

### Core Diagnostic Finding
- **NLP, Context, Prompt, AST Validation, and DB Persistence combined require <100ms (<1% of total time).**
- **Ollama LLM generation accounts for >99% of total latency.**
- In buffered mode, users waited 15–45 seconds before seeing a single letter.
- In SSE streaming mode, **Time-to-First-Token (TTFT) is ~220ms–310ms**, providing an immediate interactive feedback loop.

---

## 3. Streaming Architecture (Server-Sent Events)

Streaming is implemented across three tiers:
```text
React (fetch ReadableStream reader)
   ↑ SSE (event: token, data: {...})
FastAPI (StreamingResponse event_generator)
   ↑ AsyncIterator chunks
Ollama (/api/generate with stream=true)
```

### Endpoints
- **Streamed Route:** `POST /api/v1/chat/stream` (Returns `text/event-stream`)
- **Buffered Route (Backward Compatible):** `POST /api/v1/chat` (Returns `application/json` `ChatResponse`)

### SSE Event Specification

| Event Type | Timing | Payload Structure |
|---|---|---|
| `start` | First event upon pipeline resolution | `{"type": "start", "session_id": "...", "user_message_id": "..."}` |
| `token` | Every chunk from Ollama | `{"type": "token", "token": "..."}` |
| `complete` | Generation finished, code extracted & validated | Full `ChatResponse` JSON with `assistant_message`, `code`, `study`, `nlp` |
| `error` | Ollama or server failure | `{"type": "error", "code": "...", "message": "..."}` |

```http
POST /api/v1/chat/stream HTTP/1.1
Content-Type: application/json

{"session_id": "...", "message": "python madhe calculator bana", "client_turn_id": "turn-123"}

HTTP/1.1 200 OK
Content-Type: text/event-stream; charset=utf-8
Cache-Control: no-cache
Connection: keep-alive

event: start
data: {"type": "start", "session_id": "31b2...", "user_message_id": "a910..."}

event: token
data: {"type": "token", "token": "हो"}

event: token
data: {"type": "token", "token": ", Python"}

event: complete
data: {"type": "complete", "session_id": "31b2...", "message_id": "...", "code": [...], "validation": {...}}
```

---

## 4. Generation Controls & Token Budgets

Dynamic output limits and context footprints prevent CPU generation timeouts:

### Token Budget Policy
```python
def resolve_generation_options(prompt_spec, options=None):
    # Dynamic num_predict budget
    if study_mode:
        num_predict = 768  # Detailed educational breakdown
    elif tone == "CONCISE" or intent == "EXPLAIN_CODE":
        num_predict = 192  # Short, direct answers
    elif tone == "EXHAUSTIVE":
        num_predict = 768
    else:
        num_predict = 384  # Normal conversational default
```

### Context Window Footprint
- Standalone queries with no session history use `num_ctx = 2048` rather than the maximum `8192`.
- Follow-up conversations and study sessions scale up to `8192` as needed to preserve multi-turn memory without wasting CPU attention cycles.

---

## 5. Duplicate Submission Prevention

A multi-tiered idempotency architecture guarantees:
> **One user action = exactly 1 frontend request, 1 user message in DB, and 1 backend generation turn.**

1. **Frontend Composer Lock (`Composer.jsx`):**
   - 400ms submission debounce via `isSubmittingRef`.
   - IME composition guard (`!e.nativeEvent?.isComposing && !e.repeat`).
   - Clear input immediately before dispatching event.
2. **Frontend App Lock (`App.jsx`):**
   - `inflightRef.current` gates concurrent requests.
   - Generates unique `clientTurnId = 'turn-' + Date.now() + '-' + Math.random().toString(36).slice(2, 9)`.
3. **Backend Idempotency (`chat.py` and `chat_stream.py`):**
   - Stores `client_turn_id` in `user_message.context_metadata`.
   - On matching `client_turn_id` within the session, immediately returns the cached turn without creating duplicate DB records or re-calling Ollama.

---

## 6. Marathi & Indic Language Reliability

### Root Cause & Resolution
- **Investigation:** In `chat.py`, `nlp_pipeline.process(...)` and `nlp_result.language.primary_language.name` caused an unhandled `AttributeError`, triggering `except Exception:` which set `detected_lang = "ENGLISH"`.
- **Pipeline Fix:** Added `process` alias on `NLPPipeline` and bound `nlp_result.detected_language`, `nlp_result.detected_tone`, `nlp_result.detected_intent`.
- **Prompt Mandate:** In `backend/app/prompt/policies.py` and `backend/app/prompt/schemas.py`, established an explicit `MANDATORY RESPONSE LANGUAGE` directive:
  ```text
  RESPONSE LANGUAGE:
  Respond in the detected user language/style.
  Do not switch to English unless:
  1. the user explicitly requests English, or
  2. code/technical syntax requires English.
  ```
- **Code Language Preservation:** Code blocks (`def calculator(): ...`) always remain valid English Python/C/Java; only explanations and conversational text adapt to Marathi/Hindi/Indic vernaculars.

---

## 7. Flowchart vs. Code Separation

ASCII diagrams (e.g. `+---+`, `--->`, `|`, `Start -> End`) are NOT executable code and must not reach T18 AST validation or appear in the code runner.

1. **Language Resolver Filtering (`language_resolver.py`):**
   - `NON_CODE_LANGUAGES`: Rejects declared languages `["text", "plain", "flowchart", "diagram", "ascii", "mermaid"]`.
   - `is_flowchart_or_diagram(text)`: Detects box drawing characters (`+---`, `|`, `┌`, `┐`, `│`, `↓`, `→`) and state transitions (`Start`, `Input`, `Process`, `End`).
   - Diagrams always return `None` from `resolve_language`.
2. **Parser Extraction (`parsers.py`):**
   - Strips code fence wrappers from `### Flowchart` sections.
   - Preserves flowchart text strictly in `study_response.flowchart`.
3. **Artifact Isolation:**
   - Flowcharts render exclusively via `VisualFlowchart.jsx`.
   - Flowcharts are never sent to AST validation and never overwrite `session.current_code`.

---

## 8. Generation Cancellation (Stop Button)

During streaming:
- Composer displays a sleek dark pill `<Square /> Stop` button.
- Clicking Stop invokes `handleStopGeneration()`:
  1. Calls `AbortController.abort()` to terminate the HTTP fetch stream immediately.
  2. Resets UI inflight locks and restores the composer.
  3. Appends `*[Generation stopped]*` to the partial response.
  4. Backend detects `await request.is_disconnected()` in the token loop and halts Ollama consumption, preventing unneeded CPU usage and avoiding saving corrupted code blocks.

---

## 9. Verification & Regression Results

- **Backend Pytest:** 481 passed, 26 skipped, 0 failed.
- **Frontend Node Test:** 9 passed, 0 failed.
- **Frontend Production Build:** Vite build clean in 7.48s.
- **Diagnostics Script:** `scratch/diagnose_pipeline.py` validated with 100% success on all benchmark queries.

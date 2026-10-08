# Bhasha2Code — Context Manager (T15)

## 1. Problem Statement

While the NLP Pipeline (T14) analyzes user intent, conversational tone, and natural language on a per-turn basis, coding assistants operate primarily through multi-turn dialogues. 

Consider the interaction:
```text
Turn 1 (User):      python madhe calculator bana
Turn 2 (Assistant): [Generated calculator code]
Turn 3 (User):      yat error handling add kar
```

The user's message in Turn 3 contains no explicit mention of "calculator" or what code to modify. Without context retention, downstream generation components would fail to identify the target program.

The **Context Manager** solves this problem by answering:
> *"What is the user currently talking about, considering previous conversation context and generated code?"*

The Context Manager retrieves, isolates, filters, and packages relevant conversation turns and code artifacts into a structured `ContextPackage`. It is strictly a context retrieval and packaging engine; it does **not** call LLMs or generate responses.

---

## 2. Architecture & Pipeline Flow

The Context Manager sits cleanly between the NLP Pipeline and the downstream Prompt Builder (T16):

```text
Current User Message
        ↓
T14 NLP Pipeline (PreprocessedText, Language, Tone, Intent)
        ↓
Context Manager (T15)
        ├── Recent Session Messages (Chronological created_at ASC)
        ├── Recent Generated Code Artifacts (Newest first)
        ├── Session Metadata & Current Code
        ├── Follow-Up Detection (is_follow_up Heuristics)
        └── Context Window Policy & Budget Truncation
        ↓
Structured ContextPackage
        ↓
Future Prompt Builder (T16)
        ↓
Local LLM Execution (Ollama)
```

### Module Structure
```text
backend/app/context/
├── __init__.py           # Public exports (ContextManager, ContextPackage, policies, errors)
├── schemas.py            # Pydantic data models (ContextMessage, ContextCode, ContextPackage, etc.)
├── policies.py           # Window budgets (ContextPolicy) and is_follow_up heuristics
├── exceptions.py         # Domain errors (ContextError, SessionNotFoundError, UnauthorizedSessionError)
└── context_manager.py    # Core ContextManager implementation
```

---

## 3. Data Sources & Repository Interactions

The Context Manager reuses existing T07 database repositories without introducing new tables or raw SQL queries:

1. **`SessionRepository`**:
   - `get_by_id(session_id)`: Fetches session entity, validates existence, and verifies strict user ownership.
2. **`MessageRepository`**:
   - `count_by_session(session_id)`: Determines total history depth.
   - `list_by_session(session_id, limit, offset)`: Retrieves the most recent window of turns.
3. **`GeneratedCodeRepository`**:
   - `list_code_by_session(session_id, limit)`: Retrieves recent structured code artifacts generated during the session.
4. **Current Input & NLP Pipeline Result**:
   - Embeds the raw/normalized user message and extracts inline code segments (from Markdown fences or raw stack traces).

---

## 4. Context Selection & Relevance Hierarchy

To maintain high prompt efficiency without overloading token budgets, context selection follows a strict deterministic priority:

| Priority | Element | Description |
|---|---|---|
| **Priority 1** | Current Message & Inline Code | Always preserved; never truncated or modified. |
| **Priority 2** | Most Recent Messages | Preserves the conversational dialogue turns immediately preceding the current turn. |
| **Priority 3** | Recent Generated Code | Active code artifacts associated with previous assistant turns. |
| **Priority 4** | Older Session Messages | Retained only if within configured message and character budgets. |

---

## 5. Follow-Up Detection Heuristic

The detector `is_follow_up(message, nlp_result)` uses deterministic linguistics rules:

1. **Deictic Tokens / Pronouns**:
   - English: `it`, `this`, `that`, `these`, `those`, `same`, `again`, `above`, `previous`
   - Marathi (Latin & Devanagari): `yat`, `tyat`, `hyat`, `ya`, `tya`, `ha`, `he`, `या`, `यात`, `त्यात`, `हा`, `हे`
   - Hindi (Latin & Devanagari): `isko`, `usko`, `isme`, `usme`, `ise`, `use`, `ye`, `wo`, `इसमें`, `इसको`, `इसे`
2. **Modification / Refinement Phrases**:
   - `add error handling`, `make it shorter`, `optimize this`, `what about edge cases?`, `convert it to C++`
   - Native modification roots: `सुधार`, `बदल`, `जोड`, `काढ`, `समजाव`, `हटाओ`, `बदलो`
3. **Exclusion of Standalone Topics**:
   - Creation queries with explicit subjects (`write a python calculator`, `create a rest api using fastapi`, `what is polymorphism?`) return `is_follow_up = False`.
4. **Budget Adaptation**:
   - If `is_follow_up = True`: Allocates full `max_messages` budget (default: 12).
   - If `is_follow_up = False`: Allocates bounded `standalone_max_messages` budget (default: 4) to prevent irrelevant historical context leakage.

---

## 6. Context Window & Truncation Policy

Configurable via `ContextPolicy`:

```python
class ContextPolicy(BaseModel):
    max_messages: int = 12
    max_characters: int = 16000
    max_code_characters: int = 12000
    max_generated_code_items: int = 3
    standalone_max_messages: int = 4
```

### Truncation Guarantees
- Current user message is **never truncated**.
- If total message characters exceed `max_characters`, oldest historical turns are dropped first until the character budget is satisfied.
- If generated code artifacts exceed `max_generated_code_items` or `max_code_characters`, older artifacts are dropped, and individual snippets exceeding budget are truncated cleanly with marker `# ... [truncated to fit context budget] ...`.
- Whenever any message or code artifact is omitted due to budget constraints, `ContextPackage.truncated` is set to `True`.

---

## 7. Security, Privacy & Session Ownership

- **Strict User Isolation**:
  ```python
  session = self.session_repo.get_by_id(session_id)
  if str(session.user_id) != str(user_id):
      raise UnauthorizedSessionError(...)
  ```
  Users cannot access sessions, messages, or code belonging to another user.
- **Privacy in Logs**:
  Debug and informational logs emit only `session_id`, `user_id`, message counts, and status flags. Raw user prompts and source code snippets are **never** logged.

---

## 8. Determinism & Performance

- **Determinism**: Given identical database state and query parameters, repeated executions produce identical `ContextPackage` dictionaries.
- **O(1) Database Efficiency**: Context construction executes in constant time (3 to 4 database queries per turn):
  1. 1 query to fetch & authenticate session.
  2. 1 query to count session messages.
  3. 1 query to retrieve chronological recent messages.
  4. 1 query to retrieve newest generated code artifacts.
- Benchmark: Sub-5ms context construction on local SQLite.

---

## 9. Verification & Test Coverage

Test suite in `tests/unit/context/test_context_manager.py` (21 passing tests):
- `test_is_follow_up_affirmative_cases`: Validates follow-up detection on Marathi, Hindi, and English continuation queries.
- `test_is_follow_up_standalone_cases`: Validates standalone question detection.
- `test_new_session_empty_history`: Verifies valid package creation on zero-message sessions.
- `test_critical_acceptance_calculator_follow_up`: Verifies Turn 1 (calculator request) -> Turn 2 (assistant code) -> Turn 3 (`yat error handling add kar`) links the calculator code.
- `test_session_ownership_isolation`: Verifies cross-user isolation and `UnauthorizedSessionError`.
- `test_chronological_message_ordering`: Verifies `created_at ASC` sequence.
- `test_standalone_query_budget`: Verifies standalone queries pull bounded context.
- `test_current_code_preservation` & `test_traceback_input_preservation`: Verifies extraction of inline code and stack traces.
- `test_truncation_*`: Verifies message drop, char limit enforcement, code limit enforcement, and `truncated=True`.
- `test_context_manager_determinism`: Verifies 100% identical outputs across repeated calls.
- `test_performance_sanity_benchmark`: Verifies latency is well below 50ms.

---

## 10. Limitations & Future Semantic Retrieval

1. **Recency vs. Semantic Relevance**:
   - T15 uses recency-based sliding windows. If a user refers to code from 30 turns ago, a recency-only window with `max_messages=12` will not include it.
2. **Future Enhancements (Post-T16)**:
   - When appropriate, a future task may introduce hybrid retrieval (combining sliding-window recency with BM25 or embedding-based vector search) without altering the `ContextPackage` schema contract.

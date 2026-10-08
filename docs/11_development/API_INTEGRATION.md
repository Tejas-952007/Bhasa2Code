# T21 — Frontend ↔ FastAPI API Integration

## Overview

The Bhasha2Code API Integration (T21) connects the React/Vite frontend workspace (T20) with the offline FastAPI backend and machine learning pipeline (T14–T19). It replaces deterministic frontend mock data with real end-to-end database persistence, multilingual NLP classification, multi-turn conversational context, dynamic prompt construction, local Ollama LLM generation, T18 static code validation, and T19 secure Docker sandbox execution.

---

## Architecture Flow

```text
React / Vite Frontend (http://localhost:5173)
      │
      │ HTTP REST (JSON)
      ▼
FastAPI Server (/api/v1)
      ├── CORS & Error Handling Middleware
      ├── Dependency Injection (DB Session & User Context)
      ▼
Application Service Orchestration
      ├── T14 NLP Pipeline (Preprocessing, Language, Tone, Intent)
      ├── T15 Context Manager (Multi-turn session history & code continuity)
      ├── T16 Prompt Builder (Dynamic section planning & study policies)
      ├── T17 Local Ollama (qwen2.5-coder:3b inference)
      ├── T18 Response Validation (Static AST syntax validation)
      └── T19 Safe Code Sandbox (Gated Docker execution on user 'Run')
      ▼
Database Persistence (SQLite via SQLAlchemy Repositories)
      ├── SessionRepository
      ├── MessageRepository
      └── GeneratedCodeRepository
      ▼
Structured JSON Response
      ▼
Frontend View Model Adapter (api.js)
      ▼
React UI (AssistantMessage, CodeArtifact, VisualFlowchart, StudySections)
```

---

## API Endpoints Reference

All endpoints (except backward-compatible `/health`) are versioned under `/api/v1`.

### 1. Health & Readiness

| Method | Path | Summary | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/health` | Basic health check | Backward-compatible health endpoint returning `{"status": "healthy"}` |
| `GET` | `/api/v1/health` | Comprehensive health check | Returns status of Database, Ollama daemon, active model, and Docker sandbox |

**Example Response (`GET /api/v1/health`):**
```json
{
  "status": "healthy",
  "ollama": "available",
  "model": "qwen2.5-coder:3b",
  "sandbox": "available",
  "database": "available"
}
```

---

### 2. Session Management

| Method | Path | Summary | Description |
| :--- | :--- | :--- | :--- |
| `GET` | `/api/v1/sessions` | List sessions | Retrieves recent user sessions ordered by `updated_at` desc |
| `POST` | `/api/v1/sessions` | Create session | Creates a new active session with optional custom or default title |
| `GET` | `/api/v1/sessions/{session_id}` | Get session details | Retrieves full session conversation history, messages, and code artifacts |
| `PATCH` | `/api/v1/sessions/{session_id}` | Rename session | Updates session title |
| `DELETE` | `/api/v1/sessions/{session_id}` | Delete session | Deletes session and cascades deletion to messages and code artifacts |

**Example Request (`POST /api/v1/sessions`):**
```json
{
  "title": "Python Calculator"
}
```

**Example Response (`GET /api/v1/sessions/{session_id}`):**
```json
{
  "id": "5f4b3451-1f1c-426e-9d8d-023961ddcfd0",
  "title": "python madhe calculator bana",
  "status": "active",
  "created_at": "2026-10-08T18:22:30.216985",
  "updated_at": "2026-10-08T18:23:17.618454",
  "messages": [
    {
      "id": "ad150aaf-c0cd-4c8d-a4b2-03cce73069ed",
      "role": "user",
      "content": "python madhe calculator bana",
      "detected_language": "ENGLISH",
      "intent": "GENERATE_CODE",
      "tone": "CASUAL",
      "code_block": null,
      "study": null,
      "created_at": "2026-10-08T18:22:30.234676"
    },
    {
      "id": "d42ea97d-74b5-4b1f-8f7d-8a3b84525c29",
      "role": "assistant",
      "content": "Here is a Python calculator implementation...",
      "code_block": {
        "id": "9eab5857-866b-46bf-8675-e847c8a1a9b6",
        "language": "python",
        "filename": "solution.py",
        "code": "class MadheCalculator:\n    ...",
        "validationStatus": "VALID"
      },
      "study": null,
      "created_at": "2026-10-08T18:23:17.611627"
    }
  ]
}
```

---

### 3. Chat Generation

| Method | Path | Summary | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/chat` | Send message & generate | Orchestrates T14 NLP, T15 Context, T16 Prompt, T17 Ollama, T18 Validation, and persistence |

**Request Schema:**
```json
{
  "session_id": "optional-session-id",
  "message": "python madhe calculator bana",
  "study_mode": false
}
```

**Response Schema:**
```json
{
  "session_id": "5f4b3451-1f1c-426e-9d8d-023961ddcfd0",
  "message_id": "d42ea97d-74b5-4b1f-8f7d-8a3b84525c29",
  "user_message": {
    "id": "ad150aaf-c0cd-4c8d-a4b2-03cce73069ed",
    "content": "python madhe calculator bana",
    "detected_language": "ENGLISH"
  },
  "assistant_message": {
    "id": "d42ea97d-74b5-4b1f-8f7d-8a3b84525c29",
    "content": "This Python code defines a MadheCalculator class...",
    "explanation": [
      "Modular class mapping arithmetic operators to lambda functions."
    ],
    "example": "calc = MadheCalculator()\nprint(calc.calculate('3 + 5'))"
  },
  "nlp": {
    "language": "MARATHI_ENGLISH",
    "tone": "CASUAL",
    "intent": "GENERATE_CODE"
  },
  "code": [
    {
      "id": "9eab5857-866b-46bf-8675-e847c8a1a9b6",
      "language": "python",
      "filename": "solution.py",
      "content": "class MadheCalculator:\n    ...",
      "validation_status": "VALID"
    }
  ],
  "study": null,
  "execution": null
}
```

---

### 4. Code Validation & Sandbox Execution

| Method | Path | Summary | Description |
| :--- | :--- | :--- | :--- |
| `POST` | `/api/v1/code/validate` | Static syntax check | Invokes T18 Response Validator for AST/syntax validation |
| `POST` | `/api/v1/code/run` | Secure execution | Gates through T18, then executes in isolated Docker sandbox (T19) |

**Code Validation (`POST /api/v1/code/validate`):**
```json
// Request
{
  "language": "python",
  "code": "def add(a, b):\n    return a + b"
}

// Response
{
  "language": "python",
  "status": "VALID",
  "is_valid": true,
  "diagnostics": [],
  "line_count": 2
}
```

**Code Execution (`POST /api/v1/code/run`):**
```json
// Request
{
  "language": "python",
  "code": "print(10 + 20)",
  "stdin": ""
}

// Response
{
  "status": "SUCCESS",
  "stdout": "30\n",
  "stderr": "",
  "exit_code": 0,
  "duration_ms": 252.39,
  "diagnostics": []
}
```

---

## Error Handling & Contract

All errors return a predictable JSON envelope without exposing Python stack traces:

```json
{
  "error": {
    "code": "OLLAMA_UNAVAILABLE",
    "message": "The local model could not respond. Please check Ollama and try again."
  }
}
```

### Stable Error Codes:
- `SESSION_NOT_FOUND` (404): Session ID does not exist.
- `UNAUTHORIZED_SESSION` (403): User lacks permission to access session.
- `OLLAMA_UNAVAILABLE` (503): Local Ollama service is offline or unreachable.
- `OLLAMA_MODEL_NOT_FOUND` (503): Configured model is not installed locally.
- `VALIDATION_FAILED` (400): Static validation gate failed.
- `SANDBOX_ERROR` (500): Docker container execution error.
- `EXECUTION_TIMEOUT` (504): Code execution or generation timed out.
- `BAD_REQUEST` (400): Empty message or invalid payload.
- `INTERNAL_ERROR` (500): Unhandled exception caught by global safety handler.

---

## CORS Security

Local development origins are strictly restricted in `backend/app/core/config.py`:
- `http://localhost:5173`
- `http://127.0.0.1:5173`

Unrestricted wildcard origins (`"*"`) are disallowed.

---

## Frontend Integration (`frontend/src/services/api.js`)

The frontend communicates with FastAPI exclusively through the centralized `api.js` client:

- `health()`: Queries backend availability and model status.
- `listSessions()`: Populates sidebar sessions list on mount.
- `createSession(title)`: Triggers new chat session creation.
- `getSession(id)`: Restores messages and code artifacts on session switch.
- `renameSession(id, title)`: Renames session in SQLite.
- `deleteSession(id)`: Deletes session and clears active state.
- `sendMessage({ sessionId, message, studyMode })`: Sends user query, triggers Ollama generation, and receives validated response.
- `validateCode({ language, code })`: Validates code snippet in editor.
- `runCode({ language, code, stdin })`: Executes code safely in Docker sandbox.
- `adaptBackendMessage(msg)`: Maps database records to UI view model.
- `adaptChatResponse(chatResp)`: Converts chat response payload to UI assistant structure.

---

## Local Development Setup

### 1. Start Ollama
```bash
ollama serve
ollama run qwen2.5-coder:3b
```

### 2. Start FastAPI Backend
```bash
uvicorn backend.app.main:app --reload --host 127.0.0.1 --port 8000
```
Swagger UI available at: `http://127.0.0.1:8000/docs`

### 3. Start React/Vite Frontend
```bash
cd frontend
npm install
npm run dev
```
Workspace available at: `http://localhost:5173`

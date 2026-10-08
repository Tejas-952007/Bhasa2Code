# Response Formatting & Workspace Integration (T22)

## 1. Overview & Purpose

T22 completes the translation of raw structured backend FastAPI responses into a refined, developer-grade coding and study workspace. The implementation establishes a clean presentation architecture that avoids generic AI visual clichés (no purple gradients, neon sparkles, artificial badges, or conversational bubbles) and prioritizes readability, precision, and educational clarity.

```text
FastAPI Response
      ↓
Response Adapter / Normalizer (src/services/api.js)
      ↓
Assistant Response View Model
      ↓
Response Section Renderer (src/components/response/ResponseRenderer.jsx)
      ├── MarkdownContent
      ├── CodeArtifact (Toolbar + Edit + Validate + Run)
      ├── Study Mode Sections (Problem, Algorithm, VisualFlowchart, Viva)
      ├── ValidationDetails (Syntax verification)
      └── ExecutionResult (Terminal Console)
      ↓
User-Facing Developer & Study Workspace
```

---

## 2. Response View Model & Centralized Normalization

Backend-to-UI adaptation is centralized in `frontend/src/services/api.js` via:
- `adaptChatResponse(chatResp)`: Transforms real `/api/v1/chat` payloads into view models.
- `adaptBackendMessage(msg)`: Normalizes persisted message records from `GET /api/v1/sessions/{id}`.

### View Model Contract (`AssistantResponse`)
```typescript
interface AssistantResponse {
  id: string;
  role: 'assistant';
  content: string; // Markdown prose intro
  explanation?: string[];
  example?: string;
  codeBlock?: {
    id: string;
    code: string;
    filename: string;
    language: string;
    validationStatus: 'VALID' | 'INVALID' | 'UNSUPPORTED' | 'NOT_VALIDATED';
    executionStatus?: string | null;
    output?: string | null;
    durationMs?: number;
  };
  study?: {
    problemUnderstanding?: string;
    algorithm?: string[];
    flowchart?: string;
    flowchartNodes?: FlowchartNode[];
    importantPoints?: string[];
    vivaQuestions?: Array<{ question: string; answer: string }>;
  };
  validation?: {
    status: string;
    diagnostics: string[];
    lineCount?: number;
    language: string;
  };
  execution?: {
    status: string;
    stdout: string;
    stderr: string;
    exitCode: number;
    durationMs: number;
    diagnostics: string[];
  };
  suggestions?: string[]; // Max 3-5 subtle follow-up prompts
  changes?: string[];     // Changes breakdown for follow-up code modifications
  isFollowUp?: boolean;
  activeContext?: { filename: string } | null;
}
```

---

## 3. Section Architecture & Logical Order

The application only renders sections explicitly supplied by the backend pipeline or context. It never fabricates sections.

### Normal Generation Sequence:
1. **Introduction / Prose** (`MarkdownContent`)
2. **Follow-Up Changes** (`Changes` section if follow-up update)
3. **Code Artifact** (`CodeArtifact` with filename, language badge, syntax lines, and actions)
4. **Explanation** (Bullet points with inline code formatting)
5. **Example** (Clean sample input/output)
6. **Validation** (Syntax verification badge)
7. **Suggestions** (Max 3-5 chips)

### Study Mode Generation Sequence:
1. **Introduction / Prose**
2. **Problem Understanding** (Core requirement summary)
3. **Algorithm** (Numbered algorithmic sequence)
4. **Algorithm Flowchart** (`VisualFlowchart` supporting interactive Visual Model & Text ASCII Trace)
5. **Code** (Full implementation)
6. **Explanation** (Logic breakdown)
7. **Example / Output** (Execution trace)
8. **Important Points** (Key takeaways, edge cases, language specifics)
9. **Viva Questions & Answers** (Academic/interview preparation)

### Debugging Sequence:
1. **Problem**
2. **Cause**
3. **Fix**
4. **Corrected Code**
5. **Validation & Execution**

---

## 4. Code Artifact & Action Controls

`CodeArtifact` acts as an interactive workspace:
- **Filename & Language**: Top bar clearly declares target file (e.g. `solution.py`, `calculator.py`) and language badge.
- **Line Numbers & Syntax Display**: Monospace code editor with vertical line numbering.
- **Copy**: Smooth clipboard copy with temporary `Copied` label.
- **Inline Edit (`Save` & `Cancel`)**:
  - Clicking `Edit` enters inline drafting mode.
  - While editing, `Save` and `Cancel` buttons appear.
  - Changes are kept in a local draft state until `Save` is intentionally clicked.
- **Validate (`POST /api/v1/code/validate`)**:
  - Calls live T18 static parser without leaving the page.
  - Displays `Validating code...` loading state, followed by `✓ Validated` or `✕ Validation Failed`.
- **Run (`POST /api/v1/code/run`)**:
  - Submits code directly to the real T19 Docker sandbox.
  - Never executes code in the client browser.
  - Opens `ExecutionResult` console showing stdout, duration (`Completed · X ms`), and exit code.

---

## 5. Execution Output & Error Presentation

`ExecutionResult.jsx` implements a clean console terminal:
- **Success**: Output stream with duration (e.g. `Completed · 302 ms`).
- **Runtime Error**: Formats stack trace cleanly without exposing Docker internals.
- **Timeout**: `Execution timed out. The program exceeded the allowed runtime.`
- **Resource Limits**: `Execution stopped. The program exceeded the sandbox resource limit.`
- **Sandbox Offline**: `The code could not be executed safely. Sandbox unavailable: Docker runtime is not accessible.`
- Strictly removed legacy `SANDBOX OUTPUT (DEMO)` badges.

---

## 6. Follow-Up Continuity & Suggestions

When a session enters a follow-up conversation:
- Continuity tag displays: `Using current code: calculator.py`
- Code updates indicate `Updated Code`
- Bulleted `Changes` summary identifies modifications (e.g., input validation, zero division handling)
- 3–5 contextual follow-up suggestion chips are offered (e.g. "Add unit tests", "Format with type annotations", "Explain this code step by step").

---

## 7. Accessibility, Responsive Layout & Performance

- **Semantic HTML**: Semantic `<section>`, `<h4>`, `<ol>`, `<ul>`, and `<pre>` elements.
- **No Color-Only State**: Validation and execution status include icons (`✓`, `✕`, `!`), badges, and descriptive text.
- **Responsive Widths**:
  - Full desktop (1920×1080) to laptop (1440×900, 1366×768) and compact (1024×768).
  - Code blocks and flowchart diagrams support horizontal scrolling without horizontal page blowout.
- **Zero-Dependency Markdown**: `MarkdownContent.jsx` parses markdown headings, lists, inline code, bold, and italic safely without bulky third-party libraries.
- **No Mock Data**: All sessions, messages, validations, and sandbox runs consume real endpoints.

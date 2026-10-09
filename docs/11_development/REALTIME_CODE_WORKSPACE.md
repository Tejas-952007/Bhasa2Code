# T24 — Real-Time Code Validation & Execution UX

## 1. Overview & Purpose

Task T24 unifies Bhasha2Code's code display, inline editing, static syntax validation (T18), and secure containerized execution (T19) into a cohesive, reliable code workspace.

### Core Principles
1. **Source of Truth:** The current editor content is always the sole source of truth for all code actions (Validate, Run, Save, Cancel, Copy).
2. **Revision Synchronization:** The displayed code, validation status badge, inline diagnostics, and execution output are deterministically coupled to the exact source revision they were generated from.
3. **Stale-Result Protection:** Editing code immediately resets the validation status to `NOT_VALIDATED` and marks previous execution output as stale, preventing misleading green success states.
4. **Security Gating:** The browser never executes code directly; all execution requests route through FastAPI and are gated by server-side T18 validation before entering the isolated Docker sandbox (T19).

---

## 2. Architecture & Data Flow

```text
Current Source Revision
         |
         v
Debounced T18 Validation (750ms)
         |
         v
Revision-Matched Diagnostics
         |
         v
Explicit Run Action
         |
         v
Server-Side T18 Gate
         |
         v
T19 Isolated Sandbox
         |
         v
Revision-Matched Execution Result
```

---

## 3. Source Revision Tracking

Every code artifact instance maintains an internal monotonic revision counter (`revisionRef`):

- **Initial Load:** `revision = 1`, `validatedRevision = 1` (if initially valid), `executedRevision = null`.
- **Edit Keystroke:**
  - `revisionRef.current += 1`
  - Validation status immediately transitions to `NOT_VALIDATED`.
  - Any previous `executionResult` is marked `{ ...prev, isStale: true }`.
  - Pending debounce timers are cleared and previous in-flight validation network requests are aborted via `AbortController`.
- **Validation Completion:**
  - Response is accepted only if `requestRevision === revisionRef.current`.
  - If the user continued typing while the request was in flight, the late response is discarded.
- **Execution Completion:**
  - Execution result is flagged `isStale = (runRevision !== revisionRef.current)`.
  - If code changed while the container was running, the output displays a "Previous Revision" warning.

---

## 4. Debounce Policy

- **Delay:** 750 milliseconds after the user stops typing.
- **Keystroke Reset:** Every edit cancels the active timer and reschedules a new one.
- **Explicit Validate:** Clicking the **Validate** button bypasses the debounce delay and validates immediately.
- **Unmount Cleanup:** When switching sessions or unmounting the component, active timers and in-flight fetch requests are cancelled.

---

## 5. State Models

### Validation State Model
- `NOT_VALIDATED`: Content modified; no validation completed for current revision.
- `VALIDATING`: Static analysis request in flight.
- `VALID`: Validator verified syntax correctness.
- `INVALID`: Syntax/compiler errors detected; diagnostics displayed.
- `UNSUPPORTED`: Language unsupported for static analysis.
- `ERROR`: Network or server failure (not confused with syntax error).

### Execution State Model
- `IDLE`: No execution initiated.
- `RUNNING`: Secure container executing code.
- `SUCCESS`: Exit code 0, clean stdout.
- `RUNTIME_ERROR`: Process failed with runtime exception or non-zero exit code.
- `TIMEOUT`: Execution exceeded quota (default 5.0 seconds).
- `RESOURCE_LIMIT`: Memory limit exceeded (default 128 MB).
- `OUTPUT_LIMIT`: Stdout truncated to avoid memory overflow.
- `VALIDATION_FAILED`: Refused execution by server-side T18 gate.
- `UNSUPPORTED`: Sandbox image unavailable for language.
- `SANDBOX_ERROR`: Docker runtime communication failure.

---

## 6. Inline Diagnostics

T18 syntax error strings are parsed deterministically:
```text
[ERROR] expected ':' (line 4, column 12)
       ↓
Line 4, Column 12: expected ':'
```
- Accurate Line and Column indicators rendered with high-contrast pill badges.
- Distinguishes compiler warnings from syntax errors.
- Collapsible diagnostics drawer for compact viewing.

---

## 7. Editor Experience

- **Inline Editing Surface:** Monospace editor with matching line number column.
- **Keyboard Enhancements:**
  - `Tab`: Inserts 4 spaces (preserves cursor position).
  - `Shift + Tab`: Unindents 4 spaces.
  - `Ctrl + Enter` / `Cmd + Enter`: Triggers Run.
  - `Ctrl + S` / `Cmd + S`: Saves draft.
  - `Escape`: Cancels draft.
- **Save / Cancel Semantics:**
  - `Edit`: Creates isolated draft; original source is preserved.
  - `Cancel`: Discards draft changes; restores original code and validation state.
  - `Save`: Commits draft into primary code state, notifies parent via `onCodeChange`, triggers validation.

---

## 8. Standard Input (stdin)

- Compact, collapsible **Program Input (stdin)** drawer toggled via the `stdin` button.
- Allows supplying newline-separated inputs for interactive programs (e.g. `input()` or `scanf()`).
- Sent via `POST /api/v1/code/run` (`stdin` field).

---

## 9. Security Boundaries

1. **Client Isolation:** Code is NEVER executed in the browser (no `eval`, WebAssembly, or Web Workers).
2. **Server-Side Validation Gate:** Backend `run_code()` mandates T18 validation before launching the Docker runner.
3. **Ephemeral Containers:** T19 runs non-root containers with `network_disabled=True`, read-only root filesystems, and strict CPU/memory limits.
4. **Flowchart Exclusion:** ASCII flowcharts and educational diagrams from Study Mode are prevented from reaching code validation or execution.

---

## 10. Performance Measurements

- **Debounce pause-to-request:** ~750ms.
- **T18 Python validation:** 0.3ms – 2.6ms.
- **Docker sandbox execution round-trip:** ~180ms – 230ms for standard Python scripts.
- **UI Responsiveness:** Zero thread blocking; editor remains interactive during sandbox execution.

---

## 11. Known Limitations

- Monolithic multi-file project execution is out of scope; single-file solutions supported.
- GUI libraries (Tkinter, Pygame) and network requests are prohibited by the sandbox environment.

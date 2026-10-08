# Response Validation / Code Validation (T18)

## 1. Overview & Purpose

The **Response Validation and Code Validation** module (`backend/app/validation/`) inspects LLM-generated assistant responses to verify whether extracted code snippets are syntactically and structurally valid.

T17 generates the natural language and code response from the local Ollama LLM. T18 provides static and compiler-assisted syntax verification before responses are presented or executed.

### Core Processing Flow:

```text
T17 Local LLM
      ↓
Generated Assistant Response
      ↓
T18 Response Validator
      ├── Markdown / Code Extraction (`CodeExtractor`)
      ├── Programming Language Resolution (`resolve_language`)
      ├── Syntax / Compiler Validation (`BaseCodeValidator`)
      │     ├── Python AST Parser (`ast.parse`)
      │     ├── C Syntax Checker (`gcc -fsyntax-only`)
      │     ├── C++ Syntax Checker (`g++ -fsyntax-only`)
      │     ├── Java Compiler Checker (`javac -d <tmp>`)
      │     ├── JavaScript Syntax Checker (`node --check`)
      │     └── Static SQL Structure Parser
      ├── Structured Diagnostics (`ValidationDiagnostic`)
      └── Deterministic Status Aggregation
      ↓
ResponseValidationResult
      ↓
Future Safe Runtime Sandbox (T19)
```

---

## 2. Critical Safety Rule

> **NEVER execute generated code directly on the host system.**

- T18 performs **syntax-only and static parsing**.
- Compilers/parsers are invoked with syntax verification flags (`-fsyntax-only` for GCC/G++, `node --check` for Node.js, `ast.parse` for Python).
- Object linking, bytecode loading, binary execution, and real database execution are strictly forbidden.
- Malicious commands (e.g. `os.system("rm -rf ...")`, `Runtime.getRuntime().exec(...)`, or `fs.writeFileSync(...)`) are evaluated purely for syntax correctness and are never launched.

---

## 3. Validation Status Lifecycle

```python
class ValidationStatus(str, Enum):
    VALID = "VALID"
    INVALID = "INVALID"
    UNSUPPORTED = "UNSUPPORTED"
    NOT_VALIDATED = "NOT_VALIDATED"
```

| Status | Meaning |
|---|---|
| `VALID` | All extracted code blocks passed syntax/parser verification without errors. |
| `INVALID` | One or more code blocks failed syntax/parser/compiler verification. |
| `UNSUPPORTED` | Language was identified, but no reliable local validator is installed on the host. |
| `NOT_VALIDATED` | No code blocks were present in the response (e.g., purely conceptual discussion). |

---

## 4. Architecture & Components

```text
backend/app/validation/
├── __init__.py           # Public exports
├── schemas.py            # ValidationStatus, CodeValidationResult, ResponseValidationResult, ValidationDiagnostic
├── exceptions.py         # ValidationException, ValidatorTimeoutError, ValidatorExecutionError
├── code_extractor.py     # Markdown fenced block extraction (``` and ~~~)
├── language_resolver.py  # Language priority resolution (fence -> hint -> heuristics -> None)
├── response_validator.py # Response validation orchestrator & status aggregator
└── validators/
    ├── __init__.py
    ├── base.py           # BaseCodeValidator interface
    ├── python_validator.py     # ast.parse static validator
    ├── c_validator.py          # gcc -fsyntax-only
    ├── cpp_validator.py        # g++ -fsyntax-only
    ├── java_validator.py       # javac -d <tmp> compilation checker
    ├── javascript_validator.py # node --check syntax validator
    └── sql_validator.py        # Static SQL structural tokenizer
```

---

## 5. Supported Languages & Tooling

| Language | Primary Validator | Fallback if Tool Missing | Notes |
|---|---|---|---|
| **Python** | Python stdlib `ast.parse` | N/A (Always available) | Instant sub-millisecond AST parse |
| **C** | `gcc -fsyntax-only` | `UNSUPPORTED` | No linking, no output binary |
| **C++** | `g++ -fsyntax-only` | `UNSUPPORTED` | No linking, no output binary |
| **Java** | `javac -d <tmpdir>` | `UNSUPPORTED` | Compiles into isolated temp directory, never runs class |
| **JavaScript** | `node --check` | `UNSUPPORTED` | Syntax-only check without running scripts |
| **SQL** | Static structural parser | `UNSUPPORTED` | Validates statement balance & syntax without DB connection |

---

## 6. Language Resolution Priority

```text
Priority 1: Explicit fence identifier (e.g. ```python, ```cpp, ```sql)
    ↓
Priority 2: Contextual language hint (e.g. from T14/T15 session context)
    ↓
Priority 3: Strong deterministic lexical heuristics (unique includes, keywords, or structure)
    ↓
Priority 4: None / UNKNOWN (marked as UNSUPPORTED)
```

Common aliases are normalized automatically:
- `py`, `python3` $\to$ `python`
- `c++`, `cc`, `cxx`, `hpp` $\to$ `cpp`
- `js`, `mjs`, `cjs`, `node` $\to$ `javascript`
- `mysql`, `postgres`, `postgresql`, `sqlite` $\to$ `sql`

---

## 7. Status Aggregation Rules

When an assistant response contains multiple code blocks:
- **No blocks**: `NOT_VALIDATED` (`has_code=False`).
- **Any `INVALID`**: Overall status is `INVALID` (strict failure propagation).
- **All `VALID`**: Overall status is `VALID`.
- **All `UNSUPPORTED`**: Overall status is `UNSUPPORTED`.
- **Mixture of `VALID` and `UNSUPPORTED`**: Overall status is `UNSUPPORTED` (cannot certify partial validity without verifying all code).
- **Mixture of `VALID` and `INVALID`**: Overall status is `INVALID`.

---

## 8. Subprocess Security & Temporary Isolation

For compiler-based validators (`gcc`, `g++`, `javac`, `node`):
1. **Argument Arrays Only**: Invoked strictly via `subprocess.run(["cmd", "arg1", ...], shell=False)`.
2. **Strict Timeouts**: Default 5.0 seconds per check to prevent compiler hanging.
3. **Isolated Temporary Files**: Source code is written into `tempfile.NamedTemporaryFile` or `tempfile.TemporaryDirectory`.
4. **Guaranteed Cleanup**: Files and directories are deleted in `finally` blocks.

---

## 9. Performance Benchmarks

Measured on local test environment (average across 5 runs):

| Language | Validator Engine | Average Latency | Min Latency | Max Latency |
|---|---|---|---|---|
| **Python** | Standard AST parser | **0.04 ms** | 0.03 ms | 0.07 ms |
| **SQL** | Static structural parser | **0.05 ms** | 0.02 ms | 0.17 ms |
| **C** | `gcc -fsyntax-only` | **8.37 ms** | 7.15 ms | 10.08 ms |
| **JavaScript** | `node --check` | **60.70 ms** | 57.62 ms | 62.63 ms |
| **C++** | `g++ -fsyntax-only` | **143.37 ms** | 132.35 ms | 149.68 ms |
| **Java** | `javac -d <tmp>` | **297.40 ms** | 271.95 ms | 314.09 ms |

---

## 10. Semantic Limitations & T19 Sandbox Boundary

Syntax validity $\neq$ Logical correctness or runtime safety:
- A Python script containing `1 / 0` is syntactically `VALID` according to AST parsing, but raises `ZeroDivisionError` at runtime.
- A C program with a memory leak or null pointer dereference may pass syntax checks.
- Static syntax checking is the boundary of **T18**.
- Isolated runtime execution, test case evaluation, and execution timeouts belong to **T19 (Safe Code Sandbox)**.

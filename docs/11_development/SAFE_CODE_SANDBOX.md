# Safe Code Sandbox (T19)

## Overview

The **Safe Code Sandbox** provides an isolated, resource-constrained, non-root execution environment for untrusted user- and LLM-generated source code.

While **T18** validates the syntactic and structural validity of code without executing it, **T19** executes validated code in isolated Docker containers, capturing bounded stdout, stderr, exit codes, execution duration, and diagnostics while guaranteeing that the host system and network are never compromised.

---

## Architectural Flow

```text
User / LLM Generated Code
          ↓
T18 Static Validation (Syntax / AST check)
          ↓ (Rejects INVALID before sandbox starts)
T19 Sandbox Policy (Security invariant validation)
          ↓
Docker Isolated Container
  ├── Non-root (sandbox: UID 1000)
  ├── Network: --network none
  ├── Capabilities: --cap-drop ALL
  ├── Root Filesystem: --read-only
  ├── Temporary Space: tmpfs /tmp, tmpfs /workspace
  └── Resource Limits: Memory, CPU, PIDs, Timeout, Output
          ↓
Runtime Execution
          ↓
SandboxResult (stdout, stderr, exit_code, duration_ms, status)
```

### Host / Container Separation

The host system **never executes untrusted code directly**.
1. **No Host Directory Mounts**: Neither `/`, `/home`, `~`, project directories, nor `/var/run/docker.sock` are ever mounted into containers.
2. **Dedicated Workspace Transfer**: Source code files are packed into an in-memory tarball with UID 1000 ownership and unpacked into an isolated ephemeral Docker volume (`b2c-vol-<uuid>`).
3. **Guaranteed Cleanup**: Containers and volumes are removed in `finally` blocks upon completion, timeout, crash, or limit breach.

---

## Supported Runtime Languages

| Language | Runtime / Compiler | Container Image | Container Command |
|---|---|---|---|
| **Python** | Python 3.12 (`python:3.12-slim`) | `bhasha2code-sandbox-python:1.0.0` | `["python3", "-u", "main.py"]` |
| **C** | GCC 13 (`alpine:latest`) | `bhasha2code-sandbox-cpp:1.0.0` | `["sh", "-c", "gcc -O2 main.c -o /workspace/prog && /workspace/prog"]` |
| **C++** | G++ 13 (`alpine:latest`) | `bhasha2code-sandbox-cpp:1.0.0` | `["sh", "-c", "g++ -O2 -std=c++17 main.cpp -o /workspace/prog && /workspace/prog"]` |
| **Java** | OpenJDK 21 (`eclipse-temurin:21-alpine`) | `bhasha2code-sandbox-java:1.0.0` | `["sh", "-c", "javac <Class>.java && java <Class>"]` |
| **JavaScript** | Node.js 20 (`node:20-alpine`) | `bhasha2code-sandbox-javascript:1.0.0` | `["node", "main.js"]` |

> **Note on SQL**: SQL execution against a live database is intentionally **excluded** from T19 sandbox runtime execution. SQL remains strictly static validation (T18) until a dedicated database sandbox environment is architected.

---

## Execution Status Model

```python
class ExecutionStatus(str, Enum):
    SUCCESS = "SUCCESS"              # Program completed within all limits with exit code 0
    RUNTIME_ERROR = "RUNTIME_ERROR"  # Program executed but exited with non-zero status
    TIMEOUT = "TIMEOUT"              # Execution exceeded configured wall-clock timeout
    RESOURCE_LIMIT = "RESOURCE_LIMIT" # Terminated due to memory / OOM or PID constraints
    VALIDATION_FAILED = "VALIDATION_FAILED" # Pre-execution T18 validation failed
    UNSUPPORTED = "UNSUPPORTED"      # Requested language has no runtime runner adapter
    SANDBOX_ERROR = "SANDBOX_ERROR"  # Docker or sandbox infrastructure failure
    OUTPUT_LIMIT = "OUTPUT_LIMIT"    # Stdout/stderr breached output limit threshold
```

---

## Sandbox Result Schema

```python
class SandboxResult(BaseModel):
    status: ExecutionStatus
    language: str
    stdout: str = ""
    stderr: str = ""
    exit_code: int | None = None
    duration_ms: float | None = None
    timed_out: bool = False
    output_truncated: bool = False
    diagnostics: list[str] = Field(default_factory=list)
```

---

## Security Hardening Controls

### 1. Network Isolation
All containers are launched with `--network none`. No outbound or inbound network access is allowed, blocking reverse shells, network scans, or data exfiltration.

### 2. Capability Dropping
Every execution enforces `--cap-drop ALL`, revoking all Linux capabilities (such as `CAP_SYS_ADMIN`, `CAP_NET_ADMIN`, `CAP_DAC_OVERRIDE`).

### 3. Read-Only Root Filesystem
Container root filesystems are mounted with `--read-only`. Temporary file writing is restricted to in-memory `tmpfs` mounts (`/tmp:rw,noexec,nosuid,size=64m`).

### 4. Non-Root User
All execution images create and switch to an unprivileged `sandbox` user (`UID 1000`, `GID 1000`). Containers run with `--user 1000:1000`.

### 5. Resource Limits
- **Memory**: Default `256m` (OOM killer immediately terminates runaway allocations, reporting `RESOURCE_LIMIT` with exit code 137).
- **CPU**: Default `0.5` cores via `--cpus 0.5`.
- **Processes / PIDs**: Default `64` via `--pids-limit 64`, mitigating fork bombs.
- **Wall-Clock Timeout**: Default `3.0s` with a host-side watchdog thread.
- **Output Limit**: Default `64 KB` (65,536 bytes). Streaming output threads terminate the container immediately if output exceeds this threshold.

### 6. Command Construction Safety
All Docker commands are constructed strictly as argument arrays (`list[str]`) passed to `subprocess.Popen` / `subprocess.run` with `shell=False`. User code and input are never interpolated into shell strings.

### 7. T18 Static Validation Gate
Before a container is even spawned, the code is passed to T18 language validators (`PythonValidator`, `CValidator`, `CppValidator`, `JavaValidator`, `JavaScriptValidator`). If the code contains syntax errors, the sandbox returns `VALIDATION_FAILED` immediately without launching Docker.

---

## Configuration Reference

| Parameter | Default | Environment Variable | Description |
|---|---|---|---|
| `timeout_seconds` | `3.0` | `BHASHA2CODE_SANDBOX_TIMEOUT` | Max wall-clock execution time |
| `memory_limit_mb` | `256` | `BHASHA2CODE_SANDBOX_MEMORY_MB` | Max memory in MB |
| `cpu_limit` | `0.5` | `BHASHA2CODE_SANDBOX_CPU` | Max CPU fraction |
| `pids_limit` | `64` | `BHASHA2CODE_SANDBOX_PIDS` | Max concurrent processes |
| `output_limit_bytes` | `65536` | `BHASHA2CODE_SANDBOX_OUTPUT_LIMIT` | Max stdout/stderr capture |
| `workspace_limit_mb` | `64` | `BHASHA2CODE_SANDBOX_WORKSPACE_MB` | Tmpfs workspace size |
| `network_enabled` | `False` | - | Network isolation (must be False) |
| `run_as_non_root` | `True` | - | UID 1000 enforcement |
| `read_only_rootfs` | `True` | - | Read-only root filesystem flag |

---

## Mandatory Security Test Matrix

| Threat Scenario | Test Vector | Expected Outcome | Verified |
|---|---|---|---|
| **Syntax Error** | `def add(a, b)\n return a+b` | `VALIDATION_FAILED` (no Docker invoked) | Yes |
| **Runtime Crash** | `print(10 / 0)` | `RUNTIME_ERROR` (stderr captured) | Yes |
| **Infinite Loop** | `while True: pass` | `TIMEOUT` (process killed at 1.5s) | Yes |
| **Output Flood** | `while True: print("SPAM"*500)` | `OUTPUT_LIMIT` (truncated at limit) | Yes |
| **Network Access** | `urllib.request.urlopen(...)` | Blocked (`URLError`) | Yes |
| **Host Filesystem** | Access `/home` or project directory | Denied (`False`) | Yes |
| **Privilege Escalation** | `whoami` / `getuid` | `sandbox` (UID 1000, not root) | Yes |
| **Docker Socket** | Check `/var/run/docker.sock` | Unavailable (`False`) | Yes |
| **Environment Leak** | Read host environment variables | Hidden (`False`) | Yes |
| **Fork Bomb** | `while True: os.fork()` | Bounded by PID limit / `RESOURCE_LIMIT` | Yes |
| **Memory Exhaustion**| Unbounded list append | `RESOURCE_LIMIT` (exit code 137) | Yes |
| **Host Injection** | `"; rm -rf /; $(whoami)"` | Plain source code, zero shell execution | Yes |
| **Cleanup Verification** | Compare active containers & volumes | Zero leftover containers or volumes | Yes |

---

## Image Build Instructions

Build all sandbox images using the automated script:
```bash
bash scripts/build_sandbox_images.sh
```

---

## Running Tests

### Unit Tests (Docker Not Required)
```bash
pytest -q tests/unit/sandbox/
```

### Live Docker Integration Tests
```bash
RUN_DOCKER_SANDBOX=1 pytest -v tests/integration/sandbox/
```

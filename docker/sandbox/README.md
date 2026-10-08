# Bhasha2Code Sandbox Docker Images

This directory contains minimal, hardened Dockerfiles used by the T19 Safe Code Sandbox to run untrusted code in strict isolation.

## Image Specifications

| Image Tag | Dockerfile | Base Image | Non-root User | Purpose |
|---|---|---|---|---|
| `bhasha2code-sandbox-python:1.0.0` | `Dockerfile.python` | `python:3.12-slim` | `sandbox` (UID 1000) | Python 3.12 runtime |
| `bhasha2code-sandbox-cpp:1.0.0` | `Dockerfile.cpp` | `alpine:latest` | `sandbox` (UID 1000) | GCC & G++ compilers + musl libc |
| `bhasha2code-sandbox-java:1.0.0` | `Dockerfile.java` | `eclipse-temurin:21-alpine` | `sandbox` (UID 1000) | OpenJDK 21 compiler & runtime |
| `bhasha2code-sandbox-javascript:1.0.0` | `Dockerfile.javascript` | `node:20-alpine` | `sandbox` (UID 1000) | Node.js 20 runtime |

## Security Hardening Guarantees

1. **Non-Root Execution**: Every image runs under an unprivileged `sandbox` user (UID 1000). Containers are executed with `--security-opt no-new-privileges` and `--cap-drop ALL`.
2. **Read-Only Root Filesystem**: Root filesystems are mounted read-only (`--read-only`), with bounded tmpfs memory mounts for `/tmp` and `/workspace`.
3. **Network Isolation**: All executions run with `--network none`.
4. **No External Tools**: No SSH, git, curl, wget, docker client, or project code are installed in runtime images.
5. **No Host Access**: Host filesystem and Docker socket are strictly forbidden from container mounting.

## Building Images

Use the automated build script:
```bash
bash scripts/build_sandbox_images.sh
```

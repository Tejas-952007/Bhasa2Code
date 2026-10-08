#!/usr/bin/env bash
set -euo pipefail

# Build isolated, minimal sandbox Docker images for Bhasha2Code T19
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT_DIR="$(cd "${SCRIPT_DIR}/.." && pwd)"
DOCKER_DIR="${ROOT_DIR}/docker/sandbox"

echo "=== Building Bhasha2Code T19 Sandbox Images ==="

# Check docker availability
if ! command -v docker >/dev/null 2>&1; then
    echo "ERROR: Docker CLI not found." >&2
    exit 1
fi

if ! docker info >/dev/null 2>&1; then
    echo "ERROR: Docker daemon is not running or current user lacks access." >&2
    exit 1
fi

TAG_VERSION="1.0.0"

echo "[1/4] Building Python sandbox: bhasha2code-sandbox-python:${TAG_VERSION}"
docker build -t "bhasha2code-sandbox-python:${TAG_VERSION}" -f "${DOCKER_DIR}/Dockerfile.python" "${DOCKER_DIR}"

echo "[2/4] Building C/C++ sandbox: bhasha2code-sandbox-cpp:${TAG_VERSION}"
docker build -t "bhasha2code-sandbox-cpp:${TAG_VERSION}" -f "${DOCKER_DIR}/Dockerfile.cpp" "${DOCKER_DIR}"

echo "[3/4] Building Java sandbox: bhasha2code-sandbox-java:${TAG_VERSION}"
docker build -t "bhasha2code-sandbox-java:${TAG_VERSION}" -f "${DOCKER_DIR}/Dockerfile.java" "${DOCKER_DIR}"

echo "[4/4] Building JavaScript sandbox: bhasha2code-sandbox-javascript:${TAG_VERSION}"
docker build -t "bhasha2code-sandbox-javascript:${TAG_VERSION}" -f "${DOCKER_DIR}/Dockerfile.javascript" "${DOCKER_DIR}"

echo "=== All sandbox images built successfully ==="
docker images | grep "bhasha2code-sandbox-"

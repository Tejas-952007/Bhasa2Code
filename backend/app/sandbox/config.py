"""Configuration definitions and defaults for the safe code sandbox."""

import os
from typing import Dict
from pydantic import BaseModel, Field

from backend.app.sandbox.exceptions import SandboxConfigurationError

DEFAULT_IMAGE_TAGS: Dict[str, str] = {
    "python": "bhasha2code-sandbox-python:1.0.0",
    "python_ml": "bhasha2code-sandbox-python-ml:1.0.0",
    "c": "bhasha2code-sandbox-cpp:1.0.0",
    "cpp": "bhasha2code-sandbox-cpp:1.0.0",
    "java": "bhasha2code-sandbox-java:1.0.0",
    "javascript": "bhasha2code-sandbox-javascript:1.0.0",
}


class SandboxConfig(BaseModel):
    """Runtime limits and isolation parameters for sandbox execution."""

    timeout_seconds: float = Field(
        default=float(os.getenv("BHASHA2CODE_SANDBOX_TIMEOUT", "3.0")),
        description="Execution wall-clock timeout in seconds for standard code.",
    )
    memory_limit_mb: int = Field(
        default=int(os.getenv("BHASHA2CODE_SANDBOX_MEMORY_MB", "256")),
        description="Maximum memory allocated to container in megabytes for standard code.",
    )
    ml_timeout_seconds: float = Field(
        default=float(os.getenv("BHASHA2CODE_SANDBOX_ML_TIMEOUT", "10.0")),
        description="Execution wall-clock timeout in seconds for ML workloads.",
    )
    ml_memory_limit_mb: int = Field(
        default=int(os.getenv("BHASHA2CODE_SANDBOX_ML_MEMORY_MB", "768")),
        description="Maximum memory allocated to container in megabytes for ML workloads.",
    )
    cpu_limit: float = Field(
        default=float(os.getenv("BHASHA2CODE_SANDBOX_CPU", "0.5")),
        description="Maximum CPU fraction allowed.",
    )
    pids_limit: int = Field(
        default=int(os.getenv("BHASHA2CODE_SANDBOX_PIDS", "64")),
        description="Maximum process/PID count within container.",
    )
    output_limit_bytes: int = Field(
        default=int(os.getenv("BHASHA2CODE_SANDBOX_OUTPUT_LIMIT", "65536")),
        description="Maximum captured stdout/stderr size in bytes (default 64 KB).",
    )
    workspace_limit_mb: int = Field(
        default=int(os.getenv("BHASHA2CODE_SANDBOX_WORKSPACE_MB", "64")),
        description="Maximum writable workspace / tmpfs size in megabytes.",
    )
    network_enabled: bool = Field(
        default=False,
        description="Strict network isolation flag. Must remain False for untrusted execution.",
    )
    run_as_non_root: bool = Field(
        default=True,
        description="Enforces execution as non-root user (UID 1000).",
    )
    read_only_rootfs: bool = Field(
        default=True,
        description="Mounts container rootfs as strictly read-only.",
    )
    enable_no_new_privileges: bool = Field(
        default=True,
        description="Enforces --security-opt no-new-privileges where supported.",
    )
    docker_binary: str = Field(
        default=os.getenv("BHASHA2CODE_DOCKER_BIN", "docker"),
        description="Path or command name for Docker CLI.",
    )
    image_tags: Dict[str, str] = Field(
        default_factory=lambda: dict(DEFAULT_IMAGE_TAGS),
        description="Mapping of runtime language to container image tags.",
    )
    max_code_bytes: int = Field(
        default=1_048_576,
        description="Maximum allowed source code size in bytes (1 MB).",
    )
    max_stdin_bytes: int = Field(
        default=65_536,
        description="Maximum allowed stdin input size in bytes (64 KB).",
    )

    def validate_config(self) -> None:
        """Validate safety invariants for sandbox configuration."""
        if self.timeout_seconds <= 0:
            raise SandboxConfigurationError("timeout_seconds must be positive.")
        if self.memory_limit_mb < 16:
            raise SandboxConfigurationError("memory_limit_mb must be at least 16 MB.")
        if self.ml_timeout_seconds <= 0:
            raise SandboxConfigurationError("ml_timeout_seconds must be positive.")
        if self.ml_memory_limit_mb < 64:
            raise SandboxConfigurationError("ml_memory_limit_mb must be at least 64 MB.")
        if self.cpu_limit <= 0 or self.cpu_limit > 16.0:
            raise SandboxConfigurationError("cpu_limit must be between 0.1 and 16.0.")
        if self.pids_limit < 4:
            raise SandboxConfigurationError("pids_limit must be at least 4.")
        if self.output_limit_bytes < 1024:
            raise SandboxConfigurationError("output_limit_bytes must be at least 1024 bytes.")
        if self.network_enabled:
            raise SandboxConfigurationError("network_enabled must be False for secure sandboxing.")

"""Interactive Docker session manager for real-time bidirectional code execution."""

import asyncio
import io
import logging
import subprocess
import time
import uuid
from typing import Any, Dict, List, Optional

from backend.app.sandbox.config import SandboxConfig
from backend.app.sandbox.docker_runtime import DockerRuntime
from backend.app.sandbox.languages import get_language_runner, normalize_sandbox_language
from backend.app.sandbox.languages.base import LanguageExecutionPlan
from backend.app.sandbox.policies import SandboxSecurityPolicy
from backend.app.validation.response_validator import ResponseValidator
from backend.app.validation.schemas import ValidationStatus

logger = logging.getLogger("bhasha2code.sandbox.interactive")

# Maximum concurrent interactive sessions allowed across the server
MAX_CONCURRENT_INTERACTIVE_SESSIONS = 5
_ACTIVE_SESSIONS: Dict[str, "InteractiveDockerSession"] = {}
_ACTIVE_LOCK = asyncio.Lock()


class InteractiveDockerSession:
    """Manages lifecycle of a live bidirectional container execution session."""

    def __init__(
        self,
        language: str,
        code: str,
        docker_runtime: Optional[DockerRuntime] = None,
        idle_timeout_seconds: float = 60.0,
        total_timeout_seconds: float = 120.0,
    ) -> None:
        self.session_id = uuid.uuid4().hex[:12]
        self.language = language
        self.code = code
        self.docker_runtime = docker_runtime or DockerRuntime()
        self.config = self.docker_runtime.config
        self.security_policy = self.docker_runtime.security_policy
        self.idle_timeout_seconds = idle_timeout_seconds
        self.total_timeout_seconds = total_timeout_seconds

        self.vol_name = f"b2c-vol-{self.session_id}"
        self.cid_name = f"b2c-run-{self.session_id}"

        self.proc: Optional[asyncio.subprocess.Process] = None
        self.start_time: float = 0.0
        self.last_activity_time: float = 0.0
        self.total_output_bytes: int = 0
        self.hit_output_limit: bool = False
        self.is_terminated: bool = False
        self._cleanup_done: bool = False

    async def stage_and_start(self, plan: LanguageExecutionPlan) -> None:
        """Stage source files to an isolated volume and launch the container process."""
        loop = asyncio.get_running_loop()

        # 1. Create ephemeral Docker volume in executor thread
        def create_vol():
            res = subprocess.run(
                [self.config.docker_binary, "volume", "create", self.vol_name],
                capture_output=True,
                text=True,
                timeout=5.0,
                check=False,
            )
            if res.returncode != 0:
                raise RuntimeError(f"Failed to allocate execution volume: {res.stderr.strip()}")

        await loop.run_in_executor(None, create_vol)

        # 2. Stage files into volume using tar
        tar_bytes = self.docker_runtime._create_tar_archive(plan.files)

        def stage_tar():
            stage_cmd = [
                self.config.docker_binary,
                "run",
                "--rm",
                "-i",
                "-v",
                f"{self.vol_name}:/workspace:rw",
                "--user",
                "1000:1000",
                plan.image_tag,
                "tar",
                "-xzf",
                "-",
                "-C",
                "/workspace",
            ]
            res = subprocess.run(
                stage_cmd,
                input=tar_bytes,
                capture_output=True,
                timeout=5.0,
                check=False,
            )
            if res.returncode != 0:
                raise RuntimeError(f"Workspace file staging failed: {res.stderr.decode('utf-8', errors='replace')}")

        await loop.run_in_executor(None, stage_tar)

        # 3. Build container execution command & validate security invariants
        run_cmd = self.docker_runtime.build_docker_run_args(plan, self.vol_name, self.cid_name)
        self.security_policy.validate_security_invariants(run_cmd)

        # 4. Launch container process with unbuffered stdin/stdout/stderr pipes
        self.start_time = time.perf_counter()
        self.last_activity_time = self.start_time

        self.proc = await asyncio.create_subprocess_exec(
            *run_cmd,
            stdin=asyncio.subprocess.PIPE,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE,
        )
        logger.info(
            "Started interactive container '%s' for session '%s' (pid=%s)",
            self.cid_name,
            self.session_id,
            self.proc.pid,
        )

    async def write_stdin(self, data: str) -> None:
        """Write user-entered input data into the running process stdin."""
        if self.proc and self.proc.stdin and not self.is_terminated:
            if self.proc.returncode is not None:
                raise RuntimeError("Process has already completed. Cannot accept further input.")
            self.last_activity_time = time.perf_counter()
            self.proc.stdin.write(data.encode("utf-8"))
            await self.proc.stdin.drain()
            logger.debug("Forwarded %d bytes to stdin of session %s", len(data), self.session_id)
        else:
            raise RuntimeError("Process is not active or stdin is closed.")

    async def read_stdout_chunk(self) -> Optional[str]:
        """Read next available chunk from process stdout (up to 4096 bytes)."""
        if not self.proc or not self.proc.stdout:
            return None
        try:
            chunk = await self.proc.stdout.read(4096)
            if not chunk:
                return None
            self.last_activity_time = time.perf_counter()
            self.total_output_bytes += len(chunk)
            if self.total_output_bytes >= self.config.output_limit_bytes:
                self.hit_output_limit = True
            text = chunk.decode("utf-8", errors="replace")
            return self.security_policy.sanitize_output(text)
        except Exception as e:
            logger.debug("Error reading stdout from session %s: %s", self.session_id, e)
            return None

    async def read_stderr_chunk(self) -> Optional[str]:
        """Read next available chunk from process stderr (up to 4096 bytes)."""
        if not self.proc or not self.proc.stderr:
            return None
        try:
            chunk = await self.proc.stderr.read(4096)
            if not chunk:
                return None
            self.last_activity_time = time.perf_counter()
            self.total_output_bytes += len(chunk)
            if self.total_output_bytes >= self.config.output_limit_bytes:
                self.hit_output_limit = True
            text = chunk.decode("utf-8", errors="replace")
            return self.security_policy.sanitize_output(text)
        except Exception as e:
            logger.debug("Error reading stderr from session %s: %s", self.session_id, e)
            return None

    def is_running(self) -> bool:
        """Check if container process is currently running."""
        return self.proc is not None and self.proc.returncode is None and not self.is_terminated

    def get_duration_ms(self) -> float:
        """Calculate wall-clock execution duration in milliseconds."""
        if self.start_time <= 0:
            return 0.0
        return round((time.perf_counter() - self.start_time) * 1000, 2)

    def is_idle_timed_out(self) -> bool:
        """Check if waiting for input has exceeded the idle timeout threshold."""
        if not self.is_running():
            return False
        return (time.perf_counter() - self.last_activity_time) > self.idle_timeout_seconds

    def is_total_timed_out(self) -> bool:
        """Check if total execution time has exceeded maximum session timeout."""
        if not self.is_running():
            return False
        return (time.perf_counter() - self.start_time) > self.total_timeout_seconds

    async def terminate(self) -> None:
        """Forcefully terminate container process."""
        self.is_terminated = True
        if self.proc and self.proc.returncode is None:
            try:
                self.proc.kill()
            except Exception:
                pass
        await self.cleanup()

    async def cleanup(self) -> None:
        """Guaranteed cleanup of container and ephemeral Docker volume."""
        if self._cleanup_done:
            return
        self._cleanup_done = True
        self.is_terminated = True

        loop = asyncio.get_running_loop()

        def do_docker_cleanup():
            # Kill and remove container
            try:
                subprocess.run(
                    [self.config.docker_binary, "rm", "-f", self.cid_name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=5.0,
                    check=False,
                )
            except Exception as e:
                logger.debug("Cleanup container '%s': %s", self.cid_name, e)

            # Remove volume
            try:
                subprocess.run(
                    [self.config.docker_binary, "volume", "rm", "-f", self.vol_name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=5.0,
                    check=False,
                )
            except Exception as e:
                logger.debug("Cleanup volume '%s': %s", self.vol_name, e)

        await loop.run_in_executor(None, do_docker_cleanup)
        logger.info("Cleaned up resources for session '%s'", self.session_id)


async def register_session(session: InteractiveDockerSession) -> bool:
    """Register a new interactive session, enforcing concurrency limit."""
    async with _ACTIVE_LOCK:
        if len(_ACTIVE_SESSIONS) >= MAX_CONCURRENT_INTERACTIVE_SESSIONS:
            return False
        _ACTIVE_SESSIONS[session.session_id] = session
        return True


async def unregister_session(session_id: str) -> None:
    """Unregister an interactive session on termination."""
    async with _ACTIVE_LOCK:
        session = _ACTIVE_SESSIONS.pop(session_id, None)
        if session:
            await session.cleanup()

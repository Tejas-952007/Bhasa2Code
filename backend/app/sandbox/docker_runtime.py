"""Docker container runtime adapter for secure, isolated code execution."""

import io
import logging
import subprocess
import tarfile
import threading
import time
import uuid
from typing import Any, Dict, List, Optional

from backend.app.sandbox.config import SandboxConfig
from backend.app.sandbox.exceptions import (
    SandboxConfigurationError,
    SandboxError,
    SandboxSecurityViolationError,
    SandboxUnavailableError,
)
from backend.app.sandbox.languages.base import LanguageExecutionPlan
from backend.app.sandbox.policies import SandboxSecurityPolicy
from backend.app.sandbox.schemas import ExecutionStatus, SandboxResult

logger = logging.getLogger(__name__)


class DockerRuntime:
    """Manages container lifecycle, resource isolation, output streaming, and cleanup."""

    def __init__(
        self,
        config: Optional[SandboxConfig] = None,
        security_policy: Optional[SandboxSecurityPolicy] = None,
    ) -> None:
        self.config = config or SandboxConfig()
        self.config.validate_config()
        self.security_policy = security_policy or SandboxSecurityPolicy(self.config)
        self._no_new_privs_supported: Optional[bool] = None

    def is_available(self) -> bool:
        """Check if Docker CLI and daemon are accessible."""
        try:
            res = subprocess.run(
                [self.config.docker_binary, "info"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=3.0,
                check=False,
            )
            return res.returncode == 0
        except (subprocess.SubprocessError, FileNotFoundError, OSError):
            return False

    def check_runtime(self) -> Dict[str, Any]:
        """Perform comprehensive capability and health inspection."""
        available = self.is_available()
        version_str = "unknown"
        images_status: Dict[str, bool] = {}

        if available:
            try:
                ver_res = subprocess.run(
                    [self.config.docker_binary, "--version"],
                    capture_output=True,
                    text=True,
                    timeout=3.0,
                    check=False,
                )
                version_str = ver_res.stdout.strip()

                # Check images
                for lang, tag in self.config.image_tags.items():
                    img_res = subprocess.run(
                        [self.config.docker_binary, "image", "inspect", tag],
                        stdout=subprocess.DEVNULL,
                        stderr=subprocess.DEVNULL,
                        timeout=3.0,
                        check=False,
                    )
                    images_status[lang] = img_res.returncode == 0
            except Exception as e:
                logger.warning(f"Error checking runtime capabilities: {e}")

        return {
            "available": available,
            "docker_version": version_str,
            "images_present": images_status,
            "limits": {
                "timeout_seconds": self.config.timeout_seconds,
                "memory_limit_mb": self.config.memory_limit_mb,
                "cpu_limit": self.config.cpu_limit,
                "pids_limit": self.config.pids_limit,
                "output_limit_bytes": self.config.output_limit_bytes,
            },
        }

    def _probe_no_new_privileges(self) -> bool:
        """Detect if no-new-privileges is supported by the current host kernel and Docker setup."""
        if self._no_new_privs_supported is not None:
            return self._no_new_privs_supported

        try:
            # Probe with a fast echo command using alpine/python image
            img = self.config.image_tags.get("python", "bhasha2code-sandbox-python:1.0.0")
            res = subprocess.run(
                [
                    self.config.docker_binary,
                    "run",
                    "--rm",
                    "--security-opt",
                    "no-new-privileges",
                    img,
                    "python3",
                    "-c",
                    "pass",
                ],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                timeout=3.0,
                check=False,
            )
            self._no_new_privs_supported = res.returncode == 0
        except Exception:
            self._no_new_privs_supported = False

        return self._no_new_privs_supported

    def build_docker_run_args(
        self,
        plan: LanguageExecutionPlan,
        volume_name: str,
        container_name: str,
    ) -> List[str]:
        """Construct secure, non-privileged Docker execution command argument array."""
        args: List[str] = [
            self.config.docker_binary,
            "run",
            "--rm",
            "-i",
            "--name",
            container_name,
            "--network",
            "none",
            "--cap-drop",
            "ALL",
        ]

        # Use no-new-privileges where supported and enabled
        if self.config.enable_no_new_privileges and self._probe_no_new_privileges():
            args.extend(["--security-opt", "no-new-privileges"])

        if self.config.read_only_rootfs:
            args.append("--read-only")

        # Isolated memory-backed tmpfs for /tmp
        args.extend([
            "--tmpfs",
            f"/tmp:rw,noexec,nosuid,size={self.config.workspace_limit_mb}m",
            "--memory",
            f"{self.config.memory_limit_mb}m",
            "--cpus",
            str(self.config.cpu_limit),
            "--pids-limit",
            str(self.config.pids_limit),
            "-v",
            f"{volume_name}:/workspace:rw",
        ])

        if self.config.run_as_non_root:
            args.extend(["--user", "1000:1000"])

        # Container image
        args.append(plan.image_tag)

        # Container execution entrypoint
        args.extend(plan.entrypoint)

        return args

    def _create_tar_archive(self, files: Dict[str, str]) -> bytes:
        """Package files dictionary into tar bytes with unprivileged sandbox ownership."""
        buf = io.BytesIO()
        with tarfile.open(fileobj=buf, mode="w:gz") as tar:
            for filename, content in files.items():
                data = content.encode("utf-8")
                ti = tarfile.TarInfo(name=filename)
                ti.size = len(data)
                ti.uid = 1000
                ti.gid = 1000
                ti.mode = 0o644
                tar.addfile(ti, io.BytesIO(data))
        return buf.getvalue()

    def execute(
        self,
        plan: LanguageExecutionPlan,
        stdin: str = "",
        timeout_seconds: Optional[float] = None,
        memory_limit_mb: Optional[int] = None,
    ) -> SandboxResult:
        """Execute a language plan inside an isolated container with strict bounds and cleanup."""
        if not self.is_available():
            return SandboxResult(
                status=ExecutionStatus.SANDBOX_ERROR,
                language=plan.language,
                diagnostics=["Docker runtime is unavailable or daemon is not accessible."],
            )

        effective_timeout = timeout_seconds if (timeout_seconds and timeout_seconds > 0) else self.config.timeout_seconds
        uid = uuid.uuid4().hex[:12]
        vol_name = f"b2c-vol-{uid}"
        cid_name = f"b2c-run-{uid}"

        # 1. Create ephemeral volume
        try:
            vol_res = subprocess.run(
                [self.config.docker_binary, "volume", "create", vol_name],
                capture_output=True,
                text=True,
                timeout=5.0,
                check=False,
            )
            if vol_res.returncode != 0:
                return SandboxResult(
                    status=ExecutionStatus.SANDBOX_ERROR,
                    language=plan.language,
                    diagnostics=[f"Failed to allocate execution volume: {vol_res.stderr.strip()}"],
                )
        except Exception as e:
            return SandboxResult(
                status=ExecutionStatus.SANDBOX_ERROR,
                language=plan.language,
                diagnostics=[f"Volume creation error: {self.security_policy.sanitize_output(str(e))}"],
            )

        container_process: Optional[subprocess.Popen] = None

        try:
            # 2. Populate volume using tar archive
            tar_bytes = self._create_tar_archive(plan.files)
            stage_cmd = [
                self.config.docker_binary,
                "run",
                "--rm",
                "-i",
                "-v",
                f"{vol_name}:/workspace:rw",
                "--user",
                "1000:1000",
                plan.image_tag,
                "tar",
                "-xzf",
                "-",
                "-C",
                "/workspace",
            ]
            stage_res = subprocess.run(
                stage_cmd,
                input=tar_bytes,
                capture_output=True,
                timeout=5.0,
                check=False,
            )
            if stage_res.returncode != 0:
                return SandboxResult(
                    status=ExecutionStatus.SANDBOX_ERROR,
                    language=plan.language,
                    diagnostics=[f"Workspace file staging failed: {stage_res.stderr.decode('utf-8', errors='replace')}"],
                )

            # 3. Build container execution command
            run_cmd = self.build_docker_run_args(plan, vol_name, cid_name)
            self.security_policy.validate_security_invariants(run_cmd)

            # 4. Execute container process with monitoring threads
            start_time = time.perf_counter()
            container_process = subprocess.Popen(
                run_cmd,
                stdin=subprocess.PIPE if stdin else subprocess.DEVNULL,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            stdout_chunks: List[bytes] = []
            stderr_chunks: List[bytes] = []
            output_limit = self.config.output_limit_bytes
            hit_output_limit = False
            lock = threading.Lock()

            def read_stream(stream, chunks_list):
                nonlocal hit_output_limit
                try:
                    while True:
                        chunk = stream.read(4096)
                        if not chunk:
                            break
                        with lock:
                            chunks_list.append(chunk)
                            total = sum(len(c) for c in stdout_chunks) + sum(len(c) for c in stderr_chunks)
                            if total >= output_limit:
                                hit_output_limit = True
                                break
                except Exception:
                    pass

            t_out = threading.Thread(target=read_stream, args=(container_process.stdout, stdout_chunks))
            t_err = threading.Thread(target=read_stream, args=(container_process.stderr, stderr_chunks))
            t_out.daemon = True
            t_err.daemon = True
            t_out.start()
            t_err.start()

            # Write stdin if provided
            if stdin and container_process.stdin:
                try:
                    container_process.stdin.write(stdin.encode("utf-8"))
                    container_process.stdin.flush()
                except (BrokenPipeError, OSError):
                    pass
                finally:
                    try:
                        container_process.stdin.close()
                    except Exception:
                        pass

            # Monitor process with deadline
            timed_out = False
            deadline = start_time + effective_timeout

            while container_process.poll() is None:
                if hit_output_limit:
                    try:
                        container_process.kill()
                    except Exception:
                        pass
                    try:
                        subprocess.run(
                            [self.config.docker_binary, "kill", cid_name],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            timeout=1.0,
                            check=False,
                        )
                    except Exception:
                        pass
                    break

                if time.perf_counter() > deadline:
                    timed_out = True
                    try:
                        container_process.kill()
                    except Exception:
                        pass
                    try:
                        subprocess.run(
                            [self.config.docker_binary, "kill", cid_name],
                            stdout=subprocess.DEVNULL,
                            stderr=subprocess.DEVNULL,
                            timeout=1.0,
                            check=False,
                        )
                    except Exception:
                        pass
                    break
                time.sleep(0.05)

            try:
                container_process.wait(timeout=2.0)
            except subprocess.TimeoutExpired:
                container_process.kill()

            t_out.join(timeout=1.0)
            t_err.join(timeout=1.0)

            duration_ms = round((time.perf_counter() - start_time) * 1000, 2)
            exit_code = container_process.returncode

            # Combine collected output
            raw_stdout = b"".join(stdout_chunks)
            raw_stderr = b"".join(stderr_chunks)

            output_truncated = hit_output_limit
            if len(raw_stdout) > output_limit:
                raw_stdout = raw_stdout[:output_limit]
                output_truncated = True
            if len(raw_stderr) > output_limit:
                raw_stderr = raw_stderr[:output_limit]
                output_truncated = True

            out_text = self.security_policy.sanitize_output(raw_stdout.decode("utf-8", errors="replace"))
            err_text = self.security_policy.sanitize_output(raw_stderr.decode("utf-8", errors="replace"))

            # Determine execution status
            if hit_output_limit:
                status = ExecutionStatus.OUTPUT_LIMIT
                diagnostics = [f"Output exceeded maximum configured limit ({output_limit} bytes). Execution halted."]
            elif timed_out:
                status = ExecutionStatus.TIMEOUT
                diagnostics = [f"Execution timed out after {effective_timeout:.2f} seconds."]
            elif exit_code == 137:
                # 137 indicates SIGKILL by OOM killer or external kill
                status = ExecutionStatus.RESOURCE_LIMIT
                diagnostics = ["Process terminated due to resource constraints (memory/cgroups OOM)."]
            elif exit_code == 0:
                status = ExecutionStatus.SUCCESS
                diagnostics = []
            else:
                status = ExecutionStatus.RUNTIME_ERROR
                diagnostics = [f"Process exited with non-zero status code: {exit_code}"]

            return SandboxResult(
                status=status,
                language=plan.language,
                stdout=out_text,
                stderr=err_text,
                exit_code=exit_code if not timed_out else None,
                duration_ms=duration_ms,
                timed_out=timed_out,
                output_truncated=output_truncated,
                diagnostics=diagnostics,
            )

        finally:
            # 5. Guaranteed cleanup of container and volume
            try:
                subprocess.run(
                    [self.config.docker_binary, "rm", "-f", cid_name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
            except Exception:
                pass

            try:
                subprocess.run(
                    [self.config.docker_binary, "volume", "rm", "-f", vol_name],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    check=False,
                )
            except Exception:
                pass

"""Live integration tests and mandatory security matrix for Docker sandbox execution.

These tests run live Docker containers and are gated by RUN_DOCKER_SANDBOX=1.
"""

import os
import subprocess
import pytest

from backend.app.sandbox.config import SandboxConfig
from backend.app.sandbox.sandbox_runner import SandboxRunner
from backend.app.sandbox.schemas import ExecutionRequest, ExecutionStatus

# Gating condition: integration tests only run if RUN_DOCKER_SANDBOX=1
pytestmark = pytest.mark.skipif(
    os.getenv("RUN_DOCKER_SANDBOX") != "1",
    reason="Live Docker sandbox tests require RUN_DOCKER_SANDBOX=1 environment variable.",
)


@pytest.fixture(scope="module")
def runner():
    """Shared SandboxRunner instance with standard configuration."""
    cfg = SandboxConfig(
        timeout_seconds=3.0,
        memory_limit_mb=128,
        cpu_limit=0.5,
        pids_limit=32,
    )
    return SandboxRunner(config=cfg)


def test_docker_sandbox_health(runner):
    """Verify Docker runtime availability and readiness."""
    assert runner.is_available() is True
    runtime_info = runner.check_runtime()
    assert runtime_info["available"] is True
    assert "docker_version" in runtime_info


# =========================================================================
# Supported Language Execution Tests
# =========================================================================

def test_python_successful_execution(runner):
    """Verify basic Python execution returns SUCCESS."""
    req = ExecutionRequest(
        language="python",
        code="print('Hello Bhasha2Code')",
    )
    res = runner.execute(req)
    assert res.status == ExecutionStatus.SUCCESS
    assert res.stdout.strip() == "Hello Bhasha2Code"
    assert res.exit_code == 0
    assert res.duration_ms is not None
    assert res.timed_out is False


def test_c_successful_execution(runner):
    """Verify C compilation and execution inside container returns SUCCESS."""
    code = """#include <stdio.h>
int main() {
    printf("Hello from C sandbox\\n");
    return 0;
}"""
    req = ExecutionRequest(language="c", code=code)
    res = runner.execute(req)
    assert res.status == ExecutionStatus.SUCCESS
    assert "Hello from C sandbox" in res.stdout
    assert res.exit_code == 0


def test_cpp_successful_execution(runner):
    """Verify C++ compilation and execution inside container returns SUCCESS."""
    code = """#include <iostream>
int main() {
    std::cout << "Hello from C++ sandbox" << std::endl;
    return 0;
}"""
    req = ExecutionRequest(language="cpp", code=code)
    res = runner.execute(req)
    assert res.status == ExecutionStatus.SUCCESS
    assert "Hello from C++ sandbox" in res.stdout
    assert res.exit_code == 0


def test_java_successful_execution(runner):
    """Verify Java compilation and execution inside container returns SUCCESS."""
    code = """public class Main {
    public static void main(String[] args) {
        System.out.println("Hello from Java sandbox");
    }
}"""
    req = ExecutionRequest(language="java", code=code)
    res = runner.execute(req)
    assert res.status == ExecutionStatus.SUCCESS
    assert "Hello from Java sandbox" in res.stdout
    assert res.exit_code == 0


def test_javascript_successful_execution(runner):
    """Verify JavaScript execution in Node.js container returns SUCCESS."""
    code = 'console.log("Hello from JavaScript sandbox");'
    req = ExecutionRequest(language="javascript", code=code)
    res = runner.execute(req)
    assert res.status == ExecutionStatus.SUCCESS
    assert "Hello from JavaScript sandbox" in res.stdout
    assert res.exit_code == 0


def test_bounded_stdin_input(runner):
    """Verify standard input is correctly piped to container program."""
    code = """a = int(input())
b = int(input())
print(a + b)"""
    req = ExecutionRequest(
        language="python",
        code=code,
        stdin="15\n25\n",
    )
    res = runner.execute(req)
    assert res.status == ExecutionStatus.SUCCESS
    assert res.stdout.strip() == "40"


# =========================================================================
# Mandatory Security Test Matrix
# =========================================================================

def test_security_runtime_error(runner):
    """Verify runtime exception returns RUNTIME_ERROR with stderr captured."""
    code = "print(10 / 0)"
    req = ExecutionRequest(language="python", code=code)
    res = runner.execute(req)

    assert res.status == ExecutionStatus.RUNTIME_ERROR
    assert res.exit_code != 0
    assert "ZeroDivisionError" in res.stderr


def test_security_infinite_loop_timeout(runner):
    """Verify infinite loop triggers wall-clock TIMEOUT."""
    code = """while True:
    pass"""
    req = ExecutionRequest(
        language="python",
        code=code,
        timeout_seconds=1.5,
    )
    res = runner.execute(req)

    assert res.status == ExecutionStatus.TIMEOUT
    assert res.timed_out is True
    assert "timed out" in res.diagnostics[0].lower()


def test_security_output_abuse(runner):
    """Verify spamming stdout triggers OUTPUT_LIMIT or controlled termination."""
    code = """while True:
    print("SPAM" * 500)"""
    # Create runner with small output limit
    cfg = SandboxConfig(
        timeout_seconds=3.0,
        output_limit_bytes=2048,
    )
    custom_runner = SandboxRunner(config=cfg)
    req = ExecutionRequest(language="python", code=code)
    res = custom_runner.execute(req)

    assert res.status == ExecutionStatus.OUTPUT_LIMIT
    assert res.output_truncated is True
    assert len(res.stdout) <= 2048


def test_security_network_isolation(runner):
    """Verify outbound network connections are completely blocked."""
    code = """import urllib.request
try:
    urllib.request.urlopen("http://example.com", timeout=1)
    print("NETWORK_ACCESSIBLE")
except Exception as e:
    print("NETWORK_BLOCKED:", type(e).__name__)
"""
    req = ExecutionRequest(language="python", code=code)
    res = runner.execute(req)

    assert res.status == ExecutionStatus.SUCCESS
    assert "NETWORK_BLOCKED" in res.stdout
    assert "NETWORK_ACCESSIBLE" not in res.stdout


def test_security_host_filesystem_isolation(runner):
    """Verify container cannot access host filesystem paths."""
    code = """import os
print("HOST_HOME_FOUND:", os.path.exists("/home/tejas"))
print("PROJECT_FOUND:", os.path.exists("/home/tejas/Desktop/Bhasa2code"))
"""
    req = ExecutionRequest(language="python", code=code)
    res = runner.execute(req)

    assert res.status == ExecutionStatus.SUCCESS
    assert "HOST_HOME_FOUND: False" in res.stdout
    assert "PROJECT_FOUND: False" in res.stdout


def test_security_non_root_execution(runner):
    """Verify container runs strictly as unprivileged non-root user."""
    code = """import os, getpass
print("USER:", getpass.getuser())
print("UID:", os.getuid())
"""
    req = ExecutionRequest(language="python", code=code)
    res = runner.execute(req)

    assert res.status == ExecutionStatus.SUCCESS
    assert "USER: sandbox" in res.stdout
    assert "UID: 1000" in res.stdout
    assert "root" not in res.stdout


def test_security_docker_socket_unavailable(runner):
    """Verify Docker socket is not mounted into container."""
    code = """import os
print("SOCK_EXISTS:", os.path.exists("/var/run/docker.sock"))
"""
    req = ExecutionRequest(language="python", code=code)
    res = runner.execute(req)

    assert res.status == ExecutionStatus.SUCCESS
    assert "SOCK_EXISTS: False" in res.stdout


def test_security_environment_isolation(runner):
    """Verify container does not inherit sensitive host environment variables."""
    # Set a test environment variable on host
    os.environ["SECRET_HOST_TOKEN_XYZ"] = "host_secret_value"

    code = """import os
print("SECRET_EXISTS:", "SECRET_HOST_TOKEN_XYZ" in os.environ)
"""
    req = ExecutionRequest(language="python", code=code)
    res = runner.execute(req)

    assert res.status == ExecutionStatus.SUCCESS
    assert "SECRET_EXISTS: False" in res.stdout


def test_security_process_fork_abuse(runner):
    """Verify process fork bomb is constrained by PID limits."""
    code = """import os, time
count = 0
try:
    for _ in range(100):
        pid = os.fork()
        if pid == 0:
            time.sleep(1)
            os._exit(0)
        count += 1
    print("FORKED_ALL")
except (BlockingIOError, OSError):
    print("FORK_BLOCKED_BY_LIMIT")
"""
    req = ExecutionRequest(language="python", code=code)
    res = runner.execute(req)

    # Must either report success with fork blocked, or be bounded
    assert res.status in (ExecutionStatus.SUCCESS, ExecutionStatus.RESOURCE_LIMIT)
    if res.status == ExecutionStatus.SUCCESS:
        assert "FORK_BLOCKED_BY_LIMIT" in res.stdout


def test_security_memory_abuse_resource_limit(runner):
    """Verify runaway memory allocation triggers RESOURCE_LIMIT termination."""
    code = """x = []
while True:
    x.append("A" * (1024 * 1024))
"""
    # Create runner with tight memory limit (32MB)
    cfg = SandboxConfig(
        timeout_seconds=5.0,
        memory_limit_mb=32,
    )
    custom_runner = SandboxRunner(config=cfg)
    req = ExecutionRequest(language="python", code=code)
    res = custom_runner.execute(req)

    assert res.status == ExecutionStatus.RESOURCE_LIMIT
    assert res.exit_code == 137


def test_security_invalid_t18_code_rejected_before_docker(runner):
    """Verify malformed code is caught by T18 and does NOT execute in Docker."""
    # Syntax error in Python (missing colon)
    bad_code = """def add(a, b)
    return a + b
"""
    req = ExecutionRequest(language="python", code=bad_code)
    res = runner.execute(req)

    assert res.status == ExecutionStatus.VALIDATION_FAILED
    assert res.language == "python"
    assert len(res.diagnostics) > 0


def test_cleanup_verification(runner):
    """Verify no lingering containers or volumes remain after execution."""
    # List initial active containers with b2c prefix
    before = subprocess.check_output(
        ["docker", "ps", "-a", "--filter", "name=b2c-run-", "--format", "{{.ID}}"],
        text=True,
    ).strip()

    req = ExecutionRequest(language="python", code="print('cleanup check')")
    res = runner.execute(req)
    assert res.status == ExecutionStatus.SUCCESS

    after = subprocess.check_output(
        ["docker", "ps", "-a", "--filter", "name=b2c-run-", "--format", "{{.ID}}"],
        text=True,
    ).strip()

    assert before == after

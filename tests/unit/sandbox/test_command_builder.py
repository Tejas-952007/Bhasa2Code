"""Unit tests for language execution plans and Docker command builder."""

import pytest
from backend.app.sandbox.config import SandboxConfig
from backend.app.sandbox.docker_runtime import DockerRuntime
from backend.app.sandbox.languages import (
    CRunner,
    CppRunner,
    JavaRunner,
    JavaScriptRunner,
    PythonRunner,
    get_language_runner,
    normalize_sandbox_language,
)


def test_language_normalization():
    """Verify language alias normalization."""
    assert normalize_sandbox_language("PYTHON") == "python"
    assert normalize_sandbox_language("py") == "python"
    assert normalize_sandbox_language("c++") == "cpp"
    assert normalize_sandbox_language("js") == "javascript"
    assert normalize_sandbox_language("node") == "javascript"


def test_python_plan_builder():
    """Verify Python execution plan construction."""
    runner = PythonRunner()
    cfg = SandboxConfig()
    plan = runner.build_plan("print(42)", cfg)

    assert plan.language == "python"
    assert plan.files == {"main.py": "print(42)"}
    assert plan.entrypoint == ["python3", "-u", "main.py"]
    assert plan.image_tag == cfg.image_tags["python"]


def test_c_plan_builder():
    """Verify C execution plan construction."""
    runner = CRunner()
    cfg = SandboxConfig()
    plan = runner.build_plan("int main() { return 0; }", cfg)

    assert plan.language == "c"
    assert plan.files == {"main.c": "int main() { return 0; }"}
    assert plan.entrypoint == ["sh", "-c", "gcc -O2 main.c -o /workspace/prog && /workspace/prog"]


def test_cpp_plan_builder():
    """Verify C++ execution plan construction."""
    runner = CppRunner()
    cfg = SandboxConfig()
    plan = runner.build_plan("int main() { return 0; }", cfg)

    assert plan.language == "cpp"
    assert plan.files == {"main.cpp": "int main() { return 0; }"}
    assert plan.entrypoint == ["sh", "-c", "g++ -O2 -std=c++17 main.cpp -o /workspace/prog && /workspace/prog"]


def test_java_plan_builder_public_class():
    """Verify Java class name detection and plan building."""
    runner = JavaRunner()
    cfg = SandboxConfig()
    code = "public class Solution { public static void main(String[] args) {} }"
    plan = runner.build_plan(code, cfg)

    assert plan.language == "java"
    assert "Solution.java" in plan.files
    assert plan.entrypoint == ["sh", "-c", "javac Solution.java && java Solution"]


def test_javascript_plan_builder():
    """Verify JavaScript execution plan construction."""
    runner = JavaScriptRunner()
    cfg = SandboxConfig()
    plan = runner.build_plan("console.log(1);", cfg)

    assert plan.language == "javascript"
    assert plan.files == {"main.js": "console.log(1);"}
    assert plan.entrypoint == ["node", "main.js"]


def test_docker_command_builder_array_format():
    """Verify Docker command arguments are built strictly as argument arrays."""
    cfg = SandboxConfig(
        memory_limit_mb=128,
        cpu_limit=0.5,
        pids_limit=32,
    )
    runtime = DockerRuntime(config=cfg)
    # Mock no_new_privs probe to True
    runtime._no_new_privs_supported = True

    runner = PythonRunner()
    plan = runner.build_plan("print('hi')", cfg)

    args = runtime.build_docker_run_args(
        plan=plan,
        volume_name="b2c-vol-test",
        container_name="b2c-run-test",
    )

    assert isinstance(args, list)
    assert args[0] == "docker"
    assert "run" in args
    assert "--rm" in args
    assert "--network" in args and "none" in args
    assert "--cap-drop" in args and "ALL" in args
    assert "--read-only" in args
    assert "--memory" in args and "128m" in args
    assert "--cpus" in args and "0.5" in args
    assert "--pids-limit" in args and "32" in args
    assert "--user" in args and "1000:1000" in args
    assert "-v" in args and "b2c-vol-test:/workspace:rw" in args
    assert plan.image_tag in args
    assert args[-3:] == ["python3", "-u", "main.py"]


def test_malicious_code_never_injected_into_host_command():
    """Verify malicious shell commands in code never leak into Docker argument array."""
    cfg = SandboxConfig()
    runtime = DockerRuntime(config=cfg)
    runtime._no_new_privs_supported = False

    malicious_code = '"; rm -rf /; $(whoami); && curl attacker.com #"'
    runner = PythonRunner()
    plan = runner.build_plan(malicious_code, cfg)

    args = runtime.build_docker_run_args(
        plan=plan,
        volume_name="b2c-vol-safe",
        container_name="b2c-run-safe",
    )

    # Malicious string should NOT appear anywhere in the docker arguments array
    assert malicious_code not in args
    assert "rm -rf /" not in " ".join(args)
    assert "curl attacker.com" not in " ".join(args)
    # The code is securely stored in plan.files dictionary
    assert plan.files["main.py"] == malicious_code

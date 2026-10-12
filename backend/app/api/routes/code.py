"""Code validation and secure sandbox execution API endpoints."""

import asyncio
import logging
from typing import Optional
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect

from backend.app.api.deps import get_response_validator, get_sandbox_runner
from backend.app.api.schemas import (
    CodeRunRequest,
    CodeRunResponse,
    CodeValidateRequest,
    CodeValidateResponse,
)
from backend.app.sandbox.interactive_session import (
    InteractiveDockerSession,
    register_session,
    unregister_session,
)
from backend.app.sandbox.languages import get_language_runner, normalize_sandbox_language
from backend.app.sandbox.sandbox_runner import ExecutionRequest, SandboxRunner
from backend.app.validation.response_validator import ResponseValidator
from backend.app.validation.schemas import ValidationStatus

logger = logging.getLogger("bhasha2code.api.code")

router = APIRouter(prefix="/code", tags=["code"])


@router.post(
    "/validate",
    response_model=CodeValidateResponse,
    summary="Validate code snippet syntax",
)
def validate_code(
    payload: CodeValidateRequest,
    validator: ResponseValidator = Depends(get_response_validator),
) -> CodeValidateResponse:
    """Perform static syntax analysis on code without running it."""
    lang_norm = normalize_sandbox_language(payload.language) or payload.language.lower().strip()
    line_count = len(payload.code.splitlines()) if payload.code else 0

    if lang_norm in validator.validators:
        val_inst = validator.validators[lang_norm]
        result = val_inst.validate(payload.code)
        is_valid = result.status == ValidationStatus.VALID
        diagnostics = [
            f"[{d.severity}] {d.message}" + (f" (line {d.line})" if d.line else "")
            for d in result.diagnostics
        ]
        status_str = result.status.value.upper()
    else:
        is_valid = False
        diagnostics = [f"Language '{payload.language}' is not supported for static validation."]
        status_str = "UNSUPPORTED"

    return CodeValidateResponse(
        language=lang_norm,
        status=status_str,
        is_valid=is_valid,
        diagnostics=diagnostics,
        line_count=line_count,
    )


@router.post(
    "/run",
    response_model=CodeRunResponse,
    summary="Execute validated code in secure Docker sandbox",
)
def run_code(
    payload: CodeRunRequest,
    sandbox: SandboxRunner = Depends(get_sandbox_runner),
) -> CodeRunResponse:
    """Execute code in an isolated Docker container with resource quotas.

    Gates automatically through T18 Static Validation prior to invocation.
    """
    request = ExecutionRequest(
        language=payload.language,
        code=payload.code,
        stdin=payload.stdin or "",
    )

    result = sandbox.execute(request)

    return CodeRunResponse(
        status=result.status.value.upper(),
        stdout=result.stdout,
        stderr=result.stderr,
        exit_code=result.exit_code if result.exit_code is not None else (0 if result.status.value == "SUCCESS" else 1),
        duration_ms=round(result.duration_ms, 2) if result.duration_ms is not None else 0.0,
        diagnostics=result.diagnostics,
    )


@router.websocket("/interactive-run")
async def interactive_run_endpoint(
    websocket: WebSocket,
    validator: ResponseValidator = Depends(get_response_validator),
    sandbox: SandboxRunner = Depends(get_sandbox_runner),
) -> None:
    """Live bidirectional interactive execution session over WebSocket.

    Validates untrusted code through T18 gate, isolates in Docker sandbox,
    and supports streaming stdin, stdout, stderr, and signals.
    """
    await websocket.accept()
    session: Optional[InteractiveDockerSession] = None
    session_id: Optional[str] = None

    try:
        # 1. Receive initial 'start' handshake
        init_data = await websocket.receive_json()
        if not isinstance(init_data, dict) or init_data.get("type") != "start":
            await websocket.send_json({
                "type": "error",
                "error_type": "PROTOCOL_ERROR",
                "message": "First message must be of type 'start' with 'language' and 'code'.",
            })
            await websocket.close()
            return

        language = str(init_data.get("language") or "python").strip()
        code = str(init_data.get("code") or "")

        canonical_lang = normalize_sandbox_language(language)
        if not canonical_lang or canonical_lang not in validator.validators:
            await websocket.send_json({
                "type": "error",
                "error_type": "UNSUPPORTED",
                "message": f"Language '{language}' is not supported for interactive execution.",
            })
            await websocket.close()
            return

        # 2. T18 Syntax Validation Gate
        val_inst = validator.validators[canonical_lang]
        val_res = val_inst.validate(code)
        if val_res.status != ValidationStatus.VALID:
            diagnostics = [
                f"[{d.severity}] {d.message}" + (f" (line {d.line})" if d.line else "")
                for d in val_res.diagnostics
            ]
            await websocket.send_json({
                "type": "error",
                "error_type": "VALIDATION_FAILED",
                "message": "Syntax validation failed prior to execution.",
                "diagnostics": diagnostics or ["Syntax validation failed."],
            })
            await websocket.close()
            return

        # 3. Check Docker daemon availability
        if not sandbox.is_available():
            await websocket.send_json({
                "type": "error",
                "error_type": "SANDBOX_ERROR",
                "message": "Docker runtime is unavailable or daemon is not accessible.",
            })
            await websocket.close()
            return

        # 4. Build language execution plan
        try:
            runner = get_language_runner(canonical_lang)
            plan = runner.build_plan(code, sandbox.config)
        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "error_type": "SANDBOX_ERROR",
                "message": f"Failed to build execution plan: {str(e)}",
            })
            await websocket.close()
            return

        # 5. Create & register interactive session
        session = InteractiveDockerSession(
            language=canonical_lang,
            code=code,
            docker_runtime=sandbox.docker_runtime,
        )
        session_id = session.session_id

        registered = await register_session(session)
        if not registered:
            await websocket.send_json({
                "type": "error",
                "error_type": "RESOURCE_LIMIT",
                "message": "Maximum concurrent interactive sessions reached. Please wait and try again.",
            })
            await websocket.close()
            return

        # 6. Stage and launch container
        try:
            await session.stage_and_start(plan)
        except Exception as e:
            await websocket.send_json({
                "type": "error",
                "error_type": "SANDBOX_ERROR",
                "message": f"Container startup failed: {str(e)}",
            })
            await websocket.close()
            return

        await websocket.send_json({"type": "started"})

        # 7. Asynchronous stream forwarding tasks
        async def forward_stdout():
            while session.is_running():
                chunk = await session.read_stdout_chunk()
                if chunk:
                    await websocket.send_json({"type": "stdout", "data": chunk})
                else:
                    await asyncio.sleep(0.01)

        async def forward_stderr():
            while session.is_running():
                chunk = await session.read_stderr_chunk()
                if chunk:
                    await websocket.send_json({"type": "stderr", "data": chunk})
                else:
                    await asyncio.sleep(0.01)

        stdout_task = asyncio.create_task(forward_stdout())
        stderr_task = asyncio.create_task(forward_stderr())

        # 8. Main event loop: client messages and lifecycle checks
        while session.is_running():
            # Check timeouts and resource limits
            if session.hit_output_limit:
                await websocket.send_json({
                    "type": "resource_limit",
                    "message": "Output exceeded maximum limit. Execution terminated.",
                })
                await session.terminate()
                break

            if session.is_total_timed_out():
                await websocket.send_json({
                    "type": "timeout",
                    "message": f"Total execution time exceeded {session.total_timeout_seconds}s limit.",
                })
                await session.terminate()
                break

            if session.is_idle_timed_out():
                await websocket.send_json({
                    "type": "timeout",
                    "message": f"Input wait idle timeout exceeded ({session.idle_timeout_seconds}s).",
                })
                await session.terminate()
                break

            # Poll client messages with a 50ms timeout so we keep monitoring process status
            try:
                client_msg = await asyncio.wait_for(websocket.receive_json(), timeout=0.05)
            except asyncio.TimeoutError:
                continue
            except WebSocketDisconnect:
                logger.info("Client disconnected from interactive session %s", session_id)
                await session.terminate()
                break

            msg_type = client_msg.get("type")
            if msg_type == "stdin":
                input_data = str(client_msg.get("data", ""))
                try:
                    await session.write_stdin(input_data)
                except Exception as e:
                    logger.debug("Failed to write stdin: %s", e)
            elif msg_type == "terminate":
                logger.info("Client requested termination of session %s", session_id)
                await session.terminate()
                break

        # Cancel stream tasks
        stdout_task.cancel()
        stderr_task.cancel()
        await asyncio.gather(stdout_task, stderr_task, return_exceptions=True)

        # Drain any residual stdout/stderr
        while True:
            rem_out = await session.read_stdout_chunk()
            if not rem_out:
                break
            await websocket.send_json({"type": "stdout", "data": rem_out})

        while True:
            rem_err = await session.read_stderr_chunk()
            if not rem_err:
                break
            await websocket.send_json({"type": "stderr", "data": rem_err})

        # Process completion
        exit_code = session.proc.returncode if (session.proc and session.proc.returncode is not None) else 0
        duration_ms = session.get_duration_ms()

        try:
            await websocket.send_json({
                "type": "completed",
                "exit_code": exit_code,
                "duration_ms": duration_ms,
            })
            await websocket.close()
        except Exception:
            pass

    except WebSocketDisconnect:
        logger.info("Interactive session disconnected: %s", session_id)
    except Exception as e:
        logger.error("Error in interactive session %s: %s", session_id, e, exc_info=True)
        try:
            await websocket.send_json({
                "type": "error",
                "error_type": "INTERNAL_ERROR",
                "message": f"Session error: {str(e)}",
            })
            await websocket.close()
        except Exception:
            pass
    finally:
        if session_id:
            await unregister_session(session_id)
        if session:
            await session.terminate()


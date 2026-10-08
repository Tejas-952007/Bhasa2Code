"""Code validation and secure sandbox execution API endpoints."""

import logging
from fastapi import APIRouter, Depends

from backend.app.api.deps import get_response_validator, get_sandbox_runner
from backend.app.api.schemas import (
    CodeRunRequest,
    CodeRunResponse,
    CodeValidateRequest,
    CodeValidateResponse,
)
from backend.app.sandbox.languages import normalize_sandbox_language
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

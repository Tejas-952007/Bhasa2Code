from contextlib import asynccontextmanager
import logging
from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from backend.app.api.exceptions import APIException
from backend.app.api.routes.chat import router as chat_router
from backend.app.api.routes.chat_stream import router as chat_stream_router
from backend.app.api.routes.code import router as code_router
from backend.app.api.routes.health import router as health_router
from backend.app.api.routes.sessions import router as sessions_router
from backend.app.core.config import settings
from backend.app.database.engine import init_db

logger = logging.getLogger("bhasha2code")


def cleanup_orphaned_sandbox_resources():
    """Prune any leaked b2c-run containers or b2c-vol volumes on startup or shutdown."""
    import subprocess
    try:
        res = subprocess.run(
            ["docker", "ps", "-aq", "--filter", "name=b2c-run"],
            capture_output=True,
            text=True,
            timeout=3.0,
            check=False,
        )
        if res.stdout.strip():
            cids = res.stdout.strip().split()
            subprocess.run(["docker", "rm", "-f"] + cids, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5.0, check=False)
        v_res = subprocess.run(
            ["docker", "volume", "ls", "-q", "--filter", "name=b2c-vol"],
            capture_output=True,
            text=True,
            timeout=3.0,
            check=False,
        )
        if v_res.stdout.strip():
            vols = v_res.stdout.strip().split()
            subprocess.run(["docker", "volume", "rm", "-f"] + vols, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=5.0, check=False)
    except Exception:
        pass


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize database on startup
    init_db()
    cleanup_orphaned_sandbox_resources()
    yield
    cleanup_orphaned_sandbox_resources()


app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Offline Multilingual AI Coding & Study Assistant",
    version="1.0.0",
    lifespan=lifespan,
)

# Configure CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.exception_handler(APIException)
async def api_exception_handler(request: Request, exc: APIException) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError) -> JSONResponse:
    logger.warning("Validation error on %s: %s", request.url.path, exc)
    return JSONResponse(
        status_code=400,
        content={"error": {"code": "BAD_REQUEST", "message": "Invalid request parameters."}},
    )


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled error processing %s: %s", request.url.path, exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": {"code": "INTERNAL_ERROR", "message": "Internal server error"}},
    )


# Include API routes
# Note: chat_stream_router must be registered before chat_router (more specific prefix /chat/stream first)
app.include_router(health_router)
app.include_router(sessions_router, prefix=settings.API_V1_STR)
app.include_router(chat_stream_router, prefix=settings.API_V1_STR)
app.include_router(chat_router, prefix=settings.API_V1_STR)
app.include_router(code_router, prefix=settings.API_V1_STR)

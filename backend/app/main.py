import logging
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from backend.app.core.config import settings
from backend.app.api.routes.health import router as health_router

logger = logging.getLogger("bhasha2code")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="Offline Multilingual AI Coding & Study Assistant",
    version="1.0.0",
)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unhandled error processing %s: %s", request.url.path, exc, exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"detail": "Internal server error"},
    )


app.include_router(health_router)

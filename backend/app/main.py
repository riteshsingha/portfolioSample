"""FastAPI application entry point.

Run locally with:
    uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
"""

from __future__ import annotations

import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from .config import get_settings
from .routes.contact import limiter
from .routes.contact import router as contact_router

settings = get_settings()

logging.basicConfig(
    level=settings.LOG_LEVEL,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
log = logging.getLogger(__name__)

app = FastAPI(
    title="Ritesh Singha — Portfolio API",
    description="Backend service for the portfolio contact form.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=False,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["Content-Type", "Accept"],
)

# Wire slowapi into FastAPI.
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.include_router(contact_router)


@app.get("/api/health", tags=["health"], summary="Liveness probe")
async def health() -> dict[str, str | bool]:
    return {
        "status": "ok",
        "smtp_configured": settings.smtp_configured,
    }


@app.on_event("startup")
async def _on_startup() -> None:
    if not settings.smtp_configured:
        log.warning(
            "SMTP is NOT configured. The /api/contact endpoint will return 502 until "
            "SMTP_USER, SMTP_PASSWORD, and MAIL_TO are set in backend/.env"
        )
    else:
        log.info("SMTP configured (host=%s:%s, to=%s)",
                 settings.SMTP_HOST, settings.SMTP_PORT, settings.MAIL_TO)
    log.info("CORS origins allowed: %s", ", ".join(settings.CORS_ORIGINS))

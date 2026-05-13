"""Application settings, loaded from a `.env` file at the backend root."""

from __future__ import annotations

import os
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv

BACKEND_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = BACKEND_ROOT / ".env"
load_dotenv(ENV_PATH)


def _csv(name: str, default: str) -> list[str]:
    raw = os.getenv(name, default)
    return [item.strip() for item in raw.split(",") if item.strip()]


class Settings:
    """Runtime configuration sourced from environment variables."""

    # ── SMTP ──
    SMTP_HOST: str = os.getenv("SMTP_HOST", "smtp.gmail.com")
    SMTP_PORT: int = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER: str = os.getenv("SMTP_USER", "")
    SMTP_PASSWORD: str = os.getenv("SMTP_PASSWORD", "")  # Gmail App Password

    # ── Mail metadata ──
    MAIL_TO: str = os.getenv("MAIL_TO", "") or os.getenv("SMTP_USER", "")
    MAIL_FROM_NAME: str = os.getenv("MAIL_FROM_NAME", "Portfolio Contact Form")

    # ── CORS ──
    CORS_ORIGINS: list[str] = _csv(
        "CORS_ORIGINS",
        "http://localhost:8080,http://127.0.0.1:8080,"
        "http://localhost:5500,http://127.0.0.1:5500",
    )

    # ── Rate limiting (slowapi syntax, e.g. "5/minute") ──
    RATE_LIMIT: str = os.getenv("RATE_LIMIT", "5/minute")

    # ── Misc ──
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

    @property
    def smtp_configured(self) -> bool:
        return bool(self.SMTP_USER and self.SMTP_PASSWORD and self.MAIL_TO)


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()

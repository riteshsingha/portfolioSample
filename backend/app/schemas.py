"""Pydantic request/response models for the contact API."""

from __future__ import annotations

from pydantic import BaseModel, ConfigDict, EmailStr, Field


class ContactIn(BaseModel):
    """Payload submitted by the portfolio contact form."""

    model_config = ConfigDict(str_strip_whitespace=True, extra="ignore")

    name: str = Field(min_length=2, max_length=80, description="Sender's full name")
    email: EmailStr = Field(description="Sender's reply-to email address")
    subject: str = Field(min_length=2, max_length=120)
    message: str = Field(min_length=10, max_length=5000)

    # Honeypot — invisible to humans, bots fill it in. Reject silently if present.
    website: str | None = Field(
        default=None,
        max_length=200,
        description="Honeypot field. Leave blank.",
    )


class ContactOut(BaseModel):
    ok: bool
    message: str

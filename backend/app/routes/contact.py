"""Public contact-form endpoint.

POST /api/contact  →  validates payload → checks honeypot → sends email.
Rate-limited per IP via slowapi.
"""

from __future__ import annotations

import logging

from fastapi import APIRouter, HTTPException, Request, status
from slowapi import Limiter
from slowapi.util import get_remote_address

from ..config import get_settings
from ..email_service import EmailDeliveryError, send_contact_email
from ..schemas import ContactIn, ContactOut

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api", tags=["contact"])

# A module-level limiter so the decorator below picks it up.
# `app.main` registers `app.state.limiter = limiter` to wire it into FastAPI.
limiter = Limiter(key_func=get_remote_address)


@router.post(
    "/contact",
    response_model=ContactOut,
    status_code=status.HTTP_200_OK,
    summary="Submit a contact-form message",
)
@limiter.limit(get_settings().RATE_LIMIT)
async def submit_contact(payload: ContactIn, request: Request) -> ContactOut:
    client_ip = request.client.host if request.client else "unknown"

    # Honeypot — silently accept and discard so bots can't tell they were caught.
    if payload.website:
        logger.warning("Honeypot triggered (ip=%s, value=%r)", client_ip, payload.website)
        return ContactOut(ok=True, message="Thanks! Your message has been sent.")

    try:
        send_contact_email(payload)
    except EmailDeliveryError:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Couldn't send the message right now. Please try again later or email me directly.",
        )

    logger.info("Contact form submitted (ip=%s, email=%s)", client_ip, payload.email)
    return ContactOut(ok=True, message="Thanks! Your message has been sent.")

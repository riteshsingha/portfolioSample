"""SMTP email delivery for contact-form submissions.

Uses Python's standard library (`smtplib` + `email`) — no extra dependencies.
Designed for Gmail SMTP (smtp.gmail.com:587, STARTTLS, App Password).
"""

from __future__ import annotations

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.utils import formataddr, formatdate, make_msgid

from .config import get_settings
from .schemas import ContactIn

logger = logging.getLogger(__name__)


class EmailDeliveryError(RuntimeError):
    """Raised when the SMTP server rejects the message or is unreachable."""


def _escape_html(value: str) -> str:
    return (
        value.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&#39;")
    )


def _build_message(payload: ContactIn) -> MIMEMultipart:
    settings = get_settings()

    msg = MIMEMultipart("alternative")
    msg["Subject"] = f"[Portfolio] {payload.subject}"
    msg["From"] = formataddr((settings.MAIL_FROM_NAME, settings.SMTP_USER))
    msg["To"] = settings.MAIL_TO
    msg["Reply-To"] = formataddr((payload.name, payload.email))
    msg["Date"] = formatdate(localtime=True)
    msg["Message-ID"] = make_msgid(domain="portfolio.local")

    text_body = (
        "You received a new message via your portfolio contact form.\n\n"
        f"Name:    {payload.name}\n"
        f"Email:   {payload.email}\n"
        f"Subject: {payload.subject}\n\n"
        "Message:\n"
        f"{payload.message}\n"
    )

    safe_message = _escape_html(payload.message).replace("\n", "<br/>")
    html_body = f"""\
<!DOCTYPE html>
<html>
  <body style="font-family: -apple-system, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif; color: #1f2937; max-width: 640px; margin: 0 auto;">
    <div style="border-left: 4px solid #7c3aed; padding: 18px 22px; background: #faf5ff; border-radius: 8px;">
      <h2 style="margin: 0 0 12px; color: #7c3aed; font-size: 18px;">New portfolio contact</h2>
      <table cellpadding="6" cellspacing="0" style="border-collapse: collapse; font-size: 14px;">
        <tr><td><strong>Name</strong></td><td>{_escape_html(payload.name)}</td></tr>
        <tr><td><strong>Email</strong></td><td><a href="mailto:{_escape_html(payload.email)}">{_escape_html(payload.email)}</a></td></tr>
        <tr><td><strong>Subject</strong></td><td>{_escape_html(payload.subject)}</td></tr>
      </table>
    </div>
    <h3 style="margin: 22px 0 8px; font-size: 15px; color: #374151;">Message</h3>
    <p style="white-space: pre-wrap; line-height: 1.6; font-size: 14px; color: #1f2937;">{safe_message}</p>
    <hr style="margin: 24px 0; border: none; border-top: 1px solid #e5e7eb;" />
    <p style="font-size: 12px; color: #9ca3af;">Sent automatically from your portfolio contact form.</p>
  </body>
</html>
"""

    msg.attach(MIMEText(text_body, "plain", "utf-8"))
    msg.attach(MIMEText(html_body, "html", "utf-8"))
    return msg


def send_contact_email(payload: ContactIn) -> None:
    """Build and send a contact-form email via SMTP.

    Raises:
        EmailDeliveryError: when SMTP is misconfigured or sending fails.
    """
    settings = get_settings()

    if not settings.smtp_configured:
        raise EmailDeliveryError(
            "SMTP is not configured. Set SMTP_USER, SMTP_PASSWORD and MAIL_TO in .env."
        )

    msg = _build_message(payload)

    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=15) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.sendmail(settings.SMTP_USER, [settings.MAIL_TO], msg.as_string())
    except (smtplib.SMTPException, OSError) as exc:
        logger.exception("SMTP delivery failed")
        raise EmailDeliveryError(str(exc)) from exc

    logger.info("Contact email delivered (from=%s, to=%s)", payload.email, settings.MAIL_TO)

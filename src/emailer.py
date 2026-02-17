"""Email sending module for the MASH Newsletter."""

from __future__ import annotations

import logging
import re
import smtplib
from email.message import EmailMessage
from datetime import datetime, timezone

from src.config import (
    SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD,
    SENDER_EMAIL, RECIPIENT_EMAIL,
)

logger = logging.getLogger(__name__)


def _clean(text: str) -> str:
    """Replace non-breaking spaces and other common non-ASCII whitespace."""
    return re.sub(r"[\xa0\u200b\u200c\u200d\ufeff]", " ", text)


def send_newsletter(
    html_content: str,
    plain_text: str,
    recipient: str = RECIPIENT_EMAIL,
    subject: str | None = None,
) -> bool:
    """
    Send the newsletter via SMTP.

    Returns True if sent successfully, False otherwise.
    Requires SMTP_USER and SMTP_PASSWORD environment variables.
    """
    # Diagnostic logging so Actions logs show exactly what's missing
    logger.info("SMTP_SERVER: %s", SMTP_SERVER)
    logger.info("SMTP_PORT: %s", SMTP_PORT)
    logger.info("SMTP_USER: %s", SMTP_USER[:3] + "***" if SMTP_USER else "<empty>")
    logger.info("SMTP_PASSWORD: %s", "****" if SMTP_PASSWORD else "<empty>")
    logger.info("SENDER_EMAIL: %s", SENDER_EMAIL or "<empty>")
    logger.info("Recipient: %s", recipient)

    if not SMTP_USER or not SMTP_PASSWORD:
        logger.error(
            "SMTP credentials not configured! Set SMTP_USER and SMTP_PASSWORD "
            "as GitHub repository secrets. Newsletter saved to output/ but NOT emailed."
        )
        return False

    if subject is None:
        date_str = datetime.now(timezone.utc).strftime("%b %d, %Y")
        subject = f"MASH Intelligence Report - {date_str}"

    # Sanitise every string that touches the email – non-breaking spaces (\xa0)
    # and other invisible Unicode can creep in from web-scraped content, secrets
    # copy-pasted from web pages, or template rendering.
    html_content = _clean(html_content)
    plain_text = _clean(plain_text)
    subject = _clean(subject)
    smtp_user = _clean(SMTP_USER).strip()
    smtp_pass = _clean(SMTP_PASSWORD)
    sender = _clean(SENDER_EMAIL or SMTP_USER).strip()
    recipient = _clean(recipient).strip()

    # Use modern EmailMessage API with UTF-8 support – avoids the compat32
    # policy's ASCII-only header serialisation that caused the \xa0 crash.
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = recipient
    msg.set_content(plain_text, subtype="plain")
    msg.add_alternative(html_content, subtype="html")

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(smtp_user, smtp_pass)
            server.sendmail(smtp_user, [recipient], msg.as_bytes())
        logger.info("Newsletter emailed to %s", recipient)
        return True
    except smtplib.SMTPAuthenticationError as e:
        logger.error(
            "SMTP authentication failed: %s. "
            "If using Gmail, you need an App Password (not your regular password). "
            "Go to https://myaccount.google.com/apppasswords to generate one.",
            e,
        )
        return False
    except smtplib.SMTPException as e:
        logger.error("Failed to send email: %s", e)
        return False
    except Exception as e:
        logger.error("Unexpected error sending email: %s", e)
        return False

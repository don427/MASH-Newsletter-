"""Email sending module for the MASH Newsletter."""

from __future__ import annotations

import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, timezone

from src.config import (
    SMTP_SERVER, SMTP_PORT, SMTP_USER, SMTP_PASSWORD,
    SENDER_EMAIL, RECIPIENT_EMAIL,
)

logger = logging.getLogger(__name__)


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
        subject = f"MASH Weekly Intelligence - {date_str}"

    # Sanitise non-breaking spaces (\xa0) that creep in from web-scraped
    # content – they cause 'ascii' codec errors during message serialisation.
    html_content = html_content.replace("\xa0", " ")
    plain_text = plain_text.replace("\xa0", " ")

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject
    msg["From"] = SENDER_EMAIL or SMTP_USER
    msg["To"] = recipient

    # Attach plain text (fallback) and HTML (preferred)
    msg.attach(MIMEText(plain_text, "plain", "utf-8"))
    msg.attach(MIMEText(html_content, "html", "utf-8"))

    try:
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=30) as server:
            server.ehlo()
            server.starttls()
            server.ehlo()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.sendmail(SMTP_USER, [recipient], msg.as_bytes())
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

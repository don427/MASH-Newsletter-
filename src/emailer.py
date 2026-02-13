"""Email sending module for the MASH Newsletter."""

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
    if not SMTP_USER or not SMTP_PASSWORD:
        logger.warning(
            "SMTP credentials not configured. Set SMTP_USER and SMTP_PASSWORD "
            "environment variables. Newsletter saved to output/ but not emailed."
        )
        return False

    if subject is None:
        date_str = datetime.now(timezone.utc).strftime("%b %d, %Y")
        subject = f"MASH Weekly Intelligence - {date_str}"

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
            server.sendmail(SMTP_USER, [recipient], msg.as_string())
        logger.info("Newsletter emailed to %s", recipient)
        return True
    except smtplib.SMTPException as e:
        logger.error("Failed to send email: %s", e)
        return False

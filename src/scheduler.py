"""Scheduler for weekly Monday morning newsletter delivery."""

import logging
import time

import schedule

from src.config import SEND_DAY, SEND_TIME

logger = logging.getLogger(__name__)


def start_scheduler(job_func):
    """
    Schedule the newsletter job for every Monday at the configured time.
    This function blocks and runs the schedule loop.
    """
    getattr(schedule.every(), SEND_DAY).at(SEND_TIME).do(job_func)
    logger.info("Scheduled newsletter for every %s at %s", SEND_DAY, SEND_TIME)
    logger.info("Scheduler running. Press Ctrl+C to stop.")

    try:
        while True:
            schedule.run_pending()
            time.sleep(60)
    except KeyboardInterrupt:
        logger.info("Scheduler stopped.")

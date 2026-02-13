#!/usr/bin/env python3
"""
MASH Newsletter Agent - Main Entry Point

Usage:
    python run.py              # Generate and send newsletter now
    python run.py --now        # Same as above (explicit)
    python run.py --schedule   # Start the weekly scheduler (runs every Monday)
    python run.py --dry-run    # Generate newsletter but don't email it
    python run.py --curated    # Use curated web-search data instead of live APIs
"""

import argparse
import logging
import sys

from src.news_fetcher import fetch_all_news
from src.pubmed_fetcher import fetch_all_publications
from src.trials_fetcher import fetch_all_trials
from src.web_search_fetcher import fetch_all_curated_content
from src.formatter import render_newsletter, render_plain_text
from src.emailer import send_newsletter
from src.scheduler import start_scheduler
from src.config import LOOKBACK_DAYS, RECIPIENT_EMAIL

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)
logger = logging.getLogger("mash-newsletter")


def generate_and_send(
    dry_run: bool = False,
    lookback_days: int = LOOKBACK_DAYS,
    use_curated: bool = False,
) -> str:
    """Core pipeline: fetch -> format -> send. Returns the output filepath."""
    logger.info("=" * 60)
    logger.info("MASH Newsletter Agent - Starting collection")
    logger.info("Looking back %d days", lookback_days)
    logger.info("=" * 60)

    if use_curated:
        logger.info("Using curated web-search content...")
        news, publications, trials = fetch_all_curated_content()
    else:
        # 1. Fetch from all live sources
        logger.info("Fetching industry news from RSS feeds...")
        news = fetch_all_news(lookback_days)
        logger.info("Found %d news articles", len(news))

        logger.info("Fetching publications from PubMed...")
        publications = fetch_all_publications(lookback_days)
        logger.info("Found %d publications", len(publications))

        logger.info("Fetching clinical trial updates...")
        trials = fetch_all_trials(lookback_days)
        logger.info("Found %d trial updates", len(trials))

        # If live sources returned nothing, fall back to curated
        total_live = len(news) + len(publications) + len(trials)
        if total_live == 0:
            logger.warning("Live sources returned 0 results. Falling back to curated content.")
            news, publications, trials = fetch_all_curated_content()

    total = len(news) + len(publications) + len(trials)
    logger.info("Total items collected: %d", total)

    # 2. Render newsletter
    logger.info("Rendering newsletter...")
    html_content, filepath = render_newsletter(news, publications, trials, lookback_days)
    plain_text = render_plain_text(news, publications, trials)
    logger.info("Newsletter rendered: %s", filepath)

    # 3. Send email (unless dry-run)
    if dry_run:
        logger.info("DRY RUN - Newsletter not emailed. Saved to: %s", filepath)
    else:
        sent = send_newsletter(html_content, plain_text, RECIPIENT_EMAIL)
        if sent:
            logger.info("Newsletter emailed to %s", RECIPIENT_EMAIL)
        else:
            logger.warning(
                "Email not sent (check SMTP config). Newsletter saved to: %s", filepath
            )

    return filepath


def main():
    parser = argparse.ArgumentParser(
        description="MASH Newsletter Agent - Weekly MASH/NASH intelligence digest"
    )
    parser.add_argument(
        "--now", action="store_true", default=True,
        help="Generate and send the newsletter immediately (default)"
    )
    parser.add_argument(
        "--schedule", action="store_true",
        help="Start the weekly scheduler (runs every Monday at 7 AM)"
    )
    parser.add_argument(
        "--dry-run", action="store_true",
        help="Generate newsletter but don't send email"
    )
    parser.add_argument(
        "--curated", action="store_true",
        help="Use curated web-search data instead of live API fetchers"
    )
    parser.add_argument(
        "--lookback", type=int, default=LOOKBACK_DAYS,
        help=f"Number of days to look back (default: {LOOKBACK_DAYS})"
    )
    args = parser.parse_args()

    if args.schedule:
        logger.info("Starting weekly scheduler...")
        start_scheduler(
            lambda: generate_and_send(dry_run=args.dry_run, use_curated=args.curated)
        )
    else:
        filepath = generate_and_send(
            dry_run=args.dry_run,
            lookback_days=args.lookback,
            use_curated=args.curated,
        )
        print(f"\nNewsletter saved to: {filepath}")


if __name__ == "__main__":
    main()

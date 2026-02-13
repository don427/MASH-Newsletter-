"""Fetches MASH-related news from RSS feeds and industry sources."""

import re
import logging
from datetime import datetime, timedelta, timezone
from typing import Optional

import requests
from bs4 import BeautifulSoup
from dateutil import parser as dateparser

from src.config import NEWS_FEEDS, LOOKBACK_DAYS, RELEVANCE_REQUIRED_KEYWORDS, EXCLUSION_KEYWORDS

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 15
HEADERS = {
    "User-Agent": "MASH-Newsletter-Agent/1.0 (research newsletter aggregator)"
}


def _matches_keywords(text: str, keywords: list[str]) -> bool:
    """Check if text contains any of the given keywords (case-insensitive)."""
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def _is_relevant(text: str) -> bool:
    """Verify article is about MASH/NASH/fatty liver disease."""
    return _matches_keywords(text, RELEVANCE_REQUIRED_KEYWORDS)


def _should_exclude(text: str) -> bool:
    """Exclude animal studies, cell biology, phase 1, and preclinical content."""
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in EXCLUSION_KEYWORDS)


def _parse_date(date_str: str) -> Optional[datetime]:
    """Parse a date string into a timezone-aware datetime."""
    if not date_str:
        return None
    try:
        dt = dateparser.parse(date_str)
        if dt and dt.tzinfo is None:
            dt = dt.replace(tzinfo=timezone.utc)
        return dt
    except (ValueError, OverflowError):
        return None


def _clean_html(html: str) -> str:
    """Strip HTML tags and return plain text."""
    if not html:
        return ""
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ", strip=True)[:500]


def fetch_rss_feed(feed_config: dict, cutoff: datetime) -> list[dict]:
    """Fetch and parse a single RSS feed, filtering for MASH-relevant articles."""
    articles = []
    name = feed_config["name"]
    url = feed_config["url"]
    keywords = feed_config["keywords"]

    try:
        resp = requests.get(url, headers=HEADERS, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.warning("Failed to fetch %s (%s): %s", name, url, e)
        return articles

    soup = BeautifulSoup(resp.content, "xml")
    items = soup.find_all("item") or soup.find_all("entry")

    for item in items:
        title_tag = item.find("title")
        title = title_tag.get_text(strip=True) if title_tag else ""

        link_tag = item.find("link")
        if link_tag:
            link = link_tag.get("href") or link_tag.get_text(strip=True)
        else:
            link = ""

        desc_tag = (
            item.find("description")
            or item.find("summary")
            or item.find("content")
        )
        description = _clean_html(desc_tag.get_text() if desc_tag else "")

        pub_tag = item.find("pubDate") or item.find("published") or item.find("updated")
        pub_date = _parse_date(pub_tag.get_text(strip=True) if pub_tag else "")

        # Filter by date
        if pub_date and pub_date < cutoff:
            continue

        # Filter by keywords in title or description
        combined = f"{title} {description}"
        if not _matches_keywords(combined, keywords):
            continue

        # Strict relevance check: must mention MASH/NASH/fatty liver
        if not _is_relevant(combined):
            continue

        # Exclude animal studies, cell biology, phase 1
        if _should_exclude(combined):
            continue

        articles.append({
            "title": title,
            "link": link,
            "description": description,
            "date": pub_date.strftime("%Y-%m-%d") if pub_date else "Unknown",
            "source": name,
            "type": "industry_news",
        })

    logger.info("Fetched %d MASH articles from %s", len(articles), name)
    return articles


def fetch_all_news(lookback_days: int = LOOKBACK_DAYS) -> list[dict]:
    """Fetch MASH-relevant news from all configured RSS feeds."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)
    all_articles = []

    for feed_config in NEWS_FEEDS:
        articles = fetch_rss_feed(feed_config, cutoff)
        all_articles.extend(articles)

    # Deduplicate by title similarity
    seen_titles = set()
    unique = []
    for a in all_articles:
        normalized = re.sub(r'\W+', ' ', a["title"].lower()).strip()
        if normalized not in seen_titles:
            seen_titles.add(normalized)
            unique.append(a)

    unique.sort(key=lambda x: x["date"], reverse=True)
    logger.info("Total unique news articles: %d", len(unique))
    return unique

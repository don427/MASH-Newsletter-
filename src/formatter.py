"""Formats collected content into the newsletter HTML and plain-text versions."""

import base64
import mimetypes
import os
import logging
from datetime import datetime, timedelta, timezone

from jinja2 import Environment, FileSystemLoader

from src.config import OUTPUT_DIR, HEADSHOT_PATH, LOGO_PATH

logger = logging.getLogger(__name__)

TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "templates")


def _image_to_data_uri(filepath: str) -> str:
    """Read an image file and return a base64 data URI for embedding in HTML."""
    if not os.path.isfile(filepath):
        logger.warning("Image not found: %s", filepath)
        return ""
    mime, _ = mimetypes.guess_type(filepath)
    if not mime:
        mime = "image/png"
    with open(filepath, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{encoded}"


def _generate_executive_summary(
    news: list[dict], publications: list[dict], trials: list[dict]
) -> str:
    """Generate a brief executive summary paragraph from the collected data."""
    parts = []

    if news:
        sources = set(a["source"] for a in news)
        parts.append(
            f"{len(news)} industry news item{'s' if len(news) != 1 else ''} "
            f"from {', '.join(sorted(sources))}"
        )

    if publications:
        parts.append(
            f"{len(publications)} new publication{'s' if len(publications) != 1 else ''} "
            f"indexed in PubMed"
        )

    if trials:
        statuses = {}
        for t in trials:
            s = t.get("status", "Other")
            statuses[s] = statuses.get(s, 0) + 1
        status_parts = [f"{v} {k.lower()}" for k, v in statuses.items()]
        parts.append(
            f"{len(trials)} clinical trial update{'s' if len(trials) != 1 else ''} "
            f"({', '.join(status_parts)})"
        )

    if not parts:
        return (
            "A quiet week in the MASH space. No significant new publications, "
            "trial updates, or industry news were captured by our automated scan. "
            "Check back next week for the latest developments."
        )

    # Highlight notable items
    highlights = []
    for article in news[:2]:
        highlights.append(article["title"])
    for pub in publications[:1]:
        highlights.append(pub["title"])

    summary = f"This week: {'; '.join(parts)}."
    if highlights:
        summary += f" Notable: \"{highlights[0]}\""
        if len(highlights) > 1:
            summary += f" and \"{highlights[1]}\""
        summary += "."

    return summary


def _issue_number() -> int:
    """Calculate issue number based on weeks since project epoch."""
    epoch = datetime(2025, 1, 1, tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    return max(1, int((now - epoch).days / 7))


def render_newsletter(
    news: list[dict],
    publications: list[dict],
    trials: list[dict],
    lookback_days: int = 7,
) -> tuple[str, str]:
    """
    Render the newsletter and return (html_content, output_filepath).
    Also saves the HTML to the output directory.
    """
    now = datetime.now(timezone.utc)
    start = now - timedelta(days=lookback_days)
    date_range = f"{start.strftime('%b %d')} - {now.strftime('%b %d, %Y')}"

    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR), autoescape=True)
    template = env.get_template("newsletter.html")

    executive_summary = _generate_executive_summary(news, publications, trials)

    # Encode branding images as data URIs for email-safe embedding
    headshot_uri = _image_to_data_uri(HEADSHOT_PATH)
    logo_uri = _image_to_data_uri(LOGO_PATH)

    html = template.render(
        title=f"MASH Intelligence Report - {now.strftime('%b %d, %Y')}",
        date_range=date_range,
        issue_number=_issue_number(),
        executive_summary=executive_summary,
        news_articles=news,
        publications=publications,
        trials=trials,
        headshot_uri=headshot_uri,
        logo_uri=logo_uri,
    )

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    filename = f"mash_newsletter_{now.strftime('%Y%m%d')}.html"
    filepath = os.path.join(OUTPUT_DIR, filename)
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html)

    logger.info("Newsletter saved to %s", filepath)
    return html, filepath


def render_plain_text(
    news: list[dict],
    publications: list[dict],
    trials: list[dict],
) -> str:
    """Render a plain-text version of the newsletter for email fallback."""
    lines = []
    lines.append("=" * 60)
    lines.append("MASH INTELLIGENCE REPORT")
    lines.append("From the Desk of Dr. Don Lazas")
    lines.append("Digestive Health Research | Nashville, TN")
    lines.append(f"Issue #{_issue_number()} - {datetime.now(timezone.utc).strftime('%B %d, %Y')}")
    lines.append("=" * 60)
    lines.append("")

    lines.append(_generate_executive_summary(news, publications, trials))
    lines.append("")

    if news:
        lines.append("-" * 40)
        lines.append("INDUSTRY & PIPELINE NEWS")
        lines.append("-" * 40)
        for a in news:
            lines.append(f"\n* {a['title']}")
            lines.append(f"  Source: {a['source']} | {a['date']}")
            if a.get("description"):
                lines.append(f"  {a['description'][:200]}")
            lines.append(f"  {a['link']}")
        lines.append("")

    if publications:
        lines.append("-" * 40)
        lines.append("RECENT PUBLICATIONS")
        lines.append("-" * 40)
        for p in publications:
            lines.append(f"\n* {p['title']}")
            lines.append(f"  {p['source']} | {p['date']} | {p.get('authors', '')}")
            if p.get("description"):
                lines.append(f"  {p['description'][:200]}")
            lines.append(f"  {p['link']}")
        lines.append("")

    if trials:
        lines.append("-" * 40)
        lines.append("CLINICAL TRIAL UPDATES")
        lines.append("-" * 40)
        for t in trials:
            lines.append(f"\n* {t['title']}")
            lines.append(f"  {t['nct_id']} | {t['status']} | {t['phase']}")
            if t.get("sponsor"):
                lines.append(f"  Sponsor: {t['sponsor']}")
            lines.append(f"  {t['link']}")
        lines.append("")

    lines.append("=" * 60)
    lines.append("Automated by NueCura Newsletter Agent")
    lines.append("Data: PubMed, ClinicalTrials.gov, industry RSS feeds")
    lines.append("Verify all information from primary sources.")
    lines.append("=" * 60)

    return "\n".join(lines)

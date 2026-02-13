"""Fetches recent MASH clinical trial publications from PubMed via NCBI E-utilities."""

import logging
import time
from datetime import datetime, timedelta, timezone

import requests
from bs4 import BeautifulSoup

from src.config import PUBMED_BASE, PUBMED_SEARCH_TERMS, PUBMED_MAX_RESULTS, LOOKBACK_DAYS

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 20
HEADERS = {
    "User-Agent": "MASH-Newsletter-Agent/1.0 (research aggregator; contact don@nuecura.com)"
}


def _date_range(lookback_days: int) -> tuple[str, str]:
    """Return (mindate, maxdate) strings for PubMed in YYYY/MM/DD format."""
    end = datetime.now(timezone.utc)
    start = end - timedelta(days=lookback_days)
    return start.strftime("%Y/%m/%d"), end.strftime("%Y/%m/%d")


def search_pubmed(query: str, max_results: int, mindate: str, maxdate: str) -> list[str]:
    """Search PubMed and return a list of PMIDs."""
    params = {
        "db": "pubmed",
        "term": query,
        "retmax": max_results,
        "sort": "date",
        "datetype": "pdat",
        "mindate": mindate,
        "maxdate": maxdate,
        "retmode": "json",
    }
    try:
        resp = requests.get(
            f"{PUBMED_BASE}/esearch.fcgi", params=params,
            headers=HEADERS, timeout=REQUEST_TIMEOUT
        )
        resp.raise_for_status()
        data = resp.json()
        return data.get("esearchresult", {}).get("idlist", [])
    except requests.RequestException as e:
        logger.warning("PubMed search failed for '%s': %s", query, e)
        return []


def fetch_pubmed_details(pmids: list[str]) -> list[dict]:
    """Fetch article details for a list of PMIDs using efetch."""
    if not pmids:
        return []

    params = {
        "db": "pubmed",
        "id": ",".join(pmids),
        "retmode": "xml",
    }
    try:
        resp = requests.get(
            f"{PUBMED_BASE}/efetch.fcgi", params=params,
            headers=HEADERS, timeout=REQUEST_TIMEOUT
        )
        resp.raise_for_status()
    except requests.RequestException as e:
        logger.warning("PubMed efetch failed: %s", e)
        return []

    soup = BeautifulSoup(resp.content, "xml")
    articles = []

    for article in soup.find_all("PubmedArticle"):
        medline = article.find("MedlineCitation")
        if not medline:
            continue

        pmid_tag = medline.find("PMID")
        pmid = pmid_tag.get_text(strip=True) if pmid_tag else ""

        title_tag = medline.find("ArticleTitle")
        title = title_tag.get_text(strip=True) if title_tag else "Untitled"

        abstract_tag = medline.find("Abstract")
        if abstract_tag:
            abstract_texts = abstract_tag.find_all("AbstractText")
            abstract = " ".join(t.get_text(strip=True) for t in abstract_texts)
        else:
            abstract = ""
        # Truncate long abstracts
        if len(abstract) > 600:
            abstract = abstract[:597] + "..."

        # Journal
        journal_tag = medline.find("Journal")
        journal = ""
        if journal_tag:
            j_title = journal_tag.find("Title") or journal_tag.find("ISOAbbreviation")
            journal = j_title.get_text(strip=True) if j_title else ""

        # Date
        pub_date_tag = article.find("PubDate")
        date_str = ""
        if pub_date_tag:
            year = pub_date_tag.find("Year")
            month = pub_date_tag.find("Month")
            day = pub_date_tag.find("Day")
            parts = []
            if year:
                parts.append(year.get_text(strip=True))
            if month:
                parts.append(month.get_text(strip=True))
            if day:
                parts.append(day.get_text(strip=True))
            date_str = " ".join(parts) if parts else "Unknown"

        # Authors
        author_list = medline.find("AuthorList")
        authors = []
        if author_list:
            for auth in author_list.find_all("Author")[:3]:
                last = auth.find("LastName")
                init = auth.find("Initials")
                if last:
                    name = last.get_text(strip=True)
                    if init:
                        name += f" {init.get_text(strip=True)}"
                    authors.append(name)
            if len(author_list.find_all("Author")) > 3:
                authors.append("et al.")

        # Publication type
        pub_types = medline.find_all("PublicationType")
        type_list = [pt.get_text(strip=True) for pt in pub_types]

        articles.append({
            "title": title,
            "link": f"https://pubmed.ncbi.nlm.nih.gov/{pmid}/",
            "description": abstract,
            "date": date_str,
            "source": journal or "PubMed",
            "authors": ", ".join(authors),
            "pub_types": type_list,
            "type": "publication",
        })

    return articles


def fetch_all_publications(lookback_days: int = LOOKBACK_DAYS) -> list[dict]:
    """Run all configured PubMed searches and return deduplicated results."""
    mindate, maxdate = _date_range(lookback_days)
    all_pmids = set()

    for term in PUBMED_SEARCH_TERMS:
        pmids = search_pubmed(term, PUBMED_MAX_RESULTS, mindate, maxdate)
        all_pmids.update(pmids)
        time.sleep(0.4)  # Be nice to NCBI

    logger.info("Found %d unique PMIDs across all searches", len(all_pmids))
    articles = fetch_pubmed_details(list(all_pmids))
    articles.sort(key=lambda x: x["date"], reverse=True)
    return articles

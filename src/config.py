"""Configuration for the MASH Newsletter Agent."""

import os
from datetime import timedelta

# --- Email Configuration ---
SMTP_SERVER = os.environ.get("SMTP_SERVER", "smtp.gmail.com")
SMTP_PORT = int(os.environ.get("SMTP_PORT", "587"))
SMTP_USER = os.environ.get("SMTP_USER", "")
SMTP_PASSWORD = os.environ.get("SMTP_PASSWORD", "")
SENDER_EMAIL = os.environ.get("SENDER_EMAIL", SMTP_USER)
RECIPIENT_EMAIL = os.environ.get("RECIPIENT_EMAIL", "don@nuecura.com")

# --- Schedule ---
SEND_DAY = "monday"
SEND_TIME = "07:00"  # 7 AM

# --- Content lookback window ---
LOOKBACK_DAYS = 7

# --- PubMed / NCBI ---
PUBMED_BASE = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils"
PUBMED_SEARCH_TERMS = [
    "MASH[Title/Abstract] AND (clinical trial[Publication Type] OR review[Publication Type])",
    "metabolic dysfunction-associated steatohepatitis[Title/Abstract]",
    "NASH steatohepatitis treatment[Title/Abstract]",
]
PUBMED_MAX_RESULTS = 15

# --- ClinicalTrials.gov v2 API ---
CTGOV_API_BASE = "https://clinicaltrials.gov/api/v2/studies"
CTGOV_SEARCH_TERMS = [
    "MASH OR metabolic dysfunction-associated steatohepatitis",
    "NASH steatohepatitis",
]
CTGOV_MAX_RESULTS = 10

# --- RSS / News Feeds ---
NEWS_FEEDS = [
    {
        "name": "FiercePharma",
        "url": "https://www.fiercepharma.com/rss/xml",
        "keywords": ["MASH", "NASH", "steatohepatitis", "liver", "fibrosis"],
    },
    {
        "name": "FierceBiotech",
        "url": "https://www.fiercebiotech.com/rss/xml",
        "keywords": ["MASH", "NASH", "steatohepatitis", "liver", "fibrosis"],
    },
    {
        "name": "BioPharma Dive",
        "url": "https://www.biopharmadive.com/feeds/news/",
        "keywords": ["MASH", "NASH", "steatohepatitis", "liver"],
    },
    {
        "name": "Endpoints News",
        "url": "https://endpts.com/feed/",
        "keywords": ["MASH", "NASH", "steatohepatitis", "liver", "fibrosis"],
    },
    {
        "name": "STAT News",
        "url": "https://www.statnews.com/feed/",
        "keywords": ["MASH", "NASH", "steatohepatitis", "liver"],
    },
    {
        "name": "Healio Hepatology",
        "url": "https://www.healio.com/news/hepatology/rss",
        "keywords": ["MASH", "NASH", "steatohepatitis", "fibrosis", "liver"],
    },
]

# --- Web search fallback keywords ---
WEB_SEARCH_QUERIES = [
    "MASH metabolic steatohepatitis drug clinical trial 2025 2026",
    "NASH liver disease treatment pipeline news",
    "MASH FDA approval resmetirom obeticholic acid",
]

# --- Output ---
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")

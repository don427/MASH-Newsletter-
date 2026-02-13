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
    # Focus on human clinical studies Phase 2+, exclude animal/cell biology
    '("MASH"[Title/Abstract] OR "metabolic dysfunction-associated steatohepatitis"[Title/Abstract]) AND ("clinical trial, phase ii"[Publication Type] OR "clinical trial, phase iii"[Publication Type] OR "clinical trial, phase iv"[Publication Type] OR "randomized controlled trial"[Publication Type] OR "meta-analysis"[Publication Type] OR "practice guideline"[Publication Type] OR "systematic review"[Publication Type]) NOT ("mice"[Title] OR "mouse"[Title] OR "murine"[Title] OR "rat"[Title] OR "rats"[Title] OR "in vitro"[Title] OR "cell line"[Title] OR "hepatocyte"[Title])',
    '("NASH"[Title/Abstract] OR "nonalcoholic steatohepatitis"[Title/Abstract]) AND ("treatment"[Title/Abstract] OR "therapy"[Title/Abstract] OR "clinical outcome"[Title/Abstract] OR "fibrosis"[Title/Abstract]) AND "humans"[MeSH Terms] NOT ("phase 1"[Title/Abstract] OR "first-in-human"[Title/Abstract] OR "mice"[Title] OR "rodent"[Title])',
    '("fatty liver disease"[Title/Abstract] OR "MASLD"[Title/Abstract] OR "NAFLD"[Title/Abstract]) AND ("clinical management"[Title/Abstract] OR "patient care"[Title/Abstract] OR "diagnosis"[Title/Abstract] OR "treatment guideline"[Title/Abstract]) AND "humans"[MeSH Terms]',
]
PUBMED_MAX_RESULTS = 15

# --- ClinicalTrials.gov v2 API ---
CTGOV_API_BASE = "https://clinicaltrials.gov/api/v2/studies"
CTGOV_SEARCH_TERMS = [
    "MASH OR metabolic dysfunction-associated steatohepatitis",
    "NASH steatohepatitis",
]
CTGOV_MAX_RESULTS = 15

# --- Content relevance filters ---
# Articles MUST contain at least one of these DISEASE terms to be included.
# These are liver/MASH-specific — no ambiguous drug names that also cover
# obesity, diabetes, etc.
RELEVANCE_REQUIRED_KEYWORDS = [
    "MASH", "NASH", "steatohepatitis", "fatty liver", "MASLD", "NAFLD",
    "hepatic steatosis", "liver fibrosis", "hepatic fibrosis",
    "rezdiffra", "resmetirom",       # MASH-only drugs (safe to include)
    "efruxifermin", "pegozafermin",   # FGF21 analogues primarily for MASH
]
# NOTE: semaglutide, tirzepatide, survodutide, retatrutide are intentionally
# excluded — they have major non-MASH indications (obesity, T2D) and would
# pull in irrelevant articles.  Articles about those drugs for MASH will still
# match because they'll also mention "MASH", "NASH", "fatty liver", etc.

# Articles containing these terms are excluded (animal/preclinical/basic science)
EXCLUSION_KEYWORDS = [
    "mouse model", "murine", "rodent model", "rat model",
    "in vitro", "cell culture", "cell line", "hepatocyte culture",
    "zebrafish", "drosophila", "caenorhabditis",
    "phase 1 ", "phase i ", "first-in-human",
    "preclinical", "animal study", "animal model",
]

# Clinical trials: only include these phases (exclude Phase 1 / Early Phase 1)
TRIAL_INCLUDED_PHASES = ["PHASE2", "PHASE3", "PHASE4", "NA"]

# --- RSS / News Feeds ---
NEWS_FEEDS = [
    {
        "name": "FiercePharma",
        "url": "https://www.fiercepharma.com/rss/xml",
        "keywords": ["MASH", "NASH", "steatohepatitis", "fatty liver", "MASLD"],
    },
    {
        "name": "FierceBiotech",
        "url": "https://www.fiercebiotech.com/rss/xml",
        "keywords": ["MASH", "NASH", "steatohepatitis", "fatty liver", "MASLD"],
    },
    {
        "name": "BioPharma Dive",
        "url": "https://www.biopharmadive.com/feeds/news/",
        "keywords": ["MASH", "NASH", "steatohepatitis", "fatty liver", "MASLD"],
    },
    {
        "name": "Endpoints News",
        "url": "https://endpts.com/feed/",
        "keywords": ["MASH", "NASH", "steatohepatitis", "fatty liver", "MASLD"],
    },
    {
        "name": "STAT News",
        "url": "https://www.statnews.com/feed/",
        "keywords": ["MASH", "NASH", "steatohepatitis", "fatty liver", "MASLD"],
    },
    {
        "name": "Healio Hepatology",
        "url": "https://www.healio.com/news/hepatology/rss",
        "keywords": ["MASH", "NASH", "steatohepatitis", "fatty liver", "MASLD", "liver fibrosis"],
    },
]

# --- Web search fallback keywords ---
WEB_SEARCH_QUERIES = [
    "MASH metabolic steatohepatitis drug clinical trial 2025 2026",
    "NASH liver disease treatment pipeline news",
    "MASH FDA approval resmetirom obeticholic acid",
]

# --- Branding / Images ---
ASSETS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
HEADSHOT_PATH = os.path.join(ASSETS_DIR, "dr_lazas_headshot.jpg")
LOGO_PATH = os.path.join(ASSETS_DIR, "dhr_logo.png")

# --- Output ---
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "output")

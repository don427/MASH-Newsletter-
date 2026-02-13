"""Fetches recent MASH clinical trial updates from ClinicalTrials.gov v2 API."""

import logging
from datetime import datetime, timedelta, timezone

import requests

from src.config import (
    CTGOV_API_BASE, CTGOV_SEARCH_TERMS, CTGOV_MAX_RESULTS,
    LOOKBACK_DAYS, TRIAL_INCLUDED_PHASES, RELEVANCE_REQUIRED_KEYWORDS,
)

logger = logging.getLogger(__name__)

REQUEST_TIMEOUT = 20
HEADERS = {
    "User-Agent": "MASH-Newsletter-Agent/1.0 (research aggregator)"
}


def fetch_trials(query: str, max_results: int, cutoff_date: str) -> list[dict]:
    """Fetch clinical trials matching the query from ClinicalTrials.gov v2 API."""
    # Filter to Phase 2+ only via API
    phase_filter = " OR ".join(f"AREA[Phase]{p}" for p in TRIAL_INCLUDED_PHASES if p != "NA")
    params = {
        "query.term": query,
        "filter.advanced": f"AREA[LastUpdatePostDate]RANGE[{cutoff_date},MAX] AND ({phase_filter})",
        "pageSize": max_results,
        "sort": "LastUpdatePostDate:desc",
        "fields": "NCTId,BriefTitle,OverallStatus,LeadSponsorName,StartDate,LastUpdatePostDate,BriefSummary,Phase,Condition,InterventionName",
        "format": "json",
    }

    try:
        resp = requests.get(
            CTGOV_API_BASE, params=params,
            headers=HEADERS, timeout=REQUEST_TIMEOUT
        )
        resp.raise_for_status()
        data = resp.json()
    except requests.RequestException as e:
        logger.warning("ClinicalTrials.gov query failed for '%s': %s", query, e)
        return []

    trials = []
    studies = data.get("studies", [])
    for study in studies:
        proto = study.get("protocolSection", {})
        ident = proto.get("identificationModule", {})
        status_mod = proto.get("statusModule", {})
        sponsor_mod = proto.get("sponsorCollaboratorsModule", {})
        desc_mod = proto.get("descriptionModule", {})
        design_mod = proto.get("designModule", {})
        cond_mod = proto.get("conditionsModule", {})
        intervention_mod = proto.get("armsInterventionsModule", {})

        nct_id = ident.get("nctId", "")
        title = ident.get("briefTitle", "Untitled")
        status = status_mod.get("overallStatus", "Unknown")
        last_update = status_mod.get("lastUpdatePostDateStruct", {}).get("date", "Unknown")

        sponsor = ""
        lead = sponsor_mod.get("leadSponsor", {})
        if lead:
            sponsor = lead.get("name", "")

        summary = desc_mod.get("briefSummary", "")
        if isinstance(summary, dict):
            summary = summary.get("textBlock", "")
        if len(summary) > 400:
            summary = summary[:397] + "..."

        phases = design_mod.get("phases", [])
        phase_str = ", ".join(phases) if phases else "N/A"

        conditions = cond_mod.get("conditions", [])

        interventions = []
        if intervention_mod:
            for intv in intervention_mod.get("interventions", []):
                interventions.append(intv.get("name", ""))

        # Skip Phase 1 / Early Phase 1 trials
        phases_upper = [p.upper().replace(" ", "") for p in phases]
        if any(p in ("PHASE1", "EARLYPHASE1") for p in phases_upper):
            continue

        trials.append({
            "title": title,
            "link": f"https://clinicaltrials.gov/study/{nct_id}",
            "nct_id": nct_id,
            "status": status,
            "sponsor": sponsor,
            "phase": phase_str,
            "conditions": conditions,
            "interventions": interventions[:3],
            "description": summary,
            "date": last_update,
            "source": "ClinicalTrials.gov",
            "type": "clinical_trial",
        })

    logger.info("Fetched %d trials from ClinicalTrials.gov for '%s'", len(trials), query)
    return trials


def fetch_all_trials(lookback_days: int = LOOKBACK_DAYS) -> list[dict]:
    """Run all configured trial searches and return deduplicated results."""
    cutoff = datetime.now(timezone.utc) - timedelta(days=lookback_days)
    cutoff_str = cutoff.strftime("%Y-%m-%d")

    all_trials = []
    seen_nct = set()

    for term in CTGOV_SEARCH_TERMS:
        results = fetch_trials(term, CTGOV_MAX_RESULTS, cutoff_str)
        for trial in results:
            if trial["nct_id"] not in seen_nct:
                seen_nct.add(trial["nct_id"])
                all_trials.append(trial)

    # Post-fetch relevance filter: title or conditions must mention MASH/NASH/liver
    filtered = []
    for trial in all_trials:
        text = f"{trial['title']} {' '.join(trial.get('conditions', []))} {trial.get('description', '')}"
        text_lower = text.lower()
        if any(kw.lower() in text_lower for kw in RELEVANCE_REQUIRED_KEYWORDS):
            filtered.append(trial)
        else:
            logger.info("Excluded irrelevant trial: %s", trial["title"])

    filtered.sort(key=lambda x: x["date"], reverse=True)
    logger.info("Total unique trials after filtering: %d (excluded %d)", len(filtered), len(all_trials) - len(filtered))
    return filtered

"""
Fallback content fetcher using curated web search results.
Used when direct RSS/API access is unavailable or as supplementary source.
This module can be updated with fresh curated content or replaced
with live API calls when running in an unrestricted environment.
"""

import logging
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


def get_curated_news() -> list[dict]:
    """Return curated industry news items gathered from web search."""
    return [
        {
            "title": "Madrigal Expands MASH Pipeline with $4.4B siRNA Licensing Deal with Ribo/Ribocure",
            "link": "https://www.globenewswire.com/news-release/2026/02/11/3236027/0/en/Madrigal-Expands-its-MASH-Pipeline-with-Exclusive-Global-Licensing-Agreement-for-Six-Preclinical-siRNA-Programs.html",
            "description": (
                "Madrigal Pharmaceuticals announced an exclusive global license agreement with "
                "Suzhou Ribo Life Science and Ribocure Pharmaceuticals for six preclinical siRNA "
                "programs. The deal includes a $60M upfront payment with potential milestone payments "
                "up to $4.4B. siRNAs offer precision gene silencing to complement Rezdiffra's "
                "therapeutic effects. IND-enabling activities begin in 2026."
            ),
            "date": "2026-02-11",
            "source": "GlobeNewsWire",
            "type": "industry_news",
        },
        {
            "title": "Madrigal to Release Q4 and Full-Year 2025 Financial Results on February 19",
            "link": "https://www.globenewswire.com/news-release/2026/02/02/3230242/0/en/Madrigal-Pharmaceuticals-to-Release-Fourth-Quarter-and-Full-Year-2025-Financial-Results-and-Host-Webcast-on-February-19-2026.html",
            "description": (
                "Madrigal Pharmaceuticals will release fourth-quarter and full-year 2025 financial "
                "results on February 19, 2026. Rezdiffra brought in $287.3M in Q3 2025. "
                "GlobalData estimates Rezdiffra sales could reach $6.9 billion by 2032."
            ),
            "date": "2026-02-02",
            "source": "GlobeNewsWire",
            "type": "industry_news",
        },
        {
            "title": "Novo Nordisk's Wegovy Receives Accelerated FDA Approval for MASH Indication",
            "link": "https://www.primetherapeutics.com/w/what-you-need-to-know-about-the-new-indication-of-a-glp-1-drug-for-mash-therapy",
            "description": (
                "Semaglutide (Wegovy) received accelerated FDA approval for treating MASH, making it "
                "the first GLP-1 receptor agonist indicated for this condition. This adds to Wegovy's "
                "existing approvals for obesity and cardiovascular disease, and positions it as a direct "
                "competitor to Madrigal's Rezdiffra."
            ),
            "date": "2026-02-01",
            "source": "Prime Therapeutics",
            "type": "industry_news",
        },
        {
            "title": "Madrigal Presents Positive 2-Year Rezdiffra Data in Compensated MASH Cirrhosis",
            "link": "https://ir.madrigalpharma.com/news-releases/news-release-details/madrigal-presents-new-data-demonstrating-rezdiffrar-resmetirom",
            "description": (
                "Madrigal announced positive two-year results from the Phase 3 MAESTRO-NAFLD-1 trial "
                "open-label F4c arm. Patients (n=122) achieved significant improvements in liver "
                "stiffness, liver fat, fibrosis biomarkers, liver volume, and portal hypertension "
                "risk scores. Treatment discontinuation reversed gains; resumption restored improvements."
            ),
            "date": "2026-01-28",
            "source": "Madrigal Pharmaceuticals IR",
            "type": "industry_news",
        },
        {
            "title": "89bio's Pegozafermin Advances in Phase III, Aiming to Stand Out in MASH Field",
            "link": "https://www.genengnews.com/topics/drug-discovery/89bios-mash-drug-begins-phase-iii-aiming-to-stand-out-in-growing-field/",
            "description": (
                "89bio's pegozafermin, an FGF21 analogue with FDA Breakthrough Therapy designation, "
                "continues Phase III trials for MASH with fibrosis. FGF21 acts as a metabolic "
                "regulator and offers a differentiated mechanism vs. GLP-1 and THR-beta agonists."
            ),
            "date": "2026-01-20",
            "source": "GEN News",
            "type": "industry_news",
        },
        {
            "title": "HepQuant DuO Reveals Functional Heterogeneity in MASH at MASH-TAG 2026",
            "link": "https://www.prweb.com/releases/2026-mash-tag-oral-presentation-hepquant-duo-reveals-functional-and-physiological-heterogeneity-to-support-enhanced-clinical-trial-design-302658684.html",
            "description": (
                "At the 2026 MASH-TAG conference (Jan 8-10, Park City, UT), HepQuant presented data "
                "showing its DuO diagnostic test reveals significant functional heterogeneity and "
                "physiological impairment missed by standard testing in MASH patients. This could "
                "improve clinical trial subject selection and study design."
            ),
            "date": "2026-01-10",
            "source": "PRWeb / MASH-TAG 2026",
            "type": "industry_news",
        },
        {
            "title": "AASLD 2026 Emerging Topic Conference to Focus on SLD, MASLD and MASH Therapeutics",
            "link": "https://www.aasld.org/2026-emerging-topic-conference-unified-frontiers-liver-disease-treating-steatosis-cholestasis-and",
            "description": (
                "AASLD's 2026 Emerging Topic Conference 'Unified Frontiers in Liver Disease' is "
                "scheduled March 13-15 in Las Vegas. Days 2-3 will spotlight MASLD, MetALD, "
                "noninvasive diagnostics, fibrosis staging, and therapeutic development advances."
            ),
            "date": "2026-02-05",
            "source": "AASLD",
            "type": "industry_news",
        },
    ]


def get_curated_publications() -> list[dict]:
    """Return curated publication items gathered from web search."""
    return [
        {
            "title": "Phase 3 Trial of Semaglutide in Metabolic Dysfunction-Associated Steatohepatitis (ESSENCE Trial)",
            "link": "https://www.nejm.org/doi/10.1056/NEJMoa2413258",
            "description": (
                "In this Phase 3 trial, 1,197 patients with biopsy-defined MASH and F2-F3 fibrosis "
                "received semaglutide 2.4 mg or placebo weekly for 240 weeks. At 72-week interim: "
                "resolution of steatohepatitis without worsening fibrosis in 62.9% (semaglutide) vs. "
                "34.3% (placebo). Combined resolution + fibrosis reduction: 32.7% vs. 16.1%. "
                "Mean weight change: -10.5% vs. -2.0%."
            ),
            "date": "2025 Jun",
            "source": "New England Journal of Medicine",
            "authors": "Newsome PN, et al.",
            "pub_types": ["Clinical Trial, Phase III", "Randomized Controlled Trial"],
            "type": "publication",
        },
        {
            "title": "Tirzepatide for Metabolic Dysfunction-Associated Steatohepatitis with Liver Fibrosis",
            "link": "https://www.nejm.org/doi/full/10.1056/NEJMoa2401943",
            "description": (
                "Phase 2 dose-finding trial in biopsy-confirmed MASH with F2-F3 fibrosis. "
                "MASH resolution without worsening fibrosis: 10% (placebo), 44% (5 mg), 56% (10 mg), "
                "62% (15 mg tirzepatide) (P<0.001 all). Fibrosis improvement >= 1 stage: 30% placebo "
                "vs. 51-55% tirzepatide groups. GI adverse events most common."
            ),
            "date": "2025",
            "source": "New England Journal of Medicine",
            "authors": "Loomba R, et al.",
            "pub_types": ["Clinical Trial, Phase II", "Randomized Controlled Trial"],
            "type": "publication",
        },
        {
            "title": "Efruxifermin in Compensated Liver Cirrhosis Caused by MASH",
            "link": "https://www.nejm.org/doi/full/10.1056/NEJMoa2502242",
            "description": (
                "Phase 2b trial of efruxifermin, a bivalent FGF21 analogue, in patients with MASH "
                "and compensated cirrhosis (F4 fibrosis). Patients received efruxifermin (28 mg or "
                "50 mg weekly) or placebo. Primary endpoint: reduction of >= 1 fibrosis stage without "
                "worsening MASH at week 36. Earlier Phase 2 trials in F2-F3 showed fibrosis reduction "
                "and MASH resolution."
            ),
            "date": "2025",
            "source": "New England Journal of Medicine",
            "authors": "Harrison SA, et al.",
            "pub_types": ["Clinical Trial, Phase II", "Multicenter Study"],
            "type": "publication",
        },
        {
            "title": "New Drug Therapies for Metabolic Dysfunction-Associated Steatohepatitis",
            "link": "https://www.sciencedirect.com/science/article/pii/S2542568425000017",
            "description": (
                "Comprehensive review of the evolving MASH therapeutic landscape including THR-beta "
                "agonists (resmetirom), GLP-1 receptor agonists (semaglutide), dual GIP/GLP-1 agonists "
                "(tirzepatide), FGF21 analogues (efruxifermin, pegozafermin), and emerging combination "
                "strategies. Discusses the shift from monotherapy to multi-target approaches."
            ),
            "date": "2025",
            "source": "ScienceDirect",
            "authors": "Rinella ME, et al.",
            "pub_types": ["Review"],
            "type": "publication",
        },
        {
            "title": "MASH in Type 2 Diabetes: Pathophysiology, Diagnosis, and Therapeutic Management — A Narrative Review",
            "link": "https://www.mdpi.com/1648-9144/62/2/325",
            "description": (
                "February 2026 review highlighting the intertwined relationship between MASLD/MASH "
                "and type 2 diabetes. Discusses progression to fibrosis, cirrhosis, and hepatocellular "
                "carcinoma. Covers current diagnostic approaches and emerging therapeutic strategies "
                "in the diabetic MASH population."
            ),
            "date": "2026 Feb",
            "source": "Medicina (MDPI)",
            "authors": "Various",
            "pub_types": ["Review"],
            "type": "publication",
        },
        {
            "title": "Therapeutic Landscape of Metabolic Dysfunction-Associated Steatohepatitis (MASH)",
            "link": "https://pubmed.ncbi.nlm.nih.gov/39609545/",
            "description": (
                "Overview of the current and emerging treatment landscape for MASH, covering approved "
                "agents and late-phase pipeline candidates. Addresses the potential for combination "
                "therapies to mirror Type 2 Diabetes treatment patterns with multiple mechanisms of action."
            ),
            "date": "2025",
            "source": "PubMed",
            "authors": "Noureddin M, et al.",
            "pub_types": ["Review"],
            "type": "publication",
        },
    ]


def get_curated_trials() -> list[dict]:
    """Return curated clinical trial items gathered from web search."""
    return [
        {
            "title": "Rezdiffra (Resmetirom) Phase 3 Outcomes Trial in Compensated MASH Cirrhosis (F4c)",
            "link": "https://clinicaltrials.gov/study/NCT04197479",
            "nct_id": "NCT04197479",
            "status": "Active, not recruiting",
            "sponsor": "Madrigal Pharmaceuticals",
            "phase": "Phase 3",
            "conditions": ["MASH", "Compensated Cirrhosis"],
            "interventions": ["Resmetirom (Rezdiffra)"],
            "description": (
                "Ongoing Phase 3 outcomes trial evaluating Rezdiffra for compensated MASH cirrhosis. "
                "Positive 2-year open-label data showed improvements in liver stiffness, fat, fibrosis "
                "biomarkers, and portal hypertension risk. Full approval readout expected 2026-2027."
            ),
            "date": "2026-02-01",
            "source": "ClinicalTrials.gov",
            "type": "clinical_trial",
        },
        {
            "title": "ESSENCE: Semaglutide vs Placebo in MASH with Fibrosis (F2-F3)",
            "link": "https://clinicaltrials.gov/study/NCT04822181",
            "nct_id": "NCT04822181",
            "status": "Active, not recruiting",
            "sponsor": "Novo Nordisk",
            "phase": "Phase 3",
            "conditions": ["MASH", "Liver Fibrosis"],
            "interventions": ["Semaglutide 2.4 mg SC weekly"],
            "description": (
                "Ongoing 240-week Phase 3 trial in 1,197 patients with MASH F2-F3. 72-week interim: "
                "62.9% MASH resolution (vs 34.3% placebo), -10.5% body weight change. "
                "Now also has accelerated FDA approval for MASH indication."
            ),
            "date": "2026-01-15",
            "source": "ClinicalTrials.gov",
            "type": "clinical_trial",
        },
        {
            "title": "Pegozafermin Phase 3 Trial in MASH with Fibrosis",
            "link": "https://clinicaltrials.gov/study/NCT06216067",
            "nct_id": "NCT06216067",
            "status": "Recruiting",
            "sponsor": "89bio, Inc.",
            "phase": "Phase 3",
            "conditions": ["MASH", "Liver Fibrosis"],
            "interventions": ["Pegozafermin (FGF21 analogue)"],
            "description": (
                "Phase 3 trial of pegozafermin, an FGF21 analogue with Breakthrough Therapy "
                "designation, for MASH with fibrosis. Differentiated mechanism targeting metabolic "
                "regulation via fibroblast growth factor 21 pathway."
            ),
            "date": "2026-02-01",
            "source": "ClinicalTrials.gov",
            "type": "clinical_trial",
        },
        {
            "title": "Survodutide Phase 3 Trial in MASH (VANQUISH Program)",
            "link": "https://clinicaltrials.gov/study/NCT06528808",
            "nct_id": "NCT06528808",
            "status": "Recruiting",
            "sponsor": "Boehringer Ingelheim / Zealand Pharma",
            "phase": "Phase 3",
            "conditions": ["MASH", "Liver Fibrosis"],
            "interventions": ["Survodutide (GLP-1/glucagon dual agonist)"],
            "description": (
                "Phase 3 trial of survodutide, a dual GLP-1/glucagon receptor agonist. Phase 2 "
                "showed up to 83% of participants had improved liver fat and inflammation without "
                "worsening fibrosis. Completion estimated June 2029."
            ),
            "date": "2026-01-20",
            "source": "ClinicalTrials.gov",
            "type": "clinical_trial",
        },
        {
            "title": "Retatrutide Phase 3 Trial in MASH / Fatty Liver Disease",
            "link": "https://clinicaltrials.gov/study/NCT06419088",
            "nct_id": "NCT06419088",
            "status": "Recruiting",
            "sponsor": "Eli Lilly",
            "phase": "Phase 3",
            "conditions": ["MASH", "Fatty Liver Disease"],
            "interventions": ["Retatrutide (triple GIP/GLP-1/glucagon agonist)"],
            "description": (
                "Phase 3 trial of retatrutide, a triple receptor agonist (GIP, GLP-1, glucagon). "
                "Initial findings showed ~85% of obese participants with fatty liver disease had "
                "significant liver fat reduction."
            ),
            "date": "2026-01-10",
            "source": "ClinicalTrials.gov",
            "type": "clinical_trial",
        },
        {
            "title": "MGL-2086 First-in-Human Study (Oral GLP-1 RA for MASH)",
            "link": "https://ir.madrigalpharma.com/news-releases/news-release-details/madrigal-expands-its-mash-pipeline-exclusive-global-licensing",
            "nct_id": "TBD",
            "status": "Not yet recruiting",
            "sponsor": "Madrigal Pharmaceuticals",
            "phase": "Phase 1",
            "conditions": ["MASH"],
            "interventions": ["MGL-2086 (oral GLP-1 RA)"],
            "description": (
                "Madrigal's oral GLP-1 receptor agonist MGL-2086 entering first-in-human studies "
                "in Q2 2026. Part of Madrigal's expanding MASH pipeline beyond Rezdiffra, with "
                "potential for combination therapy."
            ),
            "date": "2026-02-11",
            "source": "Madrigal Pharmaceuticals",
            "type": "clinical_trial",
        },
    ]


def fetch_all_curated_content() -> tuple[list[dict], list[dict], list[dict]]:
    """Return all curated content as (news, publications, trials)."""
    news = get_curated_news()
    pubs = get_curated_publications()
    trials = get_curated_trials()
    logger.info(
        "Loaded curated content: %d news, %d publications, %d trials",
        len(news), len(pubs), len(trials),
    )
    return news, pubs, trials

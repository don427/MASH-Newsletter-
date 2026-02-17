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
            "link": "https://www.fiercebiotech.com/biotech/madrigal-pens-44b-deal-ribos-sirna-programs-latest-rezdiffra-mash-play",
            "description": (
                "Madrigal Pharmaceuticals announced an exclusive global license agreement with "
                "Suzhou Ribo Life Science and Ribocure Pharmaceuticals for six preclinical siRNA "
                "programs targeting MASH disease drivers. The deal includes a $60M upfront payment "
                "with potential milestone payments up to $4.4B plus royalties. siRNAs offer precision "
                "gene silencing to complement Rezdiffra's therapeutic effects. IND-enabling activities "
                "begin in 2026. Madrigal now has 10+ programs targeting different MASH drivers, "
                "cementing its position as the market leader in the space."
            ),
            "date": "2026-02-11",
            "source": "Fierce Biotech",
            "type": "industry_news",
        },
        {
            "title": "Survodutide Receives FDA Breakthrough Therapy Designation for MASH; Phase 3 LIVERAGE Trials Underway",
            "link": "https://www.pharmacytimes.com/view/fda-grants-survodutide-breakthrough-therapy-designation-for-treatment-of-adults-with-mash",
            "description": (
                "Boehringer Ingelheim and Zealand Pharma's survodutide, a dual GLP-1/glucagon "
                "receptor agonist, received FDA Breakthrough Therapy Designation for MASH. Phase 2 "
                "data showed up to 83% of patients achieved MASH improvement without worsening "
                "fibrosis (vs 18.2% placebo, p<0.0001), and 52.3% achieved fibrosis improvement. "
                "Phase 3 LIVERAGE trials (F2-F3 and F4 cirrhosis) are now recruiting, evaluating "
                "MASH resolution, fibrosis improvement, and long-term liver-related outcomes."
            ),
            "date": "2026-02-09",
            "source": "Pharmacy Times / BioPharma Dive",
            "type": "industry_news",
        },
        {
            "title": "Altimmune's Pemvidutide Wins FDA Breakthrough Therapy Designation for MASH After Strong Phase 2b Results",
            "link": "https://ir.altimmune.com/news-releases/news-release-details/altimmune-receives-fda-breakthrough-therapy-designation",
            "description": (
                "The FDA granted Breakthrough Therapy Designation to Altimmune's pemvidutide, "
                "a balanced 1:1 glucagon/GLP-1 dual receptor agonist, for MASH treatment. "
                "48-week IMPACT Phase 2b data: 32.4% of patients on 1.8mg achieved combined "
                "ELF + LSM improvement vs 3.2% placebo (p<0.0001). Liver fat reduced 54.7% "
                "(vs 8.2% placebo). ALT reduced by -37.4 IU/L. Phase 3 planned for 2026."
            ),
            "date": "2026-01-05",
            "source": "Altimmune IR / GlobeNewsWire",
            "type": "industry_news",
        },
        {
            "title": "Madrigal Licenses Pfizer's Ervogastat (DGAT-2 Inhibitor) for $50M to Build MASH Combo Strategy",
            "link": "https://ir.madrigalpharma.com/news-releases/news-release-details/madrigal-expands-its-mash-pipeline-exclusive-global-license",
            "description": (
                "Madrigal acquired exclusive global rights to ervogastat, a Phase 2 oral DGAT-2 "
                "inhibitor, from Pfizer for $50M upfront plus milestones. Phase 2 data: 72% of "
                "patients achieved >=30% liver fat reduction and 61% achieved >=50% reduction. "
                "Ervogastat blocks triglyceride assembly — a complementary mechanism to Rezdiffra's "
                "THR-beta pathway. Drug-drug interaction study with Rezdiffra planned for 2026, "
                "followed by FDA consultation on Phase 2 combo trial design."
            ),
            "date": "2026-01-09",
            "source": "Fierce Biotech",
            "type": "industry_news",
        },
        {
            "title": "MIT Develops New Tissue Models Revealing Why Resmetirom Fails in ~70% of MASH Patients",
            "link": "https://news.mit.edu/2026/new-tissue-models-could-help-researchers-develop-drugs-liver-disease-0203",
            "description": (
                "MIT researchers developed advanced liver tissue models showing resmetirom can "
                "induce an inflammatory response in liver tissue, potentially explaining why "
                "Rezdiffra is only effective in ~30% of MASH patients. With 100M+ Americans "
                "affected by MASLD, researchers stress the need for multiple drug classes: "
                "'You're never declaring victory with liver disease with one drug or one class "
                "of drugs.' Findings highlight the importance of combination approaches."
            ),
            "date": "2026-02-03",
            "source": "MIT News",
            "type": "industry_news",
        },
        {
            "title": "Novo Nordisk's Wegovy Receives Accelerated FDA Approval for MASH Indication",
            "link": "https://www.primetherapeutics.com/w/what-you-need-to-know-about-the-new-indication-of-a-glp-1-drug-for-mash-therapy",
            "description": (
                "Semaglutide (Wegovy) received accelerated FDA approval for treating MASH, making it "
                "the first GLP-1 receptor agonist indicated for this condition. This adds to Wegovy's "
                "existing approvals for obesity and cardiovascular disease, and positions it as a direct "
                "competitor to Madrigal's Rezdiffra. The MASH market is projected to reach $20.3B by "
                "2032 (CAGR 38.2%), with Rezdiffra alone forecast at $6.9B."
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
                "risk scores. Treatment discontinuation reversed gains; resumption restored improvements. "
                "Rezdiffra Q3 2025 sales: $287.3M. Awareness has driven a 50% spike in MASH diagnoses."
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
            "title": "Madrigal Q4/FY2025 Earnings on Feb 19 — Rezdiffra Commercial Momentum in Focus",
            "link": "https://www.globenewswire.com/news-release/2026/02/02/3230242/0/en/Madrigal-Pharmaceuticals-to-Release-Fourth-Quarter-and-Full-Year-2025-Financial-Results-and-Host-Webcast-on-February-19-2026.html",
            "description": (
                "Madrigal Pharmaceuticals will release Q4 and full-year 2025 financial results on "
                "February 19, 2026. Key watch items: Rezdiffra revenue trajectory (Q3: $287.3M), "
                "prescriber base growth (10,000+ prescribers, 29,500 patients reached), pipeline "
                "investment spending on siRNA, ervogastat, and MGL-2086 programs."
            ),
            "date": "2026-02-02",
            "source": "GlobeNewsWire",
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
            "title": "A Phase 2 Randomized Trial of Survodutide in MASH and Fibrosis",
            "link": "https://pubmed.ncbi.nlm.nih.gov/38847460/",
            "description": (
                "Phase 2 RCT of survodutide (dual GLP-1/glucagon agonist) in MASH with F1-F3 fibrosis. "
                "83% of patients on highest dose achieved MASH improvement without worsening fibrosis "
                "vs 18.2% placebo (p<0.0001). Fibrosis improvement in 52.3% vs 25.8% placebo. "
                "Results support Phase 3 advancement. Published in NEJM."
            ),
            "date": "2025",
            "source": "New England Journal of Medicine",
            "authors": "Sanyal AJ, et al.",
            "pub_types": ["Clinical Trial, Phase II", "Randomized Controlled Trial"],
            "type": "publication",
        },
        {
            "title": "Pemvidutide IMPACT Phase 2b Trial — 24-Week Efficacy and Safety Data in MASH",
            "link": "https://ir.altimmune.com/news-releases/news-release-details/altimmune-announces-publication-impact-phase-2b-trial-data",
            "description": (
                "Published in The Lancet. 212 patients with biopsy-confirmed MASH F2-F3. "
                "Pemvidutide (1:1 glucagon/GLP-1 dual agonist) achieved MASH resolution without "
                "worsening fibrosis at 24 weeks, with substantial liver fat reduction and improvements "
                "in non-invasive fibrosis markers (ELF, LSM). 48-week data showed continued benefit."
            ),
            "date": "2025 Nov",
            "source": "The Lancet",
            "authors": "Altimmune / Garg V, et al.",
            "pub_types": ["Clinical Trial, Phase II", "Randomized Controlled Trial"],
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
    ]


def get_curated_trials() -> list[dict]:
    """Return curated clinical trial items gathered from web search — Phase 2+ MASH trials."""
    return [
        # --- Pegozafermin (89bio) ---
        {
            "title": "Pegozafermin Phase 3 ENLIGHTEN-Fibrosis Trial in MASH (F2-F3)",
            "link": "https://clinicaltrials.gov/study/NCT06318169",
            "nct_id": "NCT06318169",
            "status": "Recruiting",
            "sponsor": "89bio, Inc.",
            "phase": "Phase 3",
            "conditions": ["MASH", "Liver Fibrosis"],
            "interventions": ["Pegozafermin (FGF21 analogue)"],
            "description": (
                "Phase 3 ENLIGHTEN-Fibrosis trial of pegozafermin, an FGF21 analogue with "
                "Breakthrough Therapy designation, for MASH with F2-F3 fibrosis. ~1,350 "
                "patients. Differentiated mechanism targeting metabolic regulation via "
                "fibroblast growth factor 21 pathway."
            ),
            "date": "2026-02-01",
            "source": "ClinicalTrials.gov",
            "type": "clinical_trial",
        },
        {
            "title": "Pegozafermin Phase 3 ENLIGHTEN-Cirrhosis Trial in MASH (F4)",
            "link": "https://clinicaltrials.gov/study/NCT06419374",
            "nct_id": "NCT06419374",
            "status": "Recruiting",
            "sponsor": "89bio, Inc.",
            "phase": "Phase 3",
            "conditions": ["MASH", "Compensated Cirrhosis"],
            "interventions": ["Pegozafermin (FGF21 analogue)"],
            "description": (
                "Phase 3 ENLIGHTEN-Cirrhosis trial of pegozafermin in patients with "
                "compensated cirrhosis due to MASH (F4 fibrosis). ~760 patients. "
                "Assessing efficacy and safety of FGF21-based therapy in the most "
                "advanced non-decompensated MASH population."
            ),
            "date": "2026-02-01",
            "source": "ClinicalTrials.gov",
            "type": "clinical_trial",
        },
        # --- Efruxifermin (Akero / Novo Nordisk) ---
        {
            "title": "Efruxifermin Phase 3 SYNCHRONY Histology Trial in MASH (F2-F3)",
            "link": "https://clinicaltrials.gov/study/NCT06215716",
            "nct_id": "NCT06215716",
            "status": "Recruiting",
            "sponsor": "Akero Therapeutics / Novo Nordisk",
            "phase": "Phase 3",
            "conditions": ["MASH", "Liver Fibrosis"],
            "interventions": ["Efruxifermin (Fc-FGF21 analogue)"],
            "description": (
                "Phase 3 SYNCHRONY Histology trial of efruxifermin, a bivalent Fc-FGF21 "
                "analogue, in MASH with F2-F3 fibrosis. ~1,650 patients at ~300 sites. "
                "Follows positive HARMONY Phase 2b results showing fibrosis improvement "
                "and MASH resolution. Novo Nordisk acquired Akero in 2024."
            ),
            "date": "2026-02-10",
            "source": "ClinicalTrials.gov",
            "type": "clinical_trial",
        },
        {
            "title": "Efruxifermin Phase 3 SYNCHRONY Outcomes Trial in MASH Cirrhosis (F4)",
            "link": "https://clinicaltrials.gov/study/NCT06528314",
            "nct_id": "NCT06528314",
            "status": "Recruiting",
            "sponsor": "Akero Therapeutics / Novo Nordisk",
            "phase": "Phase 3",
            "conditions": ["MASH", "Compensated Cirrhosis"],
            "interventions": ["Efruxifermin (Fc-FGF21 analogue)"],
            "description": (
                "Phase 3 SYNCHRONY Outcomes trial of efruxifermin in compensated MASH "
                "cirrhosis (F4). ~1,000+ patients at 155+ sites. Follows SYMMETRY Phase 2b "
                "results (NEJM 2025) showing fibrosis reduction in cirrhotic patients."
            ),
            "date": "2026-02-10",
            "source": "ClinicalTrials.gov",
            "type": "clinical_trial",
        },
        {
            "title": "Efruxifermin Phase 3 SYNCHRONY Real-World Trial in MASH",
            "link": "https://clinicaltrials.gov/study/NCT06161571",
            "nct_id": "NCT06161571",
            "status": "Active, not recruiting",
            "sponsor": "Akero Therapeutics / Novo Nordisk",
            "phase": "Phase 3",
            "conditions": ["MASH"],
            "interventions": ["Efruxifermin (Fc-FGF21 analogue)"],
            "description": (
                "Phase 3 SYNCHRONY Real-World trial. Double-blind enrollment completed "
                "January 2025 (601 patients). Evaluating efruxifermin using non-invasive "
                "tests in a real-world clinical setting. Results expected first half 2026."
            ),
            "date": "2026-02-10",
            "source": "ClinicalTrials.gov",
            "type": "clinical_trial",
        },
        # --- Survodutide (Boehringer Ingelheim / Zealand) ---
        {
            "title": "Survodutide Phase 3 LIVERAGE Trial in MASH with Fibrosis (F2-F3)",
            "link": "https://clinicaltrials.gov/study/NCT06632444",
            "nct_id": "NCT06632444",
            "status": "Recruiting",
            "sponsor": "Boehringer Ingelheim / Zealand Pharma",
            "phase": "Phase 3",
            "conditions": ["MASH", "Liver Fibrosis"],
            "interventions": ["Survodutide (GLP-1/glucagon dual agonist)"],
            "description": (
                "Phase 3 LIVERAGE trial of survodutide with FDA Breakthrough Therapy and "
                "Fast Track designations. ~1,800 patients. Phase 2: 83% MASH improvement "
                "vs 18.2% placebo; 52.3% fibrosis improvement. Evaluating MASH resolution, "
                "fibrosis improvement, and long-term liver outcomes."
            ),
            "date": "2026-02-09",
            "source": "ClinicalTrials.gov",
            "type": "clinical_trial",
        },
        {
            "title": "Survodutide Phase 3 LIVERAGE-Cirrhosis Trial in MASH (F4)",
            "link": "https://clinicaltrials.gov/study/NCT06632457",
            "nct_id": "NCT06632457",
            "status": "Recruiting",
            "sponsor": "Boehringer Ingelheim / Zealand Pharma",
            "phase": "Phase 3",
            "conditions": ["MASH", "Compensated Cirrhosis"],
            "interventions": ["Survodutide (GLP-1/glucagon dual agonist)"],
            "description": (
                "Phase 3 LIVERAGE-Cirrhosis trial evaluating survodutide in MASH patients "
                "with compensated cirrhosis (F4). Companion study to the F2-F3 LIVERAGE trial."
            ),
            "date": "2026-02-09",
            "source": "ClinicalTrials.gov",
            "type": "clinical_trial",
        },
        {
            "title": "Survodutide Phase 3 Trial in Obesity with Presumed MASH",
            "link": "https://clinicaltrials.gov/study/NCT06309992",
            "nct_id": "NCT06309992",
            "status": "Recruiting",
            "sponsor": "Boehringer Ingelheim",
            "phase": "Phase 3",
            "conditions": ["Obesity", "MASH"],
            "interventions": ["Survodutide (GLP-1/glucagon dual agonist)"],
            "description": (
                "Phase 3 trial evaluating survodutide in adults with obesity or overweight "
                "and confirmed or presumed MASH. Assessing liver fat reduction and weight "
                "loss. Part of the broader LIVERAGE program."
            ),
            "date": "2026-02-09",
            "source": "ClinicalTrials.gov",
            "type": "clinical_trial",
        },
        # --- Semaglutide (Novo Nordisk) ---
        {
            "title": "Semaglutide Phase 3 ESSENCE Trial in MASH with Fibrosis (F2-F3)",
            "link": "https://clinicaltrials.gov/study/NCT04822181",
            "nct_id": "NCT04822181",
            "status": "Active, not recruiting",
            "sponsor": "Novo Nordisk",
            "phase": "Phase 3",
            "conditions": ["MASH", "Liver Fibrosis"],
            "interventions": ["Semaglutide 2.4 mg (GLP-1 receptor agonist)"],
            "description": (
                "Phase 3 ESSENCE trial (1,197 patients, 253 sites, 37 countries). Part 1 "
                "results (NEJM 2025): MASH resolution without worsening fibrosis in 62.9% "
                "(semaglutide) vs 34.3% (placebo). Part 2 assessing clinical outcomes "
                "over 240 weeks is ongoing."
            ),
            "date": "2026-02-01",
            "source": "ClinicalTrials.gov",
            "type": "clinical_trial",
        },
        # --- Tirzepatide / Retatrutide (Eli Lilly) ---
        {
            "title": "Tirzepatide & Retatrutide Phase 3 SYNERGY-Outcomes Trial in MASLD",
            "link": "https://clinicaltrials.gov/study/NCT07165028",
            "nct_id": "NCT07165028",
            "status": "Recruiting",
            "sponsor": "Eli Lilly",
            "phase": "Phase 3",
            "conditions": ["MASLD", "MASH"],
            "interventions": [
                "Tirzepatide (GIP/GLP-1 dual agonist)",
                "Retatrutide (triple GIP/GLP-1/glucagon agonist)",
            ],
            "description": (
                "Phase 3 SYNERGY-Outcomes master protocol evaluating BOTH tirzepatide and "
                "retatrutide vs placebo for prevention of major adverse liver outcomes in "
                "high-risk MASLD. ~4,500 adults over ~224 weeks. Uses non-invasive tests "
                "rather than liver biopsy."
            ),
            "date": "2026-01-15",
            "source": "ClinicalTrials.gov",
            "type": "clinical_trial",
        },
        # --- Resmetirom (Madrigal) ---
        {
            "title": "Resmetirom Phase 3 MAESTRO-NASH-OUTCOMES Trial in MASH Cirrhosis",
            "link": "https://clinicaltrials.gov/study/NCT05500222",
            "nct_id": "NCT05500222",
            "status": "Active, not recruiting",
            "sponsor": "Madrigal Pharmaceuticals",
            "phase": "Phase 3",
            "conditions": ["MASH", "Compensated Cirrhosis"],
            "interventions": ["Resmetirom / Rezdiffra (THR-beta agonist)"],
            "description": (
                "Phase 3 MAESTRO-NASH-OUTCOMES trial — FDA-required confirmatory outcomes "
                "study for Rezdiffra's accelerated approval. Enrollment completed Oct 2024 "
                "(845 patients with compensated MASH cirrhosis). Evaluating major adverse "
                "liver outcomes. Data expected 2026-2027."
            ),
            "date": "2026-02-01",
            "source": "ClinicalTrials.gov",
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

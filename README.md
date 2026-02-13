# MASH Weekly Intelligence Newsletter

Automated agent that sweeps the web for MASH (Metabolic Dysfunction-Associated Steatohepatitis) industry publications, clinical trial updates, and pipeline news. Generates a formatted newsletter and delivers it via email every Monday morning.

## Data Sources

- **PubMed (NCBI E-utilities)** - Clinical trial publications, reviews, and research articles
- **ClinicalTrials.gov (v2 API)** - Active trial updates, status changes, new registrations
- **Industry RSS Feeds** - FiercePharma, FierceBiotech, BioPharma Dive, Endpoints News, STAT News, Healio Hepatology
- **Web search fallback** - Curated content when live APIs are unavailable

## Setup

```bash
pip install -r requirements.txt
```

### Email Configuration

Set these environment variables to enable email delivery:

```bash
export SMTP_SERVER="smtp.gmail.com"       # default
export SMTP_PORT="587"                     # default
export SMTP_USER="your-email@gmail.com"
export SMTP_PASSWORD="your-app-password"
export SENDER_EMAIL="your-email@gmail.com" # defaults to SMTP_USER
export RECIPIENT_EMAIL="don@nuecura.com"   # default
```

For Gmail, use an [App Password](https://support.google.com/accounts/answer/185833) rather than your account password.

## Usage

```bash
# Generate and send newsletter now
python run.py

# Generate without sending email (saves to output/)
python run.py --dry-run

# Use curated web-search data (fallback mode)
python run.py --curated

# Look back 14 days instead of default 7
python run.py --lookback 14

# Start weekly scheduler (every Monday at 7 AM)
python run.py --schedule

# Combine flags
python run.py --schedule --dry-run
```

## Project Structure

```
├── run.py                  # Main entry point / CLI
├── requirements.txt        # Python dependencies
├── src/
│   ├── config.py           # Configuration (feeds, API endpoints, email)
│   ├── news_fetcher.py     # RSS feed fetcher with keyword filtering
│   ├── pubmed_fetcher.py   # PubMed E-utilities integration
│   ├── trials_fetcher.py   # ClinicalTrials.gov v2 API integration
│   ├── web_search_fetcher.py  # Curated fallback content
│   ├── formatter.py        # Jinja2 newsletter renderer (HTML + plain text)
│   ├── emailer.py          # SMTP email sender
│   └── scheduler.py        # Weekly cron-like scheduler
├── templates/
│   └── newsletter.html     # Jinja2 HTML email template
└── output/                 # Generated newsletter files
```

## Newsletter Sections

1. **Executive Summary** - Auto-generated "at a glance" overview
2. **Industry & Pipeline News** - Company announcements, FDA actions, deals
3. **Recent Publications** - PubMed-indexed articles with authors, journal, abstract
4. **Clinical Trial Updates** - NCT IDs, status, sponsors, interventions, phases

## Deployment (Weekly Cron)

To run every Monday at 7 AM via crontab:

```bash
crontab -e
# Add:
0 7 * * 1 cd /path/to/MASH-Newsletter- && python run.py >> /var/log/mash-newsletter.log 2>&1
```

Or use the built-in scheduler:

```bash
nohup python run.py --schedule &
```

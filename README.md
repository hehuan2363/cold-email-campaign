# Cold Email Campaign CLI

End-to-end cold email campaign automation — from niche selection and offer writing to verified lead lists ready for [Instantly](https://instantly.ai).

Works with **Claude Code**, **Cursor**, and other AI coding agents via the included skill definition. Just type `/cold-email-campaign start` and the AI walks you through everything.

## The Full Pipeline

| Step | What | How |
|------|------|-----|
| 1 | **Pick niche & generate offers** | AI generates 2 offers (free build + free audit) with Apollo search filters |
| 2 | **Source leads** | Guidance on Apollo filters, niche databases, and CSV export |
| 3 | **Generate icebreakers** | AI writes personalized 1-line openers for each lead |
| 4 | **Shorten company names** | Cleans up long names for `{{companyName}}` template variable |
| 5 | **Verify emails** | SMTP check (free) + MillionVerifier API for blocked IPs |
| 6 | **Create clean CSV** | Removes bad emails, outputs Instantly-ready file |
| 7 | **Write email sequences** | AI generates 2-email sequences with subject line variations |
| 8 | **Launch on Instantly** | Checklist for domain setup, warmup, and monitoring |

## Quick Start

### Prerequisites
- Python 3.10+
- [uv](https://docs.astral.sh/uv/) (Python package manager)
- [Gemini API key](https://aistudio.google.com/apikey) (free)
- [MillionVerifier API key](https://millionverifier.com) (optional, ~$3/500 emails)

### Setup

```bash
git clone https://github.com/hehuan2363/cold-email-campaign.git
cd cold-email-campaign

# Set your API keys
export GEMINI_API_KEY="your-gemini-key"
export MV_API_KEY="your-mv-key"              # optional
export EHLO_DOMAIN="yourdomain.com"          # your sending domain
export SENDER_EMAIL="verify@yourdomain.com"

# Install dependencies
cd scripts && uv sync
```

### Using with an AI Coding Agent (Recommended)

If you're using **Claude Code**, **Cursor**, or any AI coding agent:

```
/cold-email-campaign start
```

The AI will guide you step-by-step through the entire pipeline — from picking your niche to launching on Instantly. It asks the right questions, generates offers and sequences, and runs all the scripts for you.

### Using the CLI Directly

```bash
cd scripts

# Step 1: Generate offers for your niche
uv run python campaign.py offers --niche "property management" --bg "I manage my own rental portfolio"

# Step 7: Generate email sequences
uv run python campaign.py sequences \
  --niche "property management" \
  --offer "I'll build you a custom invoice automation bot for free" \
  --sender "Alex" \
  --bg "I manage my own rental portfolio and automated my bookkeeping"

# Steps 3-6: Process leads (after sourcing from Apollo)
uv run python campaign.py run --file ../leads/my-leads.csv

# Or run individual steps
uv run python campaign.py icebreakers --file ../leads/my-leads.csv
uv run python campaign.py shorten --file ../leads/my-leads-with-icebreakers.csv
uv run python campaign.py verify --file ../leads/my-leads-with-icebreakers.csv
uv run python campaign.py verify-mv --file ../leads/my-leads-with-icebreakers.csv
uv run python campaign.py clean --file ../leads/my-leads-with-icebreakers.csv
uv run python campaign.py stats --file ../leads/my-leads-with-icebreakers.csv

# Check setup
uv run python campaign.py check
```

### Input Format

Export leads from [Apollo.io](https://apollo.io) as CSV. Key columns:
- `email`, `firstName`, `lastName`, `title` (required)
- `organizationName`, `organizationDescription`, `organizationSpecialities` (for icebreakers)
- `city`, `state`, `organizationSize`, `organizationIndustry`

### Output

The pipeline adds these columns and produces a clean CSV:
- `icebreaker` — Personalized opening line
- `shortenedCompanyName` — Clean company name for `{{companyName}}`
- `email_status` — `valid`, `catch_all`, `rejected`, `no_mx`, `ip_blocked`, etc.

Final output: `*-CLEAN.csv` with only sendable leads (`valid` + `catch_all`).

## Project Structure

```
cold-email-campaign/
├── scripts/
│   ├── campaign.py          # Main CLI entry point
│   ├── config.py            # Configuration (env vars)
│   ├── pyproject.toml       # Dependencies
│   └── lib/
│       ├── offers.py        # AI offer generation
│       ├── sequences.py     # AI email sequence writing
│       ├── icebreakers.py   # AI icebreaker generation
│       ├── shorten.py       # Company name shortening
│       ├── verify_smtp.py   # Local SMTP verification
│       ├── verify_mv.py     # MillionVerifier API
│       └── clean.py         # CSV cleaning
├── docs/
│   ├── Cold Email Campaign Playbook.md   # Full process documentation
│   ├── 6 Cold Email Sequences.md         # Example email templates
│   ├── 6 Offers.md                       # Example offers
│   ├── How to write offer.md             # Offer writing framework
│   └── Icebreaker Generation Guide.md    # Icebreaker guide
├── leads/                   # Your CSV files go here (gitignored)
├── .claude/skills/          # Claude Code skill definition
├── CLAUDE.md                # Claude Code project context
└── README.md
```

## Docs Included

The `docs/` directory contains guides and example templates:

- **Cold Email Campaign Playbook** — Complete 8-step process with checklists
- **6 Offers** — Example offers across 3 niches (property management, engineering, accounting)
- **6 Cold Email Sequences** — Example email templates with subject lines
- **How to Write Offer** — Framework for crafting irresistible free offers
- **Icebreaker Generation Guide** — Rules and examples for personalized openers

These are examples — customize everything for your own niche and business.

## Important Notes

- **Residential IPs are often on Spamhaus.** Outlook/Microsoft domains will return `ip_blocked`. Budget for MillionVerifier credits.
- **Cloud VMs (GCP, AWS, Oracle) block outbound port 25.** SMTP verification won't work from cloud machines.
- **All consumer VPNs block port 25.** Don't waste time with WARP, ProtonVPN, etc.
- **Target <3% bounce rate.** If bounce rate is higher, stop the campaign and re-verify.
- **All steps are resumable.** Progress is saved every 50 leads.

## License

MIT

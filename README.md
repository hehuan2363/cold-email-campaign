# Cold Email Campaign CLI

Automation toolkit that takes raw Apollo lead CSVs and produces clean, verified lead lists ready for [Instantly](https://instantly.ai).

Works great with **Claude Code**, **Cursor**, and other AI coding agents via the included skill definition.

## What It Does

1. **Generate Icebreakers** — AI-powered personalized opening lines using Gemini
2. **Shorten Company Names** — Clean up long company names for email templates
3. **Verify Emails (SMTP)** — Free local verification catches ~40% of bad emails
4. **Verify Emails (MillionVerifier)** — API verification for emails blocked by Spamhaus (~$3/500 emails)
5. **Create Clean CSV** — Removes all non-sendable leads, outputs Instantly-ready CSV

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

### Usage

```bash
# Check everything is set up
uv run python campaign.py check

# Run full pipeline on a lead file
uv run python campaign.py run --file ../leads/my-leads.csv

# Or run individual steps
uv run python campaign.py icebreakers --file ../leads/my-leads.csv
uv run python campaign.py shorten --file ../leads/my-leads-with-icebreakers.csv
uv run python campaign.py verify --file ../leads/my-leads-with-icebreakers.csv
uv run python campaign.py verify-mv --file ../leads/my-leads-with-icebreakers.csv
uv run python campaign.py clean --file ../leads/my-leads-with-icebreakers.csv

# View stats
uv run python campaign.py stats --file ../leads/my-leads-with-icebreakers.csv
```

### Input Format

Export leads from [Apollo.io](https://apollo.io) as CSV. Required columns:
- `email` — Lead's email address
- `company_name` or `organization_name` — Company name
- `first_name` — Lead's first name
- `title` — Job title
- `website` — Company website (used for icebreakers)

### Output

The pipeline adds these columns:
- `icebreaker` — Personalized opening line
- `shortenedCompanyName` — Clean company name for `{{companyName}}` template variable
- `email_status` — One of: `valid`, `catch_all`, `rejected`, `no_mx`, `ip_blocked`, `unknown`

Final output: `*-CLEAN.csv` with only `valid` and `catch_all` leads.

## Using with Claude Code

This repo includes a Claude Code skill. After cloning, just use:

```
/cold-email-campaign
```

Claude will walk you through the entire pipeline.

## Project Structure

```
cold-email-campaign/
├── scripts/
│   ├── campaign.py          # Main CLI entry point
│   ├── config.py            # Configuration (env vars)
│   ├── pyproject.toml       # Dependencies
│   └── lib/
│       ├── icebreakers.py   # Gemini icebreaker generation
│       ├── shorten.py       # Company name shortening
│       ├── verify_smtp.py   # Local SMTP verification
│       ├── verify_mv.py     # MillionVerifier API
│       └── clean.py         # CSV cleaning
├── docs/
│   ├── Cold Email Campaign Playbook.md
│   ├── 6 Cold Email Sequences.md
│   ├── 6 Offers.md
│   ├── Icebreaker Generation Guide.md
│   └── How to write offer.md
├── leads/                   # Your CSV files go here (gitignored)
├── .claude/skills/          # Claude Code skill definition
├── CLAUDE.md                # Claude Code project context
└── README.md
```

## Important Notes

- **Residential IPs are often on Spamhaus.** Outlook/Microsoft domains will return `ip_blocked`. Budget for MillionVerifier credits.
- **Cloud VMs (GCP, AWS, Oracle) block outbound port 25.** SMTP verification won't work from cloud machines.
- **All consumer VPNs block port 25.** Don't waste time with WARP, ProtonVPN, etc.
- **Target <3% bounce rate.** If bounce rate is higher, stop the campaign and re-verify.
- **All steps are resumable.** Progress is saved every 50 leads.

## License

MIT

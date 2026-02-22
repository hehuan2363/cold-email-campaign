# Cold Email Campaign — AI Agent Skill

An AI agent skill that runs your entire cold email campaign end-to-end. Just type one command, answer a few questions, and your AI agent handles everything — from writing offers to producing a verified, clean lead list ready for [Instantly](https://instantly.ai).

Built for **Claude Code**, but works with any AI coding agent that supports skill/prompt files.

## How It Works

### 1. Start a new campaign
```
/cold-email-campaign start
```

The agent asks you about your business, niche, experience, and what you can offer for free. It saves your profile so every future session remembers who you are.

### 2. Agent generates your offers and lead filters

Based on your answers, the agent:
- Writes 2 offers (Free Build + Free Audit) tailored to your niche and credibility
- Gives you niche-specific databases to check (industry associations, directories)
- Gives you exact Apollo search filters (job titles, company size, industry, keywords)
- Tells you which columns to export

### 3. You go source leads

You leave to scrape leads from Apollo (or Apify). The agent tells you:

> Save the CSV to the `leads/` folder. When you have it, come back and type:
> `/cold-email-campaign process`

### 4. Resume — agent processes everything
```
/cold-email-campaign process
```

The agent picks up where you left off. It reads your profile, finds your CSV, and runs the full pipeline:
- Generates personalized icebreakers for every lead
- Shortens company names for email templates
- Verifies every email address (SMTP + MillionVerifier)
- Removes bad emails, produces clean CSV
- Writes 2 email sequences (one per offer) with A/B subject lines
- Gives you the Instantly launch checklist

You just watch it work and review the outputs.

## Setup (5 minutes)

```bash
# 1. Clone the repo
git clone https://github.com/hehuan2363/cold-email-campaign.git
cd cold-email-campaign

# 2. Set your API keys
export GEMINI_API_KEY="your-gemini-key"        # Free at https://aistudio.google.com/apikey
export MV_API_KEY="your-mv-key"                # Optional, ~$3/500 emails at https://millionverifier.com
export EHLO_DOMAIN="yourdomain.com"            # Your sending domain
export SENDER_EMAIL="verify@yourdomain.com"

# 3. Install dependencies
cd scripts && uv sync
```

**Requirements:** Python 3.10+, [uv](https://docs.astral.sh/uv/)

## Commands

### With Claude Code (recommended)
```
/cold-email-campaign start      # New campaign — discovery + offers + lead filters
/cold-email-campaign process    # Resume after sourcing leads — process CSV + write sequences
/cold-email-campaign offers     # Just generate offers
/cold-email-campaign sequences  # Just write email sequences
/cold-email-campaign launch     # Get Instantly launch checklist
```

### With other AI coding agents
Copy `.claude/skills/cold-email-campaign/SKILL.md` into your agent's prompt or context. The skill file contains the full pipeline instructions — any AI agent that can run shell commands will be able to follow it.

### Manual CLI (if you prefer)
```bash
cd scripts
uv run python campaign.py offers --niche "property management" --bg "I manage my own rental portfolio"
uv run python campaign.py sequences --niche "..." --offer "..." --sender "Alex" --bg "..."
uv run python campaign.py run --file ../leads/my-leads.csv
uv run python campaign.py stats --file ../leads/my-leads.csv
```

## The Flow

```
/cold-email-campaign start
        │
        ▼
  Discovery (agent asks about you)
        │
        ▼
  Generate offers (2 per niche)
        │
        ▼
  Apollo filters & lead sourcing guidance
        │
        ▼
  ── You go scrape leads, save CSV to leads/ ──
        │
        ▼
/cold-email-campaign process
        │
        ▼
  Icebreakers → Shorten names → Verify emails → Clean CSV
        │
        ▼
  Write email sequences (2 per offer, A/B test)
        │
        ▼
  Instantly launch checklist
```

## What's Inside

```
cold-email-campaign/
├── .claude/skills/          # The AI agent skill definition
├── scripts/
│   ├── campaign.py          # CLI entry point (the agent runs this for you)
│   └── lib/
│       ├── offers.py        # AI offer generation
│       ├── sequences.py     # AI email sequence writing
│       ├── icebreakers.py   # AI personalized openers
│       ├── shorten.py       # Company name shortening
│       ├── verify_smtp.py   # Free local email verification
│       ├── verify_mv.py     # MillionVerifier API verification
│       └── clean.py         # CSV cleaning
├── docs/                    # Playbook, example offers, example sequences
├── leads/                   # Drop your Apollo CSV exports here
├── CLAUDE.md                # Project context for AI agents
└── README.md
```

## Good to Know

- **Residential IPs are often on Spamhaus.** Outlook domains return `ip_blocked` — that's what MillionVerifier is for.
- **Cloud VMs and VPNs block port 25.** Don't try SMTP verification from GCP, AWS, Oracle, WARP, or ProtonVPN.
- **Target <3% bounce rate.** If higher, stop and re-verify.
- **All steps are resumable.** Progress saves every 50 leads.
- **Your profile is saved.** `docs/campaign-profile.md` stores your info so new sessions pick up where you left off.
- **Docs included.** Check `docs/` for the full playbook, example offers, and example email templates.

## License

MIT

# Cold Email Campaign — AI Agent Skill

An AI agent skill that runs your entire cold email campaign end-to-end. Just type one command, answer a few questions, and your AI agent handles everything — from writing offers to producing a verified, clean lead list ready for [Instantly](https://instantly.ai).

Built for **Claude Code**, but works with any AI coding agent that supports skill/prompt files.

## How It Works

```
/cold-email-campaign start
```

That's it. Your AI agent will:

1. **Ask about your niche** — What industry? What's your experience/credibility?
2. **Generate 2 offers** — Free Build + Free Audit, customized to your niche
3. **Tell you exactly how to source leads** — Apollo search filters, niche databases, what columns to export
4. **Process your leads** — Once you drop a CSV in `leads/`, the agent runs the full pipeline:
   - Generate personalized icebreakers for every lead
   - Shorten company names for email templates
   - Verify every email (SMTP + MillionVerifier)
   - Remove bad emails, produce clean CSV
5. **Write your email sequences** — 2-email sequences with subject line A/B test variations
6. **Give you the Instantly launch checklist** — Domain setup, warmup, monitoring targets

You just answer questions and review outputs. The agent runs all the scripts.

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

## Using It

### With Claude Code (recommended)
```
/cold-email-campaign start      # New campaign from scratch
/cold-email-campaign offers     # Just generate offers
/cold-email-campaign sequences  # Just write email sequences
/cold-email-campaign verify     # Just verify a lead file
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

## The Pipeline

| Step | What happens | Who does it |
|------|-------------|-------------|
| 1. Pick niche & write offers | AI asks questions, generates 2 offers per niche | Agent |
| 2. Source leads | Agent gives you Apollo filters & niche databases | You export CSV |
| 3. Generate icebreakers | Personalized opening lines via Gemini | Agent |
| 4. Shorten company names | Clean names for `{{companyName}}` variable | Agent |
| 5. Verify emails | SMTP check + MillionVerifier for blocked IPs | Agent |
| 6. Create clean CSV | Remove bad emails → Instantly-ready file | Agent |
| 7. Write email sequences | 2-email sequences with A/B subject lines | Agent |
| 8. Launch on Instantly | Domain setup, warmup, monitoring checklist | Agent guides you |

**Cost per 1,000 leads:** ~$8.50 (Apify scraping + MillionVerifier + Gemini API)

## Good to Know

- **Residential IPs are often on Spamhaus.** Outlook domains return `ip_blocked` — that's what MillionVerifier is for.
- **Cloud VMs and VPNs block port 25.** Don't try SMTP verification from GCP, AWS, Oracle, WARP, or ProtonVPN.
- **Target <3% bounce rate.** If higher, stop and re-verify.
- **All steps are resumable.** Progress saves every 50 leads.
- **Docs included.** Check `docs/` for the full playbook, example offers, and example email templates.

## License

MIT

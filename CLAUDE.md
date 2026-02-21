# Cold Email Campaign CLI

End-to-end cold email campaign automation. Guides users from niche selection through to Instantly launch.

## Project Structure
- `scripts/` — Python CLI tools (use `uv` for virtual env)
- `scripts/lib/` — Modular pipeline: offers, sequences, icebreakers, shorten, verify, clean
- `docs/` — Playbook, example email sequences, offers, and guides
- `leads/` — Put your CSV files here (gitignored)
- `.claude/skills/cold-email-campaign/` — Claude Code skill (use `/cold-email-campaign start`)

## Quick Start
```bash
cd scripts
uv run python campaign.py check                                    # Verify setup
uv run python campaign.py offers --niche "..." --bg "..."          # Generate offers
uv run python campaign.py sequences --niche "..." --offer "..." --sender "..." --bg "..."  # Write sequences
uv run python campaign.py run --file path/to.csv                   # Full technical pipeline
uv run python campaign.py stats --file path/to.csv                 # View stats
```

### Required Environment Variables
```bash
export GEMINI_API_KEY="your-gemini-key"      # For offers, sequences, icebreakers, company names
export MV_API_KEY="your-mv-key"              # For MillionVerifier (ip_blocked emails)
export EHLO_DOMAIN="yourdomain.com"          # For SMTP verification
export SENDER_EMAIL="verify@yourdomain.com"
```

## Rules
- Always use `uv` as virtual env manager — never `pip install` globally
- Use Gemini model `gemini-3-flash-preview` — not older models
- Don't ask for permission on routine tasks — just execute
- Save progress every 50 leads in all long-running scripts

# Cold Email Campaign CLI

Automation toolkit for cold email campaigns. Takes raw Apollo lead CSVs through icebreaker generation, company name shortening, email verification, and produces clean CSVs ready for Instantly.

## Project Structure
- `scripts/` — Python CLI tools (use `uv` for virtual env)
- `scripts/lib/` — Modular pipeline library
- `docs/` — Playbook, email sequences, and offer templates
- `leads/` — Put your CSV files here (gitignored)
- `.claude/skills/cold-email-campaign/` — Claude Code skill

## Quick Start
```bash
cd scripts
uv run python campaign.py check                    # Verify setup
uv run python campaign.py run --file path/to.csv   # Full pipeline
uv run python campaign.py stats --file path/to.csv # View stats
```

### Required Environment Variables
```bash
export GEMINI_API_KEY="your-gemini-key"    # For icebreakers + company names
export MV_API_KEY="your-mv-key"            # For MillionVerifier (ip_blocked emails)
export EHLO_DOMAIN="yourdomain.com"        # For SMTP verification
export SENDER_EMAIL="verify@yourdomain.com"
```

## Rules
- Always use `uv` as virtual env manager — never `pip install` globally
- Use Gemini model `gemini-3-flash-preview` — not older models
- Don't ask for permission on routine tasks — just execute
- Save progress every 50 leads in all long-running scripts

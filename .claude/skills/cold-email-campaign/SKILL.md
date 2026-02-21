---
name: cold-email-campaign
description: Run the full cold email campaign pipeline — from niche selection and offer creation to verified clean CSV ready for Instantly. Guides you through every step including writing offers, sourcing leads, generating icebreakers, verifying emails, writing sequences, and launching.
argument-hint: [step-name or "start"]
---

# Cold Email Campaign Pipeline

You are a cold email campaign expert guiding the user through the entire process end-to-end. This is NOT just a technical tool — you actively help the user make strategic decisions at every step.

## Arguments
- `$ARGUMENTS` — optional step name or "start" for a new campaign. If no argument, ask what the user wants to do.
  - `start` — Begin a new campaign from scratch (Step 1)
  - `offers` — Generate offers for a niche
  - `sequences` — Write email sequences
  - `leads` — Get guidance on sourcing leads
  - `icebreakers` — Generate icebreakers for a CSV
  - `verify` — Verify emails
  - `clean` — Create clean CSV
  - `run` — Run the technical pipeline (icebreakers → verify → clean)
  - `launch` — Get Instantly launch checklist

## Full Pipeline (8 Steps)

Guide the user through these steps IN ORDER. At each step, be proactive — don't just run commands, explain what's happening and why.

---

### Step 1: Pick a Niche & Write Offers

**This is the most important step.** A bad offer = low reply rate no matter how good everything else is.

Ask the user:
1. "What niche are you targeting?" (industry, type of business)
2. "What's your personal connection to this niche?" (experience, proof, credibility)
3. "What can you build or do for them for FREE?" (the offer)

**Offer formula** (every offer must have ALL THREE):
- **Free** — zero financial risk to the prospect
- **Low-friction response** — one-word reply ("yes", "interested")
- **Cheap for you to deliver** — reuse existing tools/templates

**Generate 2 offers per niche:**
- **Offer A: Free Build** — build something tangible for free (bot, demo, tool, report)
- **Offer B: Free Audit** — review their workflows, give actionable plan

**Template:** "I will give you [thing] in [time] or your money back — just send me [input]."

**Risk reversal language** (add to every offer):
- "You wouldn't owe me anything unless it actually drives results"
- "No cost, no strings — I'll do all the work"
- "Worst case, you walk away with a clear action plan"

Use Gemini to help generate offers:
```bash
cd scripts && uv run python campaign.py offers --niche "description of niche" --background "your relevant experience"
```

Save the offers to `docs/offers.md`. The user should review and customize before proceeding.

Reference: `docs/6 Offers.md` for example offers, `docs/How to write offer.md` for the offer writing framework.

---

### Step 2: Source Leads

**First, find niche-specific databases** (higher quality than generic search):
- Ask AI: "Where can I find a database of [industry] firms?"
- Examples: AIA (architects), AICPA (accountants), NARPM (property managers), industry association directories
- These give 100% accurate company lists; then use Apollo to enrich with emails

**Then, help the user build Apollo search filters:**

Tell the user to search on [Apollo.io](https://apollo.io) (or use Apify's Apollo scraper for bulk export). Give them specific filters:

| Filter | What to enter |
|--------|--------------|
| **Job titles** | Decision-makers: Owner, Managing Partner, Director of Operations, VP, CEO, CTO |
| **Company size** | Sweet spot: 10-200 employees (big enough to pay, small enough to reach decision-maker) |
| **Industry** | Be specific to the niche |
| **Location** | US & Canada (English-speaking, business-friendly) |

**Key columns to keep from Apollo export:**
- `firstName`, `lastName`, `email`, `title` (required)
- `organizationName`, `organizationDescription`, `organizationSpecialities` (for icebreakers)
- `city`, `state`, `organizationSize`, `organizationFoundedYear`, `organizationIndustry`

**Naming convention:** `YYYY-MM-DD-apollo-{Niche}-{filters}.csv`

Tell the user to save the CSV to the `leads/` directory.

---

### Step 3: Generate Icebreakers

Once the user has a CSV in `leads/`, run:
```bash
cd scripts && uv run python campaign.py icebreakers --file "../leads/your-file.csv"
```

**What this does:**
- Uses Gemini API to write a personalized 1-line opening for each lead
- References something specific about their company, role, or location
- Casual/spartan tone ("typed on phone")
- Saves progress every 50 leads (resumable if interrupted)
- Output: `*-with-icebreakers.csv`

**Icebreaker rules the AI follows:**
- One sentence, 10-20 words
- Always starts with "Hey {firstName}."
- Shortens company names and locations
- Returns "SKIP" for non-person entries

---

### Step 4: Shorten Company Names

```bash
cd scripts && uv run python campaign.py shorten --file "../leads/your-file-with-icebreakers.csv"
```

Adds `shortenedCompanyName` column — used as `{{companyName}}` in email templates.
Examples: "Johnson Controls International" → "Johnson Controls", "Deloitte LLP" → "Deloitte"

---

### Step 5: Verify Emails

```bash
cd scripts && uv run python campaign.py verify --file "../leads/your-file-with-icebreakers.csv"
```

**Layer 1: Local SMTP check** (free, catches ~40% of bad emails)
- Checks: syntax → MX lookup → SMTP RCPT TO probe
- Adds `email_status` column

**Layer 2: MillionVerifier API** (for `ip_blocked` leads):
```bash
cd scripts && uv run python campaign.py verify-mv --file "../leads/your-file-with-icebreakers.csv"
```
- Cost: ~$3/500 emails
- Required because residential IPs are often on Spamhaus blocklists

**Email status meanings:**
| Status | Action |
|--------|--------|
| `valid` | Safe to send |
| `catch_all` | Risky but sendable (~60% deliverable) |
| `rejected` | REMOVE — mailbox doesn't exist |
| `no_mx` | REMOVE — domain has no mail server |
| `ip_blocked` | Needs MillionVerifier |
| `invalid_syntax` | REMOVE |

---

### Step 6: Create Clean CSV

```bash
cd scripts && uv run python campaign.py clean --file "../leads/your-file-with-icebreakers.csv"
```

Removes all non-sendable leads. Keeps only `valid` and `catch_all`. Creates `*-CLEAN.csv`.

---

### Step 7: Write Email Sequences

Help the user write 2 email sequences (one per offer, for A/B testing).

Use Gemini to generate sequences:
```bash
cd scripts && uv run python campaign.py sequences --niche "niche" --offer "the offer text" --sender "sender name" --background "credibility/experience"
```

**Email formula:**
```
{{icebreaker}} → Who am I → Why trust me → Offer → CTA
```

**Structure (2 emails per sequence):**
- **Email 1:** Icebreaker → Credibility → Offer → Soft CTA
- **Email 2 (3 days later):** Shorter follow-up, bullet points, same offer, different angle

**Subject line rules:**
- Keep them short and personal: `{{firstName}}, question` or `{{firstName}}?`
- Never use salesy subject lines
- A/B test: `{{firstName}}, quick question` vs `idea for {{companyName}}`

**CTA strategy — Sell the Video, Not the Call:**
- Instead of asking for a call: "Can I send you a 90-second video showing how it works?"
- Much lower friction than booking a call

**Tone rules:**
- Sign off with "Sent from my iPhone" (looks personal)
- No HTML, no images, no links — plain text only
- Short paragraphs (2-3 lines max)
- Casual, like texting a colleague

Reference: `docs/6 Cold Email Sequences.md` for example sequences.

---

### Step 8: Launch on Instantly

Give the user this checklist:

**Domain/Inbox Setup:**
- Use 3 domains with 5 inboxes each = 15 sending accounts
- Each inbox sends ~30 emails/day
- Total capacity: ~450 emails/day
- Warm up all inboxes for 2+ weeks before sending

**Campaign Setup:**
1. Create one campaign per sequence (A/B test two offers)
2. Upload the `*-CLEAN.csv`
3. Map variables: `{{firstName}}`, `{{companyName}}` (use `shortenedCompanyName` column), `{{icebreaker}}`
4. Set follow-up delay: 3 days
5. Schedule: Monday–Saturday, 7:00am–7:00pm recipient's timezone
6. Start at 25 emails/day per inbox, ramp up gradually

**Monitoring:**
- Target: **<3% bounce rate** (if higher, STOP and re-verify)
- Target: **>1% reply rate**
- After ~300 sends, compare A vs B offers — kill the loser
- Winner with >2% reply rate → add a 3rd follow-up email

---

## Quick Commands Reference

```bash
cd scripts

# Strategy (AI-assisted)
uv run python campaign.py offers --niche "..." --background "..."
uv run python campaign.py sequences --niche "..." --offer "..." --sender "..." --background "..."

# Technical pipeline
uv run python campaign.py check
uv run python campaign.py icebreakers --file "../leads/file.csv"
uv run python campaign.py shorten --file "../leads/file.csv"
uv run python campaign.py verify --file "../leads/file.csv"
uv run python campaign.py verify-mv --file "../leads/file.csv"
uv run python campaign.py clean --file "../leads/file.csv"
uv run python campaign.py stats --file "../leads/file.csv"

# Full technical pipeline (steps 3-6 at once)
uv run python campaign.py run --file "../leads/file.csv"
```

## Important Notes
- **Residential IPs are often on Spamhaus.** Outlook/Microsoft domains will return `ip_blocked`. Always budget for MillionVerifier.
- **Cloud VMs (GCP, AWS, Oracle) block outbound port 25.** Don't try SMTP verification from cloud machines.
- **All consumer VPNs block port 25.** Don't waste time with WARP, ProtonVPN, etc.
- **Target <3% bounce rate.** If higher, stop the campaign immediately and re-verify.
- **Save progress every 50 leads** to avoid losing work on interruption.
- **Always verify before sending.** Never send to unverified leads.

## Config
- **Gemini API key:** `GEMINI_API_KEY` env var
- **MillionVerifier API key:** `MV_API_KEY` env var
- **SMTP domain:** `EHLO_DOMAIN` and `SENDER_EMAIL` env vars
- **Python env:** Always use `uv` — never install packages globally

## Playbook Reference
Full documentation: `docs/Cold Email Campaign Playbook.md`

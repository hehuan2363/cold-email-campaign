---
name: cold-email-campaign
description: Run the full cold email campaign pipeline — from niche selection and offer creation to verified clean CSV ready for Instantly. Guides you through every step including writing offers, sourcing leads, generating icebreakers, verifying emails, writing sequences, and launching.
argument-hint: [step-name or "start"]
---

# Cold Email Campaign Pipeline

You are a cold email campaign expert guiding the user through the entire process end-to-end. This is NOT just a technical tool — you actively help the user make strategic decisions at every step.

## Arguments
- `$ARGUMENTS` — optional step name or "start" for a new campaign. If no argument, ask what the user wants to do.
  - `start` — Begin a new campaign from scratch (Step 0: Discovery)
  - `offers` — Generate offers for a niche
  - `leads` — Get guidance on sourcing leads
  - `process` — Resume after sourcing leads — run icebreakers, verify, clean, sequences
  - `sequences` — Write email sequences
  - `launch` — Get Instantly launch checklist

---

## Step 0: Discovery — Understand the User

**ALWAYS start here for new campaigns.** You cannot write good offers or sequences without understanding the user first.

Save all answers to `docs/campaign-profile.md` so any future session can pick up where the user left off.

**Ask these questions one at a time** (don't dump all at once):

1. **"What's your business? What do you sell or do?"**
   - Need: their core service/product

2. **"Who have you helped before? What results did you get them?"**
   - Need: proof, case studies, numbers — even if informal ("I automated my own bookkeeping and saved 10 hours/week")

3. **"What niche are you targeting with this campaign?"**
   - Need: specific industry (not "small businesses" — too broad)

4. **"Why this niche? Do you have personal experience or credibility here?"**
   - Need: the "why me" — this is what makes the email believable vs generic
   - Good: "I managed rental properties for 5 years" / "I was a CPA for 10 years" / "I built document search at an engineering firm"
   - If they have no connection, help them find an angle or suggest a niche where they DO have credibility

5. **"What could you realistically build or do for a prospect for FREE in under a week?"**
   - Need: the free deliverable (bot, demo, audit, report, template)
   - It must be: genuinely useful, cheap to produce (reuse templates), and easy to say "yes" to

6. **"What's your name and sending domain?"**
   - Need: first name (for email signature) and domain (for SMTP config)

**After collecting answers, write `docs/campaign-profile.md`:**
```markdown
# Campaign Profile

## Business
[what they do]

## Proof / Results
[past results, case studies, experience]

## Target Niche
[specific industry]

## Credibility / Connection
[why this niche, personal angle]

## Free Deliverable
[what they can build/do for free]

## Sender
- Name: [first name]
- Domain: [domain]
```

Then proceed to Step 1.

---

## Step 1: Generate Offers

**This is the most important step.** A bad offer = low reply rate no matter how good everything else is.

Read `docs/campaign-profile.md` to recall the user's info. Then generate offers.

**Every offer MUST have ALL THREE:**
- **Free** — zero financial risk to the prospect
- **Low-friction response** — one-word reply ("yes", "interested")
- **Cheap for you to deliver** — reuse existing tools/templates

**Generate 2 offers:**
- **Offer A: Free Build** — build something tangible for free (bot, demo, tool, report)
- **Offer B: Free Audit** — review their workflows, give actionable plan

**Template:** "I will give you [thing] in [time] or your money back — just send me [input]."

**Risk reversal language** (add to every offer):
- "You wouldn't owe me anything unless it actually drives results"
- "No cost, no strings — I'll do all the work"
- "Worst case, you walk away with a clear action plan"

Run:
```bash
cd scripts && uv run python campaign.py offers --niche "[niche from profile]" --bg "[credibility from profile]"
```

Save output to `docs/offers.md`. Present both offers to the user, explain why each works, and ask them to pick their favorite or tweak.

Reference: `docs/6 Offers.md` for examples, `docs/How to write offer.md` for the framework.

---

## Step 2: Source Leads

**First, suggest niche-specific databases** (higher quality than generic scraping):
- Search the web: "Where can I find a database/directory of [niche] firms?"
- Examples: AIA (architects), AICPA (accountants), NARPM (property managers), ABC (contractors)
- These give 100% accurate company lists; Apollo enriches with emails

**Then, give the user EXACT Apollo search filters for their niche:**

Based on their profile, generate a ready-to-paste filter set:

| Filter | Value |
|--------|-------|
| **Job titles** | [3-5 decision-maker titles specific to their niche] |
| **Company size** | [sweet spot for their niche, e.g., 10-200 employees] |
| **Industry** | [specific Apollo industry tags] |
| **Location** | US & Canada |
| **Keywords** | [niche-specific keywords to narrow results] |

**Tell the user which columns to export from Apollo:**
- Required: `firstName`, `lastName`, `email`, `title`
- For icebreakers: `organizationName`, `organizationDescription`, `organizationSpecialities`
- Optional: `city`, `state`, `organizationSize`, `organizationFoundedYear`, `organizationIndustry`

**Then tell the user:**

> Save the CSV to the `leads/` folder. When you have it, come back and type:
>
> `/cold-email-campaign process`
>
> I'll take it from there — icebreakers, verification, clean CSV, and email sequences.

**Also save the filters to `docs/campaign-profile.md`** so the user (or a future session) can reference them.

---

## Step 3: Process Leads (Resume Point)

**This is where the user comes back after scraping.** When they type `/cold-email-campaign process`:

1. **Check for CSV files** — Look in `leads/` for new CSV files:
```bash
ls -la leads/*.csv
```

2. **Read `docs/campaign-profile.md`** to recall the user's niche, credibility, offers, and sender name. If the file doesn't exist, ask the discovery questions from Step 0.

3. **Confirm with the user** — "I see `leads/[filename].csv`. Should I process this file? I'll generate icebreakers, shorten company names, verify emails, and create a clean CSV."

4. **Run the technical pipeline:**

```bash
cd scripts && uv run python campaign.py icebreakers --file "../leads/[file].csv"
```
Wait for completion, then:
```bash
cd scripts && uv run python campaign.py shorten --file "../leads/[file]-with-icebreakers.csv"
```
Then:
```bash
cd scripts && uv run python campaign.py verify --file "../leads/[file]-with-icebreakers.csv"
```
Then check stats:
```bash
cd scripts && uv run python campaign.py stats --file "../leads/[file]-with-icebreakers.csv"
```

If there are `ip_blocked` leads and MV_API_KEY is set:
```bash
cd scripts && uv run python campaign.py verify-mv --file "../leads/[file]-with-icebreakers.csv"
```
If MV_API_KEY is not set, tell the user how many leads are ip_blocked and that they need a MillionVerifier API key (~$3/500 emails) to verify these. Ask if they want to proceed without them or set the key.

Finally, create clean CSV:
```bash
cd scripts && uv run python campaign.py clean --file "../leads/[file]-with-icebreakers.csv"
```

5. **Show results** — Tell the user: total leads, how many are sendable, how many were removed, and the clean file name.

6. **Proceed to Step 4** — Offer to generate email sequences.

---

## Step 4: Write Email Sequences

**Read `docs/campaign-profile.md`** for the user's info (name, niche, credibility, offers).

Generate 2 sequences (one per offer) for A/B testing:

```bash
cd scripts && uv run python campaign.py sequences --niche "[niche]" --offer "[offer A text]" --sender "[name]" --bg "[credibility]"
```

Then run again for Offer B.

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
- Sign off with just the sender's first name
- Add "Sent from my iPhone" at the bottom
- No HTML, no images, no links — plain text only
- Short paragraphs (2-3 lines max)
- Casual, like texting a colleague

Present both sequences to the user. Let them tweak tone, adjust the offer language, or rewrite parts.

Reference: `docs/6 Cold Email Sequences.md` for example sequences.

---

## Step 5: Launch on Instantly

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

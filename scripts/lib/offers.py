"""Generate cold email offers using Gemini API."""
import os
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL

if not GEMINI_API_KEY:
    raise ValueError("Set GEMINI_API_KEY environment variable")

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are a cold email offer strategist. You help people craft irresistible free offers for cold outreach campaigns.

Every offer MUST have all three qualities:
1. **Free** — zero financial risk to the prospect
2. **Low-friction response** — prospect replies with one word ("yes", "interested")
3. **Cheap to deliver** — uses existing tools/templates, won't bankrupt you at scale

OFFER FORMULA: "I will give you [thing] in [time] or your money back — just send me [input]."

You always generate TWO offers per niche:
- **Offer A: Free Build** — build something tangible for free (bot, demo, tool, report, template)
- **Offer B: Free Audit** — review their workflows, give actionable plan

For each offer, include:
1. The offer statement (2-3 sentences, conversational tone)
2. Why it works (bullet points: risk, friction, cost to deliver, value to prospect)
3. Suggested Apollo search filters (job titles, company size, industry, location)

Add risk reversal language to each offer:
- "No cost, no strings — I'll do all the work"
- "Worst case, you walk away with a clear action plan"
- "You wouldn't owe me anything unless it actually drives results"

Also suggest niche-specific lead databases BEFORE Apollo:
- Ask: "Where can I find a database of [industry] firms?"
- Examples: AIA (architects), AICPA (accountants), NARPM (property managers)
- These give 100% accurate company lists; Apollo enriches with emails"""


def generate(niche: str, background: str) -> str:
    """Generate 2 offers for a niche."""
    prompt = f"""Generate 2 cold email offers for this niche:

NICHE: {niche}

MY BACKGROUND/CREDIBILITY: {background}

Generate:
1. Offer A (Free Build) — something tangible I can build for free
2. Offer B (Free Audit) — a review/audit I can do for free
3. Suggested Apollo search filters for finding leads in this niche
4. Niche-specific databases to check before Apollo

Format as clean markdown."""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.8,
        ),
    )
    return response.text


def process(niche: str, background: str, output_file: str = None):
    """Generate offers and save to file."""
    print(f"Generating offers for: {niche}")
    print(f"Background: {background}\n")

    result = generate(niche, background)
    print(result)

    if output_file:
        with open(output_file, "w") as f:
            f.write(f"# Offers — {niche}\n\n")
            f.write(result)
        print(f"\nSaved to: {output_file}")

    return result

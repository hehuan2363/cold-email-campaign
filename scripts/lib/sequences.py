"""Generate cold email sequences using Gemini API."""
import os
from google import genai
from google.genai import types
from config import GEMINI_API_KEY, GEMINI_MODEL

if not GEMINI_API_KEY:
    raise ValueError("Set GEMINI_API_KEY environment variable")

client = genai.Client(api_key=GEMINI_API_KEY)

SYSTEM_PROMPT = """You are a cold email copywriter. You write short, casual, high-converting cold email sequences.

STRUCTURE — each sequence has 2 emails:
- **Email 1:** {{icebreaker}} → Who am I → Why trust me → Offer → Soft CTA
- **Email 2 (sent 3 days later):** Shorter follow-up, bullet points, same offer, different angle

TONE RULES:
- Plain text only. No HTML, no images, no links.
- Short paragraphs (2-3 lines max).
- Casual, like texting a colleague. Not salesy.
- Sign off with just the sender's first name.
- Add "Sent from my iPhone" at the bottom (looks personal).
- No exclamation marks in the body.

SUBJECT LINE RULES:
- Keep them short and personal: "{{firstName}}, question" or "{{firstName}}?"
- Never use salesy subject lines
- Provide 3 subject line variations to A/B test

CTA STRATEGY — Sell the Video, Not the Call:
- Instead of asking for a call directly, offer a short Loom video
- "Can I send you a 90-second video showing how it works?"
- Also provide an alternative direct CTA for comparison

VARIABLES available:
- {{firstName}} — prospect's first name
- {{companyName}} — shortened company name
- {{icebreaker}} — personalized opening line (already generated)

IMPORTANT: The {{icebreaker}} line is generated separately and already personalized. Use it as-is at the start of Email 1. Do NOT write a new icebreaker.

Output format: Clean markdown with clear Email 1 / Email 2 sections, subject lines, and the full email body."""


def generate(niche: str, offer: str, sender: str, background: str) -> str:
    """Generate a 2-email sequence for an offer."""
    prompt = f"""Write a cold email sequence for this campaign:

NICHE: {niche}
OFFER: {offer}
SENDER NAME: {sender}
SENDER BACKGROUND: {background}

Generate:
1. Three subject line variations to A/B test
2. Email 1 (initial outreach)
3. Email 2 (follow-up, sent 3 days later)

Use {{{{icebreaker}}}}, {{{{firstName}}}}, and {{{{companyName}}}} variables where appropriate."""

    response = client.models.generate_content(
        model=GEMINI_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=SYSTEM_PROMPT,
            temperature=0.8,
        ),
    )
    return response.text


def process(niche: str, offer: str, sender: str, background: str, output_file: str = None):
    """Generate email sequence and save to file."""
    print(f"Generating email sequence for: {niche}")
    print(f"Offer: {offer[:80]}...\n")

    result = generate(niche, offer, sender, background)
    print(result)

    if output_file:
        with open(output_file, "w") as f:
            f.write(f"# Email Sequence — {niche}\n\n")
            f.write(f"**Offer:** {offer}\n\n")
            f.write(result)
        print(f"\nSaved to: {output_file}")

    return result

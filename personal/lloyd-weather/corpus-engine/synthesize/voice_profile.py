"""Build the Lloyd voice profile (system prompt) and example bank.

Reads voice_features.json and forecast_dimensions.json,
then uses Claude to compose the system prompt and curate examples.
"""
import json
import re
from pathlib import Path
from anthropic import Anthropic
from config import CORPUS_DIR, ANALYSIS_DIR, OUTPUT_DIR, CLAUDE_MODEL

client = Anthropic()

SYSTEM_PROMPT_PROMPT = """You are building a system prompt that will make Claude sound exactly like Lloyd Mallah, an amateur meteorologist in Westchester, NY who runs a $6/month weather concierge service for NYC tri-state suburbanites.

Below are two analysis documents:
1. VOICE FEATURES — Lloyd's specific linguistic patterns, verbal tics, structural habits, tonal characteristics, and audience awareness traits
2. FORECAST PROFILE — Lloyd's forecasting tendencies across 10 dimensions (model preferences, biases, communication style, etc.)

Using ONLY the evidence in these documents (no inventing), write a system prompt in Markdown format with these sections:

## Who You Are
Establish Lloyd's identity, background, personality in 2-3 sentences. Make it feel human, not robotic.

## How You Talk
Detailed, specific voice instructions. NOT "be casual" — instead "use phrases like [exact phrases from features]. Open messages with [his actual pattern]. When excited about snow, [specific behavior]." Every instruction should cite real patterns from the analysis.

## Your Forecasting Style
How Lloyd thinks about weather. Which models he trusts. How he handles uncertainty. His biases (and how they manifest). His temporal focus. Based entirely on the forecast profile.

## How You Answer Questions
- For routine questions (will it rain tomorrow): [Lloyd's pattern]
- For high-stakes decisions (cancel the party?): [Lloyd's pattern]
- For big events (nor'easter incoming): [Lloyd's pattern]
- For follow-ups: [Lloyd's pattern]

## Response Format
- Web chat: 1-3 paragraphs max. Lead with the answer, then explain.
- SMS: Under 300 characters. Same personality, tighter.
- Always give a clear recommendation — never just data.

## Things Lloyd Would NEVER Say
Anti-patterns from the analysis. Phrases, tones, and structures that would break the illusion.

## Disclaimer
End every response with a subtle, Lloyd-voiced version of: "This is entertainment, not professional meteorological advice."

---

VOICE FEATURES:
{voice_features}

FORECAST PROFILE:
{forecast_profile}"""

EXAMPLE_BANK_PROMPT = """You are curating an example bank from Lloyd Mallah's actual writing. These examples will be used for few-shot prompting — when a user asks about snow, we pull Lloyd's real snow messages as context.

From the corpus below, select 50-80 of the BEST examples. For each, provide:
- The original text (exact, unedited)
- Tags for retrieval: weather type (winter, summer, severe, daily), confidence level (bold, hedged, uncertain), format (long_analysis, quick_answer, update), topic (school_closing, beach, ski, commute, outdoor_event, general), emotional register (excited, matter_of_fact, disappointed, cautious)
- A "use_for" field: what kind of user question would this example help answer?

Output as JSON array:
[
    {{
        "text": "exact Lloyd message",
        "source": "gmail|whatsapp|twitter",
        "date": "date if available",
        "tags": {{
            "weather_type": "winter|summer|severe|daily",
            "confidence": "bold|hedged|uncertain",
            "format": "long_analysis|quick_answer|update",
            "topic": ["school_closing", "beach", ...],
            "emotion": "excited|matter_of_fact|disappointed|cautious"
        }},
        "use_for": "description of what questions this helps answer"
    }}
]

Select examples that cover the full range of Lloyd's voice — not just his best moments. Include mundane daily forecasts, follow-ups, corrections, and excitement peaks.

CORPUS (sorted by richness):
{corpus}"""


def build_voice_profile():
    """Build the system prompt and example bank.

    Saves:
    - output/voice_profile.md (the system prompt)
    - output/example_bank.jsonl (tagged examples)
    """
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    with open(ANALYSIS_DIR / "voice_features.json") as f:
        voice_features = json.load(f)
    with open(ANALYSIS_DIR / "forecast_dimensions.json") as f:
        forecast_profile = json.load(f)

    print("   Composing system prompt...")
    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=8192,
        messages=[{
            "role": "user",
            "content": SYSTEM_PROMPT_PROMPT.format(
                voice_features=json.dumps(voice_features, indent=2),
                forecast_profile=json.dumps(forecast_profile, indent=2),
            ),
        }],
    )

    system_prompt = response.content[0].text
    with open(OUTPUT_DIR / "voice_profile.md", "w") as f:
        f.write(system_prompt)

    print("   Curating example bank...")
    corpus_path = CORPUS_DIR / "corpus.jsonl"
    corpus = []
    with open(corpus_path) as f:
        for line in f:
            corpus.append(json.loads(line))

    corpus.sort(key=lambda r: r.get("word_count", 0), reverse=True)
    # Limit to ~50 messages and truncate each to avoid token limits
    corpus_text = "\n\n".join(
        f"[{r['source']}, {r.get('date', '?')}] {r.get('subject', '')}\n{r['content'][:2000]}"
        for r in corpus[:50]
    )

    response = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=8192,
        messages=[{
            "role": "user",
            "content": EXAMPLE_BANK_PROMPT.format(corpus=corpus_text),
        }],
    )

    result_text = response.content[0].text
    try:
        if "```" in result_text:
            m = re.search(r"```(?:json)?\s*\n?(.*?)```", result_text, re.DOTALL)
            if m:
                result_text = m.group(1)
        examples = json.loads(result_text)
    except json.JSONDecodeError:
        examples = [{"raw_text": result_text, "parse_error": True}]

    with open(OUTPUT_DIR / "example_bank.jsonl", "w") as f:
        for example in examples:
            f.write(json.dumps(example) + "\n")

    return len(examples)

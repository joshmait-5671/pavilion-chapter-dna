"""Extract Lloyd's voice characteristics from the corpus using Claude.

Processes the corpus in batches, extracts features per batch,
then runs a consolidation pass to synthesize the definitive voice profile.
"""
import json
import os
import re
from pathlib import Path
from config import CORPUS_DIR, ANALYSIS_DIR, CLAUDE_MODEL, BATCH_SIZE
from anthropic import Anthropic

client = Anthropic()

EXTRACTION_PROMPT = """You are analyzing writing samples from Lloyd Mallah, an amateur meteorologist who sends weather forecasts to friends and family in the NYC tri-state area. Your job is to extract his distinct voice characteristics.

Analyze these {count} messages and extract specific, concrete features in these categories:

## 1. LEXICAL FEATURES
- Signature phrases and verbal tics (exact phrases he repeats)
- Weather-specific vocabulary preferences (does he say "precip" or "precipitation"? "gonna dump" or "significant accumulation"?)
- Hedging language patterns (how he expresses uncertainty)
- Exclamation and emphasis patterns (ALL CAPS, exclamation marks, emoji)
- How he references weather models (casual "the Euro" vs formal "ECMWF")
- Slang, abbreviations, colloquialisms

## 2. STRUCTURAL FEATURES
- How he opens messages (headline first? context? greeting?)
- How he closes (sign-off style, confidence statement, call to action?)
- Paragraph structure (long blocks vs short punchy lines)
- Use of lists, bullets, formatting
- Average sentence length and variation
- Rhetorical devices and questions

## 3. TONAL FEATURES
- What triggers peak excitement (snow storms? uncertainty? being right?)
- Humor patterns (self-deprecating? observational? weather puns?)
- How he signals confidence levels (high confidence vs low confidence language)
- How he handles being wrong (deflect, own it, reframe?)
- Warmth and personality indicators

## 4. AUDIENCE AWARENESS
- Does he explain technical concepts or assume knowledge?
- Actionability language (specific advice like "bring an umbrella", "push the party")
- Empathy markers ("I know this isn't what you wanted to hear")
- Who he seems to be writing for (audience assumptions)

For EACH feature you identify, provide:
- The feature name
- 2-3 EXACT quotes from the messages demonstrating it
- How frequently it appears (every message, often, sometimes, rarely)

Be specific. "He uses casual language" is useless. "He consistently says 'gonna dump' instead of 'heavy snowfall' and 'the Euro' instead of 'ECMWF'" is useful.

Here are the messages:

{messages}"""

CONSOLIDATION_PROMPT = """You have analyzed {batch_count} batches of Lloyd Mallah's writing (an amateur meteorologist in the NYC tri-state area). Below are the voice features extracted from each batch.

Your job: synthesize these into ONE definitive voice feature set. For each feature:
1. Keep it if it appears in 2+ batches (consistent pattern, not a one-off)
2. Pick the best example quotes across all batches
3. Rate frequency: "signature" (nearly every message), "frequent" (most messages), "occasional" (some messages)
4. Flag any contradictions (e.g., sometimes formal, sometimes casual — note the context that triggers each)

Output a single JSON object with this structure:
{{
    "lexical": [
        {{
            "feature": "description of the feature",
            "examples": ["exact quote 1", "exact quote 2"],
            "frequency": "signature|frequent|occasional",
            "notes": "any context about when/why this appears"
        }}
    ],
    "structural": [...same format...],
    "tonal": [...same format...],
    "audience": [...same format...],
    "anti_patterns": [
        "Things Lloyd would NEVER say or do"
    ],
    "voice_summary": "2-3 sentence summary of Lloyd's overall voice character"
}}

Here are the batch results:

{batch_results}"""


def _load_corpus():
    """Load the normalized corpus."""
    corpus_path = CORPUS_DIR / "corpus.jsonl"
    records = []
    with open(corpus_path) as f:
        for line in f:
            records.append(json.loads(line))
    return records


def _format_messages_for_prompt(records):
    """Format a batch of records for the Claude prompt."""
    parts = []
    for i, r in enumerate(records, 1):
        source_label = {"gmail": "Email", "whatsapp": "WhatsApp", "twitter": "Tweet"}
        label = source_label.get(r["source"], r["source"])
        header = f"--- Message {i} ({label}, {r.get('date', 'date unknown')}) ---"
        if r.get("subject"):
            header += f"\nSubject: {r['subject']}"
        parts.append(f"{header}\n{r['content']}\n")
    return "\n".join(parts)


def _chunk(lst, size):
    """Split list into chunks of given size."""
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def extract_voice_features():
    """Run batched voice extraction then consolidation.

    Saves result to data/analysis/voice_features.json.
    """
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    corpus = _load_corpus()

    corpus.sort(key=lambda r: r.get("word_count", 0), reverse=True)
    corpus = corpus[:200]

    print(f"   Analyzing {len(corpus)} messages in batches of {BATCH_SIZE}...")

    batch_results = []
    for i, batch in enumerate(_chunk(corpus, BATCH_SIZE)):
        messages_text = _format_messages_for_prompt(batch)
        prompt = EXTRACTION_PROMPT.format(count=len(batch), messages=messages_text)

        print(f"   Batch {i + 1}/{len(corpus) // BATCH_SIZE + 1}...")

        response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=4096,
            messages=[{"role": "user", "content": prompt}],
        )

        batch_results.append({
            "batch_index": i,
            "message_count": len(batch),
            "result": response.content[0].text,
        })

    print("   Running consolidation pass...")
    batch_texts = "\n\n".join(
        f"=== BATCH {r['batch_index'] + 1} ({r['message_count']} messages) ===\n{r['result']}"
        for r in batch_results
    )

    consolidation = client.messages.create(
        model=CLAUDE_MODEL,
        max_tokens=8192,
        messages=[{
            "role": "user",
            "content": CONSOLIDATION_PROMPT.format(
                batch_count=len(batch_results),
                batch_results=batch_texts,
            ),
        }],
    )

    result_text = consolidation.content[0].text

    try:
        json_match = result_text
        if "```" in result_text:
            m = re.search(r"```(?:json)?\s*\n?(.*?)```", result_text, re.DOTALL)
            if m:
                json_match = m.group(1)
        features = json.loads(json_match)
    except json.JSONDecodeError:
        features = {"raw_text": result_text, "parse_error": True}

    output_path = ANALYSIS_DIR / "voice_features.json"
    with open(output_path, "w") as f:
        json.dump(features, f, indent=2)

    raw_path = ANALYSIS_DIR / "voice_batches_raw.json"
    with open(raw_path, "w") as f:
        json.dump(batch_results, f, indent=2)

    return features

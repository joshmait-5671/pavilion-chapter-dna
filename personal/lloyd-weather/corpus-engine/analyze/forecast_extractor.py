"""Map Lloyd's forecasting patterns to the 10-dimension meteorologist framework.

Uses the same batched analysis approach as voice_extractor.py.
"""
import json
import os
import re
from pathlib import Path
from config import CORPUS_DIR, ANALYSIS_DIR, CLAUDE_MODEL, BATCH_SIZE, ROOT
from anthropic import Anthropic

client = Anthropic()


def _load_framework():
    """Load the meteorologist framework definition."""
    framework_path = ROOT.parent / "meteorologist-framework.md"
    with open(framework_path) as f:
        return f.read()


EXTRACTION_PROMPT = """You are analyzing weather forecasting messages from Lloyd Mallah, an amateur meteorologist in the NYC tri-state area (Westchester, NY).

Your job: map his forecasting tendencies against this professional meteorologist framework:

{framework}

---

Analyze these {count} messages. For EACH of the 10 dimensions, provide:
1. Where Lloyd falls on the spectrum (cite the specific level/category from the framework)
2. Your confidence in this assessment (high/medium/low based on evidence available)
3. 1-3 EXACT quotes from the messages that demonstrate this placement
4. Any nuances (e.g., "usually X but when snow is involved, shifts to Y")

Here are the messages:

{messages}"""

CONSOLIDATION_PROMPT = """You analyzed {batch_count} batches of Lloyd Mallah's weather writing against a 10-dimension meteorologist framework. Below are the per-batch assessments.

Synthesize into ONE definitive profile. For each dimension:
1. Determine the final placement based on weight of evidence across all batches
2. Note if placement shifts by context (e.g., different for snow vs. daily weather)
3. Pick the 2-3 strongest evidence quotes across all batches
4. Rate confidence: high (consistent across batches), medium (some variance), low (insufficient data)

Output JSON:
{{
    "dimensions": {{
        "1_model_reliance": {{
            "placement": "where on spectrum",
            "confidence": "high|medium|low",
            "evidence": ["quote1", "quote2"],
            "nuance": "any contextual shifts",
            "summary": "one sentence"
        }},
        "2_model_allegiance": {{...}},
        "3_probabilistic_sophistication": {{...}},
        "4_bias_profile": {{...}},
        "5_temporal_focus": {{...}},
        "6_phenomenon_specialty": {{...}},
        "7_communication_style": {{...}},
        "8_verification_accountability": {{...}},
        "9_local_knowledge": {{...}},
        "10_update_discipline": {{...}}
    }},
    "overall_profile": "3-4 sentence summary of Lloyd as a forecaster"
}}

Batch assessments:

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
    for i in range(0, len(lst), size):
        yield lst[i : i + size]


def extract_forecast_dimensions():
    """Run batched forecast dimension extraction then consolidation.

    Saves result to data/analysis/forecast_dimensions.json.
    """
    ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
    framework = _load_framework()
    corpus = _load_corpus()

    corpus = [r for r in corpus if r.get("has_forecast")]
    corpus.sort(key=lambda r: r.get("word_count", 0), reverse=True)
    corpus = corpus[:150]

    print(f"   Analyzing {len(corpus)} forecast messages in batches of {BATCH_SIZE}...")

    batch_results = []
    for i, batch in enumerate(_chunk(corpus, BATCH_SIZE)):
        messages_text = _format_messages_for_prompt(batch)
        prompt = EXTRACTION_PROMPT.format(
            framework=framework,
            count=len(batch),
            messages=messages_text,
        )

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
        dimensions = json.loads(json_match)
    except json.JSONDecodeError:
        dimensions = {"raw_text": result_text, "parse_error": True}

    output_path = ANALYSIS_DIR / "forecast_dimensions.json"
    with open(output_path, "w") as f:
        json.dump(dimensions, f, indent=2)

    return dimensions

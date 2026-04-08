"""Validate the voice profile by generating test responses and judging them.

Uses a blind A/B comparison: real Lloyd vs Claude-as-Lloyd.
"""
import json
import re
import random
from pathlib import Path
from anthropic import Anthropic
from config import CORPUS_DIR, OUTPUT_DIR, CLAUDE_MODEL
from validate.scenarios import SCENARIOS

client = Anthropic()

JUDGE_PROMPT = """You are evaluating whether an AI-generated weather response successfully mimics a specific person's voice and style.

Below is a REAL message from Lloyd Mallah (an amateur meteorologist) and an AI-GENERATED response that attempts to sound like Lloyd.

Rate the AI response on these criteria (1-5 scale):
1. **Voice match** — Does it sound like the same person wrote both? Same verbal tics, vocabulary, energy level?
2. **Structural match** — Same message structure, paragraph patterns, opening/closing style?
3. **Tonal match** — Same emotional register, confidence level, humor?
4. **Authenticity** — Would someone who knows Lloyd be fooled? Or does it feel "off"?
5. **Weather quality** — Is the forecast reasoning sound and actionable?

REAL LLOYD MESSAGE:
{real_message}

AI-GENERATED RESPONSE (attempting to sound like Lloyd):
{ai_response}

Provide your rating as JSON:
{{
    "voice_match": N,
    "structural_match": N,
    "tonal_match": N,
    "authenticity": N,
    "weather_quality": N,
    "overall": N,
    "what_works": "specific things the AI got right",
    "what_fails": "specific things that break the illusion",
    "suggestions": "how to improve the voice profile"
}}"""


def _load_voice_profile():
    """Load the generated system prompt."""
    with open(OUTPUT_DIR / "voice_profile.md") as f:
        return f.read()


def _load_example_bank():
    """Load curated examples."""
    examples = []
    with open(OUTPUT_DIR / "example_bank.jsonl") as f:
        for line in f:
            examples.append(json.loads(line))
    return examples


def _find_real_example(scenario, corpus):
    """Find a real Lloyd message that's somewhat relevant to the scenario."""
    scenario_keywords = scenario["context"].lower().split()
    best = None
    best_score = 0
    for record in corpus:
        content_lower = record["content"].lower()
        score = sum(1 for kw in scenario_keywords if kw in content_lower)
        if score > best_score and record.get("word_count", 0) > 50:
            best = record
            best_score = score
    return best


def run_validation():
    """Run voice validation across all test scenarios.

    Saves output/validation_report.md.
    """
    voice_profile = _load_voice_profile()
    examples = _load_example_bank()

    corpus = []
    with open(CORPUS_DIR / "corpus.jsonl") as f:
        for line in f:
            corpus.append(json.loads(line))

    results = []

    for scenario in SCENARIOS:
        print(f"   Testing: {scenario['name']}...")

        relevant_examples = [
            e for e in examples
            if not isinstance(e, dict) or "parse_error" not in e
        ][:3]

        example_text = ""
        if relevant_examples:
            example_text = "\n\nHere are examples of how Lloyd has answered similar questions:\n"
            for ex in relevant_examples[:3]:
                if isinstance(ex, dict) and "text" in ex:
                    example_text += f"\n---\n{ex['text']}\n"

        ai_response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            system=voice_profile,
            messages=[{
                "role": "user",
                "content": f"Weather context: {scenario['context']}\n\nUser question: {scenario['question']}{example_text}",
            }],
        )
        ai_text = ai_response.content[0].text

        real_example = _find_real_example(scenario, corpus)
        real_text = real_example["content"] if real_example else "(No matching real example found)"

        judge_response = client.messages.create(
            model=CLAUDE_MODEL,
            max_tokens=1024,
            messages=[{
                "role": "user",
                "content": JUDGE_PROMPT.format(
                    real_message=real_text[:1000],
                    ai_response=ai_text,
                ),
            }],
        )

        judge_text = judge_response.content[0].text
        try:
            if "```" in judge_text:
                m = re.search(r"```(?:json)?\s*\n?(.*?)```", judge_text, re.DOTALL)
                if m:
                    judge_text = m.group(1)
            scores = json.loads(judge_text)
        except json.JSONDecodeError:
            scores = {"raw": judge_text, "parse_error": True}

        results.append({
            "scenario": scenario["name"],
            "question": scenario["question"],
            "ai_response": ai_text,
            "scores": scores,
        })

    report_lines = ["# Lloyd Voice Profile — Validation Report\n"]
    total_overall = 0
    scored_count = 0

    for r in results:
        report_lines.append(f"\n## {r['scenario']}")
        report_lines.append(f"\n**Question:** {r['question']}\n")
        report_lines.append(f"**AI Response:**\n> {r['ai_response'][:500]}\n")

        scores = r["scores"]
        if "parse_error" not in scores:
            report_lines.append(f"**Scores:**")
            for key in ["voice_match", "structural_match", "tonal_match", "authenticity", "weather_quality", "overall"]:
                val = scores.get(key, "?")
                report_lines.append(f"- {key}: {val}/5")
            report_lines.append(f"\n✅ What works: {scores.get('what_works', 'N/A')}")
            report_lines.append(f"❌ What fails: {scores.get('what_fails', 'N/A')}")
            report_lines.append(f"💡 Suggestions: {scores.get('suggestions', 'N/A')}")

            if isinstance(scores.get("overall"), (int, float)):
                total_overall += scores["overall"]
                scored_count += 1
        else:
            report_lines.append(f"*Scoring failed — see raw output*")

    if scored_count > 0:
        avg = total_overall / scored_count
        report_lines.insert(1, f"\n**Overall Average: {avg:.1f}/5** ({scored_count} scenarios scored)\n")
        if avg >= 4.0:
            report_lines.insert(2, "✅ Voice profile is strong — ready for production.\n")
        elif avg >= 3.0:
            report_lines.insert(2, "⚠️ Voice profile needs refinement — review suggestions below.\n")
        else:
            report_lines.insert(2, "❌ Voice profile needs significant work — iterate on voice_features extraction.\n")

    report = "\n".join(report_lines)
    with open(OUTPUT_DIR / "validation_report.md", "w") as f:
        f.write(report)

    with open(OUTPUT_DIR / "validation_raw.json", "w") as f:
        json.dump(results, f, indent=2)

    return avg if scored_count > 0 else 0

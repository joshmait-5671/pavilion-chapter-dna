"""Normalize all ingested data into a unified corpus format."""
import json
import hashlib
import re
from pathlib import Path
from datetime import datetime
from config import (
    RAW_DIR, CORPUS_DIR, MODEL_PATTERNS, WEATHER_TYPES,
)


def _content_hash(text):
    """SHA-256 hash for deduplication."""
    return hashlib.sha256(text.strip().lower().encode()).hexdigest()


def _detect_models(text):
    """Find weather model references in text."""
    found = []
    text_lower = text.lower()
    for model, pattern in MODEL_PATTERNS.items():
        if re.search(pattern, text_lower, re.IGNORECASE):
            found.append(model)
    return found


def _classify_weather_type(text):
    """Classify the primary weather type discussed."""
    text_lower = text.lower()
    scores = {}
    for wtype, keywords in WEATHER_TYPES.items():
        scores[wtype] = sum(1 for kw in keywords if kw in text_lower)
    if max(scores.values()) == 0:
        return None
    return max(scores, key=scores.get)


def _detect_temporal_focus(text):
    """Estimate what time horizon the message discusses."""
    text_lower = text.lower()
    if any(w in text_lower for w in ["tonight", "right now", "currently", "radar"]):
        return "nowcast"
    if any(w in text_lower for w in ["tomorrow", "today", "morning", "afternoon"]):
        return "short"
    if any(w in text_lower for w in ["this week", "next few days", "wednesday", "thursday", "friday"]):
        return "short"
    if any(w in text_lower for w in ["next week", "7 day", "7-day", "weekend"]):
        return "medium"
    if any(w in text_lower for w in ["10 day", "10-day", "long range", "seasonal", "winter outlook"]):
        return "extended"
    return None


def _has_forecast(text):
    """Heuristic: does this message contain a forecast?"""
    text_lower = text.lower()
    has_numbers = bool(re.search(r"\b\d{2,3}\s*°?\s*(degrees|f|fahrenheit)?\b", text_lower))
    has_precip = bool(re.search(r"\b\d+(\.\d+)?\s*(inch|inches|in\b|cm|mm)", text_lower))
    has_models = len(_detect_models(text)) > 0
    has_forecast_words = any(w in text_lower for w in ["forecast", "expect", "looking at", "calling for"])
    return has_numbers or has_precip or has_models or has_forecast_words


def _has_verification(text):
    """Heuristic: does this reference a past forecast's accuracy?"""
    text_lower = text.lower()
    return any(w in text_lower for w in [
        "i was wrong", "i was right", "nailed it", "bust", "busted",
        "overperformed", "underperformed", "verified", "as i said",
        "called it", "missed", "my forecast",
    ])


def _load_gmail_records():
    """Load raw Gmail JSON files into normalized records."""
    records = []
    gmail_dir = RAW_DIR / "gmail"
    if not gmail_dir.exists():
        return records

    for f_path in gmail_dir.glob("*.json"):
        with open(f_path) as f:
            raw = json.load(f)

        records.append({
            "id": f"gmail_{raw['id']}",
            "source": "gmail",
            "date": raw.get("date", ""),
            "subject": raw.get("subject", ""),
            "content": raw.get("body", ""),
        })
    return records


def _load_whatsapp_records():
    """Load raw WhatsApp JSON files into normalized records."""
    records = []
    wa_dir = RAW_DIR / "whatsapp"
    if not wa_dir.exists():
        return records

    for f_path in wa_dir.glob("*.json"):
        with open(f_path) as f:
            raw = json.load(f)

        records.append({
            "id": raw["id"],
            "source": "whatsapp",
            "date": raw.get("date", ""),
            "subject": None,
            "content": raw.get("text", ""),
        })
    return records


def _load_twitter_records():
    """Load raw Twitter JSON files into normalized records."""
    records = []
    tw_dir = RAW_DIR / "twitter"
    if not tw_dir.exists():
        return records

    for f_path in tw_dir.glob("*.json"):
        if f_path.name in ("tweets_archive.js", "manual_tweets.txt"):
            continue
        with open(f_path) as f:
            raw = json.load(f)

        records.append({
            "id": raw["id"],
            "source": "twitter",
            "date": raw.get("date", ""),
            "subject": None,
            "content": raw.get("text", ""),
        })
    return records


def normalize_corpus():
    """Load all raw data, normalize, deduplicate, tag, and write corpus.

    Returns stats dict.
    """
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)

    all_records = []
    all_records.extend(_load_gmail_records())
    all_records.extend(_load_whatsapp_records())
    all_records.extend(_load_twitter_records())

    seen_hashes = set()
    deduped = []
    for record in all_records:
        h = _content_hash(record["content"])
        if h in seen_hashes:
            continue
        seen_hashes.add(h)

        content = record["content"]
        record.update({
            "word_count": len(content.split()),
            "has_forecast": _has_forecast(content),
            "has_verification": _has_verification(content),
            "weather_type": _classify_weather_type(content),
            "temporal_reference": _detect_temporal_focus(content),
            "models_mentioned": _detect_models(content),
            "content_hash": h,
        })
        deduped.append(record)

    deduped.sort(key=lambda r: r.get("date", ""), reverse=True)

    corpus_path = CORPUS_DIR / "corpus.jsonl"
    with open(corpus_path, "w") as f:
        for record in deduped:
            f.write(json.dumps(record) + "\n")

    stats = {
        "total": len(deduped),
        "duplicates_removed": len(all_records) - len(deduped),
        "by_source": {
            "gmail": sum(1 for r in deduped if r["source"] == "gmail"),
            "whatsapp": sum(1 for r in deduped if r["source"] == "whatsapp"),
            "twitter": sum(1 for r in deduped if r["source"] == "twitter"),
        },
        "by_weather_type": {},
        "has_forecast": sum(1 for r in deduped if r["has_forecast"]),
        "has_verification": sum(1 for r in deduped if r["has_verification"]),
        "models_referenced": {},
        "avg_word_count": round(sum(r["word_count"] for r in deduped) / max(len(deduped), 1)),
    }

    for r in deduped:
        wt = r["weather_type"] or "unclassified"
        stats["by_weather_type"][wt] = stats["by_weather_type"].get(wt, 0) + 1
        for model in r["models_mentioned"]:
            stats["models_referenced"][model] = stats["models_referenced"].get(model, 0) + 1

    stats_path = CORPUS_DIR / "stats.json"
    with open(stats_path, "w") as f:
        json.dump(stats, f, indent=2)

    return stats

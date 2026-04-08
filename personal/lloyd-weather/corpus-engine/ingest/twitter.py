"""Ingest Lloyd's tweets — manual CSV/JSON import path.

Twitter API is unreliable and expensive. Instead:
1. Lloyd requests his Twitter archive (Settings → Your Account → Download Archive)
2. Extract tweets.js from the archive
3. Save as data/raw/twitter/tweets_archive.js
4. This script parses it

Alternative: manually save tweets as a text file, one per line with dates.
Format: YYYY-MM-DD | tweet text here
Save as: data/raw/twitter/manual_tweets.txt
"""
import json
import re
from pathlib import Path
from config import RAW_DIR, WEATHER_KEYWORDS


def _is_weather_related(text):
    """Check if tweet is weather-related."""
    text_lower = text.lower()
    return any(kw in text_lower for kw in WEATHER_KEYWORDS)


def _parse_twitter_archive(archive_path):
    """Parse tweets.js from Twitter data export."""
    with open(archive_path, "r") as f:
        content = f.read()

    content = re.sub(r"^window\.YTD\.tweet\.part\d+\s*=\s*", "", content)
    tweets = json.loads(content)

    records = []
    for item in tweets:
        tweet = item.get("tweet", item)
        text = tweet.get("full_text", tweet.get("text", ""))
        if not _is_weather_related(text):
            continue
        records.append({
            "id": f"tw_{tweet.get('id_str', tweet.get('id', ''))}",
            "date": tweet.get("created_at", ""),
            "text": text,
        })
    return records


def _parse_manual_file(manual_path):
    """Parse manually collected tweets (YYYY-MM-DD | text format)."""
    records = []
    with open(manual_path, "r") as f:
        for i, line in enumerate(f):
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            if "|" in line:
                date, text = line.split("|", 1)
                date = date.strip()
                text = text.strip()
            else:
                date = ""
                text = line
            if not _is_weather_related(text):
                continue
            records.append({
                "id": f"tw_manual_{i}",
                "date": date,
                "text": text,
            })
    return records


def ingest_twitter():
    """Import tweets from archive or manual file.

    Returns count of weather tweets imported.
    """
    output_dir = RAW_DIR / "twitter"
    output_dir.mkdir(parents=True, exist_ok=True)

    archive_path = output_dir / "tweets_archive.js"
    manual_path = output_dir / "manual_tweets.txt"

    records = []
    if archive_path.exists():
        records = _parse_twitter_archive(archive_path)
        print(f"   📦 Parsed Twitter archive: {len(records)} weather tweets")
    elif manual_path.exists():
        records = _parse_manual_file(manual_path)
        print(f"   📝 Parsed manual tweets file: {len(records)} weather tweets")
    else:
        print(f"   ⚠️  No Twitter data found.")
        print(f"      Place tweets_archive.js or manual_tweets.txt in {output_dir}")
        return 0

    for record in records:
        out_path = output_dir / f"{record['id']}.json"
        with open(out_path, "w") as f:
            json.dump(record, f, indent=2)

    return len(records)

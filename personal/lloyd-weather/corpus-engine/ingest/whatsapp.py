"""Ingest Lloyd's weather messages from Wash U N00bs WhatsApp export."""
import json
import re
from pathlib import Path
from config import RAW_DIR, WHATSAPP_CHAT_FILE, LLOYD_NAMES, WEATHER_KEYWORDS

MSG_RE = re.compile(
    r"^\[(\d+/\d+/\d+),\s*(\d+:\d+:\d+\s*[AP]M)\]\s*([^:]+):\s*(.+)$"
)

SKIP_CONTENT = {
    "image omitted", "video omitted", "sticker omitted",
    "audio omitted", "document omitted", "GIF omitted",
    "This message was deleted", "You deleted this message",
    "Messages and calls are end-to-end encrypted",
}


def _is_weather_related(text):
    """Check if message contains weather-related content."""
    text_lower = text.lower()
    matches = sum(1 for kw in WEATHER_KEYWORDS if kw in text_lower)
    threshold = 1 if len(text) > 100 else 2
    return matches >= threshold


def _parse_date(date_str):
    """Convert MM/DD/YY to ISO format."""
    parts = date_str.split("/")
    month, day, year = int(parts[0]), int(parts[1]), int(parts[2])
    year = 2000 + year if year < 100 else year
    return f"{year}-{month:02d}-{day:02d}"


def ingest_whatsapp():
    """Parse Lloyd's weather messages from the N00bs WhatsApp chat.

    Returns count of weather messages found.
    """
    output_dir = RAW_DIR / "whatsapp"
    output_dir.mkdir(parents=True, exist_ok=True)

    if not WHATSAPP_CHAT_FILE.exists():
        print(f"   ⚠️  WhatsApp file not found: {WHATSAPP_CHAT_FILE}")
        return 0

    count = 0

    with open(WHATSAPP_CHAT_FILE, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            m = MSG_RE.match(line)
            if not m:
                continue

            date_str, time_str, name, text = m.groups()
            name = name.strip().lstrip("\u200e").strip()
            text = text.strip().lstrip("\u200e").strip()

            if not any(lloyd_name in name for lloyd_name in LLOYD_NAMES):
                continue

            if any(skip in text for skip in SKIP_CONTENT):
                continue
            if text.startswith("http"):
                continue
            if len(text) < 30:
                continue

            if not _is_weather_related(text):
                continue

            record = {
                "id": f"wa_{_parse_date(date_str)}_{count}",
                "date": f"{_parse_date(date_str)}T{time_str.strip()}",
                "sender": name,
                "text": text,
            }

            out_path = output_dir / f"{record['id']}.json"
            with open(out_path, "w") as f_out:
                json.dump(record, f_out, indent=2)

            count += 1

    return count

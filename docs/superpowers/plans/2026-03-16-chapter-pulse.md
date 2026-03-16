# Chapter Pulse Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a pipeline that pulls a month of Slack chapter messages, summarizes them via Claude into a video script, renders an animated HTML template, and captures it as a 30-second MP4 ad.

**Architecture:** Four-stage pipeline: Slack API pull → Claude summarization → HTML template injection → Playwright frame capture + ffmpeg stitch. All Python. Manual trigger. Boston chapter first.

**Tech Stack:** Python 3.9+, slack_sdk, anthropic, playwright, ffmpeg (system), CSS keyframe animations

**Spec:** `docs/superpowers/specs/2026-03-16-chapter-pulse-design.md`

**Environment notes from discovery:**
- Python 3.9.6 installed
- `anthropic` 0.84.0 and `slack_sdk` 3.40.1 already installed
- `playwright` NOT installed — Task 1 installs it (actively maintained by Microsoft, unlike pyppeteer which is stale since 2021)
- `ffmpeg` NOT installed — Task 1 installs via `brew install ffmpeg` (expect 10+ min, many dependencies)
- Slack credentials available in `/Users/joshmait/Desktop/Claude/recapper/.env` (reuse SLACK_BOT_TOKEN, SLACK_APP_TOKEN, ANTHROPIC_API_KEY)
- Boston chapter channel ID: needs to be looked up (Task 2)

---

## Chunk 1: Project Setup + Data Pipeline

### Task 1: Project scaffolding and dependencies

**Files:**
- Create: `chapter-pulse/config.json`
- Create: `chapter-pulse/.env`
- Create: `chapter-pulse/requirements.txt`
- Create: `chapter-pulse/data/` (empty dir)
- Create: `chapter-pulse/scripts/` (empty dir)
- Create: `chapter-pulse/output/` (empty dir)
- Create: `chapter-pulse/templates/` (empty dir)
- Create: `chapter-pulse/src/` (empty dir)

- [ ] **Step 1: Install ffmpeg**

```bash
brew install ffmpeg
```

Expected: ffmpeg installs. Verify with `ffmpeg -version`.

- [ ] **Step 2: Create project directory structure**

```bash
cd /Users/joshmait/Desktop/Claude
mkdir -p chapter-pulse/{data,scripts,output,templates,src}
```

- [ ] **Step 3: Create requirements.txt**

Create `chapter-pulse/requirements.txt`:
```
slack-sdk>=3.27
anthropic>=0.25
playwright>=1.40
python-dotenv>=1.0
```

- [ ] **Step 4: Install Python dependencies**

```bash
cd /Users/joshmait/Desktop/Claude/chapter-pulse
pip3 install -r requirements.txt
playwright install chromium
```

Expected: playwright installs, then downloads Chromium browser (~150MB one-time download).

- [ ] **Step 5: Create .env file**

Create `chapter-pulse/.env` — copy values from Recapper's `.env` (`/Users/joshmait/Desktop/Claude/recapper/.env`):
```
SLACK_BOT_TOKEN=<copy from recapper .env>
SLACK_APP_TOKEN=<copy from recapper .env>
ANTHROPIC_API_KEY=<copy from recapper .env>
```

- [ ] **Step 6: Create config.json with Boston channel**

First, look up the Boston chapter channel ID from Slack:
```python
import os
from dotenv import load_dotenv
from slack_sdk import WebClient

load_dotenv()
client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])
# List channels and find Boston
result = client.conversations_list(types="public_channel", limit=1000)
for ch in result["channels"]:
    if "boston" in ch["name"].lower():
        print(f"{ch['name']}: {ch['id']}")
```

Then create `chapter-pulse/config.json`:
```json
{
  "chapters": {
    "boston": {
      "channel_id": "<ACTUAL_ID_FROM_ABOVE>",
      "display_name": "Boston"
    }
  }
}
```

- [ ] **Step 7: Create .gitignore**

Create `chapter-pulse/.gitignore`:
```
.env
output/
data/
scripts/
__pycache__/
```

- [ ] **Step 8: Commit scaffolding**

```bash
cd /Users/joshmait/Desktop/Claude
git add chapter-pulse/config.json chapter-pulse/requirements.txt chapter-pulse/.gitignore
git commit -m "feat: scaffold chapter-pulse project with deps and config"
```

---

### Task 2: Slack data pipeline (pull_messages.py)

**Files:**
- Create: `chapter-pulse/src/pull_messages.py`
- Create: `chapter-pulse/tests/test_pull_messages.py`

- [ ] **Step 1: Write test for message pulling and threshold**

Create `chapter-pulse/tests/__init__.py` (empty) and `chapter-pulse/tests/test_pull_messages.py`:

```python
import json
import os
import tempfile

def test_save_messages_creates_json():
    """Verify save_messages writes a valid JSON file with expected structure."""
    from src.pull_messages import save_messages

    messages = [
        {"user": "U123", "text": "Hello Boston", "ts": "1710000000.000000", "display_name": "Sarah", "title": "VP Sales"},
        {"user": "U456", "text": "Great event last night", "ts": "1710000001.000000", "display_name": "Mike", "title": "Director RevOps"},
    ]

    with tempfile.TemporaryDirectory() as tmpdir:
        path = save_messages(messages, "boston", "2026-03", tmpdir, display_name="Boston")
        assert os.path.exists(path)
        with open(path) as f:
            data = json.load(f)
        assert data["chapter"] == "boston"
        assert data["display_name"] == "Boston"
        assert data["month"] == "2026-03"
        assert data["message_count"] == 2
        assert data["unique_posters"] == 2
        assert len(data["messages"]) == 2


def test_threshold_check_below():
    """Verify threshold returns False when under 30 messages."""
    from src.pull_messages import check_threshold
    assert check_threshold([], "boston", 30) == False


def test_threshold_check_above():
    """Verify threshold returns True when at or above 30 messages."""
    from src.pull_messages import check_threshold
    msgs = [{"text": f"msg {i}"} for i in range(30)]
    assert check_threshold(msgs, "boston", 30) == True
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /Users/joshmait/Desktop/Claude/chapter-pulse
python3 -m pytest tests/test_pull_messages.py -v
```

Expected: FAIL — `ModuleNotFoundError: No module named 'src.pull_messages'`

- [ ] **Step 3: Implement pull_messages.py**

Create `chapter-pulse/src/__init__.py` (empty) and `chapter-pulse/src/pull_messages.py`:

```python
"""Pull messages from a Slack chapter channel for a given month."""

import json
import os
from datetime import datetime
from calendar import monthrange

from slack_sdk import WebClient


def pull_channel_messages(client: WebClient, channel_id: str, year: int, month: int) -> list:
    """Fetch all top-level messages from a channel for the given month.

    Returns list of dicts with: user, text, ts, display_name, title.
    Uses conversations.history with oldest/latest timestamps and pagination.
    """
    # Calculate month boundaries as Unix timestamps
    first_day = datetime(year, month, 1)
    last_day_num = monthrange(year, month)[1]
    next_month = datetime(year, month, last_day_num, 23, 59, 59)

    oldest = str(first_day.timestamp())
    latest = str(next_month.timestamp())

    messages = []
    cursor = None

    while True:
        kwargs = {
            "channel": channel_id,
            "oldest": oldest,
            "latest": latest,
            "limit": 200,
        }
        if cursor:
            kwargs["cursor"] = cursor

        result = client.conversations_history(**kwargs)

        for msg in result.get("messages", []):
            # Skip bot messages, subtypes (joins, edits, etc.)
            if msg.get("bot_id") or msg.get("subtype"):
                continue
            text = msg.get("text", "").strip()
            if not text:
                continue
            messages.append({
                "user": msg.get("user", "unknown"),
                "text": text,
                "ts": msg.get("ts", ""),
            })

        # Pagination
        meta = result.get("response_metadata", {})
        if result.get("has_more") and meta.get("next_cursor"):
            cursor = meta["next_cursor"]
        else:
            break

    # Reverse to chronological (Slack returns newest first)
    messages.reverse()
    return messages


def enrich_with_profiles(client: WebClient, messages: list) -> list:
    """Add display_name and title to each message by looking up user profiles.

    Caches lookups to avoid duplicate API calls.
    """
    profile_cache = {}

    for msg in messages:
        user_id = msg["user"]
        if user_id not in profile_cache:
            try:
                info = client.users_info(user=user_id)
                profile = info["user"]["profile"]
                profile_cache[user_id] = {
                    "display_name": profile.get("display_name") or profile.get("real_name", "Member"),
                    "title": profile.get("title", ""),
                }
            except Exception:
                profile_cache[user_id] = {"display_name": "Member", "title": ""}

        msg["display_name"] = profile_cache[user_id]["display_name"]
        msg["title"] = profile_cache[user_id]["title"]

    return messages


def check_threshold(messages: list, chapter: str, minimum: int = 30) -> bool:
    """Return True if message count meets threshold. Print warning if not."""
    count = len(messages)
    if count < minimum:
        print(f"{chapter.title()} had only {count} messages — below the {minimum}-message threshold. No video generated.")
        return False
    return True


def save_messages(messages: list, chapter: str, month_str: str, data_dir: str, display_name: str = None) -> str:
    """Save messages to a JSON file. Returns the file path.

    Args:
        messages: List of message dicts
        chapter: Chapter key (e.g., "boston")
        month_str: Month string (e.g., "2026-03")
        data_dir: Directory to save into
        display_name: Human-readable chapter name (e.g., "Boston")
    """
    unique_users = set(m["user"] for m in messages)

    data = {
        "chapter": chapter,
        "display_name": display_name or chapter.title(),
        "month": month_str,
        "message_count": len(messages),
        "unique_posters": len(unique_users),
        "messages": messages,
    }

    os.makedirs(data_dir, exist_ok=True)
    path = os.path.join(data_dir, f"{chapter}-{month_str}.json")
    with open(path, "w") as f:
        json.dump(data, f, indent=2)

    print(f"Saved {len(messages)} messages to {path}")
    return path
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /Users/joshmait/Desktop/Claude/chapter-pulse
python3 -m pytest tests/test_pull_messages.py -v
```

Expected: 3 tests PASS.

- [ ] **Step 5: Commit data pipeline**

```bash
cd /Users/joshmait/Desktop/Claude
git add chapter-pulse/src/ chapter-pulse/tests/
git commit -m "feat: add Slack data pipeline for chapter message pulling"
```

---

## Chunk 2: Claude Summarization + Review Gate

### Task 3: Claude summarization (generate_script.py)

**Files:**
- Create: `chapter-pulse/src/generate_script.py`
- Create: `chapter-pulse/tests/test_generate_script.py`

- [ ] **Step 1: Write test for script JSON validation**

Create `chapter-pulse/tests/test_generate_script.py`:

```python
import json


def test_validate_script_valid():
    """A correctly structured script passes validation."""
    from src.generate_script import validate_script

    script = {
        "chapter": "Boston",
        "month": "March 2026",
        "stat_hook": {"number": "43", "descriptor": "conversations in one month"},
        "moments": [
            {"quote": "Quote 1", "first_name": "Sarah", "title": "VP Sales"},
            {"quote": "Quote 2", "first_name": "Mike", "title": "Director RevOps"},
            {"quote": "Quote 3", "first_name": "Elena", "title": "CRO"},
        ],
        "beat_4_stat": {"number": "12", "descriptor": "unique voices this month"},
        "cta_line": "Boston's room is open.",
    }
    assert validate_script(script) == True


def test_validate_script_wrong_moment_count():
    """Script with != 3 moments fails validation."""
    from src.generate_script import validate_script

    script = {
        "chapter": "Boston",
        "month": "March 2026",
        "stat_hook": {"number": "43", "descriptor": "conversations"},
        "moments": [
            {"quote": "Quote 1", "first_name": "Sarah", "title": "VP Sales"},
        ],
        "beat_4_stat": {"number": "12", "descriptor": "unique voices"},
        "cta_line": "Boston's room is open.",
    }
    assert validate_script(script) == False


def test_validate_script_missing_field():
    """Script missing required field fails validation."""
    from src.generate_script import validate_script

    script = {
        "chapter": "Boston",
        "month": "March 2026",
        "stat_hook": {"number": "43", "descriptor": "conversations"},
        "moments": [],
    }
    assert validate_script(script) == False
```

- [ ] **Step 2: Run tests to verify they fail**

```bash
cd /Users/joshmait/Desktop/Claude/chapter-pulse
python3 -m pytest tests/test_generate_script.py -v
```

Expected: FAIL — `ModuleNotFoundError`

- [ ] **Step 3: Implement generate_script.py**

Create `chapter-pulse/src/generate_script.py`:

```python
"""Generate a video script from chapter messages using Claude."""

import json
import os

import anthropic


SYSTEM_PROMPT = """You are a creative director producing a 30-second video ad for Pavilion, the #1 private community for GTM leaders.

Your job: read a month of Slack messages from a local chapter and produce a structured JSON script for a video.

The video has 5 beats:
1. Chapter name (big, bold)
2. One stat hook (the most interesting number from the month)
3. Three standout quotes (shortened for screen — max 15 words each)
4. One community stat (e.g., unique voices, topics discussed)
5. A chapter-specific CTA line

Rules:
- Exactly 3 quotes. Pick for impact, not recency.
- First name only. No last names. Include their title.
- Shorten quotes to punch hard on screen. Max 15 words.
- The stat hook should make someone stop scrolling.
- The CTA should feel specific to this chapter. Not generic.
- Voice: direct, punchy, no fluff. Think the Economist meets Nike.

Return ONLY valid JSON. No markdown. No explanation. Just the JSON object."""


USER_PROMPT_TEMPLATE = """Here are {message_count} messages from the {display_name} chapter of Pavilion in {month_display}.

There were {unique_posters} unique people posting.

Messages:
{messages_text}

---

Produce the video script JSON with this exact structure:
{{
  "chapter": "{display_name}",
  "month": "{month_display}",
  "stat_hook": {{
    "number": "<the most interesting number>",
    "descriptor": "<what the number means>"
  }},
  "moments": [
    {{
      "quote": "<shortened quote, max 15 words>",
      "first_name": "<first name only>",
      "title": "<their job title>"
    }},
    ... (exactly 3)
  ],
  "beat_4_stat": {{
    "number": "<a community stat number>",
    "descriptor": "<what it means>"
  }},
  "cta_line": "<chapter-specific CTA>"
}}"""


def generate_script(messages_data: dict, anthropic_key: str) -> dict:
    """Send chapter messages to Claude and get back a video script JSON.

    Args:
        messages_data: The full JSON from pull_messages (with chapter, month, messages, etc.)
        anthropic_key: Anthropic API key

    Returns:
        Parsed script dict
    """
    client = anthropic.Anthropic(api_key=anthropic_key)

    # Format messages for the prompt
    messages_text = ""
    for msg in messages_data["messages"]:
        name = msg.get("display_name", "Member")
        title = msg.get("title", "")
        title_str = f" ({title})" if title else ""
        messages_text += f"- {name}{title_str}: {msg['text']}\n"

    # Parse month for display
    year, month_num = messages_data["month"].split("-")
    month_names = ["", "January", "February", "March", "April", "May", "June",
                   "July", "August", "September", "October", "November", "December"]
    month_display = f"{month_names[int(month_num)]} {year}"

    user_prompt = USER_PROMPT_TEMPLATE.format(
        message_count=messages_data["message_count"],
        display_name=messages_data.get("display_name", messages_data["chapter"].title()),
        month_display=month_display,
        unique_posters=messages_data["unique_posters"],
        messages_text=messages_text,
    )

    response = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=1000,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw = response.content[0].text.strip()

    # Strip markdown code fences if present
    if raw.startswith("```"):
        raw = raw.split("```")[1]
        if raw.startswith("json"):
            raw = raw[4:]
        raw = raw.strip()

    script = json.loads(raw)
    return script


def validate_script(script: dict) -> bool:
    """Validate that a script has all required fields and exactly 3 moments."""
    required_keys = ["chapter", "month", "stat_hook", "moments", "beat_4_stat", "cta_line"]
    for key in required_keys:
        if key not in script:
            print(f"Missing required field: {key}")
            return False

    if not isinstance(script["moments"], list) or len(script["moments"]) != 3:
        print(f"Expected exactly 3 moments, got {len(script.get('moments', []))}")
        return False

    for i, moment in enumerate(script["moments"]):
        for field in ["quote", "first_name", "title"]:
            if field not in moment:
                print(f"Moment {i} missing field: {field}")
                return False

    for stat_key in ["stat_hook", "beat_4_stat"]:
        stat = script[stat_key]
        if "number" not in stat or "descriptor" not in stat:
            print(f"{stat_key} missing 'number' or 'descriptor'")
            return False

    return True


def save_script(script: dict, chapter: str, month_str: str, scripts_dir: str) -> str:
    """Save the script JSON to disk. Returns file path."""
    os.makedirs(scripts_dir, exist_ok=True)
    path = os.path.join(scripts_dir, f"{chapter}-{month_str}-script.json")
    with open(path, "w") as f:
        json.dump(script, f, indent=2)
    print(f"Script saved to {path}")
    return path
```

- [ ] **Step 4: Run tests to verify they pass**

```bash
cd /Users/joshmait/Desktop/Claude/chapter-pulse
python3 -m pytest tests/test_generate_script.py -v
```

Expected: 3 tests PASS.

- [ ] **Step 5: Commit summarization module**

```bash
cd /Users/joshmait/Desktop/Claude
git add chapter-pulse/src/generate_script.py chapter-pulse/tests/test_generate_script.py
git commit -m "feat: add Claude summarization for video script generation"
```

---

### Task 4: Review gate (terminal-based approve/edit/reject)

This is part of `main.py` but we build the review function standalone first.

**Files:**
- Create: `chapter-pulse/src/review.py`

- [ ] **Step 1: Implement review.py**

Create `chapter-pulse/src/review.py`:

```python
"""Terminal-based review gate for video scripts."""

import json
import os
import subprocess
import sys
import tempfile


def print_script_preview(script: dict):
    """Pretty-print the script for terminal review."""
    print("\n" + "=" * 60)
    print(f"  CHAPTER PULSE: {script['chapter'].upper()}")
    print(f"  {script['month']}")
    print("=" * 60)

    print(f"\n  BEAT 1: {script['chapter'].upper()}")

    stat = script["stat_hook"]
    print(f"\n  BEAT 2: {stat['number']} {stat['descriptor']}")

    print(f"\n  BEAT 3: Quotes")
    for i, m in enumerate(script["moments"], 1):
        print(f"    {i}. \"{m['quote']}\"")
        print(f"       — {m['first_name']}, {m['title']}")

    b4 = script["beat_4_stat"]
    print(f"\n  BEAT 4: {b4['number']} {b4['descriptor']}")

    print(f"\n  BEAT 5: {script['cta_line']}")
    print("=" * 60)


def review_script(script: dict, script_path: str) -> str:
    """Present script for review. Returns 'approve' or 'reject'.

    If user chooses 'edit', opens the JSON file in the default editor,
    reloads, shows the updated preview, and asks again.
    """
    print_script_preview(script)

    while True:
        print("\n  Options: [a]pprove  [e]dit  [r]eject")
        choice = input("  > ").strip().lower()

        if choice in ("a", "approve"):
            print("  ✓ Script approved. Moving to render.")
            return "approve"

        elif choice in ("r", "reject"):
            print("  ✗ Script rejected. Exiting.")
            return "reject"

        elif choice in ("e", "edit"):
            # Open in default editor (macOS: 'open' opens in default app)
            editor = os.environ.get("EDITOR", "open")
            subprocess.call([editor, script_path])

            input("  Press Enter after saving your edits...")

            # Reload and show updated preview
            with open(script_path) as f:
                script = json.load(f)

            print("\n  Updated script:")
            print_script_preview(script)
            # Loop continues — user must approve or reject

        else:
            print("  Please enter 'a', 'e', or 'r'.")
```

- [ ] **Step 2: Commit review gate**

```bash
cd /Users/joshmait/Desktop/Claude
git add chapter-pulse/src/review.py
git commit -m "feat: add terminal-based script review gate"
```

---

## Chunk 3: HTML Video Template

### Task 5: Animated HTML template

This is the creative core. A single HTML file with CSS keyframe animations for the 5 beats. Placeholder values get replaced by the script JSON.

**Files:**
- Create: `chapter-pulse/templates/video-template.html`

- [ ] **Step 1: Create the animated HTML template**

Create `chapter-pulse/templates/video-template.html`:

```html
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
  @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;700;900&display=swap');

  * { margin: 0; padding: 0; box-sizing: border-box; }

  body {
    width: 1080px;
    height: 1080px;
    overflow: hidden;
    background: #180A5C;
    font-family: 'Poppins', sans-serif;
    color: #fff;
  }

  .frame {
    width: 1080px;
    height: 1080px;
    position: relative;
    overflow: hidden;
  }

  /* ── Pavilion mark (corner, persistent) ── */
  .pavilion-mark {
    position: absolute;
    top: 40px;
    right: 40px;
    font-size: 18px;
    font-weight: 700;
    color: rgba(255,255,255,0.3);
    letter-spacing: 2px;
    text-transform: uppercase;
    z-index: 10;
    opacity: 0;
    animation: fadeIn 0.3s ease forwards;
    animation-delay: 0.5s;
  }

  /* ── BEAT 1: Chapter name (0-5s) ── */
  .beat-1 {
    position: absolute;
    inset: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    opacity: 0;
    animation: slamIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards,
               fadeOut 0.3s ease forwards 4.5s;
    animation-delay: 0.2s, 4.5s;
  }
  .chapter-name {
    font-size: 180px;
    font-weight: 900;
    text-transform: uppercase;
    letter-spacing: -4px;
    line-height: 0.9;
    text-align: center;
  }

  /* ── BEAT 2: Stat hook (5-12s) ── */
  .beat-2 {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    opacity: 0;
    animation: slamIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards,
               fadeOut 0.3s ease forwards 11.5s;
    animation-delay: 5.2s, 11.5s;
  }
  .stat-number {
    font-size: 200px;
    font-weight: 900;
    color: #DF285B;
    line-height: 1;
  }
  .stat-descriptor {
    font-size: 36px;
    font-weight: 700;
    color: rgba(255,255,255,0.85);
    margin-top: 10px;
    text-transform: uppercase;
    letter-spacing: 3px;
  }

  /* ── BEAT 3: Quotes (12-22s) — 3 quotes, ~3.3s each ── */
  .quote-card {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 80px;
    text-align: center;
    opacity: 0;
  }
  .quote-text {
    font-size: 52px;
    font-weight: 700;
    line-height: 1.2;
    margin-bottom: 30px;
  }
  .quote-text::before { content: '\201C'; color: #DF285B; }
  .quote-text::after { content: '\201D'; color: #DF285B; }
  .quote-attribution {
    font-size: 24px;
    font-weight: 400;
    color: rgba(255,255,255,0.6);
  }

  /* Quote 1: 12-15.3s */
  .quote-1 {
    animation: slideInRight 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards,
               fadeOut 0.2s ease forwards 15.1s;
    animation-delay: 12.2s, 15.1s;
  }
  /* Quote 2: 15.3-18.6s */
  .quote-2 {
    animation: slideInLeft 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards,
               fadeOut 0.2s ease forwards 18.4s;
    animation-delay: 15.5s, 18.4s;
  }
  /* Quote 3: 18.6-22s */
  .quote-3 {
    animation: slideInRight 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards,
               fadeOut 0.2s ease forwards 21.7s;
    animation-delay: 18.8s, 21.7s;
  }

  /* ── BEAT 4: Community stat (22-26s) ── */
  .beat-4 {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    opacity: 0;
    animation: slamIn 0.3s cubic-bezier(0.16, 1, 0.3, 1) forwards,
               fadeOut 0.3s ease forwards 25.5s;
    animation-delay: 22.2s, 25.5s;
  }
  .beat-4 .stat-number {
    font-size: 160px;
  }

  /* ── BEAT 5: CTA (26-30s) ── */
  .beat-5 {
    position: absolute;
    inset: 0;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    gap: 30px;
    opacity: 0;
    animation: slamIn 0.4s cubic-bezier(0.16, 1, 0.3, 1) forwards;
    animation-delay: 26.2s;
  }
  .cta-line {
    font-size: 64px;
    font-weight: 900;
    text-align: center;
    line-height: 1.1;
    padding: 0 60px;
  }
  .cta-url {
    font-size: 28px;
    font-weight: 400;
    color: #DF285B;
    letter-spacing: 2px;
  }
  .cta-logo {
    font-size: 22px;
    font-weight: 700;
    color: rgba(255,255,255,0.4);
    letter-spacing: 3px;
    text-transform: uppercase;
    margin-top: 10px;
  }

  /* ── Keyframes ── */
  @keyframes slamIn {
    0% { opacity: 0; transform: scale(1.3); }
    100% { opacity: 1; transform: scale(1); }
  }
  @keyframes fadeIn {
    to { opacity: 1; }
  }
  @keyframes fadeOut {
    to { opacity: 0; }
  }
  @keyframes slideInRight {
    0% { opacity: 0; transform: translateX(100px); }
    100% { opacity: 1; transform: translateX(0); }
  }
  @keyframes slideInLeft {
    0% { opacity: 0; transform: translateX(-100px); }
    100% { opacity: 1; transform: translateX(0); }
  }
</style>
</head>
<body>
<div class="frame">

  <div class="pavilion-mark">PAVILION</div>

  <!-- BEAT 1: Chapter name -->
  <div class="beat-1">
    <div class="chapter-name">{{CHAPTER_NAME}}</div>
  </div>

  <!-- BEAT 2: Stat hook -->
  <div class="beat-2">
    <div class="stat-number">{{STAT_NUMBER}}</div>
    <div class="stat-descriptor">{{STAT_DESCRIPTOR}}</div>
  </div>

  <!-- BEAT 3: Quotes -->
  <div class="quote-card quote-1">
    <div class="quote-text">{{QUOTE_1}}</div>
    <div class="quote-attribution">{{QUOTE_1_NAME}}, {{QUOTE_1_TITLE}}</div>
  </div>
  <div class="quote-card quote-2">
    <div class="quote-text">{{QUOTE_2}}</div>
    <div class="quote-attribution">{{QUOTE_2_NAME}}, {{QUOTE_2_TITLE}}</div>
  </div>
  <div class="quote-card quote-3">
    <div class="quote-text">{{QUOTE_3}}</div>
    <div class="quote-attribution">{{QUOTE_3_NAME}}, {{QUOTE_3_TITLE}}</div>
  </div>

  <!-- BEAT 4: Community stat -->
  <div class="beat-4">
    <div class="stat-number">{{BEAT4_NUMBER}}</div>
    <div class="stat-descriptor">{{BEAT4_DESCRIPTOR}}</div>
  </div>

  <!-- BEAT 5: CTA -->
  <div class="beat-5">
    <div class="cta-line">{{CTA_LINE}}</div>
    <div class="cta-url">joinpavilion.com</div>
    <div class="cta-logo">▲ Pavilion</div>
  </div>

</div>
</body>
</html>
```

- [ ] **Step 2: Write test for template injection**

Add to `chapter-pulse/tests/test_template.py`:

```python
def test_inject_script_into_template():
    """Verify all placeholders get replaced with script values."""
    from src.template import inject_script

    script = {
        "chapter": "Boston",
        "month": "March 2026",
        "stat_hook": {"number": "43", "descriptor": "conversations in one month"},
        "moments": [
            {"quote": "I got two warm intros", "first_name": "Sarah", "title": "VP Sales"},
            {"quote": "Comp benchmarks got 6 DMs", "first_name": "Mike", "title": "Director RevOps"},
            {"quote": "Best event all year", "first_name": "Elena", "title": "CRO"},
        ],
        "beat_4_stat": {"number": "12", "descriptor": "unique voices this month"},
        "cta_line": "Boston's room is open.",
    }

    template = "<div>{{CHAPTER_NAME}} — {{STAT_NUMBER}} — {{QUOTE_1}} — {{QUOTE_1_NAME}} — {{CTA_LINE}}</div>"
    result = inject_script(template, script)

    assert "{{" not in result, f"Unresolved placeholders in: {result}"
    assert "BOSTON" in result
    assert "43" in result
    assert "I got two warm intros" in result
    assert "Sarah" in result
    assert "Boston's room is open." in result
```

- [ ] **Step 3: Run test to verify it fails**

```bash
cd /Users/joshmait/Desktop/Claude/chapter-pulse
python3 -m pytest tests/test_template.py -v
```

Expected: FAIL

- [ ] **Step 4: Implement template.py**

Create `chapter-pulse/src/template.py`:

```python
"""Inject script data into the HTML video template."""

import os


def inject_script(template_html: str, script: dict) -> str:
    """Replace all {{PLACEHOLDER}} tokens with values from the script.

    Args:
        template_html: Raw HTML string with {{PLACEHOLDER}} tokens
        script: The video script dict from Claude

    Returns:
        HTML string with all placeholders replaced
    """
    replacements = {
        "{{CHAPTER_NAME}}": script["chapter"].upper(),
        "{{STAT_NUMBER}}": script["stat_hook"]["number"],
        "{{STAT_DESCRIPTOR}}": script["stat_hook"]["descriptor"].upper(),
        "{{QUOTE_1}}": script["moments"][0]["quote"],
        "{{QUOTE_1_NAME}}": script["moments"][0]["first_name"],
        "{{QUOTE_1_TITLE}}": script["moments"][0]["title"],
        "{{QUOTE_2}}": script["moments"][1]["quote"],
        "{{QUOTE_2_NAME}}": script["moments"][1]["first_name"],
        "{{QUOTE_2_TITLE}}": script["moments"][1]["title"],
        "{{QUOTE_3}}": script["moments"][2]["quote"],
        "{{QUOTE_3_NAME}}": script["moments"][2]["first_name"],
        "{{QUOTE_3_TITLE}}": script["moments"][2]["title"],
        "{{BEAT4_NUMBER}}": script["beat_4_stat"]["number"],
        "{{BEAT4_DESCRIPTOR}}": script["beat_4_stat"]["descriptor"].upper(),
        "{{CTA_LINE}}": script["cta_line"],
    }

    result = template_html
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, value)

    return result


def build_video_html(script: dict, template_path: str, output_path: str) -> str:
    """Read template, inject script, write final HTML. Returns output path."""
    with open(template_path) as f:
        template = f.read()

    html = inject_script(template, script)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w") as f:
        f.write(html)

    print(f"Video HTML written to {output_path}")
    return output_path
```

- [ ] **Step 5: Run test to verify it passes**

```bash
cd /Users/joshmait/Desktop/Claude/chapter-pulse
python3 -m pytest tests/test_template.py -v
```

Expected: PASS

- [ ] **Step 6: Preview the template in browser with sample data**

Quick sanity check — inject sample data and open in browser:

```bash
cd /Users/joshmait/Desktop/Claude/chapter-pulse
python3 -c "
from src.template import build_video_html
import json

script = {
    'chapter': 'Boston',
    'month': 'March 2026',
    'stat_hook': {'number': '43', 'descriptor': 'conversations in one month'},
    'moments': [
        {'quote': 'I got two warm intros in one week', 'first_name': 'Sarah', 'title': 'VP Sales, Acme Corp'},
        {'quote': 'Shared our comp benchmarks and got 6 DMs', 'first_name': 'Mike', 'title': 'Director RevOps'},
        {'quote': 'Best chapter event we have had all year', 'first_name': 'Elena', 'title': 'CRO, DataStack'},
    ],
    'beat_4_stat': {'number': '12', 'descriptor': 'unique voices this month'},
    'cta_line': \"Boston's room is open.\",
}

build_video_html(script, 'templates/video-template.html', 'output/preview.html')
"
open output/preview.html
```

Expected: Opens in browser. Watch the 30-second animation play. Verify each beat appears at the right time with the right energy. Adjust CSS timing if needed.

- [ ] **Step 7: Commit template and injection**

```bash
cd /Users/joshmait/Desktop/Claude
git add chapter-pulse/templates/ chapter-pulse/src/template.py chapter-pulse/tests/test_template.py
git commit -m "feat: add animated HTML video template with script injection"
```

---

## Chunk 4: Render Pipeline + Orchestrator

### Task 6: Render video (Playwright + ffmpeg)

**Files:**
- Create: `chapter-pulse/src/render_video.py`

- [ ] **Step 1: Implement render_video.py**

Create `chapter-pulse/src/render_video.py`:

```python
"""Capture HTML animation frame-by-frame and stitch into MP4 with ffmpeg."""

import os
import shutil
import subprocess
import tempfile

from playwright.sync_api import sync_playwright


def capture_frames(html_path: str, output_dir: str, fps: int = 30, duration: int = 30, width: int = 1080, height: int = 1080):
    """Open HTML in headless Chromium, step through animation frame by frame, capture PNGs.

    Args:
        html_path: Absolute path to the injected HTML file
        output_dir: Directory to save frame PNGs
        fps: Frames per second
        duration: Total duration in seconds
        width: Viewport width
        height: Viewport height
    """
    total_frames = fps * duration

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page(viewport={"width": width, "height": height})

        # Load the HTML file
        file_url = f"file://{html_path}"
        page.goto(file_url, wait_until="networkidle")

        # Pause all animations at time 0
        page.evaluate("""() => {
            document.getAnimations().forEach(a => {
                a.pause();
                a.currentTime = 0;
            });
        }""")

        print(f"Capturing {total_frames} frames at {fps}fps...")

        for frame_num in range(total_frames):
            # Set animation time for this frame
            frame_time_ms = (frame_num / fps) * 1000
            page.evaluate(f"""() => {{
                document.getAnimations().forEach(a => {{
                    a.currentTime = {frame_time_ms};
                }});
            }}""")

            # Capture screenshot (clip to viewport for safety)
            frame_path = os.path.join(output_dir, f"frame_{frame_num:04d}.png")
            page.screenshot(path=frame_path, clip={"x": 0, "y": 0, "width": width, "height": height})

            # Progress indicator every 5 seconds of video
            if frame_num % (fps * 5) == 0:
                seconds = frame_num // fps
                print(f"  {seconds}s / {duration}s captured")

        print(f"  {duration}s / {duration}s captured — done")
        browser.close()


def stitch_to_mp4(frames_dir: str, output_path: str, fps: int = 30):
    """Use ffmpeg to stitch PNG frames into an MP4.

    Args:
        frames_dir: Directory containing frame_NNNN.png files
        output_path: Where to write the MP4
        fps: Frames per second
    """
    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)

    cmd = [
        "ffmpeg", "-y",  # overwrite output
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        "-crf", "18",  # high quality
        output_path,
    ]

    print(f"Stitching MP4: {output_path}")
    result = subprocess.run(cmd, capture_output=True, text=True)

    if result.returncode != 0:
        print(f"ffmpeg error: {result.stderr}")
        raise RuntimeError("ffmpeg failed to create MP4")

    # File size info
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"MP4 created: {output_path} ({size_mb:.1f} MB)")


def render(html_path: str, output_mp4: str, fps: int = 30, duration: int = 30):
    """Full render pipeline: capture frames + stitch to MP4.

    Args:
        html_path: Absolute path to the injected HTML file
        output_mp4: Where to save the final MP4
        fps: Frames per second
        duration: Total video duration in seconds
    """
    # Create temp directory for frames
    frames_dir = tempfile.mkdtemp(prefix="chapter_pulse_frames_")

    try:
        capture_frames(html_path, frames_dir, fps, duration)
        stitch_to_mp4(frames_dir, output_mp4, fps)

    finally:
        # Clean up temp frames
        shutil.rmtree(frames_dir, ignore_errors=True)
        print("Temp frames cleaned up.")
```

- [ ] **Step 2: Quick render test with sample HTML**

Test the render pipeline with the preview HTML from Task 5:

```bash
cd /Users/joshmait/Desktop/Claude/chapter-pulse
python3 -c "
from src.render_video import render
import os

html_path = os.path.abspath('output/preview.html')
mp4_path = os.path.abspath('output/test-render.mp4')
render(html_path, mp4_path, fps=10, duration=5)  # Quick test: 5 sec at 10fps = 50 frames
"
```

Expected: `output/test-render.mp4` created. Open it: `open output/test-render.mp4`. Verify you see the first 5 seconds of animation (chapter name beat).

Note: First run of Playwright will use its Chromium install (~150MB). This is a one-time download.

- [ ] **Step 3: Full 30-second test render**

```bash
cd /Users/joshmait/Desktop/Claude/chapter-pulse
python3 -c "
from src.render_video import render
import os

html_path = os.path.abspath('output/preview.html')
mp4_path = os.path.abspath('output/test-full.mp4')
render(html_path, mp4_path, fps=30, duration=30)
"
open output/test-full.mp4
```

Expected: Full 30-second MP4. Watch it. All 5 beats should play at the right times. This validates the entire render pipeline.

Note: 900 frames will take a few minutes to capture. Be patient.

- [ ] **Step 4: Commit render pipeline**

```bash
cd /Users/joshmait/Desktop/Claude
git add chapter-pulse/src/render_video.py
git commit -m "feat: add frame-by-frame render pipeline with Playwright + ffmpeg"
```

---

### Task 7: Orchestrator (main.py)

**Files:**
- Create: `chapter-pulse/src/main.py`

- [ ] **Step 1: Implement main.py**

Create `chapter-pulse/src/main.py`:

```python
"""Chapter Pulse orchestrator. Ties the full pipeline together.

Usage:
    python src/main.py --chapter boston
    python src/main.py --chapter boston --month 2026-03
"""

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime

from dotenv import load_dotenv

# Load .env from project root
load_dotenv(os.path.join(os.path.dirname(__file__), "..", ".env"))

from slack_sdk import WebClient

from pull_messages import pull_channel_messages, enrich_with_profiles, check_threshold, save_messages
from generate_script import generate_script, validate_script, save_script
from review import review_script
from template import build_video_html
from render_video import render


# Paths relative to project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.json")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "templates", "video-template.html")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")


def load_config():
    with open(CONFIG_PATH) as f:
        return json.load(f)


def main():
    parser = argparse.ArgumentParser(description="Chapter Pulse — Slack to video pipeline")
    parser.add_argument("--chapter", required=True, help="Chapter key from config.json (e.g., 'boston')")
    parser.add_argument("--month", default=None, help="Month as YYYY-MM (default: previous month)")
    parser.add_argument("--skip-pull", action="store_true", help="Skip Slack pull, use existing data file")
    parser.add_argument("--skip-script", action="store_true", help="Skip Claude, use existing script file")
    args = parser.parse_args()

    # Load config
    config = load_config()
    chapter_key = args.chapter.lower()

    if chapter_key not in config["chapters"]:
        print(f"Chapter '{chapter_key}' not found in config.json.")
        print(f"Available: {', '.join(config['chapters'].keys())}")
        sys.exit(1)

    chapter = config["chapters"][chapter_key]
    channel_id = chapter["channel_id"]
    display_name = chapter["display_name"]

    # Determine month
    if args.month:
        month_str = args.month
        year, month_num = int(month_str.split("-")[0]), int(month_str.split("-")[1])
    else:
        # Default to previous month
        now = datetime.now()
        if now.month == 1:
            year, month_num = now.year - 1, 12
        else:
            year, month_num = now.year, now.month - 1
        month_str = f"{year}-{month_num:02d}"

    print(f"\n{'='*60}")
    print(f"  CHAPTER PULSE: {display_name.upper()} — {month_str}")
    print(f"{'='*60}\n")

    # ── STAGE 1: Pull messages ──
    data_path = os.path.join(DATA_DIR, f"{chapter_key}-{month_str}.json")

    if args.skip_pull and os.path.exists(data_path):
        print(f"[1/4] Using existing data: {data_path}")
        with open(data_path) as f:
            messages_data = json.load(f)
    else:
        print(f"[1/4] Pulling messages from #{channel_id}...")
        client = WebClient(token=os.environ["SLACK_BOT_TOKEN"])

        # Make sure bot is in the channel
        try:
            client.conversations_join(channel=channel_id)
        except Exception:
            pass  # Already in channel

        messages = pull_channel_messages(client, channel_id, year, month_num)

        if not check_threshold(messages, display_name):
            sys.exit(0)

        messages = enrich_with_profiles(client, messages)
        save_messages(messages, chapter_key, month_str, DATA_DIR, display_name=display_name)

        with open(data_path) as f:
            messages_data = json.load(f)

    print(f"   {messages_data['message_count']} messages, {messages_data['unique_posters']} unique posters\n")

    # ── STAGE 2: Generate script via Claude ──
    script_path = os.path.join(SCRIPTS_DIR, f"{chapter_key}-{month_str}-script.json")

    if args.skip_script and os.path.exists(script_path):
        print(f"[2/4] Using existing script: {script_path}")
        with open(script_path) as f:
            script = json.load(f)
    else:
        print("[2/4] Generating video script via Claude...")
        script = generate_script(messages_data, os.environ["ANTHROPIC_API_KEY"])

        if not validate_script(script):
            print("Script validation failed. Trying again...")
            script = generate_script(messages_data, os.environ["ANTHROPIC_API_KEY"])
            if not validate_script(script):
                print("Script validation failed twice. Exiting.")
                sys.exit(1)

        save_script(script, chapter_key, month_str, SCRIPTS_DIR)

    # ── STAGE 3: Review ──
    print("\n[3/4] Review the script before rendering:\n")
    decision = review_script(script, script_path)

    if decision == "reject":
        sys.exit(0)

    # Reload script from disk in case it was edited during review
    with open(script_path) as f:
        script = json.load(f)

    # ── STAGE 4: Render ──
    print("\n[4/4] Rendering video...\n")

    # Inject script into template
    video_html_path = os.path.join(OUTPUT_DIR, f"{chapter_key}-{month_str}.html")
    build_video_html(script, TEMPLATE_PATH, video_html_path)

    # Render to MP4
    mp4_path = os.path.join(OUTPUT_DIR, f"{chapter_key}-{month_str}.mp4")
    render(os.path.abspath(video_html_path), os.path.abspath(mp4_path))

    # Open the video
    print(f"\n{'='*60}")
    print(f"  DONE: {mp4_path}")
    print(f"{'='*60}\n")
    subprocess.run(["open", mp4_path])


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test the full pipeline end-to-end with Boston**

This is the real deal. Run it:

```bash
cd /Users/joshmait/Desktop/Claude/chapter-pulse
python3 src/main.py --chapter boston
```

Expected flow:
1. Pulls messages from Boston Slack channel for previous month
2. Claude generates the video script
3. Script prints to terminal for review
4. You type `a` to approve
5. HTML renders with your data
6. Playwright captures 900 frames
7. ffmpeg stitches to MP4
8. Video opens in your default player

If the Slack pull returns < 30 messages, use `--month 2026-02` or another month with more activity.

- [ ] **Step 3: Commit orchestrator**

```bash
cd /Users/joshmait/Desktop/Claude
git add chapter-pulse/src/main.py
git commit -m "feat: add Chapter Pulse orchestrator with full pipeline"
```

- [ ] **Step 4: Final commit — all files**

```bash
cd /Users/joshmait/Desktop/Claude
git add chapter-pulse/
git commit -m "feat: Chapter Pulse v1 complete — Boston chapter video pipeline"
```

---

## Quick Reference

**Run the pipeline:**
```bash
cd /Users/joshmait/Desktop/Claude/chapter-pulse
python3 src/main.py --chapter boston
```

**Skip the Slack pull (reuse saved data):**
```bash
python3 src/main.py --chapter boston --skip-pull
```

**Skip the Claude step (reuse saved script):**
```bash
python3 src/main.py --chapter boston --skip-pull --skip-script
```

**Add a new chapter:** Edit `config.json`, add a new entry with the channel ID. Run with `--chapter <key>`.

"""Generate a video script from chapter messages using Claude."""

import json
import os

import anthropic


SYSTEM_PROMPT = """You are a creative director producing a 30-second video ad for Pavilion, the #1 private community for GTM leaders.

Your job: read a month of Slack messages from a local chapter and produce a structured JSON script that tells a NARRATIVE story. The video should feel like a fast-cut documentary trailer — energy, momentum, proof.

The video has 8 rapid-fire scenes (faster cuts = more energy):
1. COLD OPEN (0-1.5s) — Pavilion logo + chapter city slams in
2. TENSION (1.5-4s) — A provocative question or tension from the community ("Who's actually using AI?" / "Pipeline is broken")
3. PROOF WALL (4-12s) — 5-6 real Slack messages rapid-fire, some with images. This is the heartbeat of the video. Messages should tell a mini-story: someone asks → others jump in → insight emerges → momentum builds.
4. STAT PUNCH (12-15s) — One bold number that makes someone stop scrolling
5. EVIDENCE (15-18s) — 6 topic pills showing the range of conversations
6. MOMENTUM (18-22s) — 2 more quick-hit quotes that show outcomes/results
7. HEADLINE (22-25s) — Emotional one-liner about what this community actually is
8. CTA (25-30s) — Chapter-specific call to action

Rules:
- Exactly 6 quotes in "moments" array. Pick for NARRATIVE — they should tell a story in sequence.
- First name only. No last names. Include their title.
- Shorten quotes to punch hard on screen. Max 12 words. Punchy > complete.
- Mark which moments have images (has_image: true/false). If a message had a screenshot, chart, or photo attached, flag it.
- Exactly 6 topics — short labels (1-3 words each)
- The "tension" line should feel like a hook that creates curiosity
- The stat hook should make someone stop scrolling
- The headline should feel emotional and earned (not generic)
- The CTA should feel specific to this chapter. Not generic.
- Voice: direct, punchy, no fluff. Think Vice documentary meets Nike.

Return ONLY valid JSON. No markdown. No explanation. Just the JSON object."""


USER_PROMPT_TEMPLATE = """Here are {message_count} messages from the {display_name} chapter of Pavilion in {month_display}.

There were {unique_posters} unique people posting.
{images_note}

Messages:
{messages_text}

---

Produce the video script JSON with this exact structure:
{{
  "chapter": "{display_name}",
  "month": "{month_display}",
  "tension": "<provocative question or tension that hooks the viewer>",
  "stat_hook": {{
    "number": "<the most interesting number>",
    "descriptor": "<what the number means>"
  }},
  "moments": [
    {{
      "quote": "<shortened quote, max 12 words>",
      "first_name": "<first name only>",
      "title": "<their job title>",
      "has_image": false
    }},
    ... (exactly 6 — they should tell a narrative arc)
  ],
  "topics": ["<topic 1>", "<topic 2>", "<topic 3>", "<topic 4>", "<topic 5>", "<topic 6>"],
  "headline": "<emotional one-liner — the climax>",
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
    image_count = 0
    for msg in messages_data["messages"]:
        name = msg.get("display_name", "Member")
        title = msg.get("title", "")
        title_str = f" ({title})" if title else ""
        img_tag = ""
        if msg.get("images"):
            img_tag = " [📷 has image]"
            image_count += len(msg["images"])
        messages_text += f"- {name}{title_str}: {msg['text']}{img_tag}\n"

    images_note = ""
    if image_count:
        images_note = f"\n{image_count} messages included images (screenshots, charts, photos). Messages with images are marked [📷 has image]."

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
        images_note=images_note,
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
    """Validate that a script has all required fields and exactly 6 moments."""
    required_keys = ["chapter", "month", "tension", "stat_hook", "moments", "topics", "headline", "cta_line"]
    for key in required_keys:
        if key not in script:
            print(f"Missing required field: {key}")
            return False

    if not isinstance(script["moments"], list) or len(script["moments"]) != 6:
        print(f"Expected exactly 6 moments, got {len(script.get('moments', []))}")
        return False

    for i, moment in enumerate(script["moments"]):
        for field in ["quote", "first_name", "title"]:
            if field not in moment:
                print(f"Moment {i} missing field: {field}")
                return False

    stat = script["stat_hook"]
    if "number" not in stat or "descriptor" not in stat:
        print("stat_hook missing 'number' or 'descriptor'")
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

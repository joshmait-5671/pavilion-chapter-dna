"""Pull messages from a Slack chapter channel for a given month."""

import json
import os
import urllib.request
from datetime import datetime
from calendar import monthrange

from slack_sdk import WebClient


def pull_channel_messages(client: WebClient, channel_id: str, year: int, month: int) -> list:
    """Fetch all top-level messages from a channel for the given month.

    Returns list of dicts with: user, text, ts, images (list of image URLs).
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

            # Extract image attachments
            images = []
            for f in msg.get("files", []):
                if f.get("mimetype", "").startswith("image/"):
                    # url_private requires auth; thumb_720 is a good size for video
                    url = f.get("thumb_720") or f.get("url_private")
                    if url:
                        images.append(url)

            messages.append({
                "user": msg.get("user", "unknown"),
                "text": text,
                "ts": msg.get("ts", ""),
                "images": images,
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


def download_images(messages: list, token: str, output_dir: str) -> dict:
    """Download Slack images locally so the HTML template can reference them.

    Returns a mapping of original URL -> local file path.
    """
    os.makedirs(output_dir, exist_ok=True)
    url_map = {}
    idx = 0

    for msg in messages:
        for url in msg.get("images", []):
            if url in url_map:
                continue
            ext = "jpg"
            if ".png" in url:
                ext = "png"
            local_path = os.path.join(output_dir, f"img_{idx:03d}.{ext}")

            req = urllib.request.Request(url, headers={"Authorization": f"Bearer {token}"})
            try:
                with urllib.request.urlopen(req) as resp:
                    data = resp.read()
                    # Verify it's actually an image, not an HTML error page
                    if data[:5] in (b'<!DOC', b'<html'):
                        print(f"  Warning: {url} returned HTML (bot may need files:read scope)")
                        continue
                    with open(local_path, "wb") as f:
                        f.write(data)
                url_map[url] = os.path.abspath(local_path)
                idx += 1
            except Exception as e:
                print(f"  Warning: failed to download {url}: {e}")

    print(f"  Downloaded {len(url_map)} images")
    return url_map


def enrich_with_profiles(client: WebClient, messages: list) -> list:
    """Add display_name, title, and avatar_url to each message by looking up user profiles.

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
                    "avatar_url": profile.get("image_192") or profile.get("image_72", ""),
                }
            except Exception:
                profile_cache[user_id] = {"display_name": "Member", "title": "", "avatar_url": ""}

        msg["display_name"] = profile_cache[user_id]["display_name"]
        msg["title"] = profile_cache[user_id]["title"]
        msg["avatar_url"] = profile_cache[user_id]["avatar_url"]

    return messages


def download_avatars(messages: list, output_dir: str, max_avatars: int = 16) -> list:
    """Download unique profile photos for the avatar wall.

    Returns list of local file paths (up to max_avatars).
    """
    os.makedirs(output_dir, exist_ok=True)
    seen_urls = set()
    paths = []

    for msg in messages:
        url = msg.get("avatar_url", "")
        if not url or url in seen_urls:
            continue
        seen_urls.add(url)

        ext = "jpg"
        local_path = os.path.join(output_dir, f"avatar_{len(paths):03d}.{ext}")
        try:
            urllib.request.urlretrieve(url, local_path)
            paths.append(os.path.abspath(local_path))
        except Exception as e:
            print(f"  Warning: failed to download avatar {url}: {e}")

        if len(paths) >= max_avatars:
            break

    print(f"  Downloaded {len(paths)} profile photos")
    return paths


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

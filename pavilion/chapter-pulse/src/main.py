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

from pull_messages import pull_channel_messages, enrich_with_profiles, check_threshold, save_messages, download_images, download_avatars
from generate_script import generate_script, validate_script, save_script
from review import review_script
from template import build_video_html
from render_video import render


# Paths relative to project root
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CONFIG_PATH = os.path.join(PROJECT_ROOT, "config.json")
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
SCRIPTS_DIR = os.path.join(PROJECT_ROOT, "scripts")
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "templates", "video-template-v3.html")
LOGO_PATH = os.path.join(PROJECT_ROOT, "assets", "pavilion-logo.png")
IMAGES_DIR = os.path.join(PROJECT_ROOT, "data", "images")
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

    # ── STAGE 4: Download images + avatars ──
    print("\n[4/5] Downloading Slack images + profile photos...\n")
    image_paths = {}
    montage_paths = []
    avatar_paths = []
    slack_token = os.environ.get("SLACK_BOT_TOKEN", "")

    if slack_token and not args.skip_pull:
        img_dir = os.path.join(IMAGES_DIR, f"{chapter_key}-{month_str}")

        # Download message images (for proof wall + montage)
        url_map = download_images(messages_data.get("messages", []), slack_token, img_dir)

        # Map images to moments (proof wall cards)
        for i, moment in enumerate(script.get("moments", [])):
            if moment.get("has_image") and url_map:
                for url, path in url_map.items():
                    if path not in image_paths.values():
                        image_paths[i] = path
                        break

        # Use all downloaded images for montage (up to 3)
        montage_paths = list(url_map.values())[:3]

        # Download profile avatars
        avatar_dir = os.path.join(IMAGES_DIR, f"{chapter_key}-{month_str}-avatars")
        avatar_paths = download_avatars(messages_data.get("messages", []), avatar_dir)
    else:
        print("  Skipping image download (no token or --skip-pull)")

    # ── STAGE 5: Render ──
    print("\n[5/5] Rendering video...\n")

    # Inject script into template
    video_html_path = os.path.join(OUTPUT_DIR, f"{chapter_key}-{month_str}.html")
    build_video_html(script, TEMPLATE_PATH, video_html_path,
                     logo_path=os.path.abspath(LOGO_PATH),
                     image_paths=image_paths,
                     montage_paths=montage_paths,
                     avatar_paths=avatar_paths)

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

"""Build the AI in GTM Bundle 30-second ad video.

Usage:
    python src/build.py
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from template import _data_uri
from render_video import render

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
TEMPLATE_PATH = os.path.join(PROJECT_ROOT, "templates", "ai-gtm-ad.html")
LOGO_PATH = os.path.join(PROJECT_ROOT, "assets", "pavilion-logo.png")
ASSETS_DIR = os.path.join(PROJECT_ROOT, "assets")
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")


def build_logo_strip() -> str:
    """Build HTML for the company logo strip in Scene 2."""
    logo_dir = os.path.join(ASSETS_DIR, "logos")
    logos = sorted(f for f in os.listdir(logo_dir) if f.endswith(".png"))
    imgs = []
    for logo_file in logos:
        path = os.path.join(logo_dir, logo_file)
        imgs.append(f'<img src="{_data_uri(path)}">')
    return "\n      ".join(imgs)


def build_html():
    """Inject assets into the template and write the output HTML."""
    with open(TEMPLATE_PATH) as f:
        html = f.read()

    replacements = {
        "{{LOGO_PATH}}": _data_uri(LOGO_PATH),
        "{{LOGO_STRIP}}": build_logo_strip(),
        "{{HEADSHOT_1}}": f'<img src="{_data_uri(os.path.join(ASSETS_DIR, "headshots", "steven-gerry.jpg"))}">',
        "{{HEADSHOT_2}}": f'<img src="{_data_uri(os.path.join(ASSETS_DIR, "headshots", "andrew-mahr.jpg"))}">',
    }

    for placeholder, value in replacements.items():
        html = html.replace(placeholder, value)

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    output_path = os.path.join(OUTPUT_DIR, "ai-gtm-ad.html")
    with open(output_path, "w") as f:
        f.write(html)

    print(f"HTML written to {output_path}")
    return output_path


def main():
    print("\n" + "=" * 60)
    print("  AI IN GTM BUNDLE — 30-SECOND AD")
    print("=" * 60 + "\n")

    # Build HTML
    html_path = build_html()

    # Render to MP4
    mp4_path = os.path.join(OUTPUT_DIR, "ai-gtm-ad.mp4")
    render(os.path.abspath(html_path), os.path.abspath(mp4_path))

    print(f"\n{'=' * 60}")
    print(f"  DONE: {mp4_path}")
    print(f"{'=' * 60}\n")


if __name__ == "__main__":
    main()

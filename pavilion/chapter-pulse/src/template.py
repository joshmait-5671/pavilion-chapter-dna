"""Inject script data into the HTML video template."""

import base64
import mimetypes
import os


def _data_uri(path: str) -> str:
    """Convert a local image file to a base64 data URI for reliable Chromium rendering."""
    if not path:
        return ""
    if path.startswith("data:") or path.startswith("http"):
        return path
    abspath = os.path.abspath(path)
    if not os.path.isfile(abspath):
        return ""
    mime = mimetypes.guess_type(abspath)[0] or "image/jpeg"
    with open(abspath, "rb") as f:
        b64 = base64.b64encode(f.read()).decode("ascii")
    return f"data:{mime};base64,{b64}"


def _build_avatar_grid(avatar_paths: list) -> str:
    """Build HTML for the avatar wall grid — ONLY real profile photos, no placeholders."""
    cells = []
    for i, path in enumerate(avatar_paths):
        if not path:
            continue
        cls = f"avatar-cell av-{i+1}"
        cells.append(f'<div class="{cls}"><img src="{_data_uri(path)}"></div>')
        if i >= 24:  # max 25
            break
    return "\n      ".join(cells)


def _build_montage(montage_paths: list) -> dict:
    """Build HTML for the 3 montage photo slots. Only uses real images."""
    result = {}
    for i in range(3):
        key = f"{{{{MONTAGE_{i+1}}}}}"
        if i < len(montage_paths) and montage_paths[i]:
            result[key] = f'<img src="{_data_uri(montage_paths[i])}">'
        else:
            result[key] = ""
    return result


def inject_script(template_html: str, script: dict, logo_path: str = "",
                  image_paths: dict = None, montage_paths: list = None,
                  avatar_paths: list = None) -> str:
    """Replace all {{PLACEHOLDER}} tokens with values from the script."""
    if image_paths is None:
        image_paths = {}
    if montage_paths is None:
        montage_paths = []
    if avatar_paths is None:
        avatar_paths = []

    moments = script["moments"]

    replacements = {
        "{{CHAPTER_NAME}}": script["chapter"].upper(),
        "{{MONTH}}": script.get("month", ""),
        "{{LOGO_PATH}}": _data_uri(logo_path),
        "{{TENSION}}": script.get("tension", ""),
        "{{STAT_NUMBER}}": script["stat_hook"]["number"],
        "{{STAT_DESCRIPTOR}}": script["stat_hook"]["descriptor"].upper(),
        "{{HEADLINE}}": script.get("headline", ""),
        "{{CTA_LINE}}": script["cta_line"],
    }

    # Proof wall: 6 messages
    for i in range(6):
        idx = i + 1
        m = moments[i] if i < len(moments) else {"quote": "", "first_name": "", "title": ""}
        replacements[f"{{{{Q{idx}_TEXT}}}}"] = m["quote"]
        replacements[f"{{{{Q{idx}_NAME}}}}"] = m["first_name"]
        replacements[f"{{{{Q{idx}_TITLE}}}}"] = m["title"]
        replacements[f"{{{{Q{idx}_INITIAL}}}}"] = m["first_name"][0].upper() if m["first_name"] else ""

        # Image in message card
        img_html = ""
        if i in image_paths:
            img_html = f'<img class="msg-image" src="{_data_uri(image_paths[i])}">'
        elif m.get("has_image"):
            img_html = '<div style="width:100%;height:80px;border-radius:8px;margin-top:8px;background:linear-gradient(135deg,rgba(223,40,91,0.2),rgba(124,58,237,0.2));border:1px solid rgba(255,255,255,0.08);"></div>'
        replacements[f"{{{{Q{idx}_IMAGE}}}}"] = img_html

    # Momentum quotes (last 2 moments)
    bq1 = moments[4] if len(moments) > 4 else {"quote": "", "first_name": "", "title": ""}
    bq2 = moments[5] if len(moments) > 5 else {"quote": "", "first_name": "", "title": ""}
    replacements["{{BQ1_TEXT}}"] = bq1["quote"]
    replacements["{{BQ1_NAME}}"] = bq1["first_name"]
    replacements["{{BQ1_TITLE}}"] = bq1["title"]
    replacements["{{BQ2_TEXT}}"] = bq2["quote"]
    replacements["{{BQ2_NAME}}"] = bq2["first_name"]
    replacements["{{BQ2_TITLE}}"] = bq2["title"]

    # Topic pills
    topics = script.get("topics", [])
    for i in range(6):
        key = f"{{{{TOPIC_{i+1}}}}}"
        replacements[key] = topics[i] if i < len(topics) else ""

    # Photo montage — hide scene if no real images
    montage_replacements = _build_montage(montage_paths)
    replacements.update(montage_replacements)
    has_montage = any(montage_paths)
    replacements["{{SCENE_5_DISPLAY}}"] = "" if has_montage else "display:none !important;"

    # Avatar grid — only real profile photos, hide scene if none
    replacements["{{AVATAR_GRID}}"] = _build_avatar_grid(avatar_paths)
    replacements["{{SCENE_6_DISPLAY}}"] = "" if avatar_paths else "display:none !important;"

    result = template_html
    for placeholder, value in replacements.items():
        result = result.replace(placeholder, str(value))

    return result


def build_video_html(script: dict, template_path: str, output_path: str,
                     logo_path: str = "", image_paths: dict = None,
                     montage_paths: list = None, avatar_paths: list = None) -> str:
    """Read template, inject script, write final HTML. Returns output path."""
    with open(template_path) as f:
        template = f.read()

    html = inject_script(template, script, logo_path, image_paths,
                         montage_paths, avatar_paths)

    os.makedirs(os.path.dirname(output_path) or ".", exist_ok=True)
    with open(output_path, "w") as f:
        f.write(html)

    print(f"Video HTML written to {output_path}")
    return output_path

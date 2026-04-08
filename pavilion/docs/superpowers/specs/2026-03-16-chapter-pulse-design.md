# Chapter Pulse: Design Spec

**Date:** 2026-03-16
**Author:** Josh Mait + Claude
**Status:** Approved design, pending implementation

## What This Is

A system that turns monthly Slack chapter activity into 30-second MP4 videos for performance marketing. Each video highlights the best conversations, stats, and moments from a Pavilion chapter. Used on LinkedIn, email, and paid social to target prospects in local markets.

Think: the Economist meets Nike. Intelligence with swagger. This is an ad, not a webpage.

## First Use Case

Boston chapter. Manual trigger. Prove the full pipeline on one chapter before scaling.

## Architecture

Four pieces, in sequence:

```
Slack API → JSON → Claude → Script JSON → HTML Template → Playwright + ffmpeg → MP4
```

### 1. Data Pipeline

**Source:** Slack API via existing Recapper bot credentials (Socket Mode, same Slack app). The bot must be added to each chapter channel before pulling data. For Boston, verify the bot is in the Boston chapter channel first.

**Channel config:** `config.json` in project root maps chapter names to Slack channel IDs:
```json
{
  "chapters": {
    "boston": { "channel_id": "C0XXXXXX", "display_name": "Boston" }
  }
}
```
New chapters are added by adding a line to this file. No code changes needed.

**What we pull per chapter, per month:**
- Top-level messages only (no thread replies). Known limitation: great quotes buried in threads will be missed. Acceptable for v1.
- Message count, unique poster count
- Message text, author display name, timestamp

**Storage:** One JSON file per chapter per month. Format: `boston-2026-03.json`

**Trigger:** Manual for now via `python src/main.py --chapter boston`. Future: monthly Railway cron.

**Minimum threshold:** 30+ messages in the month. Below that, script exits with a warning message ("Boston had only 12 messages in March — below the 30-message threshold. No video generated.") and no video is created.

**Scale target:** Top 10-12 chapters by activity, after Boston is proven.

### 2. Claude Summarization

**Input:** Raw chapter messages JSON.

**Output:** Structured JSON script with exactly these fields:

```json
{
  "chapter": "Boston",
  "month": "March 2026",
  "stat_hook": {
    "number": "43",
    "descriptor": "conversations in one month"
  },
  "moments": [
    {
      "quote": "I got two warm intros in one week.",
      "first_name": "Sarah",
      "title": "VP Sales, Acme Corp"
    },
    {
      "quote": "Shared our comp benchmarks and got 6 DMs within an hour.",
      "first_name": "Mike",
      "title": "Director RevOps, TechCo"
    },
    {
      "quote": "Best chapter event we've had all year.",
      "first_name": "Elena",
      "title": "CRO, DataStack"
    }
  ],
  "beat_4_stat": {
    "number": "12",
    "descriptor": "unique voices this month"
  },
  "cta_line": "Boston's room is open."
}
```

**Claude's job:** Pick the most interesting stat, exactly 3 quotes (shortened for screen if needed), and write a chapter-specific CTA.

**Privacy:** First name + title only. No last names.

**Review gate:** Script JSON is printed to terminal. Josh reads it and types `approve`, `edit` (opens the JSON in default editor), or `reject` (exits). Nothing renders until approved.

**Beat 4 content:** For v1, Beat 4 always shows an additional community stat (e.g., "12 unique voices this month"). Event photos are cut from v1 to reduce complexity. Added in v2 once the core pipeline works.

### 3. HTML Video Template

**Format:** Single HTML file with CSS keyframe animations.

**Dimensions:** 1080x1080 (square). Native to LinkedIn feed, Instagram, paid social.

**Five beats:**

| Beat | Time | What's on screen |
|------|------|-----------------|
| 1 | 0-5s | Dark navy bg. Chapter name huge, fills the frame. Pavilion mark in corner. |
| 2 | 5-12s | Stat number slams in. Counting animation. Descriptor below. |
| 3 | 12-22s | 3 quotes snap in like film cards. ~3.3s each. First name + title smaller below. Fast cuts. |
| 4 | 22-26s | Community stat (e.g., "12 unique voices"). Same slam-in treatment as Beat 2. |
| 5 | 26-30s | CTA line punches in. Pavilion logo. joinpavilion.com. |

**Visual energy:**
- This is an ad. Every frame earns attention or loses it.
- Faster cuts. Nothing stays comfortable.
- Text slides, scales, punches from edges. Stats slam. Quotes snap.
- Type fills the frame. Chapter name feels too big for the screen.
- Timing designed as if there's a beat drop. Visual rhythm you can hear.
- No "welcome to" or "check out." Just: BOSTON. 43 CONVERSATIONS. Quote. JOIN THE ROOM.

**Visual language:**
- Deep navy background (`--blue-700` / `#180A5C`)
- Pink accents on stat numbers and CTA (`--pink-700` / `#DF285B`)
- White text (`#fff`) for quotes and descriptors
- Poppins 900 for chapter name and stat number
- Poppins 700 for quotes
- Poppins 400 for attribution and CTA URL
- No gradients on white. No drop shadows. Contrast and motion only.

**Template is reusable.** Same HTML, different data. Claude's JSON fills the placeholder slots. Works for every chapter.

### 4. Render Pipeline

**Approach:** Frame-by-frame capture with ffmpeg stitching. This is more reliable than real-time screen recording (no frame drops, no timing drift).

**How it works:**
1. Claude's JSON script injected into HTML template (placeholder replacement via Python string templating)
2. Python uses `playwright` (sync API) to open the HTML at 1080x1080 in headless Chromium
3. For each frame: advance CSS animation to the exact time position using JavaScript (`document.getAnimations().forEach(a => a.currentTime = frameTime)`), then capture a screenshot as PNG
4. 30 seconds at 30fps = 900 frames captured as PNGs in a temp directory
5. `ffmpeg` stitches PNGs into MP4 (H.264, high quality): `ffmpeg -framerate 30 -i frame_%04d.png -c:v libx264 -pix_fmt yuv420p output.mp4`
6. Temp PNGs deleted. Final MP4 saved to `output/boston-2026-03.mp4`

**Dependencies:**
- Python 3.9+
- `playwright` (Python, handles headless Chromium — actively maintained by Microsoft)
- `anthropic` (Python, Claude API)
- `slack_sdk` (Python, Slack API)
- `ffmpeg` (system install, must be on PATH). Install: `brew install ffmpeg`
- No Node.js required. Everything is Python + ffmpeg.

**Note on Google Fonts:** The template loads Poppins via Google Fonts URL. Playwright's `wait_until="networkidle"` ensures the font loads before frame capture begins. If network is unavailable, the system font fallback will render instead.

**Review flow:** MP4 opens in default video player after render. Three options:
- **Approve** — ready to post
- **Script change** — re-run `generate_script.py`, review new script, re-render
- **Visual tweak** — edit the HTML template, re-render

**Deployment:** Python script runs locally for now. Moves to Railway with monthly cron when scaling to multiple chapters.

## File Structure

```
/Users/joshmait/Desktop/Claude/chapter-pulse/
  data/                    # Raw Slack JSON per chapter/month
    boston-2026-03.json
  scripts/                 # Claude-generated video scripts
    boston-2026-03-script.json
  templates/
    video-template.html    # The animated HTML template
  output/                  # Final MP4s
    boston-2026-03.mp4
  src/
    pull_messages.py       # Slack data pipeline
    generate_script.py     # Claude summarization
    render_video.py        # Playwright frame capture + ffmpeg stitch
    main.py                # Orchestrator (manual trigger)
```

## What's Not In Scope

- Audio/music (silent video, captions carry it)
- Vertical format (square only for v1)
- Auto-posting to LinkedIn or ad platforms (manual upload)
- Chapter comparison or cross-chapter compilation
- Member approval of their quotes (first name + title only, low privacy risk)

## Success Criteria

1. Boston March 2026 video renders as a clean 30-second MP4
2. Josh reviews and approves the script and final video
3. Video looks like an ad, not a corporate explainer
4. Pipeline is repeatable — running it for a second chapter requires zero code changes, just a different channel ID

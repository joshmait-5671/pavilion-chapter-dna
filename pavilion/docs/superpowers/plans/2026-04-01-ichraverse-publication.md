# ICHRAverse Weekly — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an automated weekly ICHRA industry publication — scraper, Claude assembler, HTML builder, Resend notifier, and Netlify-hosted landing page with issue archive.

**Architecture:** Railway-hosted Python service runs weekly cron (Sunday night). It scrapes 11 Tier 1 + 4 Tier 2 sources, feeds content to Claude which assembles a 7-section issue, renders it into a static HTML page from a Jinja2 template, pushes to a GitHub branch triggering a Netlify Deploy Preview, and pings subscribers via Resend once approved. The Content Hub landing page is rewritten as the publication archive with subscribe form.

**Tech Stack:** Python 3.11, APScheduler, feedparser (RSS), BeautifulSoup4 (HTML scrape), Anthropic SDK, Resend SDK, Jinja2 (templating), Netlify Forms (subscribe), Railway (hosting)

**Spec:** `docs/superpowers/specs/2026-04-01-ichraverse-publication-design.md`
**Visual reference:** `healthsherpa-ichra/.superpowers/brainstorm/65721-1775095623/visual-direction-v5.html`

---

## File Structure

```
healthsherpa-ichra/
├── content-hub/
│   ├── index.html              # REWRITE — publication landing page + archive + subscribe
│   └── issues/
│       └── .gitkeep            # Generated issues go here
├── Dockerfile                  # Railway deployment image (root for build context)
├── automation/
│   ├── main.py                 # Orchestrator: scheduler + pipeline runner
│   ├── scraper.py              # RSS + HTML + Reddit scraper
│   ├── assembler.py            # Claude API: raw content → structured issue JSON
│   ├── builder.py              # Jinja2: issue JSON → static HTML page
│   ├── notifier.py             # Resend: email subscriber notifications
│   ├── deployer.py             # Git push to preview branch → Netlify Deploy Preview
│   ├── sources.json            # Source definitions (URLs, types, selectors)
│   └── requirements.txt        # Python dependencies
├── templates/
│   └── issue-template.html     # Jinja2 template (converted from v5 mockup)
├── data/
│   └── articles.json           # Existing — untouched (used by other tools)
└── shared/
    └── styles.css              # Existing — untouched
```

**Key boundaries:**
- `scraper.py` outputs raw content (list of dicts with title, url, summary, source, date)
- `assembler.py` takes raw content, returns structured issue JSON (one key per section)
- `builder.py` takes issue JSON + template, outputs HTML string
- `notifier.py` takes issue URL + subscriber list, sends emails
- `main.py` orchestrates: scrape → assemble → build → deploy → notify

---

## Chunk 1: Issue Template + Landing Page

These are the two static HTML deliverables. No Python yet.

### Task 1: Convert v5 mockup to Jinja2 issue template

**Files:**
- Create: `healthsherpa-ichra/templates/issue-template.html`
- Reference: `healthsherpa-ichra/.superpowers/brainstorm/65721-1775095623/visual-direction-v5.html`

The v5 mockup has hardcoded sample content. Convert it to a Jinja2 template with variables for each section. The template must be a complete standalone HTML page (all CSS embedded) that renders a single issue.

- [ ] **Step 1: Create template file with Jinja2 variables**

Copy the v5 mockup CSS verbatim (lines 7-507 of the mockup). Replace all hardcoded content with Jinja2 variables. The template variables map to the issue JSON schema:

```html
<!-- Template variables expected:
  issue_number: int (e.g., 7)
  issue_date: str (e.g., "MAR 31, 2026")
  mike_note: str (2-3 sentences, HTML allowed for <em> tags)
  tldr: list of {text: str, url: str}  (5 items)
  deep_read: {
    title: str,
    read_time: str,
    paragraphs: list of str (HTML allowed for <strong> tags)
  }
  market_signals: {
    stats: list of {value: str, label: str, source: str}  (4 items)
    items: list of {text: str}  (3 items, HTML allowed for <strong>)
  }
  fringe: {
    title: str,
    body: str,
    source: str
  }
  broker: {
    headline: str,
    body: str
  }
  one_question: str
  social_cards: list of {
    section: str,
    headline: str,
    gradient: str (CSS gradient value),
    stat_overlay: str|null (optional big number)
  }  (3 items)
-->
```

Key template sections (preserve exact CSS classes from mockup):

**Page wrapper + background:**
```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>ICHRAverse Weekly — Issue {{ issue_number }}</title>
<style>
  /* PASTE ALL CSS FROM v5 MOCKUP LINES 8-506 VERBATIM */
</style>
</head>
<body>
<div class="bg-word"><span>ICHRA</span><span>VERSE</span></div>
<div class="page">
  <div class="page-header">
    <h1>ICHRAverse Weekly</h1>
    <p>The pulse of the ICHRA ecosystem</p>
  </div>
```

**Masthead:**
```html
  <div class="issue">
    <div class="masthead">
      <div class="masthead-top">
        <div class="masthead-brand">ICHRAverse <span>by HealthSherpa</span></div>
        <div class="masthead-meta">ISSUE {{ "%02d"|format(issue_number) }} · {{ issue_date }}</div>
      </div>
      <div class="masthead-tagline">The pulse of the ICHRA ecosystem. Weekly.</div>
    </div>
```

**Mike's Note:**
```html
    <div class="mike-note">
      <div class="mike-avatar">ML</div>
      <div class="mike-content">
        <div class="mike-label">Mike's Note</div>
        <div class="mike-text">{{ mike_note }}</div>
      </div>
    </div>
```

**TL;DR:**
```html
    <div class="tldr">
      <div class="tldr-label">TL;DR — This Week in 30 Seconds</div>
      <ul class="tldr-list">
        {% for item in tldr %}
        <li>{{ item.text }} <a href="{{ item.url }}" target="_blank" style="color:#0970C5;">(link)</a></li>
        {% endfor %}
      </ul>
    </div>
```

**Deep Read:**
```html
    <div class="deep-read">
      <div class="section-label">The Deep Read</div>
      <div class="deep-read-hero">
        <div class="deep-read-title">{{ deep_read.title }}</div>
        <div class="deep-read-subtitle">{{ deep_read.read_time }} · Analysis by ICHRAverse Research</div>
      </div>
      <div class="deep-read-body">
        {% for p in deep_read.paragraphs %}
        <p>{{ p }}</p>
        {% endfor %}
      </div>
    </div>
```

**Market Signals:**
```html
    <div class="market-signals">
      <div class="section-label">Market Signals</div>
      <div class="signal-grid">
        {% for stat in market_signals.stats %}
        <div class="signal-card">
          <div class="signal-stat">{{ stat.value }}</div>
          <div class="signal-label">{{ stat.label }}</div>
          <div class="signal-source">{{ stat.source }}</div>
        </div>
        {% endfor %}
      </div>
      <div class="signal-items">
        {% for item in market_signals.items %}
        <div class="signal-item">
          <div class="signal-dot"></div>
          <div class="signal-text">{{ item.text }}</div>
        </div>
        {% endfor %}
      </div>
    </div>
```

**From the Fringe:**
```html
    <div class="fringe">
      <div class="fringe-label">From the Fringe</div>
      <div class="fringe-disclaimer">This section surfaces unverified claims and emerging conversations from corners of the internet. We flag it so you don't get blindsided. None of this is confirmed.</div>
      <div class="fringe-title">{{ fringe.title }}</div>
      <div class="fringe-body">{{ fringe.body }}</div>
      <div class="fringe-source">{{ fringe.source }}</div>
    </div>
```

**Broker Toolkit:**
```html
    <div class="broker">
      <div class="section-label">Broker Toolkit</div>
      <div class="broker-card">
        <div class="broker-headline">{{ broker.headline }}</div>
        <div class="broker-body">{{ broker.body }}</div>
      </div>
    </div>
```

**One Question:**
```html
    <div class="one-q">
      <div class="one-q-label">One Question</div>
      <div class="one-q-text">{{ one_question }}</div>
    </div>
```

**Footer:**
```html
    <div class="issue-footer">
      <div class="issue-footer-brand">ICHRAverse</div>
      <div class="issue-footer-links">
        <a href="../index.html">Subscribe</a>
        <a href="../index.html">Past Issues</a>
        <a href="../../index.html">ICHRAverse Tools</a>
      </div>
    </div>
  </div>
```

**Social Cards:**
```html
  <div class="social-section">
    <h2 style="color:rgba(255,255,255,0.7);">Share This Issue</h2>
    <p style="color:rgba(255,255,255,0.35);">Each story as a standalone card — built for LinkedIn and Instagram.</p>
    <div class="social-grid">
      {% for card in social_cards %}
      <div class="social-card" style="background: {{ card.gradient }};">
        <div class="social-grid-overlay"></div>
        {% if card.stat_overlay %}
        <svg viewBox="0 0 200 200" style="position:absolute;top:16px;right:16px;width:80px;height:80px;z-index:0;opacity:0.15;">
          <text x="0" y="70" font-family="Inter" font-weight="900" font-size="72" fill="#fff">{{ card.stat_overlay }}</text>
        </svg>
        {% endif %}
        <div class="social-tag">{{ card.section }}</div>
        <div class="social-headline">{{ card.headline }}</div>
      </div>
      {% endfor %}
    </div>
  </div>
</div>
</body>
</html>
```

- [ ] **Step 2: Verify template renders with sample data**

Create a quick test script at `automation/test_template.py`:

```python
"""Render the issue template with sample data to verify it works."""
from jinja2 import Environment, FileSystemLoader
import json, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

env = Environment(loader=FileSystemLoader(os.path.join(ROOT, "templates")))
template = env.get_template("issue-template.html")

sample = {
    "issue_number": 7,
    "issue_date": "MAR 31, 2026",
    "mike_note": 'ICHRA isn\'t a product category anymore — it\'s <em>infrastructure</em>. The carriers who see it that way are building for the next decade.',
    "tldr": [
        {"text": "Centene's new ICHRA president gave his first interview.", "url": "https://example.com/1"},
        {"text": "Connecticut is the sixth state to pass ICHRA tax incentives.", "url": "https://example.com/2"},
        {"text": "Oliver Wyman projects 52% CAGR through 2028.", "url": "https://example.com/3"},
        {"text": "A Reddit thread calling ICHRA 'a scam' went viral.", "url": "https://example.com/4"},
        {"text": "One case study stat that shuts down the 'sounds risky' objection.", "url": "https://example.com/5"},
    ],
    "deep_read": {
        "title": "Centene Just Hired an ICHRA President. That Changes Everything.",
        "read_time": "5 min read",
        "paragraphs": [
            "When a Fortune 25 insurer creates an entirely new executive role for ICHRA, it's not a pilot program. It's a declaration.",
            "He didn't talk about ICHRA as a product. He talked about it as <strong>distribution infrastructure</strong>.",
            "The question isn't whether to participate — it's whether you're already late.",
        ],
    },
    "market_signals": {
        "stats": [
            {"value": "124%", "label": "YoY enrollment growth", "source": "HRA Council, 2025 Report"},
            {"value": "52%", "label": "Projected CAGR through 2028", "source": "Oliver Wyman"},
            {"value": "6", "label": "States with ICHRA tax incentives", "source": "State legislatures, 2026"},
            {"value": "92%", "label": "Employer retention rate", "source": "HRA Council"},
        ],
        "items": [
            {"text": "<strong>Connecticut</strong> passes ICHRA employer tax credit — fourth state this year"},
            {"text": "<strong>Oscar Health</strong> launches ICHRA-specific HMO plans in Texas and Florida"},
            {"text": "<strong>Thatch</strong> closes $38M Series A from Index and General Catalyst"},
        ],
    },
    "fringe": {
        "title": 'Reddit: "ICHRA is a scam designed to shift risk to employees"',
        "body": "A thread in r/healthinsurance with 200+ comments is making the rounds. Worth reading if you're building broker education materials.",
        "source": "Source: r/healthinsurance · 3 days ago · 214 comments",
    },
    "broker": {
        "headline": "This week's talk track: the 18% stat",
        "body": "A 200-person Midwest manufacturer switched to ICHRA and cut benefits costs 18% in year one with 94% employee retention.",
    },
    "one_question": "If ICHRA hits 5 million covered lives by 2028, which carrier benefits the most — and why?",
    "social_cards": [
        {"section": "The Deep Read", "headline": "Centene just<br>hired an ICHRA<br>president.", "gradient": "linear-gradient(135deg, #074294, #0B8AD9)", "stat_overlay": None},
        {"section": "Market Signals", "headline": "124% YoY.<br>The climb<br>is real.", "gradient": "linear-gradient(135deg, #074294, #0D61A6)", "stat_overlay": "124%"},
        {"section": "From the Fringe", "headline": "Reddit says<br>ICHRA is<br>a scam.", "gradient": "linear-gradient(135deg, #92400E, #D97706)", "stat_overlay": None},
    ],
}

html = template.render(**sample)
out_path = os.path.join(ROOT, "content-hub", "issues", "issue-007.html")
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, "w") as f:
    f.write(html)
print(f"Rendered to {out_path}")
```

Run: `cd healthsherpa-ichra && python automation/test_template.py`
Expected: File written to `content-hub/issues/issue-007.html`. Open in browser — should look identical to the v5 mockup.

- [ ] **Step 3: Commit template**

```bash
git add templates/issue-template.html automation/test_template.py content-hub/issues/.gitkeep
git commit -m "feat(ichraverse): add Jinja2 issue template from v5 mockup"
```

---

### Task 2: Rewrite Content Hub as publication landing page

**Files:**
- Rewrite: `healthsherpa-ichra/content-hub/index.html`
- Reference: existing `content-hub/index.html` (539 lines — read before rewriting)

The current Content Hub is an article feed with filters. Replace it with:
1. **Publication masthead** — ICHRAverse Weekly branding on navy background
2. **Latest issue hero** — links to the most recent issue
3. **Issue archive** — grid of past issues (title, date, TL;DR preview)
4. **Subscribe form** — Netlify Forms (keep existing form name `ichra-newsletter`)
5. **Footer** — links back to ICHRAverse tools dashboard

- [ ] **Step 1: Write the new landing page**

Key design decisions:
- Same navy `#074294` background + ICHRA/VERSE watermark as issue pages (brand consistency)
- Issue archive reads from a `issues-index.json` file (generated by builder.py)
- Subscribe form uses existing Netlify Forms setup (form name: `ichra-newsletter`)
- Responsive: 2-column grid → 1 column on mobile
- Page links to `issues/issue-NNN.html` for each past issue
- "Latest Issue" hero card is visually prominent at top

```html
<!-- content-hub/index.html structure -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ICHRAverse Weekly — The Pulse of the ICHRA Ecosystem</title>
  <!-- Inter font, all CSS embedded -->
</head>
<body>
  <!-- Navy background + ICHRA/VERSE watermark (same as issues) -->
  <div class="bg-word"><span>ICHRA</span><span>VERSE</span></div>
  <div class="page">

    <!-- HEADER: back to dashboard + subscribe CTA -->
    <header>
      <a href="../index.html">← ICHRAverse Tools</a>
      <a href="#subscribe">Subscribe</a>
    </header>

    <!-- HERO: publication branding -->
    <div class="hero">
      <h1>ICHRAverse Weekly</h1>
      <p>The pulse of the ICHRA ecosystem. Every week.</p>
    </div>

    <!-- LATEST ISSUE: big card linking to most recent -->
    <section class="latest-issue" id="latest">
      <!-- Populated by JS from issues-index.json -->
      <!-- Fallback: "First issue coming soon. Subscribe to be first." -->
    </section>

    <!-- ARCHIVE: grid of past issues -->
    <section class="archive" id="archive">
      <h2>Past Issues</h2>
      <div class="archive-grid">
        <!-- Populated by JS from issues-index.json -->
      </div>
    </section>

    <!-- SUBSCRIBE FORM -->
    <section class="subscribe" id="subscribe">
      <h2>Never miss an issue</h2>
      <p>Weekly ICHRA intelligence. No fluff. Unsubscribe anytime.</p>
      <form name="ichra-newsletter" method="POST" data-netlify="true" netlify-honeypot="bot-field">
        <input type="hidden" name="form-name" value="ichra-newsletter">
        <p class="hidden"><label>Don't fill this out: <input name="bot-field"></label></p>
        <input type="email" name="email" placeholder="you@company.com" required>
        <button type="submit">Subscribe</button>
      </form>
    </section>

    <!-- FOOTER -->
    <footer>
      <span>ICHRAverse by HealthSherpa</span>
      <a href="https://healthsherpa.com/ichra">HealthSherpa ICHRA</a>
    </footer>
  </div>

  <script>
    // Load issues-index.json and render latest + archive
    fetch('issues-index.json')
      .then(r => r.ok ? r.json() : { issues: [] })
      .then(data => {
        renderLatest(data.issues[0]);
        renderArchive(data.issues);
      })
      .catch(() => {
        document.getElementById('latest').innerHTML =
          '<div class="empty-state">First issue coming soon. Subscribe below.</div>';
      });

    function renderLatest(issue) { /* ... card with title, date, link */ }
    function renderArchive(issues) { /* ... grid of issue cards */ }
  </script>
</body>
</html>
```

Full CSS should follow the same HealthSherpa brand tokens as the issue template:
- `#074294` navy background
- `#0970C5` primary blue for links/buttons
- `#F8FAFC` light card backgrounds
- `#E2E8F0` borders
- Inter font, same weight hierarchy
- Giant watermark text matching issue pages
- Cards: 12px border-radius, subtle shadows
- Subscribe button: rounded, blue, hover darkens (matching `.hs-btn` pattern from `shared/styles.css`)

- [ ] **Step 2: Create empty issues-index.json**

```json
{
  "_note": "Auto-generated by builder.py. Do not edit manually.",
  "issues": []
}
```

Save to `healthsherpa-ichra/content-hub/issues-index.json`.

- [ ] **Step 3: Open in browser and verify**

Open `content-hub/index.html` in browser. Verify:
- Navy background with ICHRA/VERSE watermark renders
- Empty state message shows ("First issue coming soon")
- Subscribe form is visible and has Netlify Forms attributes
- Back link to dashboard works
- Responsive on mobile viewport

- [ ] **Step 4: Commit landing page**

```bash
git add content-hub/index.html content-hub/issues-index.json
git commit -m "feat(ichraverse): rewrite content hub as publication landing page"
```

---

## Chunk 2: Scraper + Sources Config

The scraper fetches content from all Tier 1 and Tier 2 sources and returns a normalized list of content items.

### Task 3: Create sources configuration

**Files:**
- Create: `healthsherpa-ichra/automation/sources.json`

- [ ] **Step 1: Write sources.json**

```json
{
  "_note": "ICHRAverse content sources. Used by scraper.py.",
  "tier1": [
    {
      "id": "benefitspro",
      "name": "BenefitsPRO",
      "type": "rss",
      "url": "https://www.benefitspro.com/feed/",
      "keywords": ["ichra", "individual coverage", "health reimbursement"],
      "max_age_days": 7
    },
    {
      "id": "beckers",
      "name": "Becker's Payer Issues",
      "type": "rss",
      "url": "https://www.beckerspayer.com/feed/",
      "keywords": ["ichra", "individual coverage", "health reimbursement"],
      "max_age_days": 7
    },
    {
      "id": "healthcare_dive",
      "name": "Healthcare Dive",
      "type": "rss",
      "url": "https://www.healthcaredive.com/feeds/news/",
      "keywords": ["ichra", "individual coverage", "health reimbursement"],
      "max_age_days": 7
    },
    {
      "id": "remodel_health",
      "name": "Remodel Health Blog",
      "type": "html",
      "url": "https://remodelhealth.com/blog",
      "selector": "article a[href*='/blog/']",
      "title_selector": "h2, h3",
      "keywords": ["ichra"],
      "max_age_days": 14
    },
    {
      "id": "take_command",
      "name": "Take Command Blog",
      "type": "html",
      "url": "https://www.takecommandhealth.com/blog",
      "selector": "article a, .blog-post a",
      "title_selector": "h2, h3",
      "keywords": ["ichra"],
      "max_age_days": 14
    },
    {
      "id": "peopleKeep",
      "name": "PeopleKeep Blog",
      "type": "html",
      "url": "https://www.peoplekeep.com/blog",
      "selector": ".post-item a",
      "title_selector": "h2, h3",
      "keywords": ["ichra", "hra"],
      "max_age_days": 14
    },
    {
      "id": "thatch",
      "name": "Thatch Blog",
      "type": "html",
      "url": "https://www.thatch.ai/blog",
      "selector": "a[href*='/blog/']",
      "title_selector": "h2, h3",
      "keywords": ["ichra"],
      "max_age_days": 14
    },
    {
      "id": "venteur",
      "name": "Venteur Blog",
      "type": "html",
      "url": "https://www.venteur.co/blog",
      "selector": "a[href*='/blog/']",
      "title_selector": "h2, h3",
      "keywords": ["ichra"],
      "max_age_days": 14
    },
    {
      "id": "prnewswire",
      "name": "PR Newswire",
      "type": "rss",
      "url": "https://www.prnewswire.com/rss/health-care-and-hospitals-news.rss",
      "keywords": ["ichra", "individual coverage health reimbursement"],
      "max_age_days": 7
    },
    {
      "id": "federal_register",
      "name": "Federal Register",
      "type": "api",
      "url": "https://www.federalregister.gov/api/v1/documents.json?conditions[term]=ICHRA&conditions[publication_date][gte]={start_date}&per_page=10",
      "max_age_days": 7
    },
    {
      "id": "nabip",
      "name": "NABIP Podcast",
      "type": "rss",
      "url": "https://feeds.buzzsprout.com/1964107.rss",
      "keywords": ["ichra", "individual coverage", "health reimbursement"],
      "max_age_days": 14
    }
  ],
  "tier2": [
    {
      "id": "reddit_healthinsurance",
      "name": "r/healthinsurance",
      "type": "reddit",
      "subreddit": "healthinsurance",
      "keywords": ["ichra"],
      "max_age_days": 7
    },
    {
      "id": "reddit_insurance",
      "name": "r/insurance",
      "type": "reddit",
      "subreddit": "insurance",
      "keywords": ["ichra"],
      "max_age_days": 7
    },
    {
      "id": "linkedin_mike",
      "name": "Mike Levin LinkedIn",
      "type": "linkedin_scrape",
      "url": "https://www.linkedin.com/in/mikelevin/recent-activity/all/",
      "max_age_days": 7,
      "_note": "v1 deferred — LinkedIn scraping is unreliable. Mike's Note uses week themes instead."
    },
    {
      "id": "twitter_ichra",
      "name": "Twitter/X ICHRA",
      "type": "twitter",
      "keywords": ["ichra"],
      "max_age_days": 7,
      "_note": "v1 deferred — Twitter API requires paid access. Will add when publication scales."
    }
  ]
}
```

- [ ] **Step 2: Commit**

```bash
git add automation/sources.json
git commit -m "feat(ichraverse): add content source definitions"
```

---

### Task 4: Build the scraper

**Files:**
- Create: `healthsherpa-ichra/automation/scraper.py`

- [ ] **Step 1: Write scraper.py**

The scraper has four functions (one per source type) + an orchestrator:

```python
"""
ICHRAverse content scraper.

Fetches ICHRA-related content from Tier 1 (RSS, HTML, API) and
Tier 2 (Reddit, LinkedIn) sources. Returns a normalized list of
content items for the assembler.

Output schema per item:
{
    "id": str,           # source_id + hash
    "title": str,
    "url": str,
    "summary": str,      # first 300 chars of content or description
    "source_name": str,  # human-readable source name
    "source_id": str,    # matches sources.json id
    "date": str,         # ISO 8601 date
    "tier": int,         # 1 or 2
    "content_type": str  # "article", "press_release", "regulation", "discussion", "podcast", "social"
}
"""
import json
import os
import hashlib
import logging
from datetime import datetime, timedelta
from urllib.parse import urljoin

import feedparser
import requests
from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)

SOURCES_PATH = os.path.join(os.path.dirname(__file__), "sources.json")
REQUEST_TIMEOUT = 15
USER_AGENT = "ICHRAverse/1.0 (editorial content aggregator)"


def load_sources() -> dict:
    with open(SOURCES_PATH) as f:
        return json.load(f)


def _item_id(source_id: str, url: str) -> str:
    return f"{source_id}_{hashlib.md5(url.encode()).hexdigest()[:8]}"


def _matches_keywords(text: str, keywords: list[str]) -> bool:
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def _cutoff_date(max_age_days: int) -> datetime:
    return datetime.utcnow() - timedelta(days=max_age_days)


# ── RSS sources ───────────────────────────────────────────────
def scrape_rss(source: dict) -> list[dict]:
    """Parse an RSS feed and return keyword-matching items."""
    items = []
    try:
        feed = feedparser.parse(source["url"], agent=USER_AGENT)
        cutoff = _cutoff_date(source["max_age_days"])

        for entry in feed.entries:
            title = entry.get("title", "")
            summary = entry.get("summary", entry.get("description", ""))
            link = entry.get("link", "")
            published = entry.get("published_parsed") or entry.get("updated_parsed")

            if published:
                pub_date = datetime(*published[:6])
                if pub_date < cutoff:
                    continue
                date_str = pub_date.strftime("%Y-%m-%d")
            else:
                date_str = datetime.utcnow().strftime("%Y-%m-%d")

            combined_text = f"{title} {summary}"
            if not _matches_keywords(combined_text, source["keywords"]):
                continue

            items.append({
                "id": _item_id(source["id"], link),
                "title": title.strip(),
                "url": link,
                "summary": BeautifulSoup(summary, "html.parser").get_text()[:300].strip(),
                "source_name": source["name"],
                "source_id": source["id"],
                "date": date_str,
                "tier": 1,
                "content_type": "podcast" if "podcast" in source["id"] else "article",
            })
    except Exception as e:
        logger.warning(f"RSS scrape failed for {source['name']}: {e}")
    return items


# ── HTML blog sources ─────────────────────────────────────────
def scrape_html(source: dict) -> list[dict]:
    """Scrape a blog listing page for ICHRA-related posts."""
    items = []
    try:
        resp = requests.get(source["url"], timeout=REQUEST_TIMEOUT,
                            headers={"User-Agent": USER_AGENT})
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "html.parser")

        links = soup.select(source["selector"])
        seen_urls = set()

        for a_tag in links[:20]:  # cap at 20 links per source
            href = a_tag.get("href", "")
            if not href or href in seen_urls:
                continue
            url = urljoin(source["url"], href)
            seen_urls.add(url)

            # Try to find title from configured selector or link text
            title_el = a_tag.select_one(source.get("title_selector", "h2, h3"))
            title = title_el.get_text().strip() if title_el else a_tag.get_text().strip()

            if not title or len(title) < 10:
                continue

            if not _matches_keywords(title, source["keywords"]):
                continue

            items.append({
                "id": _item_id(source["id"], url),
                "title": title,
                "url": url,
                "summary": "",  # would need to fetch each page for summary
                "source_name": source["name"],
                "source_id": source["id"],
                "date": datetime.utcnow().strftime("%Y-%m-%d"),
                "tier": 1,
                "content_type": "article",
            })
    except Exception as e:
        logger.warning(f"HTML scrape failed for {source['name']}: {e}")
    return items


# ── Federal Register API ──────────────────────────────────────
def scrape_federal_register(source: dict) -> list[dict]:
    """Query Federal Register API for ICHRA-related documents."""
    items = []
    try:
        start_date = _cutoff_date(source["max_age_days"]).strftime("%Y-%m-%d")
        url = source["url"].replace("{start_date}", start_date)

        resp = requests.get(url, timeout=REQUEST_TIMEOUT,
                            headers={"User-Agent": USER_AGENT})
        resp.raise_for_status()
        data = resp.json()

        for doc in data.get("results", []):
            items.append({
                "id": _item_id(source["id"], doc["html_url"]),
                "title": doc.get("title", ""),
                "url": doc["html_url"],
                "summary": doc.get("abstract", "")[:300],
                "source_name": source["name"],
                "source_id": source["id"],
                "date": doc.get("publication_date", ""),
                "tier": 1,
                "content_type": "regulation",
            })
    except Exception as e:
        logger.warning(f"Federal Register scrape failed: {e}")
    return items


# ── Reddit ────────────────────────────────────────────────────
def scrape_reddit(source: dict) -> list[dict]:
    """Search a subreddit for ICHRA discussions via old.reddit.com RSS."""
    items = []
    try:
        # Use Reddit's public search RSS (no API key needed)
        search_url = f"https://old.reddit.com/r/{source['subreddit']}/search.rss?q={'%20OR%20'.join(source['keywords'])}&restrict_sr=on&sort=new&t=week"
        feed = feedparser.parse(search_url, agent=USER_AGENT)

        for entry in feed.entries:
            title = entry.get("title", "")
            link = entry.get("link", "")
            summary = entry.get("summary", "")

            items.append({
                "id": _item_id(source["id"], link),
                "title": title.strip(),
                "url": link,
                "summary": BeautifulSoup(summary, "html.parser").get_text()[:300].strip(),
                "source_name": source["name"],
                "source_id": source["id"],
                "date": datetime.utcnow().strftime("%Y-%m-%d"),
                "tier": 2,
                "content_type": "discussion",
            })
    except Exception as e:
        logger.warning(f"Reddit scrape failed for {source['name']}: {e}")
    return items


# ── LinkedIn (Mike Levin) ─────────────────────────────────────
def scrape_linkedin(source: dict) -> list[dict]:
    """
    LinkedIn scraping is unreliable and rate-limited.
    For v1, this returns an empty list. Mike's LinkedIn content
    will be manually added or pulled from cached posts.
    Future: use a LinkedIn scraping service or manual input.
    """
    logger.info("LinkedIn scrape skipped (v1 — not automated)")
    return []


# ── Orchestrator ──────────────────────────────────────────────
def scrape_twitter(source: dict) -> list[dict]:
    """Twitter API requires paid access. Deferred to v2."""
    logger.info("Twitter scrape skipped (v1 — API access deferred)")
    return []


SCRAPERS = {
    "rss": scrape_rss,
    "html": scrape_html,
    "api": scrape_federal_register,
    "reddit": scrape_reddit,
    "linkedin_scrape": scrape_linkedin,
    "twitter": scrape_twitter,
}


def scrape_all() -> list[dict]:
    """Run all scrapers and return combined, deduplicated content list."""
    sources = load_sources()
    all_items = []

    for source in sources.get("tier1", []) + sources.get("tier2", []):
        scraper_fn = SCRAPERS.get(source["type"])
        if not scraper_fn:
            logger.warning(f"No scraper for type: {source['type']}")
            continue

        logger.info(f"Scraping {source['name']}...")
        items = scraper_fn(source)
        logger.info(f"  → {len(items)} items from {source['name']}")
        all_items.extend(items)

    # Deduplicate by URL
    seen = set()
    unique = []
    for item in all_items:
        if item["url"] not in seen:
            seen.add(item["url"])
            unique.append(item)

    # Sort by date descending
    unique.sort(key=lambda x: x["date"], reverse=True)

    logger.info(f"Total: {len(unique)} unique items from {len(sources.get('tier1', []) + sources.get('tier2', []))} sources")
    return unique


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    items = scrape_all()
    print(json.dumps(items, indent=2))
```

- [ ] **Step 2: Test scraper standalone**

```bash
cd healthsherpa-ichra/automation
pip install feedparser requests beautifulsoup4
python scraper.py
```

Expected: JSON output with content items from accessible RSS sources. Some HTML scrapes may return 0 items if selectors don't match (that's fine for v1 — selectors get tuned later).

- [ ] **Step 3: Commit scraper**

```bash
git add automation/scraper.py
git commit -m "feat(ichraverse): add multi-source content scraper"
```

---

## Chunk 3: Assembler + Builder

The assembler sends scraped content to Claude and gets back structured issue JSON. The builder renders that JSON into HTML.

### Task 5: Build the assembler

**Files:**
- Create: `healthsherpa-ichra/automation/assembler.py`

- [ ] **Step 1: Write assembler.py**

```python
"""
ICHRAverse issue assembler.

Takes raw scraped content items and uses Claude to produce a structured
issue JSON matching the template schema.

Input: list of content items from scraper.py
Output: dict matching the issue-template.html variable schema

Requires: ANTHROPIC_API_KEY environment variable
"""
import json
import logging
import os
from datetime import datetime

from anthropic import Anthropic

logger = logging.getLogger(__name__)

MODEL = "claude-sonnet-4-20250514"
MAX_TOKENS = 4096

SYSTEM_PROMPT = """You are the editorial AI for ICHRAverse Weekly, an industry publication covering the ICHRA (Individual Coverage Health Reimbursement Arrangement) ecosystem.

You will receive a list of scraped content items from the past week. Your job is to assemble a complete issue with these sections:

1. **Mike's Note** — 2-3 sentences from HealthSherpa CEO Mike Levin's perspective. Opinionated, forward-looking. Write in first person as Mike. Not a summary — a perspective on the week's biggest theme.

2. **TL;DR** — Exactly 5 bullet points. Each is one sentence covering a key development. Include the source URL for each.

3. **The Deep Read** — Pick the single most important story. Write a 3-paragraph analysis (~300 words). Use <strong> tags for emphasis. Include a compelling title.

4. **Market Signals** — 4 stats (use real numbers from sources when available, or use established ICHRA market stats like 124% YoY growth, 52% CAGR, etc.) + 3 news-bite bullet items with <strong> entity names.

5. **From the Fringe** — Pick the most interesting unverified/community discussion (Reddit, forums). If none exist in the scraped content, write about a common ICHRA misconception circulating online.

6. **Broker Toolkit** — One actionable item: a talk track, objection handler, or case study stat that brokers can use this week.

7. **One Question** — A thought-provoking question that closes the issue.

8. **Social Cards** — 3 cards for LinkedIn/Instagram. Each needs: section name, a punchy headline (use <br> for line breaks, max 3 lines), and gradient color.

CRITICAL RULES:
- Every claim must trace back to a source in the scraped content. Do not invent statistics.
- Write for carriers and industry insiders, not consumers.
- Tone: authoritative, analytical, slightly provocative. Not corporate. Not salesy.
- This is journalism, not marketing. HealthSherpa is the publisher, not the subject.
- Return ONLY valid JSON matching the schema below. No markdown, no explanation."""

SCHEMA_INSTRUCTION = """Return JSON matching this exact schema:
{
  "mike_note": "string (HTML allowed: <em>)",
  "tldr": [{"text": "string", "url": "string"}],
  "deep_read": {
    "title": "string",
    "read_time": "string (e.g. '5 min read')",
    "paragraphs": ["string (HTML allowed: <strong>)"]
  },
  "market_signals": {
    "stats": [{"value": "string", "label": "string", "source": "string"}],
    "items": [{"text": "string (HTML allowed: <strong>)"}]
  },
  "fringe": {
    "title": "string",
    "body": "string",
    "source": "string"
  },
  "broker": {
    "headline": "string",
    "body": "string"
  },
  "one_question": "string",
  "social_cards": [
    {
      "section": "string",
      "headline": "string (use <br> for line breaks)",
      "gradient": "string (CSS linear-gradient)",
      "stat_overlay": "string or null"
    }
  ]
}"""


def assemble_issue(content_items: list[dict], issue_number: int) -> dict:
    """Send scraped content to Claude and return structured issue JSON."""
    client = Anthropic()

    # Format content items for the prompt
    formatted_items = []
    for item in content_items[:30]:  # cap at 30 items to stay within context
        formatted_items.append(
            f"- [{item['source_name']}] {item['title']}\n"
            f"  URL: {item['url']}\n"
            f"  Date: {item['date']} | Type: {item['content_type']} | Tier: {item['tier']}\n"
            f"  Summary: {item['summary'][:200]}"
        )

    content_block = "\n\n".join(formatted_items)
    if not content_block.strip():
        content_block = "(No content scraped this week. Generate the issue using established ICHRA market knowledge and recent trends.)"

    user_prompt = f"""Here are the scraped content items for this week:

{content_block}

---

Assemble ICHRAverse Weekly Issue #{issue_number} from this content.

{SCHEMA_INSTRUCTION}"""

    logger.info(f"Sending {len(content_items)} items to Claude for assembly...")

    response = client.messages.create(
        model=MODEL,
        max_tokens=MAX_TOKENS,
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": user_prompt}],
    )

    raw_text = response.content[0].text.strip()

    # Parse JSON (handle potential markdown code fences)
    if raw_text.startswith("```"):
        raw_text = raw_text.split("\n", 1)[1].rsplit("```", 1)[0].strip()

    issue_data = json.loads(raw_text)

    # Validate required keys
    required = ["mike_note", "tldr", "deep_read", "market_signals", "fringe", "broker", "one_question", "social_cards"]
    missing = [k for k in required if k not in issue_data]
    if missing:
        raise ValueError(f"Assembler output missing required keys: {missing}")

    # Add metadata
    now = datetime.utcnow()
    issue_data["issue_number"] = issue_number
    issue_data["issue_date"] = now.strftime("%b %d, %Y").upper()

    logger.info("Issue assembled successfully")
    return issue_data


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Test with sample content
    sample = [
        {
            "title": "Centene Names First ICHRA President",
            "url": "https://example.com/centene",
            "summary": "Centene Corporation announced Alan Silver as president of Ambetter Health Solutions, focused on ICHRA.",
            "source_name": "Becker's",
            "source_id": "beckers",
            "date": "2026-03-28",
            "tier": 1,
            "content_type": "article",
        }
    ]
    result = assemble_issue(sample, issue_number=8)
    print(json.dumps(result, indent=2))
```

- [ ] **Step 2: Test assembler**

```bash
cd healthsherpa-ichra/automation
export ANTHROPIC_API_KEY="..."  # must be set
python assembler.py
```

Expected: JSON output matching the issue template schema. Verify all 7 sections + social cards are present.

- [ ] **Step 3: Commit assembler**

```bash
git add automation/assembler.py
git commit -m "feat(ichraverse): add Claude-powered issue assembler"
```

---

### Task 6: Build the HTML builder

**Files:**
- Create: `healthsherpa-ichra/automation/builder.py`

- [ ] **Step 1: Write builder.py**

```python
"""
ICHRAverse HTML builder.

Takes structured issue JSON from the assembler and renders it into
a static HTML page using the Jinja2 issue template. Also updates
the issues-index.json for the landing page archive.

Input: issue dict (from assembler.py)
Output: HTML file written to content-hub/issues/issue-NNN.html
"""
import json
import logging
import os

from jinja2 import Environment, FileSystemLoader

logger = logging.getLogger(__name__)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(ROOT, "templates")
ISSUES_DIR = os.path.join(ROOT, "content-hub", "issues")
INDEX_PATH = os.path.join(ROOT, "content-hub", "issues-index.json")


def build_issue(issue_data: dict) -> str:
    """Render issue JSON to HTML and write to disk. Returns file path."""
    env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))
    template = env.get_template("issue-template.html")

    html = template.render(**issue_data)

    issue_num = issue_data["issue_number"]
    filename = f"issue-{issue_num:03d}.html"
    filepath = os.path.join(ISSUES_DIR, filename)

    os.makedirs(ISSUES_DIR, exist_ok=True)
    with open(filepath, "w") as f:
        f.write(html)

    logger.info(f"Built issue HTML: {filepath}")
    return filepath


def update_index(issue_data: dict) -> None:
    """Add the new issue to issues-index.json for the landing page."""
    # Load existing index
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH) as f:
            index = json.load(f)
    else:
        index = {"issues": []}

    issue_num = issue_data["issue_number"]

    # Build index entry (minimal — just what the landing page needs)
    entry = {
        "number": issue_num,
        "date": issue_data["issue_date"],
        "file": f"issues/issue-{issue_num:03d}.html",
        "title": issue_data.get("deep_read", {}).get("title", f"Issue {issue_num}"),
        "tldr_preview": issue_data.get("tldr", [{}])[0].get("text", "")[:120],
    }

    # Remove existing entry for this issue number (in case of re-run)
    index["issues"] = [i for i in index["issues"] if i["number"] != issue_num]

    # Add new entry at the front (newest first)
    index["issues"].insert(0, entry)

    with open(INDEX_PATH, "w") as f:
        json.dump(index, f, indent=2)

    logger.info(f"Updated issues index: {INDEX_PATH}")


def build_and_index(issue_data: dict) -> str:
    """Build the HTML issue and update the archive index. Returns file path."""
    filepath = build_issue(issue_data)
    update_index(issue_data)
    return filepath


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    # Quick test: build from inline sample data
    sample = {
        "issue_number": 7,
        "issue_date": "MAR 31, 2026",
        "mike_note": "ICHRA isn't a product category anymore — it's <em>infrastructure</em>.",
        "tldr": [{"text": "Sample bullet.", "url": "https://example.com"}] * 5,
        "deep_read": {"title": "Sample Deep Read", "read_time": "5 min read", "paragraphs": ["Sample paragraph."]},
        "market_signals": {
            "stats": [{"value": "124%", "label": "YoY growth", "source": "HRA Council"}] * 4,
            "items": [{"text": "<strong>Sample</strong> signal item"}] * 3,
        },
        "fringe": {"title": "Sample Fringe", "body": "Sample body.", "source": "r/test"},
        "broker": {"headline": "Sample headline", "body": "Sample body."},
        "one_question": "Sample question?",
        "social_cards": [
            {"section": "Deep Read", "headline": "Sample", "gradient": "linear-gradient(135deg, #074294, #0B8AD9)", "stat_overlay": None},
        ] * 3,
    }
    path = build_and_index(sample)
    print(f"Built: {path}")
```

- [ ] **Step 2: Test builder**

```bash
cd healthsherpa-ichra/automation
python builder.py
```

Expected: HTML file at `content-hub/issues/issue-007.html` + updated `issues-index.json` with one entry. Open the HTML file in browser to verify it looks correct.

- [ ] **Step 3: Commit builder**

```bash
git add automation/builder.py
git commit -m "feat(ichraverse): add Jinja2 HTML builder with archive index"
```

---

## Chunk 4: Notifier + Orchestrator + Deployment

### Task 7: Build the email notifier

**Files:**
- Create: `healthsherpa-ichra/automation/notifier.py`

- [ ] **Step 1: Write notifier.py**

```python
"""
ICHRAverse email notifier.

Reads subscribers from Netlify Forms API, sends a one-line
notification email via Resend with a link to the new issue.

Requires environment variables:
- RESEND_API_KEY
- NETLIFY_ACCESS_TOKEN
- NETLIFY_FORM_ID (the ichra-newsletter form ID)
- SITE_URL (e.g., https://fabulous-frangipane-2cc5ea.netlify.app)
"""
import logging
import os

import resend
import requests

logger = logging.getLogger(__name__)

NETLIFY_API = "https://api.netlify.com/api/v1"


def get_subscribers() -> list[str]:
    """Fetch subscriber emails from Netlify Forms API."""
    token = os.environ["NETLIFY_ACCESS_TOKEN"]
    form_id = os.environ["NETLIFY_FORM_ID"]

    headers = {"Authorization": f"Bearer {token}"}
    url = f"{NETLIFY_API}/forms/{form_id}/submissions?per_page=100"

    emails = set()
    page = 1

    while True:
        resp = requests.get(f"{url}&page={page}", headers=headers, timeout=15)
        resp.raise_for_status()
        submissions = resp.json()

        if not submissions:
            break

        for sub in submissions:
            email = sub.get("data", {}).get("email", "").strip()
            if email and "@" in email:
                emails.add(email)

        page += 1

    logger.info(f"Found {len(emails)} subscribers")
    return list(emails)


def send_notification(issue_number: int, issue_url: str) -> int:
    """Send new-issue notification to all subscribers. Returns count sent."""
    resend.api_key = os.environ["RESEND_API_KEY"]

    subscribers = get_subscribers()
    if not subscribers:
        logger.info("No subscribers — skipping notification")
        return 0

    sent = 0
    for email in subscribers:
        try:
            resend.Emails.send({
                "from": "ICHRAverse Weekly <ichraverse@updates.healthsherpa.com>",
                "to": email,
                "subject": f"ICHRAverse Weekly #{issue_number} is live",
                "html": (
                    f'<p>The latest issue of ICHRAverse Weekly is live.</p>'
                    f'<p><a href="{issue_url}">Read Issue #{issue_number} →</a></p>'
                    f'<p style="color:#999;font-size:12px;">You\'re receiving this because you subscribed at ICHRAverse. '
                    f'Reply to unsubscribe.</p>'
                ),
            })
            sent += 1
        except Exception as e:
            logger.warning(f"Failed to send to {email}: {e}")

    logger.info(f"Sent {sent}/{len(subscribers)} notification emails")
    return sent


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    subs = get_subscribers()
    print(f"Subscribers: {subs}")
```

- [ ] **Step 2: Commit notifier**

```bash
git add automation/notifier.py
git commit -m "feat(ichraverse): add Resend email notifier with Netlify Forms subscriber fetch"
```

---

### Task 7b: Build the deployer (git push to preview branch)

**Files:**
- Create: `healthsherpa-ichra/automation/deployer.py`

- [ ] **Step 1: Write deployer.py**

```python
"""
ICHRAverse deployer.

Pushes generated issue files to a preview branch on GitHub.
Netlify auto-creates a Deploy Preview for branch deploys.
Josh reviews the preview, then merges to publish.

Requires: GITHUB_TOKEN, GITHUB_REPO environment variables
"""
import logging
import os
import subprocess

logger = logging.getLogger(__name__)

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def push_preview_branch(issue_number: int) -> str:
    """Push issue files to a preview branch. Returns branch name."""
    branch = f"preview/issue-{issue_number:03d}"
    repo = os.environ["GITHUB_REPO"]
    token = os.environ["GITHUB_TOKEN"]
    remote_url = f"https://x-access-token:{token}@github.com/{repo}.git"

    try:
        # Create and switch to preview branch
        subprocess.run(["git", "checkout", "-b", branch], cwd=ROOT, check=True, capture_output=True)

        # Stage the generated files
        subprocess.run(["git", "add",
            "content-hub/issues/",
            "content-hub/issues-index.json",
        ], cwd=ROOT, check=True, capture_output=True)

        # Commit
        subprocess.run(["git", "commit", "-m",
            f"issue: ICHRAverse Weekly #{issue_number}"
        ], cwd=ROOT, check=True, capture_output=True)

        # Push to remote
        subprocess.run(["git", "push", remote_url, branch],
            cwd=ROOT, check=True, capture_output=True)

        logger.info(f"Pushed branch: {branch}")

        # Switch back to main
        subprocess.run(["git", "checkout", "main"], cwd=ROOT, check=True, capture_output=True)

        return branch

    except subprocess.CalledProcessError as e:
        logger.error(f"Git operation failed: {e.stderr.decode() if e.stderr else e}")
        # Try to get back to main
        subprocess.run(["git", "checkout", "main"], cwd=ROOT, capture_output=True)
        raise
```

- [ ] **Step 2: Commit deployer**

```bash
git add automation/deployer.py
git commit -m "feat(ichraverse): add git deployer for preview branches"
```

---

### Task 8: Build the orchestrator (main.py)

**Files:**
- Create: `healthsherpa-ichra/automation/main.py`

- [ ] **Step 1: Write main.py**

```python
"""
ICHRAverse Weekly — automation orchestrator.

Runs as a Railway service. On cron schedule (Sunday 9pm ET):
1. Scrape all sources
2. Assemble issue via Claude
3. Build HTML from template
4. Push to GitHub preview branch → triggers Netlify Deploy Preview
5. Notify Josh via console log (Slack notification can be added later)

On approval (manual merge of preview branch):
- Netlify auto-deploys production
- Email notifications sent to subscribers

Environment variables required:
- ANTHROPIC_API_KEY
- RESEND_API_KEY (for email notifications)
- NETLIFY_ACCESS_TOKEN (for subscriber list)
- NETLIFY_FORM_ID (ichra-newsletter form ID)
- SITE_URL (production Netlify URL)
- GITHUB_TOKEN (for pushing preview branches)
- GITHUB_REPO (owner/repo format, e.g. joshmait/claude)
"""
import json
import logging
import os
import subprocess
import sys
from datetime import datetime

from apscheduler.schedulers.blocking import BlockingScheduler
import pytz

from scraper import scrape_all
from assembler import assemble_issue
from builder import build_and_index, INDEX_PATH
from notifier import send_notification
from deployer import push_preview_branch

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("ichraverse")

TIMEZONE = pytz.timezone("America/New_York")


def get_next_issue_number() -> int:
    """Derive next issue number from issues-index.json (survives container redeploys)."""
    if os.path.exists(INDEX_PATH):
        with open(INDEX_PATH) as f:
            index = json.load(f)
        issues = index.get("issues", [])
        if issues:
            return max(i["number"] for i in issues) + 1
    return 1


def run_pipeline():
    """Execute the full ICHRAverse publication pipeline."""
    logger.info("=" * 60)
    logger.info("ICHRAverse Weekly — Pipeline Starting")
    logger.info("=" * 60)

    # Step 1: Scrape
    logger.info("Step 1/5: Scraping content sources...")
    content = scrape_all()
    logger.info(f"Scraped {len(content)} content items")

    if len(content) == 0:
        logger.warning("No content scraped. Proceeding with empty content (Claude will use general knowledge).")

    # Step 2: Assemble
    issue_number = get_next_issue_number()
    logger.info(f"Step 2/5: Assembling Issue #{issue_number}...")
    issue_data = assemble_issue(content, issue_number)

    # Step 3: Build HTML
    logger.info("Step 3/5: Building HTML...")
    filepath = build_and_index(issue_data)
    logger.info(f"Built: {filepath}")

    # Save issue data for debugging
    debug_path = os.path.join(os.path.dirname(filepath), f"issue-{issue_number:03d}.json")
    with open(debug_path, "w") as f:
        json.dump(issue_data, f, indent=2)

    # Step 4: Push to GitHub preview branch → triggers Netlify Deploy Preview
    logger.info("Step 4/5: Pushing to preview branch...")
    preview_url = push_preview_branch(issue_number)
    logger.info(f"Deploy Preview will be available at Netlify dashboard")

    # Step 5: Log completion
    site_url = os.environ.get("SITE_URL", "https://fabulous-frangipane-2cc5ea.netlify.app")
    issue_url = f"{site_url}/content-hub/issues/issue-{issue_number:03d}.html"
    logger.info(f"Step 5/5: Issue #{issue_number} ready for review")
    logger.info(f"Production URL (after merge): {issue_url}")

    logger.info("=" * 60)
    logger.info("Pipeline complete! Merge the preview branch to publish.")
    logger.info("=" * 60)

    return issue_number, issue_url


def run_notify(issue_number: int):
    """Send email notifications for a published issue."""
    site_url = os.environ.get("SITE_URL", "https://fabulous-frangipane-2cc5ea.netlify.app")
    issue_url = f"{site_url}/content-hub/issues/issue-{issue_number:03d}.html"
    sent = send_notification(issue_number, issue_url)
    logger.info(f"Sent {sent} notification emails for Issue #{issue_number}")


def main():
    """Entry points: --now (run pipeline), --notify N (send emails), or start scheduler."""
    if "--now" in sys.argv:
        logger.info("Running pipeline immediately (--now flag)")
        run_pipeline()
        return

    if "--notify" in sys.argv:
        idx = sys.argv.index("--notify")
        issue_num = int(sys.argv[idx + 1])
        logger.info(f"Sending notifications for Issue #{issue_num}")
        run_notify(issue_num)
        return

    logger.info("ICHRAverse automation starting...")
    logger.info("Scheduled: Sunday 9:00 PM ET")

    scheduler = BlockingScheduler(timezone=TIMEZONE)
    scheduler.add_job(
        run_pipeline,
        trigger="cron",
        day_of_week="sun",
        hour=21,
        minute=0,
    )

    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Scheduler stopped.")


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: Test pipeline end-to-end**

```bash
cd healthsherpa-ichra/automation
export ANTHROPIC_API_KEY="..."
python main.py --now
```

Expected: Full pipeline runs — scrapes sources, assembles issue via Claude, builds HTML, saves to `content-hub/issues/`. Check the generated HTML in a browser.

- [ ] **Step 3: Commit orchestrator**

```bash
git add automation/main.py
git commit -m "feat(ichraverse): add pipeline orchestrator with APScheduler cron"
```

---

### Task 9: Create requirements.txt and Dockerfile

**Files:**
- Create: `healthsherpa-ichra/automation/requirements.txt`
- Create: `healthsherpa-ichra/Dockerfile` (root level for proper build context)

- [ ] **Step 1: Write requirements.txt**

```
anthropic>=0.40.0
feedparser>=6.0
beautifulsoup4>=4.12
requests>=2.31
jinja2>=3.1
resend>=2.0
apscheduler>=3.10
pytz>=2024.1
```

- [ ] **Step 2: Write Dockerfile at project root**

File: `healthsherpa-ichra/Dockerfile` (NOT inside automation/)

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install git (needed for deployer.py)
RUN apt-get update && apt-get install -y git && rm -rf /var/lib/apt/lists/*

# Install dependencies
COPY automation/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY templates/ templates/
COPY content-hub/ content-hub/
COPY automation/ automation/

# Configure git for deployer
RUN git config --global user.email "ichraverse@healthsherpa.com" && \
    git config --global user.name "ICHRAverse Bot"

WORKDIR /app/automation
CMD ["python", "main.py"]
```

- [ ] **Step 3: Commit deployment config**

```bash
git add automation/requirements.txt Dockerfile
git commit -m "feat(ichraverse): add requirements and Dockerfile for Railway"
```

---

### Task 10: Railway deployment setup

This task is manual — instructions for Josh to follow.

- [ ] **Step 1: Document Railway setup steps**

Add a section to the bottom of the plan (this file) or create a `DEPLOY.md`:

1. Create new Railway project: "ichraverse-weekly"
2. Connect to GitHub repo
3. Set root directory to `healthsherpa-ichra`
4. Dockerfile is at root level (`Dockerfile`) — Railway should auto-detect
5. Add environment variables:
   - `ANTHROPIC_API_KEY` — Anthropic API key
   - `RESEND_API_KEY` — Resend API key (get from resend.com)
   - `NETLIFY_ACCESS_TOKEN` — Netlify personal access token
   - `NETLIFY_FORM_ID` — ID of the ichra-newsletter form (find in Netlify dashboard → Forms)
   - `SITE_URL` — `https://fabulous-frangipane-2cc5ea.netlify.app`
   - `GITHUB_TOKEN` — GitHub PAT with repo write scope
   - `GITHUB_REPO` — `joshmait/claude` (or wherever the repo lives)
6. Deploy and verify logs show "ICHRAverse automation starting..."
7. Test with manual trigger: Railway console → `python main.py --now`
8. After reviewing and merging the preview branch, send notifications: `python main.py --notify <issue_number>`

- [ ] **Step 2: Commit deploy docs**

```bash
git add automation/DEPLOY.md
git commit -m "docs(ichraverse): add Railway deployment instructions"
```

---

## Chunk 5: Mike's Guided Overlay Review

### Task 11: Build the guided overlay for Mike Levin

**Files:**
- Create: `healthsherpa-ichra/content-hub/mike-review.html`

This is a standalone HTML page that wraps the v5 mockup (or a generated sample issue) with a 5-stop guided overlay. Mike opens this URL, gets walked through the publication concept, and can approve/comment/disapprove at each stop.

- [ ] **Step 1: Write the guided overlay page**

Architecture:
- Full-page overlay with a dark scrim
- The actual issue content is visible in the background (embedded or iframe)
- 5 stops, each with:
  - Step indicator (1/5, 2/5, etc.)
  - Title + explanation (2-3 sentences)
  - The relevant section highlighted/scrolled-to in the background
  - Three buttons: Approve (green), Comment (blue textarea), Flag (red)
- Progress persisted to localStorage
- "Submit Review" at the end — copies all feedback to clipboard or sends via Netlify Forms

Stop definitions:
1. **The Concept** — "ICHRAverse Weekly is a dedicated ICHRA industry publication. No one else is doing this. We publish it, the ecosystem reads it, and HealthSherpa becomes the center of the conversation."
   - Highlights: page header + masthead
2. **Issue Structure** — "Each issue has 7 sections: Mike's Note, TL;DR, Deep Read, Market Signals, From the Fringe, Broker Toolkit, and One Question. Scroll through to see each one."
   - Highlights: full issue (auto-scrolls through sections)
3. **Content Sourcing** — "Every week we scrape 15+ industry sources automatically — BenefitsPRO, Becker's, Healthcare Dive, Reddit, regulatory filings. Claude assembles the issue. Your time commitment: zero."
   - Highlights: TL;DR section (shows source links)
4. **Visual Direction** — "The look is HealthSherpa brand elevated into a tech editorial. Navy backgrounds, grid textures, the giant ICHRA/VERSE watermark. It should feel premium but familiar."
   - Highlights: background + masthead + social cards
5. **Next Steps** — "If you approve, we launch within 2 weeks. Weekly cadence. First 4 issues with Josh reviewing, then auto-publish. Social cards for LinkedIn/Instagram included."
   - Highlights: social cards section

```html
<!-- mike-review.html structure -->
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>ICHRAverse Weekly — Review</title>
  <style>
    /* Inter font */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap');

    * { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: 'Inter', sans-serif; }

    /* Iframe holds the actual issue */
    .issue-frame {
      width: 100%;
      height: 100vh;
      border: none;
      position: fixed;
      top: 0; left: 0;
      z-index: 1;
    }

    /* Overlay scrim */
    .overlay {
      position: fixed;
      inset: 0;
      background: rgba(0,0,0,0.7);
      z-index: 10;
      display: flex;
      align-items: center;
      justify-content: center;
      opacity: 1;
      transition: opacity 0.3s;
    }
    .overlay.hidden { opacity: 0; pointer-events: none; }

    /* Review card */
    .review-card {
      background: #fff;
      border-radius: 16px;
      padding: 40px;
      max-width: 520px;
      width: 90%;
      box-shadow: 0 20px 60px rgba(0,0,0,0.3);
    }
    .step-indicator {
      font-size: 12px;
      font-weight: 700;
      color: #0970C5;
      text-transform: uppercase;
      letter-spacing: 1.5px;
      margin-bottom: 12px;
    }
    .review-card h2 {
      font-size: 24px;
      font-weight: 800;
      color: #1a1a1a;
      margin-bottom: 12px;
    }
    .review-card p {
      font-size: 15px;
      line-height: 1.65;
      color: #475467;
      margin-bottom: 24px;
    }

    /* Action buttons */
    .actions { display: flex; gap: 10px; flex-wrap: wrap; }
    .btn {
      padding: 10px 20px;
      border-radius: 8px;
      border: none;
      font-size: 14px;
      font-weight: 600;
      cursor: pointer;
      transition: all 0.15s;
    }
    .btn-approve { background: #10B981; color: #fff; }
    .btn-approve:hover { background: #059669; }
    .btn-comment { background: #0970C5; color: #fff; }
    .btn-comment:hover { background: #0D61A6; }
    .btn-flag { background: #EF4444; color: #fff; }
    .btn-flag:hover { background: #DC2626; }
    .btn-next { background: #074294; color: #fff; margin-top: 12px; }
    .btn-next:hover { background: #0D61A6; }
    .btn-peek { background: transparent; color: #0970C5; border: 1px solid #E2E8F0; }

    /* Comment textarea */
    .comment-box {
      width: 100%;
      margin-top: 12px;
      padding: 12px;
      border: 1px solid #E2E8F0;
      border-radius: 8px;
      font-family: 'Inter', sans-serif;
      font-size: 14px;
      resize: vertical;
      min-height: 80px;
      display: none;
    }
    .comment-box.visible { display: block; }

    /* Status badges */
    .status {
      display: inline-block;
      padding: 4px 10px;
      border-radius: 12px;
      font-size: 11px;
      font-weight: 700;
      margin-bottom: 16px;
    }
    .status-approved { background: #D1FAE5; color: #065F46; }
    .status-flagged { background: #FEE2E2; color: #991B1B; }
    .status-commented { background: #DBEAFE; color: #1E40AF; }
  </style>
</head>
<body>

  <!-- The actual issue -->
  <iframe class="issue-frame" src="issues/issue-007.html" id="issueFrame"></iframe>

  <!-- Overlay -->
  <div class="overlay" id="overlay">
    <div class="review-card" id="reviewCard">
      <!-- Populated by JS -->
    </div>
  </div>

  <script>
    const STOPS = [
      {
        title: "The Concept",
        body: "ICHRAverse Weekly is a dedicated ICHRA industry publication. No one else is doing this. We publish it, the ecosystem reads it, and HealthSherpa becomes the center of the conversation.",
        scrollTo: 0,
      },
      {
        title: "Issue Structure",
        body: "Each issue has 7 sections: Mike's Note, TL;DR, Deep Read, Market Signals, From the Fringe, Broker Toolkit, and One Question. Scroll through to see each one.",
        scrollTo: 200,
      },
      {
        title: "Content Sourcing",
        body: "Every week we scrape 15+ industry sources automatically — BenefitsPRO, Becker's, Healthcare Dive, Reddit, regulatory filings. Claude assembles the issue. Your time commitment: zero.",
        scrollTo: 400,
      },
      {
        title: "Visual Direction",
        body: "The look is HealthSherpa brand elevated into a tech editorial. Navy backgrounds, grid textures, the giant ICHRA/VERSE watermark. It should feel premium but familiar.",
        scrollTo: 0,
      },
      {
        title: "Next Steps",
        body: "If you approve, we launch within 2 weeks. Weekly cadence. First 4 issues with Josh reviewing before publish, then auto-publish. Social cards for LinkedIn and Instagram included with every issue.",
        scrollTo: 99999,  // scroll to bottom (social cards)
      },
    ];

    let currentStop = 0;
    const feedback = {};

    function renderStop(index) {
      const stop = STOPS[index];
      const card = document.getElementById('reviewCard');
      const existing = feedback[index];

      let statusHTML = '';
      if (existing) {
        if (existing.action === 'approve') statusHTML = '<span class="status status-approved">Approved</span>';
        else if (existing.action === 'flag') statusHTML = '<span class="status status-flagged">Flagged</span>';
        else if (existing.action === 'comment') statusHTML = '<span class="status status-commented">Has Comment</span>';
      }

      card.innerHTML = `
        <div class="step-indicator">Step ${index + 1} of ${STOPS.length}</div>
        ${statusHTML}
        <h2>${stop.title}</h2>
        <p>${stop.body}</p>
        <div class="actions">
          <button class="btn btn-approve" onclick="recordAction(${index}, 'approve')">Approve</button>
          <button class="btn btn-comment" onclick="toggleComment(${index})">Comment</button>
          <button class="btn btn-flag" onclick="recordAction(${index}, 'flag')">Flag</button>
          <button class="btn btn-peek" onclick="peekAtIssue()">View Issue ↓</button>
        </div>
        <textarea class="comment-box" id="commentBox" placeholder="What would you change?">${existing?.comment || ''}</textarea>
        ${index < STOPS.length - 1
          ? '<button class="btn btn-next" onclick="nextStop()">Next →</button>'
          : '<button class="btn btn-next" onclick="submitReview()">Submit Review</button>'
        }
      `;

      // Scroll the iframe
      try {
        document.getElementById('issueFrame').contentWindow.scrollTo({
          top: stop.scrollTo,
          behavior: 'smooth'
        });
      } catch (e) { /* cross-origin — fine */ }
    }

    function recordAction(index, action) {
      const comment = document.getElementById('commentBox')?.value || '';
      feedback[index] = { action, comment, stop: STOPS[index].title };
      renderStop(index);
    }

    function toggleComment(index) {
      const box = document.getElementById('commentBox');
      box.classList.toggle('visible');
      if (box.classList.contains('visible')) box.focus();
    }

    function peekAtIssue() {
      const overlay = document.getElementById('overlay');
      overlay.classList.add('hidden');
      // Click anywhere to return (no forced timer)
      function returnToOverlay() {
        overlay.classList.remove('hidden');
        document.removeEventListener('click', returnToOverlay);
      }
      // Small delay so the button click doesn't immediately trigger return
      setTimeout(() => document.addEventListener('click', returnToOverlay), 300);
    }

    function nextStop() {
      // Auto-save comment if present (merge with existing feedback)
      const box = document.getElementById('commentBox');
      if (box?.value) {
        const existing = feedback[currentStop] || {};
        feedback[currentStop] = {
          action: existing.action || 'comment',
          comment: box.value,
          stop: STOPS[currentStop].title,
        };
      }
      currentStop++;
      renderStop(currentStop);
    }

    function submitReview() {
      // Auto-save last stop
      const box = document.getElementById('commentBox');
      if (box?.value) {
        const existing = feedback[currentStop] || {};
        feedback[currentStop] = {
          action: existing.action || 'comment',
          comment: box.value,
          stop: STOPS[currentStop].title,
        };
      }

      // Format review summary
      const lines = ["ICHRAverse Weekly — Mike's Review", "=".repeat(40), ""];
      for (let i = 0; i < STOPS.length; i++) {
        const fb = feedback[i];
        const action = fb ? fb.action.toUpperCase() : 'SKIPPED';
        lines.push(`${i + 1}. ${STOPS[i].title}: ${action}`);
        if (fb?.comment) lines.push(`   Comment: ${fb.comment}`);
        lines.push("");
      }
      const summary = lines.join("\n");

      // Copy to clipboard
      navigator.clipboard.writeText(summary).then(() => {
        document.getElementById('reviewCard').innerHTML = `
          <h2>Review Submitted!</h2>
          <p>Your feedback has been copied to the clipboard. Josh will receive it.</p>
          <p style="margin-top:16px;font-size:13px;color:#9CA3AF;">You can close this tab or scroll through the issue below.</p>
          <button class="btn btn-peek" onclick="document.getElementById('overlay').classList.add('hidden')" style="margin-top:16px;">View the full issue →</button>
        `;
      });

      // Also save to localStorage
      localStorage.setItem('ichraverse_review', JSON.stringify(feedback));
    }

    // Init
    renderStop(0);
  </script>

</body>
</html>
```

- [ ] **Step 2: Test the overlay**

Open `content-hub/mike-review.html` in browser. Verify:
- Overlay appears on top of the issue
- All 5 stops render with correct titles and descriptions
- Approve/Comment/Flag buttons work and show status badges
- "View Issue" button hides overlay temporarily
- Submit copies feedback to clipboard
- Steps advance correctly

Note: The iframe will work when served via HTTP (e.g., `python -m http.server` in the `healthsherpa-ichra` directory). Won't work via `file://` due to cross-origin restrictions.

- [ ] **Step 3: Commit guided overlay**

```bash
git add content-hub/mike-review.html
git commit -m "feat(ichraverse): add Mike Levin guided review overlay"
```

---

## Railway Deployment Checklist

After all code is committed, deploy to Railway:

- [ ] Create Railway project "ichraverse-weekly"
- [ ] Connect GitHub repo, set root directory to `healthsherpa-ichra`
- [ ] Set Dockerfile path: `automation/Dockerfile`
- [ ] Add env vars: `ANTHROPIC_API_KEY`, `RESEND_API_KEY`, `NETLIFY_ACCESS_TOKEN`, `NETLIFY_FORM_ID`, `SITE_URL`, `GITHUB_TOKEN`, `GITHUB_REPO`
- [ ] Deploy and verify "ICHRAverse automation starting..." in logs
- [ ] Test: `python main.py --now` in Railway console
- [ ] Verify generated issue HTML at Netlify URL
- [ ] Send Mike the review URL: `{SITE_URL}/content-hub/mike-review.html`

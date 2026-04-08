# ICHRAverse Weekly — Publication Design Spec
**Date:** 2026-04-01
**Client:** HealthSherpa (ICHRA division)
**Project type:** Automated weekly ICHRA industry publication

---

## Problem

There is no dedicated trade publication for the ICHRA ecosystem. The market is growing at 52% CAGR, carriers are creating executive roles for it, states are passing tax incentives — and nobody is covering it as a beat. HealthSherpa wants to own this gap as a thought leadership play, positioning themselves as the authoritative voice in the ICHRA ecosystem rather than just another platform vendor.

## Positioning

**ICHRAverse is an industry publication, not HealthSherpa marketing.** It must feel like an independent editorial voice that happens to be published by HealthSherpa. Think Bloomberg Businessweek, not a company blog. The brand line: *"The pulse of the ICHRA ecosystem."*

## Audiences (priority order)
1. **Carriers** — sales VPs and product leaders (primary readers)
2. **ICHRA platforms** — competitors, partners, ecosystem players (secondary)
3. **Brokers** — benefits consultants and advisors (tertiary, but get their own section)

## Format: Web-First Publication

The publication is a **web page** — an online magazine issue, not an email newsletter. Email is a notification mechanism that drives traffic to the site. This avoids email deliverability issues (a known problem for HealthSherpa with carrier contacts) and allows richer formatting, social sharing, and SEO value.

Each issue lives at its own URL. The existing Content Hub page (`content-hub/index.html`) is replaced/rewritten as the publication landing page — issue archive + subscribe form.

## Frequency

**Weekly.** The ICHRA ecosystem generates 15-25 scrapeable content pieces per week across RSS feeds, blogs, press releases, regulatory filings, and social media — enough to sustain a weekly cadence without filler.

## Issue Structure (7 sections)

### 1. Editor's Note
**Purpose:** Brief editorial perspective. Sets the week's frame.
**Length:** 2-3 sentences.
**Source:** AI synthesis of the week's themes.
**Tone:** Opinionated, forward-looking. Not a summary — a perspective.

### 2. TL;DR — This Week in 30 Seconds
**Purpose:** 5 bullet points covering the week's most important ICHRA developments.
**Format:** One sentence per bullet + source link labeled "(link)".
**Source:** Automated scraping of Tier 1 sources (see Content Sources below).

### 3. The Deep Read
**Purpose:** One featured analysis piece per week. The anchor content.
**Length:** 3-4 paragraphs (~300 words).
**Format:** Hero card with gradient background + body text below.
**Source:** AI-written analysis based on the week's biggest story, using scraped source material.
**Tone:** Analytical, not sensational. "Here's what this means" framing.

### 4. Market Signals
**Purpose:** Quantitative snapshot of the ICHRA market.
**Format:** 4-stat grid (big numbers) + 3 bullet items (news bites with bold entity names).
**Source:** HRA Council reports, Oliver Wyman projections, state legislative trackers, funding announcements.
**Note:** Stats can be recurring/updated (e.g., enrollment growth) or new each week.

### 5. From the Fringe
**Purpose:** Surface unverified but interesting claims and conversations from Reddit, forums, social media.
**Format:** Amber/warning-styled section with explicit disclaimer: "None of this is confirmed."
**Tone:** "We flag it so you don't get blindsided." Useful, not alarmist.
**Source:** r/healthinsurance, r/insurance, Twitter/X, LinkedIn comments, niche forums.

### 6. Broker Toolkit
**Purpose:** One actionable resource for brokers each week.
**Format:** Single card with headline + 2-3 sentence description.
**Content types:** Talk tracks, objection handlers, case study stats, client conversation starters.
**Source:** AI-generated from scraped case studies and industry data.

### 7. One Question
**Purpose:** Provoke engagement and thought. Closes each issue.
**Format:** Single question, centered, on dark blue background.
**Examples:** "If ICHRA hits 5M covered lives by 2028, which carrier benefits most — and why?"

## Visual Direction

**Brand foundation:** HealthSherpa brand system — but with a tech editorial elevation.
- **Primary palette:** Navy `#074294`, blue `#0970C5`, white, with `#F8FAFC` section backgrounds
- **Accent:** Amber `#D97706` for From the Fringe section only
- **Typography:** Inter, weights 400-900. Heavy use of 800/900 for headlines.
- **Grid overlay:** Subtle CSS grid lines (`rgba(255,255,255,0.03)`) on dark sections for tech texture
- **Light blooms:** Radial gradient circles on dark sections for cinematic depth
- **Background:** Full page sits on `#074294` navy with giant "ICHRA/VERSE" watermark text (42vw, 0.12 opacity white)
- **Cards:** 12px border-radius, `1px solid #E2E8F0` borders, subtle hover states
- **Masthead:** Gradient blue header with "ICHRAverse by HealthSherpa" branding + issue number/date

**Social cards:** Each section produces a standalone square card (1:1 aspect ratio) for LinkedIn/Instagram sharing. Same brand, grid overlay, gradient backgrounds. These appear at the bottom of each issue as "Share This Issue." Generated as static HTML cards within the issue template (not images) — CSS handles the visual treatment. Screenshot-to-image can be added later if needed.

**Reference mockup:** `healthsherpa-ichra/.superpowers/brainstorm/65721-1775095623/visual-direction-v5.html`

## Content Sources (Automated Scraping)

### Tier 1 — Primary (RSS/HTML, reliable, weekly output)
| Source | Type | Access |
|--------|------|--------|
| BenefitsPRO | Trade pub | RSS |
| Becker's Payer Issues | Trade pub | RSS |
| Healthcare Dive | Trade pub | RSS |
| Remodel Health Blog | ICHRA platform | HTML scrape |
| Take Command Blog | ICHRA platform | HTML scrape |
| PeopleKeep Blog | ICHRA platform | HTML scrape |
| Thatch Blog | ICHRA platform | HTML scrape |
| Venteur Blog | ICHRA platform | HTML scrape |
| PR Newswire | Press releases | RSS (ICHRA keyword filter) |
| Federal Register | Regulatory | API |
| NABIP Podcast | Industry association | RSS |

### Tier 2 — Social & Community
| Source | Type | Access |
|--------|------|--------|
| r/healthinsurance | Reddit | API/scrape |
| r/insurance | Reddit | API/scrape |
| LinkedIn (Mike Levin) | Social | Manual/API |
| Twitter/X ICHRA hashtag | Social | API |

### Volume estimate
15-25 relevant pieces per week across all sources. More than enough for weekly cadence.

## Automation Pipeline

```
Weekly cron (Sunday night)
    │
    ├─ Scrape all Tier 1 sources (RSS + HTML)
    ├─ Scrape Tier 2 sources (Reddit, social)
    │
    ▼
Claude assembles issue:
    ├─ Score and rank scraped content by relevance
    ├─ Select top 5 stories → TL;DR bullets
    ├─ Select #1 story → Deep Read analysis
    ├─ Pull stats → Market Signals grid
    ├─ Flag unverified/fringe content → From the Fringe
    ├─ Generate broker talk track → Broker Toolkit
    ├─ Synthesize Mike's Note from week's themes
    ├─ Generate One Question
    ├─ Generate social card content
    │
    ▼
Build static HTML issue from template
    │
    ▼
Deploy to Netlify (new issue page + update archive)
    │
    ▼
Email notification to subscriber list via Resend
    ("New issue is live — read it here")
```

**Pipeline hosting:** Railway (Python service, same pattern as Recapper and Outreach Agent). Weekly cron trigger. Environment variables for API keys (Anthropic, Resend, Reddit).

**Human review gate:** Pipeline deploys each issue to a Netlify Deploy Preview (branch deploy). Josh gets a Slack/email notification with the preview URL. He clicks "approve" (merges the branch) to promote to production. Once confidence is established after ~4 weeks, can switch to auto-publish.

**Editorial voice:** The Editor's Note is AI-generated from the week's themes. No individual attribution needed — ICHRAverse speaks as a publication, not a person.

## Subscribe / Mailing List Strategy

- **Subscribe form** on Content Hub landing page (Netlify Forms, free tier) — captures email addresses
- **Subscriber export:** Pipeline reads subscribers via Netlify Forms API (`GET /api/v1/forms/{form_id}/submissions`) on each run
- **Email delivery:** Resend (free tier: 100 emails/day, more than sufficient). Sends a one-line notification + link to the new issue.
- **Email = notification only**, not the full issue. One line + link to web issue.
- **Landing page** serves as archive of all past issues + subscribe CTA
- **No email deliverability risk** — the publication lives on the web, email just pings subscribers

## Review Plan

ICHRAverse is broader than HealthSherpa — it's an independent industry publication. Share the v5 mockup and spec directly with stakeholders. No guided overlay needed; the prototype speaks for itself.

## Success Metrics

- **Launch:** First automated issue published within 2 weeks of approval
- **Cadence:** Unbroken weekly publication for 8+ weeks
- **Engagement:** Subscriber growth, social card shares, time on page
- **Positioning:** Mike can reference ICHRAverse in carrier conversations as proof of thought leadership

## File Structure

```
healthsherpa-ichra/
├── content-hub/
│   ├── index.html          # Landing page / archive (reimagined)
│   ├── issues/
│   │   └── issue-007.html  # Individual issue pages
│   └── assets/
│       └── social/         # Generated social cards
├── automation/
│   ├── scraper.py          # Source scraper (RSS + HTML)
│   ├── assembler.py        # Claude issue assembly
│   ├── builder.py          # HTML template builder
│   └── sources.json        # Source configuration
├── data/
│   ├── articles.json       # Scraped article archive
│   └── subscribers.json    # Netlify Forms export
└── templates/
    └── issue-template.html # Issue HTML template (from v5 mockup)
```

## Accuracy Standard

Inherited from the ICHRAverse suite spec: every statistic, regulatory claim, and market number must be sourced. When content is AI-generated, it's based on real scraped sources — not invented. Source attribution appears inline (TL;DR links) and in Market Signals cards.

## What This Is NOT

- Not a HealthSherpa product blog
- Not a sales email sequence
- Not content marketing disguised as journalism
- Not dependent on anyone's time to produce

It's an automated industry publication that makes HealthSherpa the center of the ICHRA conversation.

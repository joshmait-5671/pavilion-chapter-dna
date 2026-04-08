# ICHRAverse Engagement Suite — Design Spec
**Date:** 2026-03-31
**Client:** HealthSherpa (ICHRA division)
**Project type:** Multi-tool carrier engagement suite

---

## Problem

HealthSherpa ICHRA has a positioning and sales activation problem:
- Brand has trust baggage with some carriers (PMPM pricing history)
- No defined sales cycle — carrier journey is a wall of objections, not a funnel
- ICHRAx stealing "neutral infrastructure" narrative
- Carriers know HS as the healthcare.gov alternative, not ICHRA infrastructure
- Pipes get built but never activated — carriers sign, volume never flows
- No ICHRA-specific trade media exists — giant content leadership gap

## Strategic Frame

The carrier journey is **objection clearance**, not a funnel:
1. "Should we just build this ourselves?" (build vs. buy)
2. "Won't ICHRA cannibalize our group book?"
3. "The market feels too small"
4. "We don't know where to start"
5. "We'll just go direct to the top 1-2 platforms"

Every tool addresses one or more of these objections.

## Audiences (priority order)
1. **Carriers** — sales VPs and product leaders (primary)
2. **ICHRA Platforms** — largely done (40/43 connected), repurpose as social proof
3. **Brokers** — influencer channel, future phase

## Suite Overview

Six standalone projects, each deployable independently to Netlify, linked via master dashboard.

---

## Project 1: Master Dashboard
**File:** `index.html`
**Purpose:** Hub page linking all tools. Sets brand. First thing a rep shares with a carrier.
**Features:**
- HS-branded header with "ICHRAverse by HealthSherpa"
- 5 tool cards with description, status, and launch button
- Market momentum stats bar (adoption %, carriers connected, platforms live)
- Single CTA: "Talk to our ICHRA team"

---

## Project 2: ICHRA Adoption Map
**File:** `map/index.html`
**Purpose:** Destroy the "feels small" objection with live visual proof
**Features:**
- US choropleth map — states colored by ICHRA adoption intensity
- Per-state stats: employer count, covered lives, YoY growth
- Carrier layer: which carriers are active in each state
- Platform layer: which ICHRA platforms are operating
- Data structure pre-wired for live HS API hookup
- Mock data ships with the tool; swap to live with one config change
**Data files:** `data/states.json`, `data/carriers.json`, `data/platforms.json`
**Kills objection:** "Feels small" / "Market isn't ready"

---

## Project 3: Strategy Builder
**File:** `strategy-builder/index.html`
**Purpose:** Help carriers who "haven't baked their strategy" build one in 10 minutes
**Features:**
- 6-step wizard: market position → employer segments → product design → integration approach → broker strategy → timeline
- Each step has guided questions + multiple choice options
- Output: downloadable PDF "ICHRA Strategy Brief" personalized to their answers. Generated client-side using jsPDF + html2canvas (no backend required, consistent with Netlify-only deploy). PDF renders a styled summary of wizard answers.
- Shareable inside carrier org (internal sales tool)
- Completion CTA: "Want us to review your strategy?"
**Kills objection:** "We don't have a strategy yet" / "Don't know where to start"

---

## Project 4: ROI Calculator
**File:** `roi-calculator/index.html`
**Purpose:** Build the financial case for carrier investment
**Financial model inputs (with suggested defaults — replace with HS-provided actuals):**
- Current group book size (lives): default 50,000
- Estimated ICHRA-eligible segment (% of small group): default 15%
- PMPM rate (HS fee — HealthSherpa to confirm actual rate): default $2.50 PMPM (placeholder only, must be validated)
- Integration cost estimate: Build = $250K–$500K, Buy (HS) = TBD by HS sales team
- Time-to-revenue (months to activation): default 6 months
- Cannibalization offset — % of group members retained as individual market members: default 70%
- Note: All defaults labeled as illustrative. HS sales team must validate PMPM and integration cost figures before client use.
**Output:** 3-year revenue model, break-even point, net vs. direct integration cost
**Kills objection:** "We don't know the ROI" / "Cannibalization fear"

---

## Project 5: Build vs. Buy Guide
**File:** `build-vs-buy/index.html`
**Purpose:** Pre-empt DIY thinking before it kills the deal
**Format:** Scrollable content piece (not a wizard)
**Sections:**
- "Why AI doesn't solve the real problem" (CMS trust, regulatory complexity)
- The true cost of building (engineering time, maintenance, compliance debt)
- The 12-24 month window problem (ICHRA is at inflection NOW)
- HS vs. ICHRAx vs. direct integrations — honest comparison
- "Save yourself from yourself" framing (per client respondent language)
**Copy:** Developer generates authoritative placeholder copy for all 5 sections using the ICHRA Briefing Document (`ICHRA-Briefing-Document.md`) as the source of truth. HS reviews and edits before client use.
**Kills objection:** "We'll just build it" / "Why not go direct?"

---

## Project 6: ICHRA Content Hub
**File:** `content-hub/index.html`
**Purpose:** Own the media layer — position HS as authoritative ICHRA intelligence source
**Features:**
- Newsletter landing with subscribe form (wires to Netlify Forms, no backend required)
- "Latest ICHRA Intelligence" article feed (mock articles, JSON-driven, curated + original)
- Market data snapshots (powered by HS data)
- ICHRAverse branding: "The pulse of the ICHRA ecosystem"
- Separate from HS product marketing — editorial tone
**Subscribe form:** Netlify Forms (free tier, no backend). Form submissions go to HS team email.
**Mock article data:** `data/articles.json` — 6 placeholder articles with title, date, summary, tag, author.
**Kills objection:** "HS is just a healthcare.gov alternative, not an ICHRA authority" — establishes thought leadership credibility
**Long game:** Becomes the industry publication that doesn't exist yet

---

## Brand & Design System
*(sourced from healthsherpa.com and info.healthsherpa.com/ICHRA)*
- **Primary blue:** `#0970C5` / `rgba(0,112,240,1.0)`
- **Light blue:** `#2EB6FF` / `rgba(171,226,255,1.0)` (accents, inactive states)
- **Dark blue:** `#0D61A6` / `#074294` (hover states, deep accents)
- **Borders:** `#D3E0E8` / `#E5E7EB`
- **Body text:** `#344054` / `#475467`
- **Background:** White primary, subtle `rgba(246,244,242,0.2)` section accents
- **Font:** Helvetica/Inter, sans-serif. Weights 500/600/700 for hierarchy.
- **Buttons:** Rounded (90px border-radius), blue bg, hover darkens. Copy: conversational ("Let's talk", not "Submit")
- **Cards:** 12px border-radius, 24px padding, `1px solid #D3E0E8`
- **Section spacing:** 40–80px between major sections
- **Tone:** Professional but approachable. Problem-solution. Credibility-first. NOT salesy.
- **Name:** "ICHRAverse" as suite brand, "by HealthSherpa" as attribution
- **Shared CSS/components:** `shared/styles.css`, `shared/header.js` (vanilla JS component, injected via script tag)
- **Tool card status convention:** Blue pill = "Live" · Gray pill = "Coming Soon" · Yellow pill = "Beta"

## Accuracy Standard
Healthcare executives will fact-check. Every statistic, financial figure, regulatory claim, and market number must be sourced and accurate. No rounded estimates presented as facts. No invented PMPM figures. All data tied to a named source (HRA Council, Oliver Wyman, CMS, HealthSherpa internal). When data is mock/placeholder, label it clearly as "sample data — replace with live HS data."

## Landing Pages & Marketing Campaigns
Each of the 6 tools gets:
- **Its own landing page** — what it is, the problem it solves, how it works, CTA
- **Its own marketing campaign** — designed individually, not bundled
- Campaign assets TBD per tool (email, LinkedIn, carrier outreach sequence, broker outreach)
- Landing pages built as separate HTML files within each tool's folder: `map/landing.html`, `strategy-builder/landing.html`, etc.

## Deployment Model
**Single Netlify site** — the entire `/healthsherpa-ichra/` directory deploys as one site. This means:
- Shared CSS works via relative paths (`../shared/styles.css`)
- All internal tool links work via relative paths (`../map/index.html`)
- One deploy command, one root URL (e.g., `ichraverse-hub.netlify.app`)
- Individual tools are URL paths: `/map/`, `/strategy-builder/`, etc.
- A rep shares either the dashboard URL or a direct tool URL depending on context

## ICHRAx Context (for Build vs. Buy content)
ICHRAx is a competitor positioning itself as "neutral ground" — a non-profit-like standards body for ICHRA connectivity. Led by Kyle Estep (ex-SVP Strategy at Take Command). Claims: "Connect once, access every participating carrier/administrator." Uses an Advisory Board model where participants have a vote — explicitly designed to appeal to carriers wary of depending on a single commercial vendor like HealthSherpa. It is purpose-built for ICHRA (vs. HS which started as ACA exchange infrastructure). The counter-argument: HealthSherpa has real scale (50%+ of Federal Marketplace enrollments), real CMS trust, and 40+ live platform connections today. ICHRAx has credibility but no comparable enrollment infrastructure.

## Folder Structure
```
/healthsherpa-ichra/
  index.html                    ← Master dashboard
  map/
    index.html                  ← ICHRA Adoption Map
    landing.html                ← Map landing page
  strategy-builder/
    index.html                  ← Strategy Builder tool
    landing.html                ← Strategy Builder landing page
  roi-calculator/
    index.html                  ← ROI Calculator
    landing.html                ← ROI Calculator landing page
  build-vs-buy/
    index.html                  ← Build vs. Buy Guide
    landing.html                ← Build vs. Buy landing page
  content-hub/
    index.html                  ← Content Hub
    landing.html                ← Content Hub landing page
  shared/
    styles.css                  ← Shared design system (referenced as ../shared/styles.css)
    header.js                   ← Shared header component (vanilla JS, injected via script tag)
  data/
    states.json                 ← State adoption mock data (map)
    carriers.json               ← Carrier mock data
    platforms.json              ← Platform network mock data
```

## Deployment
- Each tool deploys independently to Netlify
- Master dashboard links to all tools via absolute URLs
- Mock data ships with each tool; live HS data requires API key config

## Success Criteria
- A sales rep can pull up any tool on a call and walk a carrier through it in under 5 minutes
- The map alone destroys the "feels small" objection
- The strategy builder output is good enough that a carrier VP shares it internally
- The suite as a whole positions HS as the authoritative ICHRA infrastructure layer


# AI Buddy Program — Operational Design & Waitlist Page

## Overview

The AI Buddy Program matches Pavilion members (and eventually prospects) with peers to share AI knowledge and serve as thinking partners. This spec covers the matching system redesign, automated lifecycle management, and a standalone waitlist page that collects matching data upfront.

## Program Design

### Matching Criteria (Priority Order)

1. **Function** (required, non-negotiable) — Sales, Marketing, CS, RevOps, Finance, HR & People, Operations, Product, Founder, Other
2. **Company revenue stage** (required, non-negotiable) — <$10M, $10-25M, $25-50M, $50M+
3. **Location** — Same city ideal, same timezone fallback
4. **Engagement style** — How they want to interact with their buddy
5. **AI experience level** — Matched as peers (same level preferred, adjacent acceptable)

### Matching Tiers (Fallback Logic)

When a new person enters the pool, the system scans for the best available match over 5 business days:

| Day | Tier | Criteria |
|-----|------|----------|
| Day 1 | Tier 1 — Perfect | Function + revenue + city + engagement style + AI level |
| Day 2 | Tier 2 — Strong | Function + revenue + timezone + engagement style + AI level |
| Day 3 | Tier 3 — Good | Function + revenue + timezone + adjacent AI level |
| Day 5 | Tier 4 — Acceptable | Function + revenue + any timezone |
| Day 5+ | No match | "We're finding the right person" email. Re-scan triggers each time someone new enters the pool. |

**Function and revenue stage are always required.** Everything else degrades gracefully.

### Buddy Lifecycle

Matches are rolling — no fixed cohorts. The 8-week clock starts when the match is made.

| Touchpoint | Timing | Action | Automated? |
|------------|--------|--------|------------|
| Intro email | Day 0 | Claude writes personalized intro, sends from Josh's Gmail, cc's both | Yes |
| Connection check | Week 1 | "Did you connect with your buddy?" (Yes/No/Need help) | Yes |
| Pulse check | Week 4 | "How's it going?" (1-5 rating + optional notes) | Yes |
| Decision point | Week 8 | "Want to keep your buddy, get a new one, or add a second?" | Yes |
| Long-term pulse | Quarterly | For pairs that stayed together — light check-in | Yes |

**Options at Week 8:**
- **Keep** → System stops check-ins, shifts to quarterly pulse
- **New buddy** → Person re-enters pool, gets matched within 5 business days
- **Add a buddy** → Person stays with current buddy AND enters pool for an additional match (can accumulate multiple buddies over time)

### Human-in-the-Loop

- **First 2-3 months:** Josh reviews all matches before intro emails send (same approval workflow as current system)
- **After confidence is built:** Flip to fully automated — matches send without approval
- **Edge cases always route to human:** complaints, requests to unmatch, weird situations

### Automated Emails

All emails sent from josh.mait@joinpavilion.com via existing Gmail integration. Claude writes personalized content for:

1. **Intro email** — warm, personal, explains why they were matched, suggests first step based on their shared engagement style preference
2. **Week 1 check-in** — short, friendly, just confirming they connected
3. **Week 4 pulse** — brief survey (1-5 rating, open text, "anything we can do better?")
4. **Week 8 decision** — presents three options (keep/new/add), links to simple form
5. **No match yet** — sets expectations, confirms they're in the pool, re-assures quality > speed
6. **Waitlist → launch** — "You're in the first batch" email when we hit 100 signups

## Waitlist Page

### Purpose

Collect signups with full matching data upfront so we have a pre-built pool ready for instant matches on launch day. Launch trigger: 100 signups.

### Fields to Collect

| Field | Type | Required | Why |
|-------|------|----------|-----|
| First name | Text | Yes | Personalization |
| Last name | Text | Yes | Personalization |
| Work email | Email | Yes | Communication |
| Function | Dropdown | Yes | Matching (required) |
| Company name | Text | Yes | Context |
| Company revenue | Dropdown | Yes | Matching (required) |
| City | Text | Yes | Matching (location) |
| Timezone | Dropdown | Yes | Matching (fallback) |
| AI experience level | Radio | Yes | Matching (peer level) |
| How do you want to engage with your buddy? | Multi-select | Yes | Matching (engagement style) |
| Pavilion member? | Yes/No | Yes | Segmentation |
| Anything specific you want help with? | Text | No | Matching context + intro email fodder |

### AI Experience Levels
- Just getting started — curious but haven't done much yet
- Using it regularly — have tools in my workflow
- Building with it — creating custom solutions, automating processes

### Engagement Style Options (multi-select)
- Quick async check-ins (Slack, text)
- Bi-weekly video call
- Weekly video call
- Share resources and articles
- Accountability partner — hold each other to goals

### Page Design Direction

**Visual identity: "Tech platform" not "professional community."**

This page should push Pavilion's visual language forward. Less corporate brochure, more modern product. Think:
- Cleaner, more minimal than current Pavilion pages
- Subtle tech/product cues — monospace accents, cleaner grid, maybe a dark mode option
- Still Pavilion brand colors but used more sparingly
- The form should feel like signing up for a product, not filling out a lead gen form
- Animated counter showing live signup count (builds social proof and urgency toward the 100 threshold)

**Page structure:**
1. Hero — headline, one line of copy, CTA to scroll to form
2. How it works — 3 steps, ultra simple
3. What we match on — show the criteria so people know this is thoughtful, not random
4. The form — all matching fields, clean and fast
5. FAQ — 3-4 questions (How long? Who are the buddies? Is it free? When does it launch?)

**Headline options:**
- "Find your AI thinking partner."
- "Better together." (simple, clean)
- "Stop figuring out AI alone. Get matched with a peer who gets it."

### Data Storage

- **Phase 1 (now):** Google Sheet — Waitlist tab added to existing AI Buddy Program sheet
- **Phase 2 (200+ people):** Migrate to Airtable or database
- **Future:** Pull member data from Salesforce to pre-fill fields

### Launch Sequence

1. Waitlist page goes live → link from AI GTM Bundle page
2. Promote through Pavilion channels (Slack, email, etc.)
3. Monitor signup count
4. At 100 signups → run matching algorithm across entire pool
5. Launch day → first batch of matches all go out same day
6. From that point → rolling intake, 5-day matching window

## Technical Architecture

### Current System (keep and extend)
- Python scripts in `/Users/joshmait/Desktop/Claude/outreach-agent/`
- Google Sheets API for data
- Gmail API for sending (via josh.mait@joinpavilion.com)
- Claude API for writing personalized emails
- Campaign config in `campaigns/ai_buddy_program.yaml`

### What Needs to Be Built/Updated
1. **Waitlist page** — standalone HTML, deployed to Netlify
2. **Form → Sheet integration** — form submissions write to Google Sheet (Apps Script or similar)
3. **Updated matching algorithm** — new scoring with revenue stage, timezone, engagement style
4. **Tiered matching with daily scan** — cron job or scheduled task that scans pool daily
5. **Automated lifecycle emails** — Week 1, 4, 8 check-ins triggered by match date
6. **Feedback collection** — simple forms for Week 1/4/8 responses, write back to Sheet
7. **Re-entry logic** — "want a new buddy" response puts person back in pool

### Matching Scoring (Updated)

| Criterion | Points | Notes |
|-----------|--------|-------|
| Same function (required) | 40 | No match without this |
| Same revenue stage (required) | 30 | No match without this |
| Same city | 20 | |
| Same timezone (if not same city) | 10 | |
| Same engagement style (any overlap) | 15 | Multi-select, any shared preference counts |
| Same AI experience level | 15 | |
| Adjacent AI experience level | 5 | One level apart |
| Member + non-member mix | 5 | Nice to have, not required |

Minimum viable match: Function (40) + Revenue (30) = 70 points (Tier 4)

## Open Items

- [ ] Google Sheet — add Waitlist tab or create new sheet?
- [ ] Confirm existing sheet ID still works: `1nXqkzcW2HMA04jS4zjfB2Y7DT0RTjUdtVZY4XM1WFoY`
- [ ] Salesforce fields available for members (future integration)
- [ ] Waitlist page Calendly or contact link for questions
- [ ] Promotion plan — how/where to announce the waitlist
- [ ] Legal/privacy — do we need a consent checkbox for email communications?

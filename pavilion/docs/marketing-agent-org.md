# Pavilion Marketing + Membership
## Last updated: 2026-04-08

---

## The Humans

- **Josh Mait** — Creative direction, brand, strategy, builds things
- **Kyler** — Execution workhorse, AI-fluent, field intel from member conversations
- **Laura** — Design, UX, digital, analytics, website ownership
- **Melanie** — Events, chapter dinners, sponsorships, IRL
- **TBD (Melanie's Hire)** — Events support. Coordinates logistics, sponsor deliverables, chapter dinner ops. Melanie drives strategy and relationships, this person runs the machine.
- **TBD (New Hire)** — Member Experience. Owns classes, Slack engagement, content programming, and whether the product is landing. The bridge between what we build and whether members feel it.

---

## The Agents

### 1. SYDNEY — MEMBER PROMOTION
**Humans:** Kyler (field intel) + Josh (picks)
**Agent role:** Scout + packager

Kyler submits members worth spotlighting via simple intake (name + why they're interesting right now). Agent cross-references with engagement data, chapter activity, event participation, LinkedIn activity, and content contributions. Surfaces 5 names/week with a one-paragraph case for each. Josh picks. Agent drafts the asset (profile, feature, quote pull, whatever format Josh decides).

- **Input:** Kyler nominations, membership engagement data
- **Output:** Weekly shortlist + draft assets on approval
- **Trigger:** Scheduled weekly
- **Autonomy:** Agent scouts and enriches. Josh picks.

```
KYLER (nominates) --> AGENT (validates + enriches + ranks) --> JOSH (picks + greenlights)
```

---

### 2. DON — CM1 / THE BUILD ENGINE
**Human:** Josh
**Agent role:** Creative interrogator + production multiplier

Two phases:

**Phase 1: Intake.** A deep conversational flow — one question at a time — built for how Josh thinks. 40 questions deep, adaptive. Not "what's the headline" but:
- Who is this for and what are they afraid of right now?
- What do they believe that's wrong?
- What's the one thing we want them to do after this?
- What existing thing in culture does this feel like?
- What would make you embarrassed to ship this?
- What would make the competitor's version of this?
- What's the emotional state before vs. after?
- What does the world look like if this works?
- What's off-limits tonally?
- What format(s) does this need to live in?
Skips irrelevant questions based on earlier answers. By the end, produces a creative brief richer than any human strategist would write.

**Phase 2: Build.** Takes the brief and builds multi-format assets. One brief becomes: email, landing page, LinkedIn post, ad copy, one-pager, deck slide. Josh reviews and ships.

- **Input:** Josh's brain via intake flow
- **Output:** Creative brief + multi-format assets
- **Trigger:** Josh starts a new campaign
- **Autonomy:** Agent builds. Josh approves.

---

### 3. SUSIE — CM2 / DEPLOYMENT + MONITORING
**Human:** Kyler
**Agent role:** Scheduler + watchdog + optimizer

Deploys assets on the calendar. Monitors performance against defined thresholds (open rate, CTR, unsubscribe spikes, conversion). Makes small optimizations autonomously: send time shifts, subject line variants, audience segment tweaks. Surfaces alerts with recommended actions — not just "this is low" but "this subject line underperformed the last 3 by 40%, here are 3 alternatives." Kyler gets a daily digest. Steps in for new campaigns or strategic shifts.

- **Input:** Assets from CM1, channel calendar, performance thresholds
- **Output:** Deployed campaigns, daily digest, threshold alerts with recommendations, autonomous small optimizations
- **Trigger:** Scheduled deploys + threshold breaches
- **Autonomy:** Routine deploys and small optimizations are autonomous. New campaigns and strategic shifts go through Kyler.

---

### 4. CONDOR — MARKET INTELLIGENCE
**Human:** None. Fully autonomous.
**Agent role:** Scanner + filter

3 sources: Reddit, LinkedIn/industry, competitor sites.
2 lenses: What's moving in AI+GTM. What members are talking about.
1 output: Weekly brief, max 1 page, 3 "consider this" prompts ranked by urgency.

Not a firehose. A filter. Goes to Josh and Kyler. They forward what matters.

- **Input:** Defined source list + keyword watchlist
- **Output:** Weekly brief (1 page, 3 ranked prompts)
- **Trigger:** Scheduled Monday morning
- **Autonomy:** Fully autonomous. No human in the loop.

---

### 5. FLASH — WEBSITE MANAGER
**Human:** Laura
**Agent role:** Optimizer + implementer

Pulls analytics weekly. Identifies worst-performing pages by bounce/conversion. Makes copy and CTA changes autonomously on low-traffic pages, runs tests, reports results. Laura gets a daily changelog. High-traffic pages (homepage, pricing) require Laura's approval. Everything else: ship and measure.

Also receives signals from Susie (campaign landing pages needed) and Performance Oversight (strategic pivots).

- **Input:** Analytics data, requests from CM2 and Performance Oversight
- **Output:** Weekly optimization report, autonomous changes on low-traffic pages, change requests for high-traffic pages
- **Trigger:** Weekly analytics pull + inbound requests
- **Autonomy:** Autonomous on low-traffic pages. Laura approves high-traffic changes.

---

### 6. GONZO — PERFORMANCE OVERSIGHT
**Human:** Laura (tactical) + Josh (strategic)
**Agent role:** Dashboard + alarm system + tactical coordinator

The layer above CM2, Website Manager, and Market Intelligence. Ingests data from all of them and synthesizes into one view. Acts on tactical issues autonomously: sees email open rates dropping, tells Susie to test new subject lines, tells Website Manager to swap a CTA, logs every decision. Laura reviews the log and overrides when the agent gets it wrong. Agent learns from overrides.

Josh gets strategic flags: "Pipeline is 15% behind target and email open rates dropped 3 consecutive weeks — recommend shifting budget to LinkedIn."

- **Input:** All other agent outputs + pipeline/revenue data
- **Output:** Weekly scorecard, real-time alerts, autonomous tactical adjustments
- **Trigger:** Weekly synthesis + real-time on critical thresholds
- **Autonomy:** Tactical adjustments autonomous. Strategic shifts flagged to Josh.

---

### 7. NANCY — SALES + SUCCESS ENABLEMENT
**Human:** Kyler
**Agent role:** Builder + feedback processor

Builds and updates: competitive one-pagers, ROI calculators, talk tracks, objection handling docs, case study drafts. Two inputs:

1. Win/loss data and rep feedback (structured intake form — "I lost because they asked about X and I had nothing")
2. Market Intel's weekly brief for competitive shifts

When feedback maps to an existing asset, agent updates and pushes live. Kyler gets notified. Net-new assets go through Kyler.

- **Input:** Rep feedback form, Market Intel brief, win/loss data
- **Output:** Updated enablement assets, monthly gap analysis
- **Trigger:** New feedback submitted + monthly review cycle
- **Autonomy:** Updates to existing assets autonomous. New assets through Kyler.

---

### 8. CHARLIE — INSTAGRAM GOLD
**Human:** Josh (direction) + Emily R + Sam J (input)
**Agent role:** Calendar + content production

Maintains a 2-week rolling content calendar. Emily and Sam submit real-world moments (events, dinners, behind-the-scenes) via simple intake: photo + 1 sentence context. Agent drafts: caption, hashtags, posting time, story vs. feed recommendation. Josh approves the weekly queue in one batch. Agent posts on schedule.

Curated lifestyle magazine feel. Not a content mill — a point of view.

- **Input:** Photo + context submissions, Josh's editorial direction
- **Output:** Drafted posts for weekly approval, scheduled publishing
- **Trigger:** New submissions + weekly approval cycle
- **Autonomy:** Human-approved. Josh greenlights the weekly queue. Agent handles everything else.

---

### 9. MELANIE — IRL ENGINE
**Human:** Melanie
**Agent role:** Event ops + sponsor tracker

Owns events, chapter dinners, sponsorships, and all IRL programming. Agent handles: event logistics tracking, sponsor deliverable checklists (co-marketing obligations, partner landing pages, content commitments), chapter dinner coordination, post-event follow-up sequences. Melanie drives strategy and relationships. Agent keeps the operational plates spinning.

- **Input:** Event calendar, sponsor contracts, chapter leader requests
- **Output:** Logistics timelines, sponsor deliverable tracking, post-event follow-up triggers
- **Trigger:** Event milestones + sponsor contract dates
- **Autonomy:** Logistics and tracking autonomous. New sponsorship commitments through Melanie.

---

### 10. HARRIET — MEMBER HEALTH + RETENTION
**Human:** Laura
**Agent role:** Churn radar + engagement watchdog

Watches the back door. Monitors: login frequency, event attendance decay, Slack activity drops, renewal dates approaching, downgrades, NPS signals. Flags at-risk members before they churn — not after. Feeds signals to Sales Enablement (save plays), Performance Oversight (trend data), and Member Promotion (re-engage candidates).

- **Input:** Membership platform data, Slack activity, event attendance, NPS, renewal dates
- **Output:** Weekly at-risk member list, churn trend report, re-engagement recommendations
- **Trigger:** Engagement decay thresholds + 60/30 days before renewal
- **Autonomy:** Fully autonomous monitoring. Re-engagement outreach flagged for human approval.

---

### 11. MEMBERSHIP EXPERIENCE (Agent TBD)
**Human:** New Hire (TBD)
**Agent role:** Program amplifier + engagement curator

Owns the internal member experience of classes, Slack, events, and content programming. Ensures what Pavilion builds actually reaches the members who are paying for it. Pulls from existing agents:

- Susie deploys internal member comms (not just acquisition)
- Harriet provides engagement data on what's landing and what's dead
- Condor surfaces what members are asking for in Slack
- Charlie promotes standout moments on Instagram
- Sydney spots members who crushed a class or event

The agent curates a rolling "what's happening at Pavilion" feed, flags underperforming programs, and coordinates internal promotion so no great class dies in silence.

- **Input:** Class calendar, Slack activity, event attendance, Harriet's engagement data, Condor's community signals
- **Output:** Internal promotion calendar, program health dashboard, "what's happening" member comms, underperforming program alerts
- **Trigger:** New program launch + weekly engagement review
- **Autonomy:** Internal comms autonomous. New program positioning through TBD hire.

---

## Autonomy Spectrum

### Fully Autonomous (do it, report what you did)
- Condor — Market Intelligence
- Flash — Website Manager (low-traffic pages)
- Gonzo — Performance Oversight (tactical adjustments)
- Susie — CM2 (routine deploys + small optimizations)
- Nancy — Sales Enablement (updates to existing assets)
- Melanie — IRL Engine (logistics tracking + sponsor deliverables)
- Harriet — Member Health (monitoring + at-risk flagging)

### Human Approves (draft it, I'll greenlight)
- Flash — Website Manager (high-traffic pages)
- Charlie — Instagram Gold (weekly queue)
- Nancy — Sales Enablement (net-new assets)
- Melanie — IRL Engine (new sponsorship commitments)
- Harriet — Member Health (re-engagement outreach)

### Human Drives (I set the direction, you build)
- Don — CM1 (Josh's intake → agent builds)
- Sydney — Member Promotion (Kyler nominates, agent enriches, Josh picks)

---

## Hierarchy

```
JOSH (brand, creative, strategy)
  |-- Don (builds what Josh briefs)
  |-- Sydney (Kyler nominates, Don enriches, Josh picks)
  |-- Charlie (Josh approves weekly queue)
  |-- Gonzo (strategic flags to Josh)

KYLER (execution, deployment, enablement, field intel)
  |-- Susie (Kyler owns channels)
  |-- Nancy (Kyler owns tools)
  |-- Sydney (Kyler is the nomination source)

LAURA (website, analytics, UX, retention)
  |-- Flash (Laura reviews changelog)
  |-- Gonzo (Laura reviews tactical log)
  |-- Harriet (Laura reviews at-risk list + approves outreach)

MELANIE (events, sponsorships, IRL programming)
  |-- Melanie agent (Melanie owns strategy, agent tracks logistics)

TBD HIRE (member experience, classes, Slack, programming)
  |-- Member Experience agent (program amplification + engagement curation)
  |-- Harriet (engagement data feeds into program health)

AUTONOMOUS
  |-- Condor (feeds everyone, no human owner)
```

---

## Blindspots + Known Gaps

- **Email as a priority lane:** Email gets its own explicit priority lane under CM2/Susie — not lumped in with "routine deploys." Highest-volume channel, highest-stakes when it breaks.
- **Market Intelligence internal scanning:** Market Intel now includes internal Slack/community scanning — not just external Reddit/LinkedIn/competitor sources. Member conversations are signal.
- **Content library / asset management:** Known gap. As production scales across CM1, Sales Enablement, Instagram, and IRL Engine, there's no centralized content library or asset management layer. Needs solving before the volume outgrows tribal knowledge of where things live.

# New Member Onboarding Wizard — Design Spec
**Date:** 2026-04-09
**Status:** Approved for implementation
**Replaces:** joinpavilion.com/new-member-onboarding (current static page)

---

## What We're Building

A mobile-first, B2C-quality onboarding wizard for new Pavilion members. 15 numbered steps + 1 video interlude = 16 total screens. One question per screen. ~4 minutes start to finish. The experience culminates in a personalized reveal — your channels, your upcoming event, your intro — built from the answers they just gave.

The thesis: the brand is the experience. This wizard is the first real thing a new member does inside Pavilion. It should feel premium, warm, and smart — not like a form.

---

## Visual Design

**Direction:** B Refined — Pavilion's light palette, adapted for a focused wizard context.

**Font:** Poppins exclusively. Headlines 800, body 300–400, labels 600.

**Color palette (Pavilion brand):**
- `--blue-100: #EDEAFF` — top band background per step, selected card state
- `--navy-dk: #180A5C` — headlines
- `--navy: #2B1887` — accents, checked state, progress fill
- `--pink: #DF285B` — primary CTA (pill, `border-radius: 100px`), step category eyebrow
- `--white: #ffffff` — screen body, card default state

**Per-step layout:**
- Top band (blue-100): progress segments + category eyebrow (pink, 9px/700/0.22em tracking) + headline (Poppins 800, ~24px, navy-dk, -0.02em tracking)
- White body: brief instruction note (Poppins 300, 11px, slate) + interaction area + pink pill CTA + "Skip for now" ghost text

**Progress indicator:** Row of equal-width segments at top of every screen. Done = `--navy`. Active = `--pink`. Future = `rgba(43,24,135,0.12)`. 2px height.

**Selection state (channels, events, options):** Unselected = blue-100 bg, transparent border. Selected = white bg, 1.5px navy border.

**CTA button:** Always pink, always pill-shaped (`border-radius: 100px`), Poppins 700, full-width.

---

## The 15-Step Arc

| # | Step | Section | Interaction |
|---|------|---------|-------------|
| 1 | Welcome, [Name] | — | Celebration screen. Avatar stack showing nearby members. No question. "Let's set you up →" |
| 2 | Slack channels | Your Community | Multi-select list. Curated by role/function. Pick 3–5. |
| 3 | Email preferences | Your Community | Multi-select toggle. Weekly digest / event alerts / member spotlights. |
| 4 | Can we text you? | Your Community | Phone number input + opt-in checkbox. Context: "Intros, event reminders, someone asked about you." |
| 5 | Events near you | Your Calendar | 3 real upcoming events in their city. RSVP or "Save for later." |
| 6 | Do you travel frequently to another city? | Your Calendar | City input. Optional. "We'll show you events there too." |
| 7 | Classes on your radar | Your Calendar | Multi-select from upcoming classes. "Enroll now" or "Remind me in X days." |
| 8 | People near you | Meet Someone | Show 8 members in their city. Select 1–2 to be introduced to. |
| —* | **Video interlude** | — | iPhone-camera member story. Autoplay muted. 20–40 sec. Skip option. Does not count toward the 15 numbered steps. |
| 9 | Where would you like us to promote your insights and ideas? | Your Voice | Multi-select: LinkedIn, Slack, newsletter, podcast. Or "not at all." |
| 10 | Benchmarks you care about | Your Data | Multi-select: team size, GTM data, hiring plans. |
| 11 | Are you looking for expertise around your comp package? | Your Data | Yes / No / Tell me more. Routes to exec comp resources if yes. |
| 12 | One thing the community should know | The Human Part | Open text. Short. |
| 13 | 12 months from now, what does success look like? | The Human Part | Open text. Their commitment. |
| 14 | Favorite song right now | The Human Part | Open text. "We're building a Pavilion Spotify playlist." |
| 15 | Your Pavilion | The Reveal | Personalized summary: channels added, event saved, intro coming, benchmark report queued. Dark navy. |

---

## Video Interlude

**Placement:** Between Step 8 (People near you) and Step 9 (Your Voice). Right before asking for contribution, a real human voice earns it.

**Format:** iPhone vertical, no production. 20–40 seconds. 3–5 members rotating on each new session load.

**Player behavior:** Autoplays on screen entry, muted by default. Tap to unmute. "Skip" in top right appears after 5 seconds.

**Content script structure:** "Before Pavilion, I was [struggling with X]. In the first [timeframe], [specific thing happened]. Now [outcome]."

**V1 stub:** Until real videos exist, show a branded placeholder card (dark navy, play icon, member name + title, duration badge). Visually indistinguishable from the real thing — just not playable yet.

---

## Data Capture

**Backend:** Google Apps Script → Google Sheet (same pipeline as AI Buddy Program). One row per member. Column per step answer. Sheet: "Pavilion Onboarding Responses."

**Trigger:** Each step submits on CTA tap. Progressive save — partial completion is useful data.

**Sheet columns:** timestamp, member_name, member_email (pre-populated from URL param or session), city, slack_channels[], email_prefs[], sms_opt_in, phone, events_rsvp[], travel_city, classes[], intro_requests[], promote_channels[], benchmarks[], comp_interest, one_thing, commitment, favorite_song.

**Pre-population:** URL params (`?name=Sarah&email=sarah@company.com&city=San+Francisco`) passed from HubSpot onboarding email. No login required for V1.

**Missing param fallback:** If name/email/city params are absent or malformed, the wizard degrades gracefully: Step 1 shows "Welcome!" without a name, Steps 5/8 skip city-specific content and show generic upcoming events/members instead, and the email field on data capture is left blank. The wizard never breaks — it just personalizes less.

**No auth required for V1** — link-based access. Each new member gets a personalized URL from HubSpot.

---

## Technical Architecture

**Type:** Single-page application (static HTML/CSS/JS). No framework. Deployed to Netlify.

**Navigation:** Back navigation is supported — tapping back shows the previous step without losing any data. Steps stored in JS object, submitted progressively on each CTA tap.

**State management:** JS object in memory. LocalStorage backup so refresh doesn't lose progress.

**Step rendering:** Single `<div id="step-container">` swapped on each advance. CSS transitions between steps (slide left, ~200ms ease-out).

**Mobile-first:** Max-width 420px centered. Feels like a native app on phone, looks clean on desktop.

**Animations:** Step transitions: slide out left, slide in right. Celebration on Step 1: confetti burst (canvas, 1.5s). Selection tap: immediate border + background update (no delay). CTA on Step 15: subtle scale pulse.

---

## The Reveal Screen (Step 15)

Dark navy background (`--navy-xdk: #080122`). White Poppins 800 headline: "Your Pavilion is ready."

Personalized summary cards (dark glass, rgba white 5%):
- Channels added (count + names)
- Event saved (specific event name + date)
- Intro incoming: if member selected names in Step 8, show "Expect a message this week from [selected name]." If Step 8 was skipped or no match is available, show fallback: "We're working on your first intro. Expect a message within the week."
- Benchmark report queued (if selected)
- Comp resources sent (if opted in)

CTA: "Go to Slack →" (pink pill). No secondary action in V1 — "Download your summary" is out of scope.

---

## What This Replaces / Doesn't Replace

**Replaces:** The current static page at joinpavilion.com/new-member-onboarding. New URL: Netlify deploy, linked from HubSpot welcome email.

**Does not replace** (V1): Actual Slack channel enrollment (captured, actioned manually or via Zapier). Actual intro facilitation (flagged in sheet, done by team). Actual event RSVPs (captured, confirmed separately).

**V2 scope (not now):** Direct Slack API enrollment, HubSpot contact update, real event RSVP confirmation, intro automation via AI Buddy engine.

---

## Success Criteria

- Completion rate target: >65% (industry B2C average: 40–60%)
- Time to complete: ≤4 minutes
- Step abandonment visible in sheet (partial rows = drop-off data)
- Qualitative: new members feel welcomed, not processed

---

## Open Questions (Non-blocking for V1)

1. Who sends the personalized URL — HubSpot automation or manual? (Assume manual V1)
2. Real member videos — who records, who edits, timeline? (V1 = placeholder card)
3. "Intro incoming" on Step 15 — generated from Step 8 selections or always generic? (V1 = generic if no AI Buddy match available)
4. Sheet owner / Zapier hookup to existing Pavilion ops tools — coordinate with ops team post-launch.

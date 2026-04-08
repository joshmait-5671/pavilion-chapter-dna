# Coinfully Homepage — Design Spec
**Date:** 2026-03-29
**Project:** 100 YARDS / Coinfully
**Approach:** C — Hybrid (Story-First + Persona Split + Guided AI Moment)
**Status:** Approved for implementation

---

## Project Brief

Rebuild the Coinfully homepage to flip from company-centric to customer-centric. Warm, emotional, human. Modern but not corporate. Authentic brand that serves real people. Conservative-leaning audience.

**Two primary personas:**
- Inheritors (lead — emotional, uncertain, need guidance)
- Investors (secondary — more informed, care about maximizing value)

**Two secondary:**
- Estate/legal channel (small CTA)
- Catch-all

**Two products:**
- Mail-in appraisal (volume, entry point — accessible, leads everywhere)
- At-home visit (premium — surfaces mid-journey as the upgrade)

---

## Visual Identity

Retain Coinfully brand with modernization:
- **Colors:** Black, yellow/gold (#F5C342), white, warm cream (#FAFAF5)
- **Logo:** Existing COINFULLY wordmark with coin-O
- **Typography:** Bold heavy sans-serif headlines (keep weight, improve hierarchy), clean body text
- **Modernizations:** Cleaner section spacing, sharper type scale, less decorative noise (reduce yellow circle overuse), photography-forward, more editorial feel
- **Feel:** Authentic craftsperson brand — think Patagonia meets Main Street jeweler. Not luxury. Not retail. Real.

---

## Page Architecture

### 1. NAV
- Logo left
- Links: For Inheritors | For Investors | How It Works | Stories | Blog
- CTAs: "Get a Free Appraisal" (yellow) | "Ask Travis" (outlined)

### 2. HERO
**Headline:** Every coin story is a money story.
**Subhead:** Sorting through an inheritance. Managing an investment. Everyone wants to get to the right decision — Fast. Friendly. Fair.
**Visual:** Full-bleed cinematic photo or short looping video (Charlotte office or at-home appraisal in action)
**No CTA here** — let the headline breathe, the persona cards below do the work

### 3. PERSONA CARDS (immediately below hero)
Two cards side by side, not buttons — they feel like a choice the visitor makes for themselves:

**Card 1 — Inheritor**
- Label: "I inherited a collection"
- 1-line description: "You're not sure what you have. That's exactly where we start."
- Anchor-links down to Inheritor section

**Card 2 — Investor**
- Label: "I'm managing an investment"
- 1-line description: "You know coins. Let's talk about what your collection is actually worth today."
- Anchor-links down to Investor section

**Small tertiary link below cards:**
- "Involved in an estate sale or legal process? →"

### 4. TRUST BAR
- G2 rating badge (API pull — live star rating + review count)
- "Authorized Member — PNG/ANA logos" (numismatic orgs)
- "As seen in: VoyageRaleigh" etc.
- Simple single row, no fanfare

### 5. INHERITOR JOURNEY SECTION
**Headline:** The coin is not the hard part. The decision is.
**Subhead:** You inherited something. Maybe it's valuable. Maybe it's complicated. Probably both. Here's what you need to know.

Three columns (what do you have / what it may be worth / what should you do next) — simple, human language, no jargon

**Travis AI Moment:**
- Illustrated avatar of Travis (beard, comic book tee, friendly)
- Prompt: "Not sure where to start? Ask Travis."
- Controlled question set: collection type, rough size, how they came to have it, what they're hoping for
- Advances understanding, builds commitment, natural handoff to real human

**Product options (for inheritors):**
- Mail-in: "Start with photos. We'll take it from there." → CTA: Get a Free Appraisal
- At-home (premium): "Large or historically significant collection? We come to you." → CTA: See If You Qualify

### 6. INVESTOR JOURNEY SECTION
**Headline:** You built this. Now let's find out what it's really worth.
**Subhead:** Market-leading offers. No coin shop lowballs. No auction house delays.

Value props rewritten in human language:
- "You'll know exactly what you have — authenticated, graded, valued"
- "We move fast. Most collections wrapped in a day"
- "Payment issued in minutes when you accept"

**Travis AI Moment (investor version):**
- Same avatar, different prompt: "What kind of collection are you working with? Ask Travis."
- Controlled question set: coin categories, collection size, timeline, goals
- More precise, market-focused answers

**Product options (for investors):**
- Mail-in → CTA: Get Your Offer
- At-home (premium) → CTA: Schedule a Visit

### 7. VIDEO — CHARLOTTE OFFICE
Full-width video section
- Section label: "Where the work happens"
- Placeholder for Charlotte office video
- Tone: Behind the scenes, real people, craft and expertise — not a commercial

### 8. HOME VISIT STORIES (3-4 videos)
Grid of 3-4 video story cards — shot in people's homes
- Each card: thumbnail, first name + city, one-line teaser ("Margaret had no idea what her father left behind.")
- Human, emotional, not sappy — a nod to the real stories behind collections
- Section headline: "Every collection has a story."

### 9. HOW IT WORKS
Simplified 3-step process — cleaner than current
- Step 1: Tell us about your collection (photos or call)
- Step 2: We appraise, authenticate, value
- Step 3: Accept the offer. Get paid immediately.
- Note: "For large collections, we come to you."

### 10. SOCIAL PROOF / TESTIMONIALS
- G2 reviews pulled via API (live)
- Mix of inheritor and investor voices
- Real names, not initials
- Section headline: "What people say after."

### 11. CONTENT SECTION (Blog/Resources)
More robust than current — 3-4 article cards
- Tagged by persona: [For Inheritors] [For Investors]
- Headline: "Things worth knowing."
- CTA: "Read more on the blog"

### 12. ESTATE/LEGAL CHANNEL CTA
Small, tasteful band — not a full section
- "Working through an estate sale or legal process? We can help with documentation, valuation, and coordination."
- CTA: "Let's talk"

### 13. FINAL CTA / FOOTER HERO
- Headline: "Ready to find out what yours is worth?"
- Two buttons: "Get a Free Appraisal" | "Ask Travis"
- Footer: standard nav, locations, legal

---

## Travis — The AI Guide

- **Character:** Illustrated avatar, Travis-inspired (beard, comic book tee)
- **Tone:** Knowledgeable friend, not a bot. Warm, plain-spoken, slightly nerdy about coins in the best way
- **Placement:** Appears in both Inheritor and Investor sections — not on page load, earns its moment
- **Mechanics:** Controlled question set (not open-ended AI), advances knowledge, builds commitment, hands off to human when appropriate
- **Design:** Illustrated style, consistent with brand — warmer than a photo, more distinctive than a stock avatar

---

## SEO Architecture

**Primary keyword journeys:**
- Inheritors: "how to sell inherited coin collection," "inherited coins value," "what to do with inherited coins"
- Investors: "sell coin collection best price," "coin collection appraisal," "coin collection value"

**Secondary:**
- "at home coin appraisal," "estate coin collection," "numismatic appraisal"

H1/H2 structure, meta tags, and page copy written with these journeys in mind.

---

## CTAs — Optimized

| Location | Primary CTA | Secondary CTA |
|----------|-------------|---------------|
| Nav | Get a Free Appraisal | Ask Travis |
| Persona cards | I inherited a collection | I'm managing an investment |
| Inheritor section | Get a Free Appraisal | See If You Qualify (at-home) |
| Investor section | Get Your Offer | Schedule a Visit (at-home) |
| Footer hero | Get a Free Appraisal | Ask Travis |

---

## Emotional Core (from raw research)

**The real fear driving this audience:** *"It's not to get the best price — it's not to get ripped off and feel like a sucker."*

This is the emotional undercurrent of the entire page. Rational on the surface, fear-driven underneath. The homepage needs to acknowledge this fear and resolve it — not by talking about features, but by making the visitor feel seen and safe.

**Four inheritor journey triggers (expand persona cards if needed):**
1. Inheritance — death in the family, collection must be dealt with
2. The basement box — burdensome collection that's been sitting untouched for years
3. Scammed parents — conservative, god-fearing people who got hoodwinked by predatory coin sellers
4. Urgency — gold is high, moving, probate, insurance requires valuation

**The scam angle is real and important:** Conservative older audience targeted by predatory coin sellers via magazines and phone calls. Parents spending $800K on coins worth a fraction of that. Coinfully is the antidote — but needs to address this without being preachy.

**Key brand proof point:** "When we physically get in front of a deal — 9 out of 10 we win." At-home = conversion.

**The forgotten part of estate planning** — strong potential headline for inheritor SEO page.

---

## Technical Notes

### G2 Integration
- Fetch G2 data at build time (not runtime) via G2 API or embed widget
- Fallback: hard-coded rating with last-updated date if API unavailable
- Display: star rating + review count + "Read reviews on G2" link
- Confirm with Coinfully that G2 API access exists before build

### Travis AI Mechanics
**Inheritor question flow (5 steps max):**
1. "What best describes your situation?" (Inherited / Clearing a family collection / Urgency to sell)
2. "Roughly how many coins are we talking?" (A handful / A few dozen / Hundreds or more / No idea)
3. "Do you know anything about the collection?" (Yes, some / No idea / Been told it's valuable)
4. "What matters most to you right now?" (Understanding what I have / Getting the best price / Moving quickly)
5. Response: curated 2-3 sentence answer + "Ready to talk to a real person?" → phone/form CTA

**Investor question flow (5 steps max):**
1. "What type of coins are you working with?" (Bullion / Rare/collectible / Mix / Not sure)
2. "Roughly what's the collection size?" (Under $10K / $10K–$50K / $50K+ / Unknown)
3. "What's your timeline?" (Ready now / Few weeks / Just exploring)
4. "Preferred next step?" (Get an offer / Learn about the process / Talk to someone)
5. Response: precise market-relevant answer + "Get your offer →" CTA

**Handoff trigger:** After step 5, show phone number + "Or we'll call you — just leave your number"
**Travis is built in static HTML/JS** — no external AI API needed for MVP. Responses are pre-written and mapped to question combinations.

### Mobile
- Hero: full-bleed image, headline stacked, no CTA
- Persona cards: stacked vertically (inheritor on top)
- Three-column sections: single column on mobile
- Travis: full-width card, same flow
- Video grid: single column
- Trust bar: horizontal scroll on mobile

### Video Sections
- Hosted on Vimeo or YouTube — embedded iframes, not self-hosted
- Lazy-loaded with poster image placeholder
- Aspect ratio: 16:9 preserved via padding-top trick

### Build
- Static HTML/CSS/JS in `/100yards/coinfully/` folder
- Deployed to Netlify with custom URL (coinfully-homepage.netlify.app or similar)
- SEO: meta tags, OG tags, LocalBusiness schema with Charlotte HQ address
- Blog cards: hard-coded for MVP (3-4 articles), update manually

# ICHRAverse Build vs. Buy Guide — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan.

**Goal:** Build a scrollable editorial content piece that pre-empts the "we'll just build it ourselves" objection from carriers evaluating ICHRA infrastructure options.
**Architecture:** Single self-contained HTML file. Editorial scrollable layout. Sticky ToC sidebar on desktop. No backend.
**Tech Stack:** HTML, CSS, JavaScript (vanilla — Intersection Observer for active nav). Inter font.
**Spec:** `docs/superpowers/specs/2026-03-31-ichraverse-suite-design.md`

---

## Brand Tokens

```css
--hs-blue: #0970C5
--hs-navy: #074294
--hs-border: #D3E0E8
--hs-text: #344054
--hs-text-light: #475467
```

Font: Inter via Google Fonts (`weights: 400, 500, 600, 700`).

---

## File Location

**Working directory:** `/Users/joshmait/Desktop/Claude/healthsherpa-ichra/build-vs-buy/`
**Output file:** `index.html`
**Deployment:** Part of the ICHRAverse Netlify site. Deploy from `/healthsherpa-ichra/` root.

---

## Chunk 1: Shell + Layout

### Task 1: HTML Shell + Editorial Layout

Create `/Users/joshmait/Desktop/Claude/healthsherpa-ichra/build-vs-buy/index.html` as a self-contained HTML file.

**Header:**
- HealthSherpa logo (text: "HealthSherpa" in `--hs-navy`, font-weight 700, 20px) on the left
- Back link on the right: `← Back to ICHRAverse` linking to `../index.html`
- Header border-bottom: `1px solid var(--hs-border)`
- Header padding: 16px 32px
- Header is NOT sticky — it scrolls away

**Page layout (two-column on desktop, single column on mobile):**
```
[  content column (max 720px)  ] [ sidebar (240px) ]
```
- Outer wrapper: max-width 1100px, centered, padding 48px 24px
- Content column: `flex: 1`, max-width 720px
- Sidebar: width 240px, position sticky, top 32px, align-self flex-start
- On mobile (< 900px): sidebar hidden, single column

**Section structure:** Each of the 5 content sections has:
- `id` attribute for anchor linking (e.g., `id="section-ai"`)
- Section header: label in `--hs-blue`, font-size 12px, font-weight 600, letter-spacing 0.08em, text-transform uppercase, margin-bottom 8px
- Section title: `h2`, font-size 26px, font-weight 700, color `--hs-navy`, margin-bottom 20px
- Body copy: font-size 17px, line-height 1.75, color `--hs-text`
- Section divider: `<hr>` with border-top `1px solid var(--hs-border)`, margin 56px 0

**Pull quote styling:**
- Left border: 4px solid `--hs-blue`
- Padding: 16px 24px
- Font-size: 20px, font-weight: 600, color: `--hs-navy`
- Font-style: italic
- Background: `#F0F6FD`
- Border-radius: 0 8px 8px 0
- Margin: 32px 0

---

### Task 2: Hero Section

Place immediately after the header, before the two-column layout begins.

**Hero contents:**
- Eyebrow label: `ICHRAverse Research` in `--hs-blue`, font-size 13px, font-weight 600, letter-spacing 0.06em, text-transform uppercase
- Headline: `"Why building your own ICHRA infrastructure is harder than it looks."` — font-size 40px, font-weight 700, color `--hs-navy`, line-height 1.2, max-width 720px
- Deck/subhead: `"A carrier's guide to the real costs, the competitive window, and the honest case for partnership."` — font-size 19px, color `--hs-text-light`, margin-top 16px, max-width 640px
- Byline row (margin-top 24px): `By ICHRAverse Research Team` · `March 2025` · `12 min read` — font-size 14px, color `--hs-text-light`, items separated by `·` with padding 0 8px
- Bottom border/divider below hero: `2px solid var(--hs-border)`, margin-bottom 48px

---

## Chunk 2: The 5 Content Sections

### Task 3: Section 1 — "Why AI Doesn't Solve the Real Problem"

**Section anchor:** `id="section-ai"`
**Section label:** `Section 1`
**Section title:** `Why AI Doesn't Solve the Real Problem`

**Placeholder copy (~200 words):**

```
Every few months, a carrier's engineering team surfaces the same idea: "We could just use AI to handle the enrollment logic." It's an appealing thought. Large language models are increasingly capable. Automation is real. Why pay for infrastructure when intelligence is cheap?

Here's why: the problem was never intelligence. It's trust.

CMS doesn't care how smart your code is. The Centers for Medicare & Medicaid Services requires specific EDI transaction formats — 834 for enrollment, 820 for premium payment — with validation rules that have been codified over decades of regulatory evolution. These aren't guidelines. They're requirements, and they come with audit trails.

Machine learning doesn't fix enrollment validation rules. A model that hallucinates a field value or misroutes a transaction doesn't just create a bug — it creates a compliance event. CMS requires human-auditable logic, not probabilistic inference. The difference between a deterministic system and a probabilistic one is the difference between passing a CMS audit and failing it.

And AI definitely cannot get you a CMS trading partner ID faster. That requires a relationship. It requires a track record. HealthSherpa has both — built over a decade of processing more than half of all Federal Marketplace enrollments.

The question isn't whether AI is powerful. It is. The question is whether AI is what's standing between you and a functioning ICHRA channel. It isn't.
```

**Pull quote (place after second paragraph):**
> "The problem isn't intelligence. It's trust. CMS doesn't trust code it can't audit."

---

### Task 4: Section 2 — "The True Cost of Building"

**Section anchor:** `id="section-cost"`
**Section label:** `Section 2`
**Section title:** `The True Cost of Building`

**Placeholder copy (~200 words, with comparison table):**

```
When carriers say "we'll build it," the conversation usually ends there. It shouldn't. The real question is: build what, by when, with whom, at what cost — and then maintain it how?

Building ICHRA enrollment infrastructure isn't a sprint. It's a multi-year infrastructure commitment that competes for engineering resources against your core product roadmap. Here's what that typically looks like:
```

**Comparison table (place after intro paragraph):**

| | Build Yourself | Partner with HealthSherpa |
|---|---|---|
| **Time to first enrollment** | 18–24 months | 60–90 days |
| **Engineering headcount** | 4–6 FTE | 0 FTE |
| **Ongoing compliance maintenance** | 1–2 FTE ongoing | 0 FTE |
| **CMS relationship** | Start from zero | Pre-established |
| **Platform connections** | Manual outreach to each | 40+ live today |
| **Year 1 cost** | $500K–$1M+ | Contact for pricing |

**Table styling:**
- Full-width, border-collapse collapse
- Header row: background `--hs-navy`, color white, font-size 13px, padding 12px 16px
- Body rows: alternating white / `#F8FAFC`, font-size 15px, padding 12px 16px
- Bold first column
- Border: `1px solid var(--hs-border)`
- Border-radius 8px (wrap in a div with overflow hidden)
- Margin: 32px 0

**Copy after table:**

```
These numbers aren't meant to discourage building. They're meant to make the tradeoff visible. Engineering time spent on enrollment infrastructure is engineering time not spent on your differentiated product. Every month in the queue is a month your competitors are activating channels.

The carriers who've moved fastest on ICHRA aren't the ones with the biggest engineering teams. They're the ones who made a clear-eyed decision about what's a core competency and what's a commodity infrastructure layer.
```

**Pull quote (place after table):**
> "Every month building is a month not selling. The carriers who moved fastest made a deliberate choice: infrastructure is not their product."

---

### Task 5: Section 3 — "The 12–24 Month Window"

**Section anchor:** `id="section-window"`
**Section label:** `Section 3`
**Section title:** `The 12–24 Month Window`

**Placeholder copy (~200 words):**

```
ICHRA isn't emerging. It's accelerating. According to the HRA Council's 2025 data, ICHRA membership grew 124% year-over-year. The employers who are adopting ICHRA aren't waiting for the market to mature — they're making vendor and carrier decisions right now.

This matters for carriers because employer plan selection is sticky. Once a benefits platform is integrated into an employer's HR workflow, switching costs are high. The carriers that are available in those platforms in 2025 and 2026 will have a structural advantage that compounds over time. Employers who onboard on Platform A with Carrier X don't easily move. The channel shapes the relationship.

The carriers who wait until 2027 won't find an open market. They'll find a market where platform relationships are established, employer preferences are set, and the first movers are entrenched. Enrollment volume will still grow — ICHRA is real — but the share available to late entrants will be smaller, harder to win, and require more pricing concession to capture.

This is a first-mover dynamic. Not in the sense that the market disappears — it won't. But in the sense that the cost of entry increases with every quarter of delay.
```

**Pull quote (place after second paragraph):**
> "The window for first-mover advantage in ICHRA is 2025–2026. Carriers who wait will find the channel already shaped."

---

### Task 6: Section 4 — "The Options: An Honest Comparison"

**Section anchor:** `id="section-options"`
**Section label:** `Section 4`
**Section title:** `The Options: An Honest Comparison`

**Intro copy:**

```
There are three realistic paths for a carrier who wants to participate in the ICHRA channel. We're going to describe all three honestly — including the one that leads to us. The goal isn't to win an argument. It's to help you make the right call for your organization.
```

**Three-column comparison cards (place after intro):**

Card layout: `display: flex; gap: 24px;` on desktop, stacked on mobile. Each card: background white, border `1px solid var(--hs-border)`, border-radius 12px, padding 28px, flex: 1.

**Card 1 — Direct Integration**
- Label (top): `Option A` in `--hs-text-light`, font-size 12px, font-weight 600, text-transform uppercase
- Title: `Build Direct` — font-size 20px, font-weight 700, color `--hs-navy`
- Subtitle: `Full control. High commitment.`
- Divider line
- Bullet points:
  - Build your own enrollment infrastructure
  - 18–24 months to production-ready
  - $500K–$1M+ in Year 1
  - You own the CMS relationship from scratch
  - Full control over the roadmap
  - Engineering resources locked for 2+ years
- Bottom note (italic, `--hs-text-light`): `Best if: ICHRA is a 5-year strategic priority and you have engineering capacity to spare.`

**Card 2 — ICHRAx**
- Label (top): `Option B` in `--hs-text-light`, font-size 12px, font-weight 600, text-transform uppercase
- Title: `ICHRAx` — font-size 20px, font-weight 700, color `--hs-navy`
- Subtitle: `Standards body. Credible vision. Early stage.`
- Divider line
- Bullet points:
  - Connect-once standards approach
  - Led by experienced ICHRA operators (ex-Take Command)
  - Advisory Board model with carrier/platform input
  - 12–18 months to meaningful volume (estimated)
  - No existing CMS trading partner relationship
  - Unproven at enrollment scale
- Bottom note (italic, `--hs-text-light`): `Best if: You want a standards-based approach and are willing to wait for the ecosystem to mature.`

**Card 3 — HealthSherpa** (add a subtle blue top border `4px solid var(--hs-blue)` to distinguish)
- Label (top): `Option C` in `--hs-blue`, font-size 12px, font-weight 600, text-transform uppercase
- Title: `HealthSherpa` — font-size 20px, font-weight 700, color `--hs-navy`
- Subtitle: `Live today. CMS-trusted. 40+ platforms.`
- Divider line
- Bullet points:
  - 50%+ of Federal Marketplace enrollments
  - CMS trading partner relationship: established
  - 40+ live platform connections today
  - 60–90 days to first enrollment
  - 0 FTE required from carrier
  - Fastest path to activated ICHRA channel
- Bottom note (italic, `--hs-blue`, font-weight 500): `Best if: You want to be in market this year.`

**Copy after cards:**

```
ICHRAx is a real initiative led by credible people. We're not dismissing it. Standards bodies matter, and the ICHRA ecosystem will benefit from better connectivity standards over time. But "standards body" and "enrollment infrastructure" are different things. One shapes how the market works. The other processes your enrollments today.

We're not asking you to trust us. We're asking you to look at what's live.
```

---

### Task 7: Section 5 — "Save Yourself From Yourself"

**Section anchor:** `id="section-save"`
**Section label:** `Section 5`
**Section title:** `Save Yourself From Yourself`

**Placeholder copy (~150 words):**

```
Here's the honest version of what's happening when a carrier says "we'll build it."

Most of the time, it doesn't mean "we have a plan to build it." It means "we're not ready to commit to ICHRA yet." That's a legitimate position. ICHRA may not be the right channel for every carrier right now. Regulatory appetite varies. Distribution strategy varies. Risk tolerance varies.

But if the answer is yes to ICHRA — if the strategic decision has been made — then the fastest path to revenue is infrastructure you don't have to build, maintain, or audit. The carriers who've moved fastest on ICHRA are the ones who didn't try to become software companies. They made a clear-eyed decision: their job is to underwrite risk and serve members. The plumbing that connects them to the market is someone else's problem.

That's not a concession. That's a strategy.
```

**Quote block (styled differently from pull quotes — centered, larger, no left border):**
```
"The carriers who've moved fastest are the ones who didn't try to become software companies."
```
Style: font-size 24px, font-weight 600, color `--hs-navy`, text-align center, padding 32px 48px, background `#F0F6FD`, border-radius 12px, margin 40px 0.

**Closing line (after quote, before CTA):**
```
The question isn't build vs. buy. It's how fast do you want to be in market?
```
Style: font-size 20px, font-weight 600, color `--hs-navy`, text-align center, margin-top 24px.

---

## Chunk 3: Sidebar + Nav

### Task 8: Sticky Sidebar Table of Contents

**Sidebar placement:** Right column of the two-column layout, sticky on scroll. Hidden on mobile (< 900px).

**Sidebar contents:**
- Label: `In this guide` — font-size 11px, font-weight 600, text-transform uppercase, letter-spacing 0.08em, color `--hs-text-light`, margin-bottom 16px
- Nav links (one per section):
  1. `Why AI isn't the answer` → `#section-ai`
  2. `The true cost of building` → `#section-cost`
  3. `The 12–24 month window` → `#section-window`
  4. `An honest comparison` → `#section-options`
  5. `Save yourself from yourself` → `#section-save`

**Link styling (default):**
- display block, padding 8px 12px
- font-size 14px, color `--hs-text-light`
- border-left: 2px solid transparent
- text-decoration none
- transition: all 0.15s ease

**Link styling (active — `.is-active`):**
- color `--hs-blue`
- border-left-color `--hs-blue`
- font-weight 500
- background `#F0F6FD`
- border-radius 0 6px 6px 0

**JavaScript — Intersection Observer:**

```javascript
const sections = document.querySelectorAll('section[id]');
const navLinks = document.querySelectorAll('.toc-nav a');

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      navLinks.forEach(link => link.classList.remove('is-active'));
      const activeLink = document.querySelector(`.toc-nav a[href="#${entry.target.id}"]`);
      if (activeLink) activeLink.classList.add('is-active');
    }
  });
}, {
  rootMargin: '-20% 0px -70% 0px',
  threshold: 0
});

sections.forEach(section => observer.observe(section));
```

Each of the 5 content sections must use a `<section id="section-XX">` wrapper element (not just a div) for the Intersection Observer to target them correctly.

---

## Chunk 4: CTA + Deploy

### Task 9: Bottom CTA Section

Place after the last section divider, spanning full width (outside the two-column layout), before the closing `</main>`.

**CTA styling:**
- Background: `--hs-navy`
- Padding: 64px 48px
- Text-align: center
- Border-radius: 16px
- Max-width: 720px, centered, margin: 56px auto

**CTA contents:**
- Eyebrow: `Ready to move?` — font-size 13px, font-weight 600, text-transform uppercase, letter-spacing 0.06em, color `rgba(255,255,255,0.6)`, margin-bottom 12px
- Headline: `Want to see HealthSherpa's infrastructure in action?` — font-size 28px, font-weight 700, color white, line-height 1.3
- Subhead: `Talk to the ICHRAverse team about what a live integration looks like.` — font-size 16px, color `rgba(255,255,255,0.75)`, margin-top 12px
- Button: `Schedule a Demo →` — background `--hs-blue`, color white, padding 14px 32px, border-radius 8px, font-size 16px, font-weight 600, border none, cursor pointer, text-decoration none, display inline-block, margin-top 28px
- Button `href`: `https://info.healthsherpa.com/ICHRA`
- Button hover: background `#0860B0` (darken slightly)

**Footer below CTA:**
- Simple centered text: `© 2025 HealthSherpa · ICHRA carrier solutions` — font-size 13px, color `--hs-text-light`, margin-top 48px, padding-bottom 32px

---

### Task 10: Deploy

From the terminal, run:

```bash
cd /Users/joshmait/Desktop/Claude/healthsherpa-ichra
npx netlify-cli deploy --prod --dir .
```

This redeploys the entire ICHRAverse site (all tools live at the same Netlify project). The Build vs. Buy Guide will be accessible at `[site-url]/build-vs-buy/`.

Confirm the deploy succeeded and return the live URL.

---

## Completion Checklist

- [ ] HTML shell created at `/Users/joshmait/Desktop/Claude/healthsherpa-ichra/build-vs-buy/index.html`
- [ ] Header with back link to `../index.html`
- [ ] Hero section with headline, deck, byline, reading time
- [ ] Two-column layout: 720px content + 240px sticky sidebar
- [ ] All 5 sections with `<section id="section-XX">` wrappers
- [ ] Section 1: AI copy + pull quote
- [ ] Section 2: Cost copy + comparison table + pull quote
- [ ] Section 3: Window copy + pull quote
- [ ] Section 4: Options intro + three comparison cards + closing copy
- [ ] Section 5: Save yourself copy + centered quote block + closing line
- [ ] Sticky sidebar with Intersection Observer active state
- [ ] Bottom CTA in `--hs-navy`, linking to `https://info.healthsherpa.com/ICHRA`
- [ ] Footer
- [ ] Mobile responsive (sidebar hidden, single column)
- [ ] Deployed to Netlify, live URL confirmed

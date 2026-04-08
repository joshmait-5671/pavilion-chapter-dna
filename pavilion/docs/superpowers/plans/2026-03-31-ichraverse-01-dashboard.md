# ICHRAverse Master Dashboard — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build the ICHRAverse master hub page — a single `index.html` that links to all 6 tools, sets the brand, and serves as the first thing a HS rep shares with a carrier.

**Architecture:** Single self-contained HTML file. HealthSherpa brand colors and visual language. 6 tool cards, market stats bar, single CTA. No backend, no dependencies.

**Tech Stack:** HTML, CSS, JavaScript (vanilla). Inter font via Google Fonts. No frameworks.

**Spec:** `docs/superpowers/specs/2026-03-31-ichraverse-suite-design.md`

---

## Chunk 1: Shell + Brand

### Task 1: Seed shared design system

**Files:**
- Create: `healthsherpa-ichra/shared/styles.css`

- [ ] Create `shared/styles.css` with the brand variables and base resets that all tools will import:
```css
/* ICHRAverse Shared Design System */
:root {
  --hs-blue: #0970C5;
  --hs-blue-light: #2EB6FF;
  --hs-blue-dark: #0D61A6;
  --hs-navy: #074294;
  --hs-border: #D3E0E8;
  --hs-text: #344054;
  --hs-text-light: #475467;
  --hs-bg: #F8FAFC;
}
* { margin: 0; padding: 0; box-sizing: border-box; }
body { font-family: 'Inter', Helvetica, sans-serif; color: var(--hs-text); background: white; }
.hs-btn {
  padding: 12px 28px; border-radius: 90px; border: none;
  background: var(--hs-blue); color: white; font-weight: 600;
  font-size: 15px; cursor: pointer; transition: background 0.2s;
  font-family: inherit;
}
.hs-btn:hover { background: var(--hs-blue-dark); }
.hs-btn-outline {
  background: white; color: var(--hs-blue);
  border: 2px solid var(--hs-blue);
}
.hs-btn-outline:hover { background: #f0f7ff; }
.hs-card {
  border: 1px solid var(--hs-border); border-radius: 12px;
  padding: 24px; background: white;
}
```

- [ ] Verify file exists at `healthsherpa-ichra/shared/styles.css`.

- [ ] Commit:
```bash
git add healthsherpa-ichra/shared/styles.css
git commit -m "feat: ichraverse shared design system seed"
```

---

### Task 2: Project folder and base HTML shell

**Files:**
- Create: `healthsherpa-ichra/index.html`

- [ ] Create the file with DOCTYPE, head, meta tags, Google Fonts (Inter), title "ICHRAverse | HealthSherpa ICHRA"

- [ ] Add base CSS reset and brand variables:
```css
:root {
  --hs-blue: #0970C5;
  --hs-blue-light: #2EB6FF;
  --hs-blue-dark: #0D61A6;
  --hs-navy: #074294;
  --hs-border: #D3E0E8;
  --hs-text: #344054;
  --hs-text-light: #475467;
  --hs-bg: #F8FAFC;
}
```

- [ ] Open `index.html` in browser. Verify: blank white page, no console errors.

- [ ] Commit:
```bash
git add healthsherpa-ichra/index.html
git commit -m "feat: ichraverse dashboard shell"
```

---

### Task 3: Header

**Files:**
- Modify: `healthsherpa-ichra/index.html`

- [ ] Add sticky header: HS logo (SVG shield/cross), "ICHRAverse" bold, "by HealthSherpa" subdued. Right side: "Talk to our ICHRA team →" button (blue, 90px border-radius).

- [ ] Header CSS: `background: var(--hs-blue)`, white text, `padding: 0 48px`, `height: 64px`, flex layout.

- [ ] Verify in browser: header renders full-width, button visible, looks like HealthSherpa brand.

- [ ] Commit:
```bash
git commit -m "feat: ichraverse dashboard header"
```

---

### Task 4: Market Stats Bar

**Files:**
- Modify: `healthsherpa-ichra/index.html`

- [ ] Add stats bar below header: 4 stats in a row.
  - "40+ ICHRA Platforms Connected" — source: HealthSherpa
  - "500K–1M Lives on ICHRA" — source: HRA Council 2025
  - "124% YoY Membership Growth" — source: HRA Council 2025
  - "52% Projected CAGR" — source: Oliver Wyman

- [ ] Each stat: large number in `--hs-blue`, label in `--hs-text-light`, source in tiny gray italic. No invented numbers.

- [ ] Stats bar CSS: white background, `border-bottom: 1px solid var(--hs-border)`, `padding: 20px 48px`.

- [ ] Verify in browser: 4 stats visible in a row, numbers prominent.

- [ ] Commit:
```bash
git commit -m "feat: ichraverse dashboard stats bar"
```

---

## Chunk 2: Tool Cards

### Task 5: Hero Section

**Files:**
- Modify: `healthsherpa-ichra/index.html`

- [ ] Add hero: H1 "The ICHRA infrastructure layer. Built for carriers." Subhead: "A suite of tools to help you understand the market, build your strategy, and activate your ICHRA channel — powered by the platform processing 50%+ of Federal Marketplace enrollments."

- [ ] Hero CSS: centered, max-width 800px, `padding: 64px 48px 32px`. H1 at 40px, font-weight 800, `color: var(--hs-blue)`.

- [ ] Verify: hero text renders cleanly.

- [ ] Commit:
```bash
git commit -m "feat: ichraverse dashboard hero"
```

---

### Task 6: Tool Cards Grid

**Files:**
- Modify: `healthsherpa-ichra/index.html`

- [ ] Add 6 tool cards in a 3-col grid (2-col on mobile). Each card:
  - Icon (SVG, 40×40, blue bg circle)
  - Tool name (bold, 18px)
  - One-line description
  - "Kills" tag (the objection it addresses) in light blue pill
  - "Open tool →" button (outline style, blue)
  - Card border: `1px solid var(--hs-border)`, border-radius 12px, 24px padding

- [ ] Tool card content:
  1. **ICHRA Adoption Map** — "See where ICHRA is growing, state by state." Kills: "Feels too small" — links to `map/index.html`
  2. **Strategy Builder** — "Build your carrier ICHRA strategy in 10 minutes." Kills: "No strategy yet" — links to `strategy-builder/index.html`
  3. **ROI Calculator** — "Model your 3-year return on ICHRA investment." Kills: "No clear ROI" — links to `roi-calculator/index.html`
  4. **Build vs. Buy Guide** — "Why AI won't save you from CMS compliance." Kills: "We'll just build it" — links to `build-vs-buy/index.html`
  5. **ICHRA Content Hub** — "The pulse of the ICHRA ecosystem." Kills: "Market awareness" — links to `content-hub/index.html`
  6. **Discovery Assessment** — "Answer 7 questions. Get a custom ICHRA brief." Kills: "Don't know where to start" — links to `#` as placeholder (replace with absolute Netlify URL once `ichra-discovery` is deployed independently)

- [ ] Verify in browser: 6 cards render in grid, all links present (even if destinations 404 for now).

- [ ] Commit:
```bash
git commit -m "feat: ichraverse dashboard tool cards"
```

---

## Chunk 3: Footer + Deploy

### Task 7: Closing CTA + Footer

**Files:**
- Modify: `healthsherpa-ichra/index.html`

- [ ] Add closing CTA section: "Ready to activate your ICHRA channel?" with blue button "Talk to our ICHRA team →" (links to `https://info.healthsherpa.com/ICHRA`).

- [ ] Footer: HealthSherpa logo, "© 2026 HealthSherpa. ICHRA infrastructure for carriers and platforms." Links: HealthSherpa.com, ICHRA docs, Privacy.

- [ ] Verify full page scroll top-to-bottom looks polished.

- [ ] Commit:
```bash
git commit -m "feat: ichraverse dashboard CTA and footer"
```

---

### Task 8: Deploy to Netlify

- [ ] From `/healthsherpa-ichra/`:
```bash
npx netlify-cli deploy --prod --dir . --name ichraverse-hub
```

- [ ] Verify live URL loads correctly.

- [ ] Update MEMORY.md with live URL.

- [ ] Commit:
```bash
git commit -m "feat: ichraverse dashboard live"
```

---

**Plan complete. Build time estimate: ~1 hour.**

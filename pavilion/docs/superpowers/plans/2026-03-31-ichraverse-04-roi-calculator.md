# ICHRAverse ROI Calculator — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan.

**Goal:** Build a self-contained ICHRA ROI Calculator that helps carriers quantify 3-year revenue potential, break-even timing, and cannibalization offset from ICHRA adoption.
**Architecture:** Single self-contained HTML file. Pure CSS bar chart. window.print() for save. No backend.
**Tech Stack:** HTML, CSS, JavaScript (vanilla). Inter font.
**Spec:** `docs/superpowers/specs/2026-03-31-ichraverse-suite-design.md`

---

## Chunk 1: Shell + Inputs

### Task 1: HTML Shell with HS Header

**Files:**
- Create: `healthsherpa-ichra/roi-calculator/index.html`

- [ ] Create `healthsherpa-ichra/roi-calculator/` directory if it does not exist
- [ ] Create `healthsherpa-ichra/roi-calculator/index.html` with full HTML5 boilerplate
- [ ] Add `<meta charset="UTF-8">`, `<meta name="viewport" content="width=device-width, initial-scale=1.0">`, `<title>ICHRA ROI Calculator — ICHRAverse</title>`
- [ ] Import Inter font: `<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">`
- [ ] Add CSS custom properties in `:root`:
  ```css
  --hs-blue: #0970C5;
  --hs-navy: #074294;
  --hs-border: #D3E0E8;
  --hs-text: #344054;
  --hs-text-light: #475467;
  --hs-bg: #F8FAFC;
  --hs-white: #FFFFFF;
  --hs-green: #027A48;
  --hs-green-bg: #ECFDF3;
  --hs-warning: #B54708;
  --hs-warning-bg: #FFFAEB;
  ```
- [ ] Set `body { font-family: 'Inter', sans-serif; color: var(--hs-text); background: var(--hs-bg); margin: 0; padding: 0; }`
- [ ] Build site header bar: full-width `<header>` with `background: var(--hs-navy)`, padding `16px 32px`, flex row space-between
  - Left: Back link `← ICHRAverse Suite` pointing to `../index.html`, white text, no underline, font-size 14px, font-weight 500
  - Right: HealthSherpa wordmark in white, font-weight 700, font-size 18px, letter-spacing -0.02em (plain text, no image needed)
- [ ] Below header: page hero section with `background: linear-gradient(135deg, var(--hs-navy) 0%, var(--hs-blue) 100%)`, padding `48px 32px 56px`, text centered
  - `<h1>` "ICHRA ROI Calculator" in white, font-size 32px, font-weight 700, margin-bottom 12px
  - `<p>` subhead: "Build the financial case for your ICHRA investment. Model 3-year revenue, break-even timing, and the retention story for your group book." — white at 85% opacity, font-size 16px, max-width 600px, centered (margin auto)
- [ ] Main content container: `<main>` with max-width 1100px, margin `0 auto`, padding `32px 24px`
- [ ] Two-column grid layout inside `<main>`: left column (inputs, ~420px) and right column (results, flex-grow). Use CSS Grid: `display: grid; grid-template-columns: 420px 1fr; gap: 32px; align-items: start;`
- [ ] On screens under 900px: stack to single column (`grid-template-columns: 1fr`)

- [ ] Commit:
```bash
git commit -m "feat: roi-calculator — HTML shell, HS header, hero section, two-column grid"
```

---

### Task 2: Input Panel — 6 Sliders/Inputs

**Files:**
- Edit: `healthsherpa-ichra/roi-calculator/index.html`

- [ ] Create a `<div class="input-panel">` in the left column — white card, border `1px solid var(--hs-border)`, border-radius 12px, padding 28px
- [ ] Add panel heading: `<h2>` "Your Numbers" — font-size 18px, font-weight 600, color `var(--hs-navy)`, margin-bottom 4px
- [ ] Add panel subhead: `<p>` "Adjust inputs to model your opportunity" — font-size 13px, color `var(--hs-text-light)`, margin-bottom 24px

**Input 1 — Group Book Size:**
- [ ] `<div class="input-group">` with label "Group Book Size (lives)", label font-size 14px, font-weight 500
- [ ] Live value display: `<span id="book-size-val">50,000</span>` aligned right on same row as label — font-weight 600, color `var(--hs-blue)`
- [ ] `<input type="range" id="book-size" min="10000" max="500000" step="5000" value="50000">`
- [ ] Below range: helper text "10K — 500K lives" font-size 12px, color `var(--hs-text-light)`

**Input 2 — ICHRA-Eligible Segment:**
- [ ] `<div class="input-group">` with label "ICHRA-Eligible Segment (% of small group)"
- [ ] Live value display: `<span id="eligible-pct-val">15%</span>`
- [ ] `<input type="range" id="eligible-pct" min="5" max="40" step="1" value="15">`
- [ ] Helper text: "5% — 40% of group book"

**Input 3 — PMPM Rate:**
- [ ] `<div class="input-group">` with label "PMPM Rate (HealthSherpa fee)"
- [ ] Live value display: `<span id="pmpm-val">$2.50</span>`
- [ ] `<input type="range" id="pmpm" min="1" max="10" step="0.25" value="2.50">`
- [ ] Helper text: "$1.00 — $10.00 per member per month"
- [ ] Warning badge below input: amber background (`var(--hs-warning-bg)`), amber text (`var(--hs-warning)`), border-radius 6px, padding `6px 10px`, font-size 12px, font-weight 500. Text: "⚠️ Placeholder rate — validate with HS sales team before use"

**Input 4 — Integration Cost Model (Toggle):**
- [ ] `<div class="input-group">` with label "Integration Cost Model"
- [ ] Two-option toggle built with radio buttons styled as pill buttons side-by-side:
  - Option A: `<input type="radio" id="model-build" name="cost-model" value="build">` + `<label for="model-build">Build In-House</label>`
  - Option B: `<input type="radio" id="model-partner" name="cost-model" value="partner" checked>` + `<label for="model-partner">Partner with HS</label>`
- [ ] Toggle container: `display: flex; border: 1px solid var(--hs-border); border-radius: 8px; overflow: hidden;`
- [ ] Each label: `flex: 1; text-align: center; padding: 8px 12px; font-size: 13px; font-weight: 500; cursor: pointer;`
- [ ] Selected state: `background: var(--hs-blue); color: white;` (unselected: white background, `var(--hs-text)` color)
- [ ] Below toggle, show conditional cost note in a `<div id="cost-note">`:
  - If build: "Estimated cost: $250K–$500K (midpoint $375K used for break-even)"
  - If partner: "Contact HealthSherpa for integration pricing"
  - Font-size 12px, color `var(--hs-text-light)`, margin-top 6px

**Input 5 — Time to Revenue:**
- [ ] `<div class="input-group">` with label "Time to Revenue (months)"
- [ ] Live value display: `<span id="time-to-revenue-val">6 months</span>`
- [ ] `<input type="range" id="time-to-revenue" min="3" max="24" step="1" value="6">`
- [ ] Helper text: "3 — 24 months to first ICHRA revenue"

**Input 6 — Group Retention Rate:**
- [ ] `<div class="input-group">` with label "Group Retention Rate" + tooltip icon `ⓘ` (using `<span class="tooltip-trigger">`)
- [ ] Tooltip (CSS-only, shown on hover via `::after` pseudo-element): "% of group members who stay as individual market members after ICHRA switch — reducing net cannibalization"
  - `position: absolute; background: var(--hs-navy); color: white; font-size: 12px; border-radius: 6px; padding: 8px 12px; width: 240px; bottom: calc(100% + 8px); left: 50%; transform: translateX(-50%); z-index: 10;`
- [ ] Live value display: `<span id="retention-val">70%</span>`
- [ ] `<input type="range" id="retention" min="50" max="95" step="5" value="70">`
- [ ] Helper text: "50% — 95% of eligible group members retained"

**Slider Shared Styles:**
- [ ] `input[type="range"]`: `width: 100%; accent-color: var(--hs-blue); height: 4px; cursor: pointer; margin: 8px 0;`
- [ ] Each `.input-group`: `margin-bottom: 24px;` with `padding-bottom: 24px; border-bottom: 1px solid var(--hs-border);` — last child has no border-bottom
- [ ] Label row: `display: flex; justify-content: space-between; align-items: center; margin-bottom: 6px;`
- [ ] Label text: `font-size: 14px; font-weight: 500; color: var(--hs-text);`
- [ ] Value display span: `font-size: 14px; font-weight: 600; color: var(--hs-blue);`

- [ ] Commit:
```bash
git commit -m "feat: roi-calculator — 6 input sliders with live value display and toggle"
```

---

### Task 3: Disclaimer Banner

**Files:**
- Edit: `healthsherpa-ichra/roi-calculator/index.html`

- [ ] Add a full-width disclaimer banner between the hero section and `<main>`, OR at the top of the input panel (inside `<main>`, above the two-column grid)
- [ ] Recommended placement: full-width strip below hero, above `<main>` content
- [ ] Styles: `background: var(--hs-warning-bg); border-bottom: 1px solid #FEC84B; padding: 12px 32px; text-align: center;`
- [ ] Inner text: "**All figures are illustrative.** Consult your HS account team for validated PMPM rates and integration costs before using in financial planning."
- [ ] Font-size 13px, color `var(--hs-warning)`. Bold the first sentence using `<strong>`.
- [ ] Max-width 900px, centered via `margin: 0 auto` on inner `<p>`

- [ ] Commit:
```bash
git commit -m "feat: roi-calculator — illustrative data disclaimer banner"
```

---

## Chunk 2: Calculation Engine + Results

### Task 4: JavaScript Calculation Engine

**Files:**
- Edit: `healthsherpa-ichra/roi-calculator/index.html`

- [ ] Add `<script>` block at the bottom of `<body>` (before `</body>`)
- [ ] Define a `calculate()` function that reads all 6 inputs and returns a results object:

```javascript
function calculate() {
  const bookSize = parseInt(document.getElementById('book-size').value);
  const eligiblePct = parseFloat(document.getElementById('eligible-pct').value);
  const pmpm = parseFloat(document.getElementById('pmpm').value);
  const costModel = document.querySelector('input[name="cost-model"]:checked').value;
  const timeToRevenue = parseInt(document.getElementById('time-to-revenue').value);
  const retentionRate = parseFloat(document.getElementById('retention').value);

  const ichraEligibleLives = Math.round(bookSize * (eligiblePct / 100));
  const annualRevenue = ichraEligibleLives * pmpm * 12;
  const year1Revenue = annualRevenue * ((12 - timeToRevenue) / 12);
  const year2Revenue = annualRevenue;
  const year3Revenue = annualRevenue * 1.15;
  const total3yr = year1Revenue + year2Revenue + year3Revenue;
  const buildCost = 375000; // midpoint of $250K–$500K
  const breakevenMonths = costModel === 'build'
    ? (annualRevenue > 0 ? Math.ceil(buildCost / (annualRevenue / 12)) : null)
    : null;
  const retainedLives = Math.round(bookSize * (eligiblePct / 100) * (retentionRate / 100));

  return {
    ichraEligibleLives,
    annualRevenue,
    year1Revenue,
    year2Revenue,
    year3Revenue,
    total3yr,
    buildCost,
    breakevenMonths,
    retainedLives,
    costModel,
    bookSize,
    eligiblePct,
    retentionRate,
    pmpm,
    timeToRevenue
  };
}
```

- [ ] Define a `formatMoney(n)` helper: `return '$' + Math.round(n).toLocaleString('en-US');`
- [ ] Define a `formatNumber(n)` helper: `return Math.round(n).toLocaleString('en-US');`
- [ ] Define an `updateLiveValues()` function that reads each slider and updates its display span:
  - `book-size-val`: `formatNumber(val)` (e.g., "50,000")
  - `eligible-pct-val`: `val + '%'`
  - `pmpm-val`: `'$' + parseFloat(val).toFixed(2)`
  - `time-to-revenue-val`: `val + ' months'`
  - `retention-val`: `val + '%'`
- [ ] Define a `updateCostNote()` function: reads `cost-model` radio value, sets `cost-note` innerHTML to appropriate message
- [ ] Define a `render()` function that calls `calculate()`, calls `updateLiveValues()`, calls `updateCostNote()`, then calls `updateResultCards()`, `updateChart()`, `updateCannibalizationSection()`
- [ ] Attach `render` as `oninput` handler on all range sliders and as `onchange` handler on radio buttons
- [ ] Call `render()` once on page load (`document.addEventListener('DOMContentLoaded', render)`)

- [ ] Commit:
```bash
git commit -m "feat: roi-calculator — JS calculation engine with formula implementation"
```

---

### Task 5: Results Section — 4 Big Number Cards

**Files:**
- Edit: `healthsherpa-ichra/roi-calculator/index.html`

- [ ] Create `<div class="results-column">` in the right grid column — contains results card grid, chart section, and cannibalization section
- [ ] Add a results heading: `<h2>` "Your Revenue Model" — font-size 18px, font-weight 600, color `var(--hs-navy)`, margin-bottom 16px
- [ ] Create `<div class="result-cards">` — CSS Grid: `display: grid; grid-template-columns: 1fr 1fr; gap: 16px; margin-bottom: 24px;`

**Card structure (repeat 4x):**
```html
<div class="result-card">
  <div class="result-label">ICHRA-Eligible Lives</div>
  <div class="result-value" id="card-eligible-lives">—</div>
  <div class="result-sublabel">based on your book size × eligible %</div>
</div>
```

- [ ] Card 1: id `card-eligible-lives`, label "ICHRA-Eligible Lives", sublabel "book size × eligible %"
- [ ] Card 2: id `card-year1`, label "Year 1 Revenue", sublabel "partial year (activation delay)"
- [ ] Card 3: id `card-3yr`, label "3-Year Total Revenue", sublabel "incl. 15% growth in Year 3"
- [ ] Card 4: id `card-breakeven`, label "Break-Even (Build)", sublabel "months from go-live to cost recovery"

**Card styles:**
- [ ] `.result-card`: `background: white; border: 1px solid var(--hs-border); border-radius: 12px; padding: 20px; text-align: center;`
- [ ] `.result-label`: `font-size: 12px; font-weight: 500; color: var(--hs-text-light); text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 8px;`
- [ ] `.result-value`: `font-size: 28px; font-weight: 700; color: var(--hs-navy); line-height: 1; margin-bottom: 4px;`
- [ ] `.result-sublabel`: `font-size: 11px; color: var(--hs-text-light);`
- [ ] Card 3 (3-year total): add accent styling — `border-color: var(--hs-blue); background: linear-gradient(135deg, #EBF4FF 0%, #DBEAFE 100%);` and `.result-value` color `var(--hs-blue)`

**updateResultCards() function:**
- [ ] Reads from `calculate()` result object
- [ ] Sets `card-eligible-lives` to `formatNumber(r.ichraEligibleLives)`
- [ ] Sets `card-year1` to `formatMoney(r.year1Revenue)`
- [ ] Sets `card-3yr` to `formatMoney(r.total3yr)`
- [ ] Sets `card-breakeven`:
  - If `r.costModel === 'partner'`: display "N/A" with sublabel "partnering with HS"
  - If `r.breakevenMonths === null` or `r.annualRevenue === 0`: display "—"
  - Otherwise: display `r.breakevenMonths + ' mo'`

- [ ] Commit:
```bash
git commit -m "feat: roi-calculator — 4 result cards with live calculated values"
```

---

### Task 6: 3-Year Pure CSS Bar Chart

**Files:**
- Edit: `healthsherpa-ichra/roi-calculator/index.html`

- [ ] Below `.result-cards`, add `<div class="chart-section">`:
  - Heading: `<h3>` "3-Year Revenue Projection" — font-size 15px, font-weight 600, color `var(--hs-navy)`, margin-bottom 16px
  - `<div class="bar-chart">` containing 3 bar groups

- [ ] Each bar group structure:
```html
<div class="bar-group">
  <div class="bar-label-top" id="chart-y1-label">$0</div>
  <div class="bar-track">
    <div class="bar-fill" id="chart-y1-bar" style="height: 0%;"></div>
  </div>
  <div class="bar-label-bottom">Year 1</div>
</div>
```
- [ ] IDs: `chart-y1-label`, `chart-y1-bar`, `chart-y2-label`, `chart-y2-bar`, `chart-y3-label`, `chart-y3-bar`

**Chart CSS:**
- [ ] `.bar-chart`: `display: flex; gap: 16px; align-items: flex-end; height: 200px; background: white; border: 1px solid var(--hs-border); border-radius: 12px; padding: 20px 24px 16px;`
- [ ] `.bar-group`: `flex: 1; display: flex; flex-direction: column; align-items: center; height: 100%;`
- [ ] `.bar-track`: `flex: 1; width: 100%; background: var(--hs-bg); border-radius: 6px; overflow: hidden; display: flex; align-items: flex-end; margin: 8px 0;`
- [ ] `.bar-fill`: `width: 100%; background: linear-gradient(180deg, var(--hs-blue) 0%, var(--hs-navy) 100%); border-radius: 6px; transition: height 0.4s ease;`
- [ ] Year 3 bar: add `background: linear-gradient(180deg, #34D399 0%, var(--hs-blue) 100%);` to distinguish growth year
- [ ] `.bar-label-top`: `font-size: 11px; font-weight: 600; color: var(--hs-blue); text-align: center; white-space: nowrap;`
- [ ] `.bar-label-bottom`: `font-size: 12px; font-weight: 500; color: var(--hs-text-light); text-align: center;`

**updateChart() function:**
- [ ] Reads `r.year1Revenue`, `r.year2Revenue`, `r.year3Revenue`
- [ ] Finds `maxVal = Math.max(r.year1Revenue, r.year2Revenue, r.year3Revenue)`
- [ ] Sets each bar's `style.height` to `(yearN / maxVal * 100).toFixed(1) + '%'` (if maxVal > 0, else 0%)
- [ ] Sets each label to shorthand format via:
  ```javascript
  function shortMoney(n) {
    if (n >= 1000000) return '$' + (n / 1000000).toFixed(1) + 'M';
    if (n >= 1000) return '$' + (n / 1000).toFixed(0) + 'K';
    return '$' + Math.round(n);
  }
  ```
- [ ] Add note below chart (font-size 11px, color `var(--hs-text-light)`, text-align right): "Year 3 includes 15% growth assumption. All figures illustrative."

- [ ] Commit:
```bash
git commit -m "feat: roi-calculator — pure CSS bar chart with animated height transitions"
```

---

### Task 7: Cannibalization Analysis Section

**Files:**
- Edit: `healthsherpa-ichra/roi-calculator/index.html`

- [ ] Below the chart section, add `<div class="cannibalization-section">`:
  - Green accent card: `background: var(--hs-green-bg); border: 1px solid #A6F4C5; border-radius: 12px; padding: 24px; margin-top: 16px;`
- [ ] Card heading: `<h3>` "The Retention Argument" — font-size 16px, font-weight 600, color `var(--hs-green)`, margin-bottom 12px
- [ ] Subhead: `<p>` "ICHRA is not pure cannibalization — here's why:" — font-size 14px, color `var(--hs-text)`, margin-bottom 16px

- [ ] Stat row (flex, space-between, gap 16px):
  - Stat 1: `<div class="retention-stat">` — big number `<span id="retained-lives-val">—</span>` + label "lives retained in network"
  - Stat 2: Same pattern — `<span id="ichra-eligible-val">—</span>` + label "ICHRA-eligible lives"
  - Stat 3: `<span id="retention-pct-display">70%</span>` + label "group retention rate"

- [ ] `.retention-stat`: `text-align: center; flex: 1;`
- [ ] Big number style: `font-size: 24px; font-weight: 700; color: var(--hs-green); display: block; margin-bottom: 4px;`
- [ ] Label style: `font-size: 12px; color: var(--hs-text-light); font-weight: 500;`

- [ ] Narrative paragraph below stats: `<p id="cannibalization-narrative">` — dynamically generated text:
  ```javascript
  `With a ${retentionRate}% group retention rate, ${formatNumber(retainedLives)} of your
  ${formatNumber(ichraEligibleLives)} ICHRA-eligible members stay in-network as individual
  market enrollees. ICHRA replaces group revenue with individual PMPM — not zero.`
  ```
  Font-size 13px, color `var(--hs-text)`, line-height 1.6, margin-top 12px, padding-top 12px, border-top `1px solid #A6F4C5`

**updateCannibalizationSection() function:**
- [ ] Sets `retained-lives-val` to `formatNumber(r.retainedLives)`
- [ ] Sets `ichra-eligible-val` to `formatNumber(r.ichraEligibleLives)`
- [ ] Sets `retention-pct-display` to `r.retentionRate + '%'`
- [ ] Sets `cannibalization-narrative` innerHTML to narrative string above

- [ ] Commit:
```bash
git commit -m "feat: roi-calculator — cannibalization retention argument section"
```

---

## Chunk 3: Share + CTA

### Task 8: Print-to-PDF Save Button

**Files:**
- Edit: `healthsherpa-ichra/roi-calculator/index.html`

- [ ] Add a `<div class="save-row">` below the cannibalization section, above the CTA:
  - `display: flex; justify-content: flex-end; margin-top: 20px;`
- [ ] Button: `<button onclick="window.print()" class="btn-save">⬇ Save as PDF</button>`
- [ ] `.btn-save` styles: `background: white; border: 1.5px solid var(--hs-border); color: var(--hs-text); padding: 10px 20px; border-radius: 90px; font-size: 14px; font-weight: 500; cursor: pointer; font-family: inherit;`
- [ ] Hover: `border-color: var(--hs-blue); color: var(--hs-blue);`

**Print CSS (`@media print`):**
- [ ] Hide: `.hs-header`, `.hero-section`, `.disclaimer-bar`, `.save-row`, `.cta-section`, `input[type="range"]`, `.toggle-wrapper`, `.warning-badge`
- [ ] Show range slider current values only (they're already in `<span>` elements, so they survive)
- [ ] `.result-card`: add `border: 1pt solid #999; break-inside: avoid;`
- [ ] `.bar-chart`: `break-inside: avoid;`
- [ ] Add a print-only header at top of page: `@media print { .print-header { display: block !important; } }` — `.print-header` is `display: none` normally
- [ ] Print header content: "ICHRA ROI Calculator — Generated by ICHRAverse / HealthSherpa" + date via JS: `document.querySelector('.print-date').textContent = new Date().toLocaleDateString('en-US', {year:'numeric',month:'long',day:'numeric'});`
- [ ] Page title for print: already set in `<title>`, prints at top of PDF by default

- [ ] Commit:
```bash
git commit -m "feat: roi-calculator — print-to-PDF save button with print-friendly CSS"
```

---

### Task 9: Completion CTA

**Files:**
- Edit: `healthsherpa-ichra/roi-calculator/index.html`

- [ ] Add `<div class="cta-section">` as the last element inside `<main>`, below the two-column grid (full-width, not inside either column)
- [ ] Styles: `background: linear-gradient(135deg, var(--hs-navy) 0%, var(--hs-blue) 100%); border-radius: 16px; padding: 40px 32px; text-align: center; margin-top: 32px;`
- [ ] `<h2>` "Ready to validate these numbers with our team?" — white, font-size 22px, font-weight 700, margin-bottom 12px
- [ ] `<p>` "Get real PMPM rates, integration cost clarity, and a tailored revenue model from HealthSherpa's ICHRA experts." — white at 80% opacity, font-size 15px, max-width 520px, margin `0 auto 24px`
- [ ] CTA button: `<a href="https://info.healthsherpa.com/ICHRA" target="_blank" class="btn-cta">Talk to the Team</a>`
- [ ] `.btn-cta` styles: `display: inline-block; background: white; color: var(--hs-navy); padding: 14px 32px; border-radius: 90px; font-size: 15px; font-weight: 600; text-decoration: none; letter-spacing: -0.01em;`
- [ ] Hover: `background: #EBF4FF; transform: translateY(-1px);` with `transition: all 0.2s ease;`
- [ ] Below button: small disclaimer text (white 60% opacity, font-size 11px, margin-top 16px): "All projections are illustrative. HealthSherpa does not guarantee specific revenue outcomes."

- [ ] Commit:
```bash
git commit -m "feat: roi-calculator — completion CTA linking to HealthSherpa ICHRA contact page"
```

---

## Chunk 4: Deploy

### Task 10: Deploy to Netlify

**Files:**
- No file changes — deploy step only

- [ ] Verify the tool file exists at `healthsherpa-ichra/roi-calculator/index.html`
- [ ] Open a browser or test locally with `open healthsherpa-ichra/roi-calculator/index.html` to confirm page loads without errors
- [ ] Check browser console for JS errors — verify `render()` fires on load and all 6 slider updates work
- [ ] Test all 6 slider inputs: confirm live value displays update correctly
- [ ] Test cost model toggle: confirm cost note text updates and break-even card changes between a value and "N/A"
- [ ] Test print: `Cmd+P` in browser — confirm chart, result cards, and input values all appear; confirm hidden elements (header, sliders, CTA) are suppressed
- [ ] Verify CTA link opens `https://info.healthsherpa.com/ICHRA` in new tab
- [ ] From `/Users/joshmait/Desktop/Claude/healthsherpa-ichra/` run:
```bash
npx netlify-cli deploy --prod --dir .
```
- [ ] Confirm deploy URL resolves to `fabulous-frangipane-2cc5ea.netlify.app`
- [ ] Navigate to `fabulous-frangipane-2cc5ea.netlify.app/roi-calculator/index.html` and verify full tool loads
- [ ] Verify "← ICHRAverse Suite" back link navigates to `../index.html` (suite landing)
- [ ] Confirm disclaimer banner is visible above the input panel
- [ ] Confirm sliders update all result cards and bar chart in real time

- [ ] Commit:
```bash
git commit -m "deploy: roi-calculator live at fabulous-frangipane-2cc5ea.netlify.app/roi-calculator/"
```

---

## Summary

| Chunk | Tasks | Deliverable |
|---|---|---|
| 1: Shell + Inputs | 1–3 | Full input panel with 6 sliders, toggle, disclaimer |
| 2: Calculation + Results | 4–7 | Live JS engine, 4 KPI cards, CSS bar chart, retention section |
| 3: Share + CTA | 8–9 | Print-to-PDF, HS contact CTA |
| 4: Deploy | 10 | Live at `/roi-calculator/index.html` on Netlify |

**Key formula reminders:**
- Year 1 is partial: `annualRevenue * ((12 - timeToRevenue) / 12)`
- Year 3 includes 15% growth: `annualRevenue * 1.15`
- Break-even only shown for "build" model; uses $375K midpoint
- Retained lives: `bookSize × (eligiblePct/100) × (retentionRate/100)`
- All defaults labeled illustrative; PMPM has amber ⚠️ warning

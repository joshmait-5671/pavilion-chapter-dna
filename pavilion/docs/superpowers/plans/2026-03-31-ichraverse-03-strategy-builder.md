# ICHRAverse Strategy Builder — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan.

**Goal:** Build a 6-step wizard that helps carrier VPs build an ICHRA strategy in 10 minutes and download a personalized "ICHRA Strategy Brief" PDF.
**Architecture:** Single self-contained HTML file. jsPDF + html2canvas for PDF. No backend. Netlify deploy.
**Tech Stack:** HTML, CSS, JavaScript (vanilla). Inter font. jsPDF + html2canvas via CDN.
**Spec:** `docs/superpowers/specs/2026-03-31-ichraverse-suite-design.md`

---

## Chunk 1: Shell + Step Framework

### Task 1: HTML shell with HS header

**Files:**
- Create: `healthsherpa-ichra/strategy-builder/index.html`

- [ ] Create the file at `healthsherpa-ichra/strategy-builder/index.html`
- [ ] Add `<!DOCTYPE html>` with `lang="en"`, `charset="UTF-8"`, `viewport` meta tag
- [ ] Link Inter font from Google Fonts: `https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap`
- [ ] Define CSS custom properties in `:root`:
  - `--hs-blue: #0970C5`
  - `--hs-navy: #074294`
  - `--hs-border: #D3E0E8`
  - `--hs-text: #344054`
  - `--hs-text-light: #475467`
  - `--hs-bg: #F8FAFC`
  - `--hs-white: #FFFFFF`
  - `--hs-radius-btn: 90px`
  - `--hs-radius-card: 12px`
- [ ] Apply `font-family: 'Inter', sans-serif` globally; `color: var(--hs-text)`; `background: var(--hs-bg)`; `margin: 0`
- [ ] Build a sticky header `<header>` with:
  - Left: back link `← Back to ICHRAverse` pointing to `../index.html` — styled in `--hs-blue`, no underline, `font-size: 14px`
  - Center: HealthSherpa wordmark text "HealthSherpa" in `--hs-navy`, `font-weight: 700`, `font-size: 20px`
  - Right: CTA button "Talk to a Strategist" linking to `https://info.healthsherpa.com/ICHRA` — `background: var(--hs-blue)`, white text, `border-radius: var(--hs-radius-btn)`, `padding: 8px 20px`, `font-size: 14px`, `font-weight: 600`
  - Header styling: `background: white`, `border-bottom: 1px solid var(--hs-border)`, `padding: 16px 40px`, `display: flex; align-items: center; justify-content: space-between`, `position: sticky; top: 0; z-index: 100`
- [ ] Add a page hero section below header (inside `<main>`):
  - Headline: "Build Your ICHRA Strategy" — `font-size: 32px`, `font-weight: 700`, `color: var(--hs-navy)`
  - Subhead: "Answer 6 questions. Get a personalized strategy brief you can take into any room." — `font-size: 16px`, `color: var(--hs-text-light)`
  - Centered, `padding: 48px 40px 32px`
- [ ] Add a `<div id="wizard-container">` centered, `max-width: 680px`, `margin: 0 auto`, `padding: 0 24px 80px`

- [ ] Commit:
```bash
git commit -m "feat: strategy builder — HTML shell and HS header"
```

---

### Task 2: Step indicator (progress bar + numbered steps)

**Files:**
- Modify: `healthsherpa-ichra/strategy-builder/index.html`

- [ ] Above the wizard card, insert a `<div id="step-indicator">` containing:
  - A flex row of 6 step nodes, each a `<div class="step-node">` with:
    - A circle `<div class="step-circle">` showing the step number (1–6)
    - A label `<div class="step-label">` with short names: "Market Position", "Employer Segments", "Product Design", "Integration", "Broker Strategy", "Timeline"
    - A connecting line between nodes (except after node 6) — `<div class="step-connector">`
  - Step circle styles:
    - Default: `width: 32px; height: 32px; border-radius: 50%; background: white; border: 2px solid var(--hs-border); color: var(--hs-text-light); font-size: 13px; font-weight: 600; display: flex; align-items: center; justify-content: center`
    - Active (`.step-node.active .step-circle`): `background: var(--hs-blue); border-color: var(--hs-blue); color: white`
    - Completed (`.step-node.completed .step-circle`): `background: var(--hs-navy); border-color: var(--hs-navy); color: white` — replace number with checkmark `✓`
  - Step label styles: `font-size: 11px; color: var(--hs-text-light); margin-top: 6px; text-align: center; white-space: nowrap`
  - Active label: `color: var(--hs-blue); font-weight: 600`
  - Connector styles: `flex: 1; height: 2px; background: var(--hs-border); margin: 0 4px; margin-top: -20px` (aligns with circle center)
  - Completed connector: `background: var(--hs-navy)`
- [ ] Below the step nodes, add a progress bar:
  - Outer: `<div id="progress-bar-track">` — `height: 4px; background: var(--hs-border); border-radius: 2px; margin-top: 16px`
  - Inner: `<div id="progress-bar-fill">` — `height: 100%; background: var(--hs-blue); border-radius: 2px; transition: width 0.3s ease`
  - Width controlled by JS: `((currentStep - 1) / 6) * 100 + '%'` (0% on step 1, 100% when all complete)
- [ ] Add JS function `updateStepIndicator(currentStep)`:
  - Loops over all `.step-node` elements (index 0–5)
  - Adds class `completed` if index < currentStep - 1
  - Adds class `active` if index === currentStep - 1
  - Removes both classes otherwise
  - Updates progress bar fill width
  - Replaces number with `✓` in completed circles, restores number in non-completed

- [ ] Commit:
```bash
git commit -m "feat: strategy builder — step indicator and progress bar"
```

---

### Task 3: Step navigation (Next/Back buttons, keyboard support, validation)

**Files:**
- Modify: `healthsherpa-ichra/strategy-builder/index.html`

- [ ] Add a `<div id="step-card">` inside `#wizard-container` — this is the main card container:
  - `background: white; border-radius: var(--hs-radius-card); border: 1px solid var(--hs-border); padding: 40px; margin-top: 24px`
  - `box-shadow: 0 1px 4px rgba(0,0,0,0.06)`
- [ ] Inside `#step-card`, add `<div id="step-content">` where step HTML is injected by JS
- [ ] Below `#step-card`, add `<div id="step-nav">` with:
  - Left: `<button id="btn-back">← Back</button>` — outline style: `border: 1px solid var(--hs-border); background: white; color: var(--hs-text); border-radius: var(--hs-radius-btn); padding: 12px 28px; font-size: 15px; font-weight: 600; cursor: pointer`
  - Right: `<button id="btn-next">Next →</button>` — filled style: `background: var(--hs-blue); color: white; border: none; border-radius: var(--hs-radius-btn); padding: 12px 28px; font-size: 15px; font-weight: 600; cursor: pointer`
  - Nav container: `display: flex; justify-content: space-between; align-items: center; margin-top: 24px`
  - On step 1, hide Back button (`display: none`)
  - On step 6, change Next button label to "Build My Strategy Brief →"
- [ ] Add JS state object `const state = { currentStep: 1, answers: {} }`
- [ ] Add JS function `renderStep(stepNum)`:
  - Injects the appropriate step HTML into `#step-content`
  - Calls `updateStepIndicator(stepNum)`
  - Restores previously selected answer if user navigated back (checks `state.answers[stepNum]`)
  - Manages Back button visibility
  - Updates Next button label on step 6
- [ ] Add JS function `validateStep(stepNum)` → returns `true` if at least one option is selected for the given step; otherwise shows inline error message "Please select an option to continue." in red (`color: #D92D20; font-size: 14px; margin-top: 12px`) and returns `false`
- [ ] Wire `#btn-next` click:
  - Calls `saveAnswer(state.currentStep)` to store selection in `state.answers`
  - Calls `validateStep(state.currentStep)` — aborts if false
  - If `state.currentStep < 6`: increments `state.currentStep`, calls `renderStep(state.currentStep)`
  - If `state.currentStep === 6`: calls `showResultsPage()`
- [ ] Wire `#btn-back` click:
  - Saves current answer first
  - Decrements `state.currentStep`, calls `renderStep(state.currentStep)`
- [ ] Add keyboard support via `document.addEventListener('keydown', ...)`:
  - `Enter` or `ArrowRight`: triggers Next button click
  - `ArrowLeft`: triggers Back button click
- [ ] Add JS function `saveAnswer(stepNum)`:
  - For radio inputs: stores `document.querySelector('input[name="step' + stepNum + '"]:checked')?.value`
  - For checkbox inputs: stores array of checked values
  - Saves to `state.answers[stepNum]`
- [ ] On page load, call `renderStep(1)` to initialize

- [ ] Commit:
```bash
git commit -m "feat: strategy builder — step navigation, validation, keyboard support"
```

---

## Chunk 2: The 6 Steps

### Task 4: Step 1 — Market Position

**Files:**
- Modify: `healthsherpa-ichra/strategy-builder/index.html`

- [ ] Create JS function `renderStep1()` that returns HTML string for step 1:
  - Step tag: `<div class="step-tag">Step 1 of 6</div>` — `font-size: 12px; font-weight: 600; color: var(--hs-blue); text-transform: uppercase; letter-spacing: 0.5px; margin-bottom: 12px`
  - Title: `<h2>Market Position</h2>` — `font-size: 24px; font-weight: 700; color: var(--hs-navy); margin-bottom: 8px`
  - Guiding question: `<p class="step-question">How does your carrier currently think about individual market vs. group?</p>` — `font-size: 16px; color: var(--hs-text-light); margin-bottom: 28px`
  - 4 radio options as styled option cards (see option card spec below):
    1. value: `individual-leader` | Label: "Individual Market Leader" | Description: "We have strong ACA/marketplace presence and want ICHRA to extend it"
    2. value: `group-with-exposure` | Label: "Strong Group with Individual Exposure" | Description: "Group is our core but we've dabbled in individual — ICHRA is our bridge"
    3. value: `primarily-group` | Label: "Primarily Group" | Description: "We're a group carrier looking to expand — individual is new territory"
    4. value: `exploring` | Label: "Exploring Individual" | Description: "We're evaluating the market before committing to a direction"
- [ ] Option card spec (applies to all steps):
  - Each option is a `<label class="option-card">` wrapping a hidden `<input type="radio" name="step1" value="...">` and the visible content
  - Card styles: `display: flex; align-items: flex-start; gap: 14px; padding: 16px 20px; border: 1.5px solid var(--hs-border); border-radius: var(--hs-radius-card); cursor: pointer; margin-bottom: 12px; transition: border-color 0.15s, background 0.15s`
  - Hover state: `border-color: var(--hs-blue); background: #F0F7FF`
  - Selected state (via JS class `.selected`): `border-color: var(--hs-blue); background: #EBF4FF`
  - Custom radio circle: `<div class="radio-circle">` — `width: 18px; height: 18px; border-radius: 50%; border: 2px solid var(--hs-border); flex-shrink: 0; margin-top: 2px; transition: border-color 0.15s`
  - Selected radio circle: `border-color: var(--hs-blue); background: var(--hs-blue)` with inner white dot via `box-shadow: inset 0 0 0 3px white`
  - Option label text: `font-size: 15px; font-weight: 600; color: var(--hs-text)`
  - Option description text: `font-size: 13px; color: var(--hs-text-light); margin-top: 2px`
- [ ] Add JS event delegation: on click of any `.option-card` inside `#step-content`, remove `.selected` from all cards in that step, add `.selected` to clicked card, update the radio input's checked state, and update the radio circle styles

- [ ] Commit:
```bash
git commit -m "feat: strategy builder — step 1 market position"
```

---

### Task 5: Step 2 — Employer Segments

**Files:**
- Modify: `healthsherpa-ichra/strategy-builder/index.html`

- [ ] Create JS function `renderStep2()` that returns HTML string for step 2:
  - Step tag: "Step 2 of 6"
  - Title: "Employer Segments"
  - Guiding question: "Which employer segments are in scope for ICHRA?"
  - Instruction note: `<p class="multi-note">Select all that apply.</p>` — `font-size: 13px; color: var(--hs-text-light); margin-bottom: 20px; font-style: italic`
  - 5 checkbox options (use `<input type="checkbox" name="step2" value="...">` instead of radio):
    1. value: `1-50` | Label: "1–50 Employees" | Description: "Small employers — highest ICHRA adoption today, pure defined contribution play"
    2. value: `51-100` | Label: "51–100 Employees" | Description: "Mid-small — often ALE-adjacent, strong interest in cost predictability"
    3. value: `100-500` | Label: "100–500 Employees" | Description: "Mid-market — evaluating ICHRA as supplement or full replacement"
    4. value: `500-plus` | Label: "500+ Employees" | Description: "Large employers — often complex, may require custom network and support"
    5. value: `all` | Label: "All Segments" | Description: "We want full market coverage — prioritization TBD"
  - Checkbox card spec: same option card styling as radio, but uses checkmark icon instead of radio circle
  - Checkmark icon: `<div class="check-box">` — `width: 18px; height: 18px; border-radius: 4px; border: 2px solid var(--hs-border); flex-shrink: 0; margin-top: 2px`
  - Selected checkbox: `border-color: var(--hs-blue); background: var(--hs-blue)` with white `✓` centered inside (`font-size: 11px; color: white; display: flex; align-items: center; justify-content: center`)
- [ ] Step 2 validation: at least one checkbox must be checked before advancing
- [ ] In `saveAnswer(2)`: collect array of all checked checkbox values for step 2

- [ ] Commit:
```bash
git commit -m "feat: strategy builder — step 2 employer segments"
```

---

### Task 6: Step 3 — Product Design

**Files:**
- Modify: `healthsherpa-ichra/strategy-builder/index.html`

- [ ] Create JS function `renderStep3()` that returns HTML string for step 3:
  - Step tag: "Step 3 of 6"
  - Title: "Product Design"
  - Guiding question: "What's your ICHRA product approach?"
  - 5 radio options:
    1. value: `off-shelf-aca` | Label: "Off-the-Shelf ACA Plans" | Description: "Use existing marketplace plans as-is — fastest to market, lowest lift"
    2. value: `curated-tier` | Label: "Curated Plan Tier" | Description: "Subset of plans curated for ICHRA employers — quality over breadth"
    3. value: `white-label` | Label: "White-Label Plans" | Description: "Plans branded and structured specifically for ICHRA employer relationships"
    4. value: `employer-custom` | Label: "Employer-Specific Custom" | Description: "Bespoke plan designs per employer — maximum flexibility, maximum complexity"
    5. value: `not-decided` | Label: "Not Decided Yet" | Description: "We need to understand the tradeoffs before committing to a product approach"

- [ ] Commit:
```bash
git commit -m "feat: strategy builder — step 3 product design"
```

---

### Task 7: Step 4 — Integration Approach

**Files:**
- Modify: `healthsherpa-ichra/strategy-builder/index.html`

- [ ] Create JS function `renderStep4()` that returns HTML string for step 4:
  - Step tag: "Step 4 of 6"
  - Title: "Integration Approach"
  - Guiding question: "How do you want to connect to ICHRA platforms and administrators?"
  - 5 radio options:
    1. value: `direct-api` | Label: "Direct API Integrations" | Description: "Build point-to-point connections with each major ICHRA platform — full control"
    2. value: `aggregator` | Label: "Third-Party Aggregator" | Description: "Use an aggregator layer to reach multiple platforms through one integration"
    3. value: `ichraX` | Label: "Neutral Standards Body (ICHRAx)" | Description: "Align to the emerging industry standard for interoperability across the ecosystem"
    4. value: `healthsherpa-infra` | Label: "HealthSherpa Infrastructure" | Description: "Leverage HealthSherpa's existing carrier and administrator connections"
    5. value: `undecided-integration` | Label: "Undecided" | Description: "We haven't evaluated integration options in depth yet"

- [ ] Commit:
```bash
git commit -m "feat: strategy builder — step 4 integration approach"
```

---

### Task 8: Step 5 — Broker Strategy

**Files:**
- Modify: `healthsherpa-ichra/strategy-builder/index.html`

- [ ] Create JS function `renderStep5()` that returns HTML string for step 5:
  - Step tag: "Step 5 of 6"
  - Title: "Broker Strategy"
  - Guiding question: "What role will brokers play in your ICHRA distribution model?"
  - 4 radio options:
    1. value: `primary-distribution` | Label: "Primary Distribution Channel" | Description: "Brokers are central — we'll invest in broker tools, training, and comp structures"
    2. value: `supplemental` | Label: "Supplemental Channel" | Description: "Brokers complement direct and platform channels — important but not primary"
    3. value: `direct-only` | Label: "Direct to Employer Only" | Description: "We're going direct — no broker layer in the ICHRA model"
    4. value: `undecided-broker` | Label: "Undecided" | Description: "We need to evaluate broker appetite and market dynamics before deciding"

- [ ] Commit:
```bash
git commit -m "feat: strategy builder — step 5 broker strategy"
```

---

### Task 9: Step 6 — Timeline

**Files:**
- Modify: `healthsherpa-ichra/strategy-builder/index.html`

- [ ] Create JS function `renderStep6()` that returns HTML string for step 6:
  - Step tag: "Step 6 of 6"
  - Title: "Timeline"
  - Guiding question: "When do you need to be ICHRA-ready?"
  - Subtext below question: `<p class="step-subtext">"ICHRA-ready" means: compliant plans available, integration live, and distribution activated.</p>` — `font-size: 13px; color: var(--hs-text-light); margin-bottom: 24px; font-style: italic`
  - 4 radio options:
    1. value: `within-6mo` | Label: "Within 6 Months" | Description: "We have a committed date — need to move fast and make decisions now"
    2. value: `6-12mo` | Label: "6–12 Months" | Description: "We have a planning horizon — building the roadmap and sequencing work"
    3. value: `12-24mo` | Label: "12–24 Months" | Description: "We're building deliberately — plenty of time but want to get the strategy right"
    4. value: `exploring-only` | Label: "Exploring Only (No Committed Date)" | Description: "We're in research mode — no hard date, but want to understand the landscape"
  - After the options, add a motivating note: `<div class="timeline-note">` with text "Regardless of your timeline, your strategy brief will include a recommended sequencing for your first 90 days." — styled with light blue background (`background: #EBF4FF; border-left: 3px solid var(--hs-blue); padding: 12px 16px; border-radius: 6px; font-size: 13px; color: var(--hs-text); margin-top: 24px`)
- [ ] On step 6, change Next button text to "Build My Strategy Brief →"

- [ ] Commit:
```bash
git commit -m "feat: strategy builder — step 6 timeline"
```

---

## Chunk 3: PDF Output

### Task 10: Results summary page

**Files:**
- Modify: `healthsherpa-ichra/strategy-builder/index.html`

- [ ] Create JS function `showResultsPage()` that:
  - Hides `#step-indicator`, `#step-card`, `#step-nav`
  - Shows `#results-page` div (hidden by default with `display: none`)
- [ ] Build `#results-page` HTML (injected into DOM on load, hidden initially):
  - Hero section:
    - Icon: `✓` in a green circle (`background: #ECFDF3; color: #027A48; width: 48px; height: 48px; border-radius: 50%`) — centered
    - Headline: "Your ICHRA Strategy Brief is Ready" — `font-size: 28px; font-weight: 700; color: var(--hs-navy); text-align: center`
    - Subhead: "Here's a summary of your strategy. Add your company name and download the PDF." — centered, `color: var(--hs-text-light)`
  - Company name input field:
    - Label: "Your Company Name" — `font-size: 14px; font-weight: 600`
    - Input `<input type="text" id="company-name" placeholder="e.g. Acme Health Plan">` — `width: 100%; padding: 12px 16px; border: 1.5px solid var(--hs-border); border-radius: 8px; font-size: 15px; font-family: Inter, sans-serif; box-sizing: border-box`
    - Focus state: `border-color: var(--hs-blue); outline: none`
    - Wrapper: `max-width: 400px; margin: 24px auto`
  - Summary card `<div id="summary-card">`:
    - `background: white; border: 1px solid var(--hs-border); border-radius: var(--hs-radius-card); padding: 32px; max-width: 600px; margin: 24px auto`
    - Header row: HealthSherpa wordmark (left) + "ICHRA Strategy Brief" label (right, `font-size: 12px; font-weight: 600; color: var(--hs-blue); text-transform: uppercase`)
    - Divider: `border-top: 1px solid var(--hs-border); margin: 16px 0`
    - 6 answer rows, each:
      - Step label: `font-size: 12px; font-weight: 600; color: var(--hs-text-light); text-transform: uppercase; letter-spacing: 0.4px`
      - Answer value: `font-size: 15px; font-weight: 600; color: var(--hs-text); margin-top: 2px`
      - Separator line between rows
    - "Recommended Next Steps" section (below answer rows):
      - Section title: `font-size: 14px; font-weight: 700; color: var(--hs-navy); margin-top: 24px; margin-bottom: 12px`
      - Populated by JS function `generateNextSteps(answers)` — returns an array of 3 bullet strings based on answers (see logic below)
      - Each bullet: `<div class="next-step-item">` with `→` prefix, `font-size: 14px; color: var(--hs-text); margin-bottom: 8px`
    - HS contact block at bottom of card:
      - `background: var(--hs-navy); color: white; border-radius: 8px; padding: 20px; margin-top: 24px; text-align: center`
      - Text: "Ready to activate this strategy?" `font-size: 15px; font-weight: 600`
      - Sub-text: "HealthSherpa works with carriers at every stage of ICHRA readiness." `font-size: 13px; opacity: 0.85; margin-top: 4px`
      - Contact: "ichra@healthsherpa.com" in white, underlined
- [ ] Implement `generateNextSteps(answers)` logic:
  - If step 1 answer is `individual-leader`: include "Leverage your existing ACA book to lead employer groups toward ICHRA migration"
  - If step 1 answer is `primarily-group` or `exploring`: include "Start with a pilot segment (1–50 employees) to build ICHRA operational muscle before scaling"
  - If step 2 answers include `1-50`: include "Prioritize small group ICHRA — the market is live today and growing quarter over quarter"
  - If step 3 answer is `not-decided`: include "Run a 2-week product design sprint to select your initial plan approach before committing to integration"
  - If step 4 answer is `healthsherpa-infra`: include "Engage HealthSherpa's carrier integration team for an accelerated onboarding assessment"
  - If step 4 answer is `ichraX`: include "Align your technical roadmap to ICHRAx standards for maximum long-term interoperability"
  - If step 5 answer is `primary-distribution`: include "Build broker portal and comp structures in parallel with product — distribution readiness gates launch"
  - If step 6 answer is `within-6mo`: include "With a 6-month horizon, week-by-week sequencing is critical — start integration conversations this week"
  - If step 6 answer is `exploring-only`: include "Commission a carrier readiness assessment to identify your critical path before committing to a timeline"
  - Default fallback (always include if fewer than 3 bullets selected): "Schedule a strategy review with HealthSherpa to pressure-test your approach before execution"
  - Return exactly 3 items (truncate or pad with fallback as needed)
- [ ] Call `populateSummaryCard(state.answers)` inside `showResultsPage()` to fill in all answer rows and next steps

- [ ] Commit:
```bash
git commit -m "feat: strategy builder — results summary page with dynamic next steps"
```

---

### Task 11: PDF generation with jsPDF + html2canvas

**Files:**
- Modify: `healthsherpa-ichra/strategy-builder/index.html`

- [ ] Add CDN scripts in `<head>` (load after page content):
  ```html
  <script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/2.5.1/jspdf.umd.min.js"></script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/html2canvas/1.4.1/html2canvas.min.js"></script>
  ```
- [ ] Add "Download Strategy Brief (PDF)" button to results page:
  - `<button id="btn-download-pdf">⬇ Download Strategy Brief (PDF)</button>`
  - Styles: `background: var(--hs-blue); color: white; border: none; border-radius: var(--hs-radius-btn); padding: 14px 32px; font-size: 16px; font-weight: 600; cursor: pointer; display: block; margin: 24px auto`
  - Loading state: on click, change text to "Generating PDF..." and disable button; restore on completion
- [ ] Implement `downloadPDF()` function:
  - Get company name from `#company-name` input (default to "Your Carrier" if empty)
  - Call `html2canvas(document.getElementById('summary-card'), { scale: 2, useCORS: true, backgroundColor: '#FFFFFF' })`
  - On canvas ready:
    - Create `new jspdf.jsPDF({ orientation: 'portrait', unit: 'mm', format: 'a4' })`
    - Set PDF title metadata: `doc.setProperties({ title: 'ICHRA Strategy Brief — ' + companyName })`
    - Add HS blue header band at top: `doc.setFillColor(9, 112, 197)` then `doc.rect(0, 0, 210, 22, 'F')`
    - Add white title text in header: "ICHRA Strategy Brief" — `doc.setTextColor(255,255,255); doc.setFontSize(16); doc.setFont('helvetica','bold'); doc.text('ICHRA Strategy Brief', 14, 14)`
    - Add company name in header (right-aligned): `doc.setFontSize(11); doc.setFont('helvetica','normal'); doc.text(companyName, 196, 14, { align: 'right' })`
    - Add generated date below header: `doc.setTextColor(100,100,100); doc.setFontSize(9); doc.text('Generated ' + new Date().toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' }), 14, 30)`
    - Convert canvas to image: `const imgData = canvas.toDataURL('image/png')`
    - Calculate image dimensions to fit A4 width (186mm usable): `const imgWidth = 186; const imgHeight = (canvas.height * imgWidth) / canvas.width`
    - Add image: `doc.addImage(imgData, 'PNG', 12, 34, imgWidth, imgHeight)`
    - Add HS blue footer band: `doc.setFillColor(9, 112, 197)` then `doc.rect(0, 282, 210, 15, 'F')`
    - Footer text: `doc.setTextColor(255,255,255); doc.setFontSize(9); doc.text('HealthSherpa ICHRA Suite  |  ichra@healthsherpa.com  |  healthsherpa.com', 105, 291, { align: 'center' })`
    - Save: `doc.save('ICHRA-Strategy-Brief-' + companyName.replace(/\s+/g, '-') + '.pdf')`
  - Wrap in try/catch; on error show alert "PDF generation failed. Please try again."
  - Restore button text and re-enable on completion
- [ ] Wire `#btn-download-pdf` click to `downloadPDF()`

- [ ] Commit:
```bash
git commit -m "feat: strategy builder — PDF generation with jsPDF and html2canvas"
```

---

### Task 12: Completion CTA

**Files:**
- Modify: `healthsherpa-ichra/strategy-builder/index.html`

- [ ] Below the download button on the results page, add a completion CTA section `<div id="completion-cta">`:
  - Outer: `max-width: 600px; margin: 0 auto; text-align: center; padding: 32px 0 64px`
  - Divider line above: `border-top: 1px solid var(--hs-border); margin-bottom: 32px`
  - Headline: "Want us to review your strategy?" — `font-size: 22px; font-weight: 700; color: var(--hs-navy)`
  - Subhead: "Our ICHRA team works with carriers at every stage — from first exploration to full activation. A 30-minute review can unlock your critical path." — `font-size: 15px; color: var(--hs-text-light); margin: 12px 0 24px; max-width: 480px; margin-left: auto; margin-right: auto`
  - CTA button: `<a href="https://info.healthsherpa.com/ICHRA" target="_blank" id="btn-review-cta">Request a Strategy Review →</a>`
    - Styles: `display: inline-block; background: var(--hs-navy); color: white; text-decoration: none; border-radius: var(--hs-radius-btn); padding: 16px 36px; font-size: 16px; font-weight: 700`
    - Hover: `background: #052f6b`
  - Below button: `<p class="cta-note">Or email us directly: <a href="mailto:ichra@healthsherpa.com">ichra@healthsherpa.com</a></p>` — `font-size: 13px; color: var(--hs-text-light); margin-top: 16px`
    - Email link: `color: var(--hs-blue); text-decoration: none`
- [ ] Add a "Start Over" text link below the CTA: `<a href="#" id="btn-restart">← Start over</a>` — `font-size: 14px; color: var(--hs-text-light); display: block; margin-top: 24px; text-decoration: none`
  - On click: reset `state = { currentStep: 1, answers: {} }`, hide results page, show step indicator + step card + step nav, call `renderStep(1)`

- [ ] Commit:
```bash
git commit -m "feat: strategy builder — completion CTA and restart flow"
```

---

## Chunk 4: Deploy

### Task 13: Deploy to Netlify

**Files:**
- No file changes — deploy from `/Users/joshmait/Desktop/Claude/healthsherpa-ichra/`

- [ ] Verify `healthsherpa-ichra/strategy-builder/index.html` exists and is complete
- [ ] Verify `healthsherpa-ichra/index.html` has a link to `./strategy-builder/index.html` (the Strategy Builder card in the tool grid should already exist from the suite nav)
- [ ] From `/Users/joshmait/Desktop/Claude/healthsherpa-ichra/`, run:
  ```bash
  npx netlify-cli deploy --prod --dir . --site fabulous-frangipane-2cc5ea
  ```
- [ ] Confirm deploy URL: `https://fabulous-frangipane-2cc5ea.netlify.app/strategy-builder/index.html`
- [ ] Test the live URL:
  - All 6 steps render correctly
  - Back/Next navigation works
  - Validation blocks advance without selection
  - Results page populates all 6 answers
  - PDF downloads with correct filename and company name
  - "Request a Strategy Review" CTA opens `https://info.healthsherpa.com/ICHRA` in new tab
  - "Start over" link resets wizard to step 1
- [ ] Commit final deploy confirmation:
  ```bash
  git commit -m "feat: strategy builder — deployed to Netlify (fabulous-frangipane-2cc5ea)"
  ```

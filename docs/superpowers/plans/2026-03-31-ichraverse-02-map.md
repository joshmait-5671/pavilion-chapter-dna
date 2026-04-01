# ICHRAverse ICHRA Adoption Map — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build an interactive US map showing ICHRA adoption by state — employer count, covered lives, YoY growth, active carriers, active platforms. Mock data pre-wired with the exact schema HealthSherpa needs to plug in live data.

**Architecture:** Single `map/index.html` file. SVG-based US map (no external tile servers). D3.js for data binding and choropleth coloring. Tooltip on hover. Three layers: adoption intensity, carriers, platforms. Data loaded from `data/states.json`. Live data hookup: swap one URL in config.

**Tech Stack:** HTML, CSS, JavaScript (vanilla + D3.js v7 via CDN). No backend.

**Spec:** `docs/superpowers/specs/2026-03-31-ichraverse-suite-design.md`

**Accuracy note:** All mock data must be labeled "Sample data — replace with live HealthSherpa data." No invented statistics presented as real. Growth percentages sourced from HRA Council where used.

---

## Chunk 1: Data Structure + Mock Data

### Task 1: Create mock data files

**Files:**
- Create: `healthsherpa-ichra/data/states.json`
- Create: `healthsherpa-ichra/data/carriers.json`
- Create: `healthsherpa-ichra/data/platforms.json`
- Create: `healthsherpa-ichra/data/README.md`

- [ ] Create `states.json` with all 50 states + DC. Schema:
```json
{
  "states": [
    {
      "code": "TX",
      "name": "Texas",
      "employers": 4200,
      "covered_lives": 18500,
      "yoy_growth_pct": 134,
      "carriers_active": 8,
      "platforms_active": 12,
      "market_stage": "early_growth",
      "data_note": "Sample data — replace with live HealthSherpa data"
    }
  ]
}
```

- [ ] `market_stage` values: `"nascent"` | `"early_growth"` | `"accelerating"` | `"leading"` — drives map color intensity.

- [ ] Populate all 50 states + DC with plausible but clearly mock data. Higher adoption in TX, FL, CA, NY, IL, OH. Lower in MT, WY, ND, SD, AK. Labeled mock throughout.

- [ ] Create `carriers.json`:
```json
{
  "carriers": [
    {
      "id": "centene",
      "name": "Centene / Ambetter",
      "states": ["TX","FL","GA","OH","AZ","NV","WA","KY","MS","NM"],
      "ichra_status": "active",
      "hs_connected": true
    }
  ]
}
```

- [ ] Create `platforms.json` with 15 named platforms (use real names from research: Remodel Health, Take Command, Venteur, Nexben, Thatch, Zorro, Gravie, BenefitBay, zizzl, Alegeus, BenefitFocus, etc.), states active, hs_connected flag.

- [ ] Create `data/README.md` explaining schema and how to swap mock for live data.

- [ ] Commit:
```bash
git add healthsherpa-ichra/data/
git commit -m "feat: ichra map mock data files"
```

---

## Chunk 2: Map Shell + SVG

### Task 2: HTML shell with HS header

**Files:**
- Create: `healthsherpa-ichra/map/index.html`

- [ ] Create file: DOCTYPE, head, Google Fonts (Inter), D3.js v7 CDN (`https://cdn.jsdelivr.net/npm/d3@7`), title "ICHRA Adoption Map | ICHRAverse".

- [ ] Add shared HS header matching dashboard: blue bg, "ICHRAverse" brand, "← Back to suite" link, "Talk to our ICHRA team →" CTA button.

- [ ] Add page intro: H1 "ICHRA Adoption Map", subhead "Where ICHRA is growing — by state, by carrier, by platform. Data reflects the HealthSherpa ICHRA network."

- [ ] Add mock data disclaimer banner: light yellow bg, "📊 Displaying sample data. Live HealthSherpa network data available via API integration."

- [ ] Verify: page loads, header renders, no JS errors.

- [ ] Commit:
```bash
git commit -m "feat: ichra map shell and header"
```

---

### Task 3: US SVG Map + Choropleth

**Files:**
- Modify: `healthsherpa-ichra/map/index.html`

- [ ] Load all three data files at initialization. Use `Promise.all` so all data is available before rendering:
```javascript
Promise.all([
  d3.json("../data/states.json"),
  d3.json("../data/carriers.json"),
  d3.json("../data/platforms.json"),
  d3.json("https://cdn.jsdelivr.net/npm/us-atlas@3/states-10m.json")
]).then(([statesData, carriersData, platformsData, topoData]) => {
  // store globally for sidebar + layer toggles
  window.APP = { statesData, carriersData, platformsData };
  renderMap(topoData, statesData);
});
```

- [ ] Build FIPS-to-state-code lookup. TopoJSON features use FIPS numeric IDs (e.g., `48` = Texas), not state codes. Add this hardcoded lookup before render:
```javascript
const FIPS_TO_CODE = {
  "01":"AL","02":"AK","04":"AZ","05":"AR","06":"CA","08":"CO","09":"CT",
  "10":"DE","11":"DC","12":"FL","13":"GA","15":"HI","16":"ID","17":"IL",
  "18":"IN","19":"IA","20":"KS","21":"KY","22":"LA","23":"ME","24":"MD",
  "25":"MA","26":"MI","27":"MN","28":"MS","29":"MO","30":"MT","31":"NE",
  "32":"NV","33":"NH","34":"NJ","35":"NM","36":"NY","37":"NC","38":"ND",
  "39":"OH","40":"OK","41":"OR","42":"PA","44":"RI","45":"SC","46":"SD",
  "47":"TN","48":"TX","49":"UT","50":"VT","51":"VA","53":"WA","54":"WV",
  "55":"WI","56":"WY"
};
// Build lookup: state code → state data object
const stateByCode = new Map(statesData.states.map(s => [s.code, s]));
```

- [ ] In `renderMap`, join each TopoJSON feature to state data via FIPS:
```javascript
const stateCode = FIPS_TO_CODE[String(feature.id).padStart(2,"0")];
const stateInfo = stateByCode.get(stateCode);
const stage = stateInfo ? stateInfo.market_stage : "nascent";
```

- [ ] Color scale based on `market_stage`:
```javascript
const colorScale = {
  "nascent": "#E8F4FD",
  "early_growth": "#93C5FD",
  "accelerating": "#2EB6FF",
  "leading": "#0970C5"
};
```

- [ ] Each state path: fill from colorScale, `stroke: white`, `stroke-width: 0.5`. Hover: darken fill, `cursor: pointer`.

- [ ] Map container: full-width, max-height 500px, centered. SVG responsive (viewBox, preserveAspectRatio).

- [ ] Verify: map renders all 50 states + DC, colored by adoption stage, no blank/gray states.

- [ ] Commit:
```bash
git commit -m "feat: ichra map choropleth render with FIPS lookup"
```

---

### Task 4: Hover Tooltip

**Files:**
- Modify: `healthsherpa-ichra/map/index.html`

- [ ] Create floating tooltip div (absolute positioned, white bg, shadow, border-radius 8px, 16px padding).

- [ ] On state `mouseover`: populate tooltip with:
  - State name (bold, 16px, hs-blue)
  - Employers using ICHRA: `4,200` (formatted with commas)
  - Covered lives: `18,500`
  - YoY growth: `+134%`
  - Active carriers: `8`
  - Active platforms: `12`
  - "Sample data" note in gray italic

- [ ] On `mousemove`: reposition tooltip to follow cursor (offset 12px from pointer).

- [ ] On `mouseleave`: hide tooltip.

- [ ] Verify: hover any state → tooltip appears with correct data, follows mouse, disappears on leave.

- [ ] Commit:
```bash
git commit -m "feat: ichra map state tooltip"
```

---

## Chunk 3: Layer Controls + Sidebar

### Task 5: Layer Toggle Controls

**Files:**
- Modify: `healthsherpa-ichra/map/index.html`

- [ ] Add 3 toggle buttons above map:
  - "Adoption Intensity" (active by default, blue)
  - "Carrier Coverage"
  - "Platform Network"

- [ ] Toggle behavior:
  - **Adoption Intensity:** choropleth coloring (default view)
  - **Carrier Coverage:** overlay carrier dots on states where `hs_connected: true` carriers are active. Dot size = carrier count. Position using `d3.geoCentroid(feature)` through the Albers USA projection: `const [cx, cy] = projection(d3.geoCentroid(feature));`
  - **Platform Network:** overlay platform dots. Green = connected to HS. Gray = not connected.

- [ ] Active toggle: solid blue bg, white text. Inactive: white bg, blue border.

- [ ] Verify: clicking toggles changes map visual correctly.

- [ ] Commit:
```bash
git commit -m "feat: ichra map layer toggles"
```

---

### Task 6: State Detail Sidebar

**Files:**
- Modify: `healthsherpa-ichra/map/index.html`

- [ ] On state `click`: open right sidebar (320px wide, slides in). Contains:
  - State name + adoption stage badge (color-coded pill — US state flag emojis don't exist in Unicode, use stage badge instead)
  - Adoption stage badge (color-coded pill)
  - Stats grid: employers, covered lives, YoY growth
  - "Carriers active in [State]" — list from `carriers.json` with HS-connected badge
  - "Platforms active in [State]" — list from `platforms.json`
  - "Sample data" disclaimer at bottom
  - Close (×) button

- [ ] Map shrinks to accommodate sidebar on click (flexbox layout).

- [ ] Verify: click Texas → sidebar shows with all data populated, close button works.

- [ ] Commit:
```bash
git commit -m "feat: ichra map state detail sidebar"
```

---

## Chunk 4: Legend + Footer + Deploy

### Task 7: Legend + National Stats Bar

**Files:**
- Modify: `healthsherpa-ichra/map/index.html`

- [ ] Add map legend (bottom-left): 4 color swatches with labels (Nascent / Early Growth / Accelerating / Leading). Small, unobtrusive.

- [ ] Add national summary bar below map:
  - Total employers on ICHRA: "500K–1M" (HRA Council 2025)
  - HS-connected platforms: "40+"
  - States with active ICHRA market: count from data
  - YoY growth: "124%" (HRA Council "Growth Trends for ICHRA & QSEHRA" Volume 4, June 2025 — https://www.hracouncil.org/report)
  - All figures sourced.

- [ ] Commit:
```bash
git commit -m "feat: ichra map legend and national stats"
```

---

### Task 8: Live Data Hookup Config

**Files:**
- Modify: `healthsherpa-ichra/map/index.html`

- [ ] Add config block at top of script:
```javascript
const CONFIG = {
  dataSource: "mock", // Change to "live" to use HS API
  mockDataPath: "../data/states.json",
  liveApiEndpoint: "https://api.healthsherpa.com/ichra/v1/map-data", // placeholder
  apiKey: "" // SECURITY NOTE: Never put a real API key here. For live mode, route through a Netlify serverless function proxy that holds the key server-side. Client-side key exposure = public credential leak.
};
```

- [ ] Data loading respects CONFIG:
```javascript
const dataUrl = CONFIG.dataSource === "live"
  ? CONFIG.liveApiEndpoint
  : CONFIG.mockDataPath;
```

- [ ] Add `data/README.md` section: "To switch to live data: change CONFIG.dataSource to 'live', set CONFIG.liveApiEndpoint to the HealthSherpa API endpoint, set CONFIG.apiKey."

- [ ] Commit:
```bash
git commit -m "feat: ichra map live data hookup config"
```

---

### Task 9: Deploy

**Deployment model:** The entire `/healthsherpa-ichra/` directory is ONE Netlify site (`ichraverse-hub`). The map is served at `/map/` path, not as a separate Netlify site. Deploy from the root:

- [ ] Deploy from `/healthsherpa-ichra/`:
```bash
cd /Users/joshmait/Desktop/Claude/healthsherpa-ichra
npx netlify-cli deploy --prod --dir . --name ichraverse-hub
```

- [ ] Verify map at `https://ichraverse-hub.netlify.app/map/` — all states render with colors, tooltips work, toggles work.

- [ ] Commit final:
```bash
git commit -m "feat: ichra adoption map complete"
```

---

**Plan complete. Build time estimate: ~2-3 hours.**

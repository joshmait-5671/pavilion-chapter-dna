# ICHRAverse Content Hub — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development or superpowers:executing-plans to implement this plan.

**Goal:** Build the ICHRAverse Content Hub — a media/intelligence hub that positions HealthSherpa as the authoritative ICHRA intelligence source, featuring a newsletter subscribe form, article feed, and market data snapshot.
**Architecture:** Single HTML file + articles.json data. Netlify Forms for subscribe. No backend.
**Tech Stack:** HTML, CSS, JavaScript (vanilla — fetch articles.json, filter logic). Inter font.
**Spec:** `docs/superpowers/specs/2026-03-31-ichraverse-suite-design.md`

---

## Working Directory

`/Users/joshmait/Desktop/Claude/healthsherpa-ichra/content-hub/`

Full site root: `/Users/joshmait/Desktop/Claude/healthsherpa-ichra/`

Article data lives at: `/Users/joshmait/Desktop/Claude/healthsherpa-ichra/data/articles.json`

The HTML file loads articles via: `fetch('../data/articles.json')`

---

## Brand Tokens

```css
--hs-blue: #0970C5
--hs-navy: #074294
--hs-border: #D3E0E8
--hs-text: #344054
--hs-text-light: #475467
--hs-bg: #F8FAFC
```

Font: Inter (Google Fonts). Weights: 400, 500, 600, 700.

Editorial tone — premium industry newsletter (Morning Brew for ICHRA). NOT a product page.

---

## Chunk 1: Data + Shell

### Task 1: Create `healthsherpa-ichra/data/articles.json`

Create the file at `/Users/joshmait/Desktop/Claude/healthsherpa-ichra/data/articles.json`.

If the `data/` directory does not exist, create it first.

Exact file contents:

```json
{
  "_note": "SAMPLE CONTENT — all articles, statistics, and attributions are illustrative placeholders for design and demonstration purposes only.",
  "articles": [
    {
      "id": "ichra-q1-2026-growth",
      "title": "ICHRA Membership Grows 124% YoY — What It Means for Carriers",
      "date": "2026-03-15",
      "summary": "New HRA Council data shows ICHRA is no longer a fringe benefit. Enrollment has crossed the million-life threshold and the growth trajectory is steepening. Here's what carrier strategy teams need to know heading into Q2 2026.",
      "tag": "Market Data",
      "author": "ICHRAverse Research Team",
      "read_time": "4 min read"
    },
    {
      "id": "carrier-activation-playbook-2026",
      "title": "The Carrier Activation Playbook: How Leading Insurers Are Winning ICHRA",
      "date": "2026-03-08",
      "summary": "The carriers gaining market share in ICHRA aren't the biggest — they're the most connected. A look at the activation moves that separate leaders from laggards: platform partnerships, broker toolkits, and real-time eligibility.",
      "tag": "Strategy",
      "author": "ICHRAverse Research Team",
      "read_time": "6 min read"
    },
    {
      "id": "broker-education-gap",
      "title": "The Broker Education Gap Is ICHRA's Biggest Growth Barrier",
      "date": "2026-02-28",
      "summary": "Survey data from 400 independent brokers reveals that 61% cannot explain ICHRA compliantly to an employer group. That's not a product problem — it's a distribution problem. And carriers are uniquely positioned to fix it.",
      "tag": "Strategy",
      "author": "ICHRAverse Research Team",
      "read_time": "5 min read"
    },
    {
      "id": "cms-compliance-update-2026",
      "title": "CMS 2026 ICHRA Guidance: What Changed and What Carriers Must Do",
      "date": "2026-02-14",
      "summary": "CMS released updated ICHRA affordability and substantiation guidance in February 2026. This summary covers the four changes that directly affect carrier administration, reporting obligations, and employee notice requirements.",
      "tag": "Compliance",
      "author": "ICHRAverse Research Team",
      "read_time": "7 min read"
    },
    {
      "id": "ichraverse-vs-competitors",
      "title": "Platform Comparison: Why Carriers Are Choosing HealthSherpa for ICHRA Distribution",
      "date": "2026-02-03",
      "summary": "Not all ICHRA platforms are built for carrier needs. We break down the key differentiators — enrollment volume, API depth, carrier portal quality, and compliance tooling — across the top platforms currently serving the market.",
      "tag": "Carriers",
      "author": "ICHRAverse Research Team",
      "read_time": "5 min read"
    },
    {
      "id": "employer-adoption-case-study",
      "title": "How a 200-Person Manufacturer Switched to ICHRA and Cut Benefits Cost 18%",
      "date": "2026-01-22",
      "summary": "A Midwest manufacturing company with 200 employees moved from a fully-insured group plan to ICHRA in 2025. Twelve months in: 18% cost reduction, 94% employee retention, zero compliance issues. Here's how they did it — and what carriers learned.",
      "tag": "Market Data",
      "author": "ICHRAverse Research Team",
      "read_time": "8 min read"
    }
  ]
}
```

### Task 2: HTML Shell

Create `/Users/joshmait/Desktop/Claude/healthsherpa-ichra/content-hub/index.html`.

The shell includes:

- `<head>` with Inter font via Google Fonts, CSS variables, base reset, responsive meta tag
- **HS Header:** thin top bar with HealthSherpa wordmark on the left (text-based, color `--hs-blue`) and a back link "← Back to ICHRAverse" that links to `../index.html`
- **Editorial Masthead:** centered, below the header. Large bold text "ICHRAverse Intelligence" — use `font-size: 2.5rem`, `font-weight: 700`, `letter-spacing: -0.5px`, `color: var(--hs-navy)`. Below it, tagline in `--hs-text-light`: "The pulse of the ICHRA ecosystem." Below the tagline, a thin `1px` border in `--hs-border`. This masthead sits on a white background with `padding: 2rem 0`.
- Body background: `--hs-bg` (`#F8FAFC`)

---

## Chunk 2: Hero + Subscribe

### Task 3: Hero Subscribe Section

Add below the masthead. Full-width section with `background: var(--hs-navy)`, `color: white`, `padding: 4rem 2rem`.

Contents (centered, max-width 600px):

**Headline:** `"Stay ahead of the ICHRA market."` — `font-size: 2rem`, `font-weight: 700`, white.

**Subhead:** `"Weekly intelligence for carrier executives and ICHRA professionals. Curated by the HealthSherpa ICHRA team."` — `font-size: 1rem`, `opacity: 0.85`, `margin-top: 0.75rem`.

**Netlify Forms subscribe form:**

```html
<form
  name="ichra-newsletter"
  method="POST"
  data-netlify="true"
  netlify-honeypot="bot-field"
  style="margin-top: 2rem; display: flex; gap: 0.75rem; flex-wrap: wrap; justify-content: center;"
>
  <input type="hidden" name="form-name" value="ichra-newsletter" />
  <input type="hidden" name="source" value="content-hub" />
  <p style="display:none;">
    <label>Don't fill this out: <input name="bot-field" /></label>
  </p>
  <input
    type="email"
    name="email"
    placeholder="your@email.com"
    required
    style="padding: 0.75rem 1rem; border-radius: 6px; border: none; font-size: 1rem; min-width: 260px; color: #344054;"
  />
  <button
    type="submit"
    style="padding: 0.75rem 1.5rem; background: #0970C5; color: white; border: none; border-radius: 6px; font-size: 1rem; font-weight: 600; cursor: pointer;"
  >
    Subscribe
  </button>
</form>
```

**Social proof line** below the form: `"Join 200+ carrier and platform leaders — [SAMPLE]"` — `font-size: 0.8rem`, `opacity: 0.65`, `margin-top: 1rem`.

---

## Chunk 3: Article Feed

### Task 4: Article Cards (2-col grid)

Add a section below the hero with `padding: 3rem 2rem`, `max-width: 1100px`, `margin: 0 auto`.

Section heading: `"Latest ICHRA Intelligence"` — `font-size: 1.5rem`, `font-weight: 700`, `color: var(--hs-navy)`. Add a sample note in small muted text: `"All articles are sample content for illustration purposes."`.

**JavaScript: Fetch and render articles**

```javascript
async function loadArticles(activeTag = 'All') {
  const res = await fetch('../data/articles.json');
  const data = await res.json();
  const articles = activeTag === 'All'
    ? data.articles
    : data.articles.filter(a => a.tag === activeTag);
  renderArticles(articles);
}

function renderArticles(articles) {
  const grid = document.getElementById('article-grid');
  grid.innerHTML = articles.map(a => `
    <div class="article-card">
      <span class="tag-pill tag-${slugify(a.tag)}">${a.tag}</span>
      <h3 class="article-title"><a href="#">${a.title}</a></h3>
      <p class="article-summary">${a.summary}</p>
      <div class="article-meta">
        <span>${a.author}</span>
        <span>${formatDate(a.date)}</span>
        <span>${a.read_time}</span>
      </div>
      <a href="#" class="read-more">Read more →</a>
    </div>
  `).join('');
}
```

**Article card CSS:**

```css
#article-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 1.5rem;
  margin-top: 1.5rem;
}

@media (max-width: 768px) {
  #article-grid { grid-template-columns: 1fr; }
}

.article-card {
  background: white;
  border: 1px solid var(--hs-border);
  border-radius: 10px;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
  transition: box-shadow 0.2s ease, transform 0.2s ease;
  cursor: pointer;
}

.article-card:hover {
  box-shadow: 0 8px 24px rgba(7, 66, 148, 0.12);
  transform: translateY(-2px);
}

.article-title a {
  font-size: 1.05rem;
  font-weight: 600;
  color: var(--hs-navy);
  text-decoration: none;
  line-height: 1.4;
}

.article-card:hover .article-title a {
  color: var(--hs-blue);
}

.article-summary {
  font-size: 0.9rem;
  color: var(--hs-text-light);
  line-height: 1.6;
}

.article-meta {
  display: flex;
  gap: 1rem;
  font-size: 0.8rem;
  color: var(--hs-text-light);
  flex-wrap: wrap;
}

.read-more {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--hs-blue);
  text-decoration: none;
  margin-top: auto;
}

.tag-pill {
  display: inline-block;
  padding: 0.25rem 0.6rem;
  border-radius: 999px;
  font-size: 0.75rem;
  font-weight: 600;
  width: fit-content;
}

.tag-market-data { background: #EFF6FF; color: #1D4ED8; }
.tag-strategy     { background: #F0FDF4; color: #15803D; }
.tag-compliance   { background: #FFF7ED; color: #C2410C; }
.tag-carriers     { background: #FAF5FF; color: #7E22CE; }
```

Tag slug mapping for CSS classes: "Market Data" → `tag-market-data`, "Strategy" → `tag-strategy`, "Compliance" → `tag-compliance`, "Carriers" → `tag-carriers`.

Helper functions:

```javascript
function slugify(tag) {
  return tag.toLowerCase().replace(/\s+/g, '-');
}

function formatDate(dateStr) {
  const d = new Date(dateStr);
  return d.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
}
```

### Task 5: Filter Buttons

Add above the article grid, below the section heading. A row of filter buttons:

Tags: `All`, `Market Data`, `Strategy`, `Compliance`, `Carriers`

```html
<div id="filter-bar" style="display: flex; gap: 0.5rem; flex-wrap: wrap; margin-top: 1rem;">
  <button class="filter-btn active" data-tag="All">All</button>
  <button class="filter-btn" data-tag="Market Data">Market Data</button>
  <button class="filter-btn" data-tag="Strategy">Strategy</button>
  <button class="filter-btn" data-tag="Compliance">Compliance</button>
  <button class="filter-btn" data-tag="Carriers">Carriers</button>
</div>
```

Filter button CSS:

```css
.filter-btn {
  padding: 0.4rem 1rem;
  border-radius: 999px;
  border: 1px solid var(--hs-border);
  background: white;
  color: var(--hs-text);
  font-size: 0.85rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.15s ease;
}

.filter-btn:hover {
  border-color: var(--hs-blue);
  color: var(--hs-blue);
}

.filter-btn.active {
  background: var(--hs-blue);
  color: white;
  border-color: var(--hs-blue);
}
```

Filter button JavaScript:

```javascript
document.querySelectorAll('.filter-btn').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    loadArticles(btn.dataset.tag);
  });
});
```

Call `loadArticles()` on `DOMContentLoaded`.

---

## Chunk 4: Market Data Snapshot

### Task 6: Market Pulse Section

Add below the article grid. Section heading: `"Market Pulse"` — same style as "Latest ICHRA Intelligence". Subheading: `"Key metrics shaping the ICHRA landscape."` in `--hs-text-light`.

Four data cards in a 4-col grid (2-col on mobile), each with `background: var(--hs-navy)`, `color: white`, `border-radius: 10px`, `padding: 1.5rem`, `text-align: center`.

Card contents:

| Stat | Label | Source |
|------|-------|--------|
| 124% YoY Growth | ICHRA enrollment, year-over-year | HRA Council, 2025 |
| 500K–1M Lives | Currently on ICHRA nationally | Industry estimate |
| 40+ Platforms | Connected to HealthSherpa | HealthSherpa internal |
| 52% CAGR | Projected ICHRA growth through 2028 | Oliver Wyman |

Each card structure:

```html
<div class="pulse-card">
  <div class="pulse-stat">124%</div>
  <div class="pulse-label">YoY Growth</div>
  <div class="pulse-source">HRA Council, 2025</div>
</div>
```

CSS:

```css
#pulse-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 1rem;
  margin-top: 1.5rem;
}

@media (max-width: 768px) {
  #pulse-grid { grid-template-columns: repeat(2, 1fr); }
}

.pulse-card {
  background: var(--hs-navy);
  color: white;
  border-radius: 10px;
  padding: 1.5rem;
  text-align: center;
}

.pulse-stat {
  font-size: 2rem;
  font-weight: 700;
  line-height: 1;
}

.pulse-label {
  font-size: 0.85rem;
  font-weight: 500;
  margin-top: 0.4rem;
  opacity: 0.9;
}

.pulse-source {
  font-size: 0.7rem;
  opacity: 0.6;
  margin-top: 0.5rem;
}
```

Below the 4 cards, add a muted footnote line:
`"Data updated quarterly by the ICHRAverse research team. All figures are sample/illustrative values."`
— `font-size: 0.8rem`, `color: var(--hs-text-light)`, `margin-top: 1rem`, `text-align: center`.

---

## Chunk 5: CTA + Deploy

### Task 7: Footer CTA

Add a full-width footer CTA section above the page footer. Dark navy background (`var(--hs-navy)`), white text, centered, `padding: 3rem 2rem`.

```html
<section style="background: var(--hs-navy); color: white; text-align: center; padding: 3rem 2rem;">
  <p style="font-size: 0.85rem; font-weight: 600; letter-spacing: 0.08em; opacity: 0.7; text-transform: uppercase; margin-bottom: 0.75rem;">
    Ready to go deeper?
  </p>
  <h2 style="font-size: 1.75rem; font-weight: 700; margin-bottom: 0.75rem;">
    Working on your ICHRA carrier strategy?
  </h2>
  <p style="font-size: 1rem; opacity: 0.85; max-width: 500px; margin: 0 auto 2rem;">
    Talk to the HealthSherpa ICHRA team about distribution, platform integration, and market intelligence.
  </p>
  <a
    href="https://info.healthsherpa.com/ICHRA"
    target="_blank"
    style="display: inline-block; padding: 0.875rem 2rem; background: white; color: var(--hs-navy); border-radius: 6px; font-size: 1rem; font-weight: 700; text-decoration: none;"
  >
    Talk to our ICHRA team
  </a>
</section>
```

Below the CTA, add a minimal page footer: `padding: 1.5rem 2rem`, `border-top: 1px solid var(--hs-border)`, centered, muted text: `"© 2026 HealthSherpa · ICHRAverse Intelligence · Sample content for illustration purposes"`.

### Task 8: Deploy

From the site root `/Users/joshmait/Desktop/Claude/healthsherpa-ichra/`, run:

```bash
npx netlify-cli deploy --prod --dir .
```

This deploys the full ICHRAverse suite including the content hub at `/content-hub/index.html` and the article data at `/data/articles.json`.

Verify the Netlify Forms submission is visible in the Netlify dashboard after deploy (Forms tab). The form is named `ichra-newsletter` and should appear automatically after first deploy because of `data-netlify="true"`.

---

## File Structure After This Plan

```
healthsherpa-ichra/
├── index.html                        # ICHRAverse suite home (existing)
├── data/
│   └── articles.json                 # NEW — 6 mock articles (Task 1)
├── content-hub/
│   └── index.html                    # NEW — Content Hub (Tasks 2–7)
└── [other tool directories]
```

---

## Implementation Checklist

- [ ] Task 1: Create `data/articles.json` with all 6 articles (exact content above)
- [ ] Task 2: HTML shell with HS header and editorial masthead
- [ ] Task 3: Hero section with Netlify Forms subscribe form
- [ ] Task 4: Article cards (2-col grid, fetch from JSON, hover effects)
- [ ] Task 5: Filter buttons with active state and tag filtering
- [ ] Task 6: Market Pulse section with 4 dark data cards
- [ ] Task 7: Footer CTA linking to `https://info.healthsherpa.com/ICHRA`
- [ ] Task 8: Deploy full site via `npx netlify-cli deploy --prod --dir .`

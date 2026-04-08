# Coinfully Homepage Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a customer-centric, emotionally resonant homepage for Coinfully.com that splits inheritor and investor journeys, surfaces both products clearly, and includes the Travis AI guided discovery component.

**Architecture:** Single static HTML file with companion CSS and JS files. No framework, no build step. Deployed to Netlify. Travis AI is pure JS with pre-written response trees — no external API. Visual identity is an evolution of coinfully.com (black, yellow/gold, warm cream) — modernized typography, cleaner spacing, sharper hierarchy.

**Tech Stack:** HTML5, CSS3 (custom properties), vanilla JS, Netlify

**Spec:** `docs/superpowers/specs/2026-03-29-coinfully-homepage-design.md`

**Design principle:** Evolution not revolution — keep the Coinfully DNA (black, yellow, bold type, coin photography), sharpen everything.

---

## File Structure

```
100yards/coinfully/
├── index.html              # Full homepage — all sections
├── css/
│   ├── style.css           # All styles — variables, layout, components
│   └── travis.css          # Travis component styles (isolated)
├── js/
│   ├── main.js             # Scroll behavior, smooth anchors, minor interactions
│   └── travis.js           # Travis AI question flow — pre-written response trees
├── assets/
│   └── travis-avatar.svg   # Illustrated Travis avatar (beard, comic book tee)
└── .netlify/
    └── state.json          # Netlify site ID
```

---

## Chunk 1: Foundation

### Task 1: Project Setup

**Files:**
- Create: `100yards/coinfully/index.html`
- Create: `100yards/coinfully/css/style.css`
- Create: `100yards/coinfully/js/main.js`
- Create: `100yards/coinfully/js/travis.js`
- Create: `100yards/coinfully/css/travis.css`

- [ ] Create the folder structure:
```bash
mkdir -p /Users/joshmait/Desktop/Claude/100yards/coinfully/css
mkdir -p /Users/joshmait/Desktop/Claude/100yards/coinfully/js
mkdir -p /Users/joshmait/Desktop/Claude/100yards/coinfully/assets
mkdir -p /Users/joshmait/Desktop/Claude/100yards/coinfully/.netlify
```

- [ ] Create `css/style.css` with CSS custom properties:
```css
:root {
  /* Brand colors */
  --black: #0A0A0A;
  --yellow: #F5C342;
  --yellow-dark: #D4A520;
  --white: #FFFFFF;
  --cream: #FAFAF5;
  --gray-light: #F2F0EB;
  --gray-mid: #8A8A8A;
  --gray-dark: #3A3A3A;

  /* Typography */
  --font-heading: 'Inter', 'Helvetica Neue', Arial, sans-serif;
  --font-body: 'Inter', 'Helvetica Neue', Arial, sans-serif;

  /* Spacing scale */
  --space-xs: 8px;
  --space-sm: 16px;
  --space-md: 32px;
  --space-lg: 64px;
  --space-xl: 96px;
  --space-2xl: 128px;

  /* Radii */
  --radius-sm: 6px;
  --radius-md: 12px;
  --radius-lg: 24px;
  --radius-pill: 100px;

  /* Max width */
  --max-w: 1200px;
  --max-w-text: 760px;
}

* { box-sizing: border-box; margin: 0; padding: 0; }

html { scroll-behavior: smooth; }

body {
  font-family: var(--font-body);
  background: var(--white);
  color: var(--black);
  font-size: 16px;
  line-height: 1.6;
  -webkit-font-smoothing: antialiased;
}

img { max-width: 100%; display: block; }

.container {
  max-width: var(--max-w);
  margin: 0 auto;
  padding: 0 var(--space-md);
}

.section { padding: var(--space-xl) 0; }
.section--cream { background: var(--cream); }
.section--black { background: var(--black); color: var(--white); }
.section--yellow { background: var(--yellow); }

/* Typography */
.headline-xl {
  font-size: clamp(40px, 6vw, 80px);
  font-weight: 900;
  line-height: 1.05;
  letter-spacing: -0.02em;
}
.headline-lg {
  font-size: clamp(28px, 4vw, 52px);
  font-weight: 800;
  line-height: 1.1;
  letter-spacing: -0.02em;
}
.headline-md {
  font-size: clamp(22px, 3vw, 36px);
  font-weight: 700;
  line-height: 1.2;
  letter-spacing: -0.01em;
}
.headline-sm {
  font-size: clamp(18px, 2vw, 24px);
  font-weight: 700;
  line-height: 1.3;
}
.subhead {
  font-size: clamp(16px, 2vw, 20px);
  line-height: 1.6;
  color: var(--gray-mid);
}
.label {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--gray-mid);
}
.accent { color: var(--yellow-dark); }

/* Buttons */
.btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 14px 28px;
  border-radius: var(--radius-pill);
  font-weight: 700;
  font-size: 15px;
  text-decoration: none;
  cursor: pointer;
  border: none;
  transition: all 0.15s ease;
  white-space: nowrap;
}
.btn-primary {
  background: var(--yellow);
  color: var(--black);
}
.btn-primary:hover { background: var(--yellow-dark); }
.btn-outline {
  background: transparent;
  color: var(--black);
  border: 2px solid var(--black);
}
.btn-outline:hover { background: var(--black); color: var(--white); }
.btn-outline-white {
  background: transparent;
  color: var(--white);
  border: 2px solid rgba(255,255,255,0.4);
}
.btn-outline-white:hover { border-color: var(--white); }
```

- [ ] Verify the CSS file is clean and has no syntax errors (visual check)

- [ ] Commit:
```bash
git add 100yards/coinfully/
git commit -m "feat: coinfully homepage project setup — CSS variables and base styles"
```

---

### Task 2: Base HTML Shell + Google Fonts

**Files:**
- Modify: `100yards/coinfully/index.html`

- [ ] Create `index.html` with the full HTML shell:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Coinfully — Knowledgeable. Transparent. Fair.</title>
  <meta name="description" content="Inherited a coin collection? Managing a coin investment? Coinfully helps you understand what you have, what it's worth, and what to do next. Fast, friendly, and fair.">
  <meta property="og:title" content="Coinfully — Knowledgeable. Transparent. Fair.">
  <meta property="og:description" content="Every coin story is a money story. We help inheritors and investors make the right call with confidence.">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://www.coinfully.com">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="css/style.css">
  <link rel="stylesheet" href="css/travis.css">
</head>
<body>
  <!-- NAV -->
  <!-- HERO -->
  <!-- PERSONA CARDS -->
  <!-- TRUST BAR -->
  <!-- INHERITOR SECTION -->
  <!-- INVESTOR SECTION -->
  <!-- CHARLOTTE VIDEO -->
  <!-- HOME VISIT STORIES -->
  <!-- HOW IT WORKS -->
  <!-- TESTIMONIALS -->
  <!-- CONTENT SECTION -->
  <!-- ESTATE CTA BAND -->
  <!-- FOOTER HERO -->
  <!-- FOOTER -->

  <script src="js/main.js"></script>
  <script src="js/travis.js"></script>
</body>
</html>
```

- [ ] Open in browser and confirm blank page loads with no console errors
- [ ] Commit: `git commit -m "feat: coinfully homepage HTML shell"`

---

## Chunk 2: Nav + Hero + Persona Cards

### Task 3: Navigation

**Files:**
- Modify: `100yards/coinfully/index.html`
- Modify: `100yards/coinfully/css/style.css`

- [ ] Add nav HTML (replace `<!-- NAV -->` comment):
```html
<nav class="nav">
  <div class="container nav__inner">
    <a href="/" class="nav__logo">
      <svg width="140" height="28" viewBox="0 0 140 28" fill="none">
        <!-- Coinfully wordmark with coin-O -->
        <text x="0" y="22" font-family="Inter" font-weight="900" font-size="22" fill="#0A0A0A" letter-spacing="-1">C</text>
        <circle cx="20" cy="14" r="9" fill="#F5C342" stroke="#0A0A0A" stroke-width="2"/>
        <text x="15.5" y="19" font-family="Inter" font-weight="900" font-size="12" fill="#0A0A0A">$</text>
        <text x="32" y="22" font-family="Inter" font-weight="900" font-size="22" fill="#0A0A0A" letter-spacing="-1">INFULLY</text>
      </svg>
    </a>
    <ul class="nav__links">
      <li><a href="#inheritors">For Inheritors</a></li>
      <li><a href="#investors">For Investors</a></li>
      <li><a href="#how-it-works">How It Works</a></li>
      <li><a href="#stories">Stories</a></li>
      <li><a href="https://coinfully.com/blog">Blog</a></li>
    </ul>
    <div class="nav__ctas">
      <a href="#travis-inheritor" class="btn btn-outline">Ask Travis</a>
      <a href="https://coinfully.com/appraisal" class="btn btn-primary">Get a Free Appraisal</a>
    </div>
    <button class="nav__burger" aria-label="Menu">
      <span></span><span></span><span></span>
    </button>
  </div>
</nav>
```

- [ ] Add nav CSS to `style.css`:
```css
/* NAV */
.nav {
  position: fixed;
  top: 0; left: 0; right: 0;
  z-index: 100;
  background: rgba(255,255,255,0.96);
  backdrop-filter: blur(8px);
  border-bottom: 1px solid rgba(0,0,0,0.08);
  height: 68px;
}
.nav__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  height: 68px;
  gap: var(--space-md);
}
.nav__logo { text-decoration: none; }
.nav__links {
  display: flex;
  list-style: none;
  gap: var(--space-md);
  align-items: center;
}
.nav__links a {
  text-decoration: none;
  font-size: 14px;
  font-weight: 600;
  color: var(--gray-dark);
  transition: color 0.15s;
}
.nav__links a:hover { color: var(--black); }
.nav__ctas { display: flex; gap: var(--space-sm); align-items: center; }
.nav__ctas .btn { padding: 10px 20px; font-size: 14px; }
.nav__burger { display: none; flex-direction: column; gap: 5px; background: none; border: none; cursor: pointer; padding: 4px; }
.nav__burger span { display: block; width: 22px; height: 2px; background: var(--black); border-radius: 2px; }

@media (max-width: 768px) {
  .nav__links { display: none; }
  .nav__ctas .btn-outline { display: none; }
  .nav__burger { display: flex; }
}
```

- [ ] Check: Nav renders correctly at desktop and mobile widths
- [ ] Commit: `git commit -m "feat: coinfully nav — fixed with mobile burger"`

---

### Task 4: Hero Section

**Files:**
- Modify: `100yards/coinfully/index.html`
- Modify: `100yards/coinfully/css/style.css`

- [ ] Add hero HTML (replace `<!-- HERO -->` comment):
```html
<section class="hero">
  <div class="hero__bg"></div>
  <div class="hero__overlay"></div>
  <div class="container hero__content">
    <p class="label hero__label">Knowledgeable. Transparent. Fair.</p>
    <h1 class="headline-xl hero__headline">
      Every coin story<br>is a money story.
    </h1>
    <p class="hero__subhead">
      Sorting through an inheritance.<br>
      Managing an investment.<br>
      Everyone wants to get to the right decision —<br>
      <strong>Fast. Friendly. Fair.</strong>
    </p>
    <p class="hero__scroll-hint">↓ Where do you start?</p>
  </div>
</section>
```

- [ ] Add hero CSS:
```css
/* HERO */
.hero {
  position: relative;
  min-height: 100vh;
  display: flex;
  align-items: center;
  padding-top: 68px;
  overflow: hidden;
  background: var(--black);
}
.hero__bg {
  position: absolute;
  inset: 0;
  background-image: url('https://images.unsplash.com/photo-1605792657660-596af9009e82?w=1600&q=80');
  background-size: cover;
  background-position: center;
  opacity: 0.35;
}
.hero__overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(
    to bottom,
    rgba(10,10,10,0.3) 0%,
    rgba(10,10,10,0.7) 60%,
    rgba(10,10,10,0.95) 100%
  );
}
.hero__content {
  position: relative;
  z-index: 2;
  padding-top: var(--space-xl);
  padding-bottom: var(--space-2xl);
  max-width: 800px;
}
.hero__label {
  color: var(--yellow);
  margin-bottom: var(--space-sm);
}
.hero__headline {
  color: var(--white);
  margin-bottom: var(--space-md);
}
.hero__subhead {
  font-size: clamp(18px, 2.5vw, 24px);
  color: rgba(255,255,255,0.8);
  line-height: 1.7;
  margin-bottom: var(--space-lg);
}
.hero__subhead strong { color: var(--yellow); font-weight: 700; }
.hero__scroll-hint {
  font-size: 14px;
  font-weight: 600;
  color: rgba(255,255,255,0.4);
  letter-spacing: 1px;
  animation: bounce 2s infinite;
}
@keyframes bounce {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(6px); }
}
@media (max-width: 768px) {
  .hero { min-height: 85vh; }
  .hero__subhead { font-size: 17px; }
}
```

- [ ] Check: Hero fills viewport, text is readable, coin photo background visible
- [ ] Commit: `git commit -m "feat: coinfully hero — full bleed, emotional headline"`

---

### Task 5: Persona Cards

**Files:**
- Modify: `100yards/coinfully/index.html`
- Modify: `100yards/coinfully/css/style.css`

- [ ] Add persona cards HTML (replace `<!-- PERSONA CARDS -->` comment):
```html
<section class="persona-cards" id="start">
  <div class="container">
    <p class="label persona-cards__label">Where do you start?</p>
    <div class="persona-cards__grid">
      <a href="#inheritors" class="persona-card persona-card--inheritor">
        <div class="persona-card__icon">🏡</div>
        <div class="persona-card__label">I inherited a collection</div>
        <p class="persona-card__desc">You're not sure what you have. Maybe you've been dreading this for years. That's exactly where we start.</p>
        <span class="persona-card__cta">Start here →</span>
      </a>
      <a href="#investors" class="persona-card persona-card--investor">
        <div class="persona-card__icon">📊</div>
        <div class="persona-card__label">I'm managing an investment</div>
        <p class="persona-card__desc">You know coins. You want to know what your collection is actually worth today — and who will pay a fair price for it.</p>
        <span class="persona-card__cta">Start here →</span>
      </a>
    </div>
    <p class="persona-cards__tertiary">
      Working through an estate sale or legal process?
      <a href="#estate">We can help →</a>
    </p>
  </div>
</section>
```

- [ ] Add persona cards CSS:
```css
/* PERSONA CARDS */
.persona-cards {
  background: var(--black);
  padding: 0 0 var(--space-xl) 0;
  margin-top: -2px;
}
.persona-cards__label {
  color: rgba(255,255,255,0.4);
  text-align: center;
  padding: var(--space-md) 0 var(--space-lg) 0;
}
.persona-cards__grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-md);
  max-width: 860px;
  margin: 0 auto;
}
.persona-card {
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
  padding: var(--space-lg) var(--space-md);
  border-radius: var(--radius-lg);
  border: 2px solid rgba(255,255,255,0.1);
  text-decoration: none;
  color: var(--white);
  background: rgba(255,255,255,0.04);
  transition: all 0.2s ease;
  cursor: pointer;
}
.persona-card:hover {
  border-color: var(--yellow);
  background: rgba(245,195,66,0.08);
  transform: translateY(-3px);
}
.persona-card__icon { font-size: 36px; }
.persona-card__label {
  font-size: 22px;
  font-weight: 800;
  line-height: 1.2;
}
.persona-card__desc {
  font-size: 15px;
  color: rgba(255,255,255,0.6);
  line-height: 1.6;
  flex: 1;
}
.persona-card__cta {
  font-size: 14px;
  font-weight: 700;
  color: var(--yellow);
  margin-top: var(--space-sm);
}
.persona-cards__tertiary {
  text-align: center;
  margin-top: var(--space-lg);
  font-size: 14px;
  color: rgba(255,255,255,0.35);
}
.persona-cards__tertiary a {
  color: rgba(255,255,255,0.5);
  text-decoration: underline;
}
@media (max-width: 640px) {
  .persona-cards__grid { grid-template-columns: 1fr; }
}
```

- [ ] Check: Two cards render side by side, hover state works, mobile stacks correctly
- [ ] Commit: `git commit -m "feat: coinfully persona cards — inheritor and investor journey entry"`

---

### Task 6: Trust Bar

**Files:**
- Modify: `100yards/coinfully/index.html`
- Modify: `100yards/coinfully/css/style.css`

- [ ] Add trust bar HTML (replace `<!-- TRUST BAR -->` comment):
```html
<section class="trust-bar">
  <div class="container trust-bar__inner">
    <div class="trust-bar__item">
      <div class="trust-bar__stars">★★★★★</div>
      <div class="trust-bar__text">
        <strong>4.9 on G2</strong>
        <span>from 200+ reviews</span>
      </div>
    </div>
    <div class="trust-bar__divider"></div>
    <div class="trust-bar__item">
      <div class="trust-bar__text">
        <strong>ANA Member</strong>
        <span>American Numismatic Association</span>
      </div>
    </div>
    <div class="trust-bar__divider"></div>
    <div class="trust-bar__item">
      <div class="trust-bar__text">
        <strong>PNG Member</strong>
        <span>Professional Numismatists Guild</span>
      </div>
    </div>
    <div class="trust-bar__divider"></div>
    <div class="trust-bar__item">
      <div class="trust-bar__text">
        <strong>As Seen In</strong>
        <span>VoyageRaleigh · Charlotte Observer</span>
      </div>
    </div>
  </div>
</section>
```

- [ ] Add trust bar CSS:
```css
/* TRUST BAR */
.trust-bar {
  background: var(--cream);
  border-top: 1px solid rgba(0,0,0,0.08);
  border-bottom: 1px solid rgba(0,0,0,0.08);
  padding: var(--space-md) 0;
}
.trust-bar__inner {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-md);
  flex-wrap: wrap;
}
.trust-bar__item {
  display: flex;
  align-items: center;
  gap: var(--space-xs);
}
.trust-bar__stars {
  color: var(--yellow-dark);
  font-size: 18px;
  letter-spacing: 2px;
}
.trust-bar__text {
  display: flex;
  flex-direction: column;
  font-size: 13px;
  line-height: 1.3;
}
.trust-bar__text strong { font-weight: 700; font-size: 14px; }
.trust-bar__text span { color: var(--gray-mid); }
.trust-bar__divider {
  width: 1px;
  height: 32px;
  background: rgba(0,0,0,0.12);
}
@media (max-width: 640px) {
  .trust-bar__divider { display: none; }
  .trust-bar__inner { gap: var(--space-sm); justify-content: flex-start; }
}
```

- [ ] Check: Trust bar renders as a single row on desktop, wraps cleanly on mobile
- [ ] Commit: `git commit -m "feat: coinfully trust bar — G2, org memberships, press"`

---

## Chunk 3: Journey Sections

### Task 7: Inheritor Section

**Files:**
- Modify: `100yards/coinfully/index.html`
- Modify: `100yards/coinfully/css/style.css`

- [ ] Add inheritor section HTML (replace `<!-- INHERITOR SECTION -->` comment):
```html
<section class="section section--cream journey" id="inheritors">
  <div class="container">
    <p class="label">For Inheritors</p>
    <h2 class="headline-lg journey__headline">
      The coin is not the hard part.<br>
      <span class="accent">The decision is.</span>
    </h2>
    <p class="journey__intro">
      You inherited something. Maybe it's valuable. Maybe you've been dreading this for years.
      Maybe your parents were sold something they shouldn't have been.
      Probably all of it. Here's what you need to know.
    </p>

    <div class="journey__three-cols">
      <div class="journey__col">
        <div class="journey__col-num">01</div>
        <h3 class="headline-sm">What do you have?</h3>
        <p>Most people have no idea — and that's completely normal. We help you understand your collection without jargon, pressure, or guesswork.</p>
      </div>
      <div class="journey__col">
        <div class="journey__col-num">02</div>
        <h3 class="headline-sm">What might it be worth?</h3>
        <p>Market-leading appraisals from people who actually know this field. Not a coin shop offer. Not an auction house estimate. A real number.</p>
      </div>
      <div class="journey__col">
        <div class="journey__col-num">03</div>
        <h3 class="headline-sm">What should you do next?</h3>
        <p>That's your call. We give you the information and the options. No pressure. No sales pitch. Just clarity so you can decide with confidence.</p>
      </div>
    </div>

    <!-- Travis AI Component — Inheritor -->
    <div class="travis-block" id="travis-inheritor">
      <div class="travis-block__avatar">
        <!-- Travis SVG inserted by JS -->
        <div class="travis-placeholder"></div>
      </div>
      <div class="travis-block__content">
        <p class="travis-block__prompt">Not sure where to start?</p>
        <p class="travis-block__name">Ask Travis.</p>
        <p class="travis-block__desc">He's been doing this his whole career. Four questions and you'll know exactly where you stand.</p>
        <button class="btn btn-primary travis-trigger" data-persona="inheritor">Start a conversation →</button>
      </div>
    </div>

    <!-- Product options -->
    <div class="journey__products">
      <div class="journey__product">
        <div class="journey__product-label">Mail-In Appraisal</div>
        <p class="journey__product-desc">Start with photos. We'll take it from there. Most collections valued within 24 hours.</p>
        <a href="https://coinfully.com/appraisal" class="btn btn-primary">Get a Free Appraisal</a>
      </div>
      <div class="journey__product journey__product--premium">
        <div class="journey__product-badge">Premium Service</div>
        <div class="journey__product-label">We Come to You</div>
        <p class="journey__product-desc">Large or historically significant collection? Our team travels to you. No shipping. No risk. No hassle.</p>
        <a href="https://coinfully.com/at-home" class="btn btn-outline">See If You Qualify</a>
      </div>
    </div>
  </div>
</section>
```

- [ ] Add inheritor section CSS:
```css
/* JOURNEY SECTIONS */
.journey__headline { margin: var(--space-sm) 0 var(--space-md); }
.journey__intro {
  max-width: var(--max-w-text);
  font-size: 18px;
  line-height: 1.7;
  color: var(--gray-dark);
  margin-bottom: var(--space-lg);
}
.journey__three-cols {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-md);
  margin-bottom: var(--space-xl);
}
.journey__col {
  padding: var(--space-md);
  background: var(--white);
  border-radius: var(--radius-md);
  border: 1px solid rgba(0,0,0,0.07);
}
.journey__col-num {
  font-size: 48px;
  font-weight: 900;
  color: rgba(0,0,0,0.06);
  line-height: 1;
  margin-bottom: var(--space-sm);
}
.journey__col h3 { margin-bottom: var(--space-xs); }
.journey__col p { font-size: 15px; color: var(--gray-dark); line-height: 1.6; }

/* Products */
.journey__products {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: var(--space-md);
  margin-top: var(--space-xl);
  max-width: 700px;
}
.journey__product {
  padding: var(--space-md);
  border-radius: var(--radius-md);
  border: 1px solid rgba(0,0,0,0.1);
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}
.journey__product--premium {
  border-color: var(--yellow-dark);
  background: rgba(245,195,66,0.06);
  position: relative;
}
.journey__product-badge {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--yellow-dark);
}
.journey__product-label { font-size: 18px; font-weight: 800; }
.journey__product-desc { font-size: 14px; color: var(--gray-dark); line-height: 1.5; flex: 1; }

@media (max-width: 768px) {
  .journey__three-cols { grid-template-columns: 1fr; }
  .journey__products { grid-template-columns: 1fr; max-width: 100%; }
}
```

- [ ] Check: Section renders correctly, three columns, product cards, Travis placeholder visible
- [ ] Commit: `git commit -m "feat: coinfully inheritor journey section"`

---

### Task 8: Investor Section

**Files:**
- Modify: `100yards/coinfully/index.html`
- Modify: `100yards/coinfully/css/style.css`

- [ ] Add investor section HTML (replace `<!-- INVESTOR SECTION -->` comment):
```html
<section class="section journey" id="investors">
  <div class="container">
    <p class="label">For Investors</p>
    <h2 class="headline-lg journey__headline">
      You built this.<br>
      <span class="accent">Let's find out what it's really worth.</span>
    </h2>
    <p class="journey__intro">
      Market-leading offers. No coin shop lowballs. No auction house delays.
      When you're ready to convert your collection, we move fast.
    </p>

    <div class="investor-props">
      <div class="investor-prop">
        <div class="investor-prop__icon">⚡</div>
        <h3 class="headline-sm">We move fast</h3>
        <p>Most collections wrapped in a day. Largest ones in 2–3 days. Payment issued in minutes when you accept.</p>
      </div>
      <div class="investor-prop">
        <div class="investor-prop__icon">🔍</div>
        <h3 class="headline-sm">You'll know exactly what you have</h3>
        <p>Authenticated, graded, and valued by experts who have spent their careers in this field. No guesswork.</p>
      </div>
      <div class="investor-prop">
        <div class="investor-prop__icon">💰</div>
        <h3 class="headline-sm">We write the check</h3>
        <p>Coin shops pay 40% of market value. We don't. We buy your entire collection in one transaction — no splitting, no waiting, no middlemen.</p>
      </div>
    </div>

    <!-- Travis AI Component — Investor -->
    <div class="travis-block travis-block--dark" id="travis-investor">
      <div class="travis-block__avatar">
        <div class="travis-placeholder"></div>
      </div>
      <div class="travis-block__content">
        <p class="travis-block__prompt">What kind of collection are you working with?</p>
        <p class="travis-block__name">Ask Travis.</p>
        <p class="travis-block__desc">He'll tell you exactly what to expect — pricing, process, and timeline — in under two minutes.</p>
        <button class="btn btn-primary travis-trigger" data-persona="investor">Start a conversation →</button>
      </div>
    </div>

    <!-- Product options -->
    <div class="journey__products">
      <div class="journey__product">
        <div class="journey__product-label">Send It In</div>
        <p class="journey__product-desc">Photos, list, or full inventory — we'll have an offer within 24 hours.</p>
        <a href="https://coinfully.com/appraisal" class="btn btn-primary">Get Your Offer</a>
      </div>
      <div class="journey__product journey__product--premium">
        <div class="journey__product-badge">Premium Service</div>
        <div class="journey__product-label">We Come to You</div>
        <p class="journey__product-desc">Qualifying collections get an on-site visit. We assess, offer, and pay — all at your location.</p>
        <a href="https://coinfully.com/at-home" class="btn btn-outline">Schedule a Visit</a>
      </div>
    </div>
  </div>
</section>
```

- [ ] Add investor section CSS:
```css
/* INVESTOR PROPS */
.investor-props {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-md);
  margin-bottom: var(--space-xl);
}
.investor-prop {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}
.investor-prop__icon { font-size: 32px; margin-bottom: var(--space-xs); }
.investor-prop h3 { margin-bottom: 4px; }
.investor-prop p { font-size: 15px; color: var(--gray-dark); line-height: 1.6; }

@media (max-width: 768px) {
  .investor-props { grid-template-columns: 1fr; }
}
```

- [ ] Check: Investor section renders correctly alongside inheritor section
- [ ] Commit: `git commit -m "feat: coinfully investor journey section"`

---

## Chunk 4: Travis AI Component

### Task 9: Travis Avatar SVG

**Files:**
- Create: `100yards/coinfully/assets/travis-avatar.svg`
- Modify: `100yards/coinfully/css/travis.css`

- [ ] Create illustrated Travis avatar SVG (beard, comic book tee, friendly):
```svg
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">
  <!-- Background circle -->
  <circle cx="60" cy="60" r="58" fill="#F5C342" stroke="#0A0A0A" stroke-width="2"/>
  <!-- Body/shirt -->
  <rect x="28" y="78" width="64" height="40" rx="8" fill="#1a1a2e"/>
  <!-- Comic book graphic on shirt (lightning bolt) -->
  <polygon points="52,85 62,95 56,95 66,108 50,96 57,96" fill="#F5C342"/>
  <!-- Neck -->
  <rect x="50" y="70" width="20" height="14" rx="4" fill="#D4956A"/>
  <!-- Head -->
  <ellipse cx="60" cy="52" rx="26" ry="28" fill="#D4956A"/>
  <!-- Hair -->
  <ellipse cx="60" cy="26" rx="26" ry="12" fill="#3D2B1F"/>
  <rect x="34" y="26" width="52" height="8" rx="4" fill="#3D2B1F"/>
  <!-- Beard -->
  <ellipse cx="60" cy="68" rx="20" ry="12" fill="#4A3728"/>
  <ellipse cx="60" cy="64" rx="16" ry="8" fill="#D4956A"/>
  <!-- Eyes -->
  <circle cx="50" cy="50" r="4" fill="#2C1810"/>
  <circle cx="70" cy="50" r="4" fill="#2C1810"/>
  <circle cx="51.5" cy="48.5" r="1.5" fill="white"/>
  <circle cx="71.5" cy="48.5" r="1.5" fill="white"/>
  <!-- Eyebrows -->
  <path d="M44 44 Q50 41 56 44" stroke="#3D2B1F" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <path d="M64 44 Q70 41 76 44" stroke="#3D2B1F" stroke-width="2.5" fill="none" stroke-linecap="round"/>
  <!-- Smile (friendly) -->
  <path d="M50 62 Q60 70 70 62" stroke="#3D2B1F" stroke-width="2" fill="none" stroke-linecap="round"/>
  <!-- Glasses -->
  <circle cx="50" cy="50" r="7" fill="none" stroke="#0A0A0A" stroke-width="2"/>
  <circle cx="70" cy="50" r="7" fill="none" stroke="#0A0A0A" stroke-width="2"/>
  <line x1="57" y1="50" x2="63" y2="50" stroke="#0A0A0A" stroke-width="2"/>
  <line x1="34" y1="49" x2="43" y2="50" stroke="#0A0A0A" stroke-width="2"/>
  <line x1="77" y1="50" x2="84" y2="49" stroke="#0A0A0A" stroke-width="2"/>
</svg>
```

- [ ] Add travis.css:
```css
/* TRAVIS COMPONENT */
.travis-block {
  display: flex;
  align-items: center;
  gap: var(--space-lg);
  padding: var(--space-lg) var(--space-xl);
  background: var(--black);
  border-radius: var(--radius-lg);
  margin: var(--space-xl) 0;
  color: var(--white);
  max-width: 780px;
}
.travis-block--dark {
  background: var(--gray-dark);
}
.travis-block__avatar {
  flex-shrink: 0;
  width: 100px;
  height: 100px;
}
.travis-block__avatar img,
.travis-block__avatar svg {
  width: 100%;
  height: 100%;
}
.travis-placeholder {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background: var(--yellow);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 48px;
}
.travis-block__content {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.travis-block__prompt {
  font-size: 13px;
  color: rgba(255,255,255,0.5);
  font-weight: 600;
  letter-spacing: 0.5px;
}
.travis-block__name {
  font-size: 28px;
  font-weight: 900;
  color: var(--yellow);
  line-height: 1;
  margin-bottom: 4px;
}
.travis-block__desc {
  font-size: 15px;
  color: rgba(255,255,255,0.7);
  line-height: 1.6;
  margin-bottom: var(--space-sm);
}

/* TRAVIS MODAL */
.travis-modal {
  display: none;
  position: fixed;
  inset: 0;
  z-index: 200;
  align-items: center;
  justify-content: center;
  background: rgba(0,0,0,0.7);
  backdrop-filter: blur(4px);
}
.travis-modal.active { display: flex; }
.travis-modal__inner {
  background: var(--white);
  border-radius: var(--radius-lg);
  padding: var(--space-lg);
  max-width: 520px;
  width: 90%;
  max-height: 80vh;
  overflow-y: auto;
  position: relative;
}
.travis-modal__header {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  margin-bottom: var(--space-md);
}
.travis-modal__avatar { width: 56px; height: 56px; flex-shrink: 0; }
.travis-modal__name { font-size: 18px; font-weight: 800; }
.travis-modal__title { font-size: 13px; color: var(--gray-mid); }
.travis-modal__close {
  position: absolute;
  top: var(--space-md);
  right: var(--space-md);
  background: none;
  border: none;
  font-size: 24px;
  cursor: pointer;
  color: var(--gray-mid);
  line-height: 1;
  padding: 4px;
}
.travis-modal__question {
  font-size: 20px;
  font-weight: 700;
  line-height: 1.3;
  margin-bottom: var(--space-md);
  color: var(--black);
}
.travis-modal__options {
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
}
.travis-option {
  padding: var(--space-sm) var(--space-md);
  border-radius: var(--radius-md);
  border: 2px solid rgba(0,0,0,0.1);
  background: var(--cream);
  font-size: 15px;
  font-weight: 600;
  cursor: pointer;
  text-align: left;
  transition: all 0.15s;
  color: var(--black);
}
.travis-option:hover {
  border-color: var(--yellow-dark);
  background: rgba(245,195,66,0.1);
}
.travis-modal__response {
  font-size: 16px;
  line-height: 1.7;
  color: var(--gray-dark);
  margin-bottom: var(--space-md);
}
.travis-modal__progress {
  font-size: 12px;
  color: var(--gray-mid);
  margin-bottom: var(--space-sm);
}
.travis-modal__back {
  background: none;
  border: none;
  color: var(--gray-mid);
  font-size: 13px;
  cursor: pointer;
  text-decoration: underline;
  margin-top: var(--space-sm);
}

@media (max-width: 640px) {
  .travis-block {
    flex-direction: column;
    text-align: center;
    padding: var(--space-md);
  }
}
```

- [ ] Verify avatar SVG renders correctly in browser
- [ ] Commit: `git commit -m "feat: travis avatar SVG and component CSS"`

---

### Task 10: Travis JS — Question Flow

**Files:**
- Modify: `100yards/coinfully/js/travis.js`

- [ ] Write full travis.js with pre-written question trees:
```javascript
// Travis AI — Controlled Question Flow
// No external API. All responses pre-written.

const TRAVIS = {
  inheritor: {
    questions: [
      {
        id: 'situation',
        q: "What best describes your situation?",
        options: [
          { label: "I inherited a collection from a family member", value: 'inherited' },
          { label: "I have a family collection that's been sitting untouched", value: 'sitting' },
          { label: "My parents (or I) may have bought coins that weren't worth it", value: 'scammed' },
          { label: "I need to sell or value coins quickly", value: 'urgent' }
        ]
      },
      {
        id: 'size',
        q: "Roughly how many coins are we talking?",
        options: [
          { label: "A handful — maybe a shoebox", value: 'small' },
          { label: "A few dozen — albums, folders, a collection", value: 'medium' },
          { label: "Hundreds or more — serious collection", value: 'large' },
          { label: "Honestly, no idea", value: 'unknown' }
        ]
      },
      {
        id: 'knowledge',
        q: "How much do you know about the collection?",
        options: [
          { label: "Almost nothing", value: 'none' },
          { label: "A little — I know some of the coins", value: 'some' },
          { label: "I've been told it might be valuable", value: 'told' },
          { label: "I've tried researching it myself", value: 'researched' }
        ]
      },
      {
        id: 'priority',
        q: "What matters most to you right now?",
        options: [
          { label: "Understanding what I actually have", value: 'understand' },
          { label: "Getting a fair price", value: 'price' },
          { label: "Making this as easy as possible", value: 'easy' },
          { label: "Just getting it done", value: 'done' }
        ]
      }
    ],
    responses: {
      // Situation-based openers
      inherited: "Dealing with an inherited collection is more common than people think — and almost nobody knows where to start. That's completely normal.",
      sitting: "Collections that have been sitting untouched for years can be surprisingly valuable. The longer they've been held, the more interesting the story.",
      scammed: "Unfortunately, predatory coin sellers have been targeting good people for decades — especially through magazines and phone solicitations. You're not alone, and it's not your fault.",
      urgent: "Whether it's probate, a move, or just a decision that can't wait — we can move quickly. Most collections are valued within 24 hours.",

      // Size context
      small: "Even a small collection can carry real value. A single coin can be worth thousands. Let's find out what you actually have.",
      medium: "A collection of a few dozen coins is often worth more than people expect — especially if it's been kept in albums or folders.",
      large: "A large collection is our specialty. We've processed everything from single trays to estate-sized holdings. We know how to handle it.",
      unknown: "Not knowing what you have is the perfect starting point. That's literally what we're here for.",

      // Final CTA message
      final: "Here's what I'd suggest: start with a free appraisal. Send us a few photos, and we'll tell you what you're looking at — no obligation, no pressure. If the collection is large enough, we'll come to you."
    }
  },

  investor: {
    questions: [
      {
        id: 'type',
        q: "What type of coins are you working with?",
        options: [
          { label: "Bullion — gold, silver, platinum coins or bars", value: 'bullion' },
          { label: "Rare or collectible coins", value: 'rare' },
          { label: "A mix of both", value: 'mix' },
          { label: "I'm not entirely sure", value: 'unsure' }
        ]
      },
      {
        id: 'size',
        q: "Roughly what's the collection worth?",
        options: [
          { label: "Under $10,000", value: 'small' },
          { label: "$10,000 – $50,000", value: 'medium' },
          { label: "$50,000 or more", value: 'large' },
          { label: "I don't know — that's part of why I'm here", value: 'unknown' }
        ]
      },
      {
        id: 'timeline',
        q: "What's your timeline?",
        options: [
          { label: "Ready to move now", value: 'now' },
          { label: "A few weeks — I'm still deciding", value: 'weeks' },
          { label: "Just exploring for now", value: 'exploring' }
        ]
      },
      {
        id: 'priority',
        q: "What matters most?",
        options: [
          { label: "Getting the best possible offer", value: 'price' },
          { label: "Speed — I want this done fast", value: 'speed' },
          { label: "Making sure I understand the process", value: 'process' }
        ]
      }
    ],
    responses: {
      bullion: "Bullion is our most straightforward category — gold and silver prices are market-based, and we pay at or near spot. Fast, clean, no drama.",
      rare: "Rare and collectible coins are where knowledge really matters. Most buyers undervalue them. We know what they're actually worth.",
      mix: "Mixed collections are typical for serious investors. We assess the whole thing — bullion at market, collectibles at what they're actually worth on the open market.",
      unsure: "Not being sure is fine. Part of what we do is identify what you actually have before making any offer.",
      large: "Collections at $50K+ typically qualify for our at-home service — we come to you, assess on-site, and can make an offer the same day.",
      final: "The fastest path is to get us a photo inventory or contact form — we'll come back to you with a real number, usually within 24 hours. For larger collections, we can schedule a visit."
    }
  }
};

// Build response summary based on answers
function buildResponse(persona, answers) {
  const tree = TRAVIS[persona];
  const msgs = [];

  // First question response
  if (answers.situation) msgs.push(tree.responses[answers.situation]);
  if (answers.type) msgs.push(tree.responses[answers.type]);

  // Size context
  if (answers.size) msgs.push(tree.responses[answers.size] || '');

  // Final CTA
  msgs.push(tree.responses.final);

  return msgs.filter(Boolean).join(' ');
}

// ---- Modal UI ----
let currentPersona = null;
let currentStep = 0;
let answers = {};

function createModal() {
  const modal = document.createElement('div');
  modal.className = 'travis-modal';
  modal.id = 'travis-modal';
  modal.innerHTML = `
    <div class="travis-modal__inner">
      <button class="travis-modal__close" id="travis-close">✕</button>
      <div class="travis-modal__header">
        <div class="travis-modal__avatar">
          <img src="assets/travis-avatar.svg" alt="Travis" onerror="this.parentNode.innerHTML='🪙'">
        </div>
        <div>
          <div class="travis-modal__name">Travis</div>
          <div class="travis-modal__title">Co-Founder, Coinfully</div>
        </div>
      </div>
      <div id="travis-body"></div>
    </div>
  `;
  document.body.appendChild(modal);

  document.getElementById('travis-close').addEventListener('click', closeTravis);
  modal.addEventListener('click', (e) => { if (e.target === modal) closeTravis(); });
}

function openTravis(persona) {
  currentPersona = persona;
  currentStep = 0;
  answers = {};

  const modal = document.getElementById('travis-modal');
  if (!modal) createModal();

  document.getElementById('travis-modal').classList.add('active');
  renderStep();
}

function closeTravis() {
  document.getElementById('travis-modal').classList.remove('active');
}

function renderStep() {
  const tree = TRAVIS[currentPersona];
  const body = document.getElementById('travis-body');

  if (currentStep >= tree.questions.length) {
    renderResponse();
    return;
  }

  const q = tree.questions[currentStep];
  const progress = `${currentStep + 1} of ${tree.questions.length}`;

  body.innerHTML = `
    <p class="travis-modal__progress">Question ${progress}</p>
    <p class="travis-modal__question">${q.q}</p>
    <div class="travis-modal__options">
      ${q.options.map(opt => `
        <button class="travis-option" data-value="${opt.value}" data-qid="${q.id}">
          ${opt.label}
        </button>
      `).join('')}
    </div>
    ${currentStep > 0 ? '<button class="travis-modal__back" id="travis-back">← Back</button>' : ''}
  `;

  body.querySelectorAll('.travis-option').forEach(btn => {
    btn.addEventListener('click', () => {
      answers[btn.dataset.qid] = btn.dataset.value;
      currentStep++;
      renderStep();
    });
  });

  const back = body.querySelector('#travis-back');
  if (back) back.addEventListener('click', () => { currentStep--; renderStep(); });
}

function renderResponse() {
  const body = document.getElementById('travis-body');
  const response = buildResponse(currentPersona, answers);
  const cta = currentPersona === 'inheritor'
    ? '<a href="https://coinfully.com/appraisal" class="btn btn-primary">Get a Free Appraisal</a>'
    : '<a href="https://coinfully.com/appraisal" class="btn btn-primary">Get Your Offer</a>';

  body.innerHTML = `
    <div class="travis-modal__response">${response}</div>
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:8px;">
      ${cta}
      <button class="btn btn-outline" id="travis-restart">Ask another question</button>
    </div>
  `;

  document.getElementById('travis-restart').addEventListener('click', () => {
    currentStep = 0;
    answers = {};
    renderStep();
  });
}

// Init
document.addEventListener('DOMContentLoaded', () => {
  createModal();
  document.querySelectorAll('.travis-trigger').forEach(btn => {
    btn.addEventListener('click', () => openTravis(btn.dataset.persona));
  });

  // Load Travis avatar into placeholders
  document.querySelectorAll('.travis-placeholder').forEach(el => {
    const img = document.createElement('img');
    img.src = 'assets/travis-avatar.svg';
    img.alt = 'Travis';
    img.style.cssText = 'width:100%;height:100%;border-radius:50%;object-fit:cover;';
    img.onerror = () => { el.textContent = '🪙'; };
    el.replaceWith(img);
  });
});
```

- [ ] Test Travis flow: Open modal → click through all 4 questions → see final response → click CTA
- [ ] Test: Back button works correctly
- [ ] Test: Close button and click-outside close both work
- [ ] Test: Both inheritor and investor flows render different questions
- [ ] Commit: `git commit -m "feat: travis AI question flow — inheritor and investor trees"`

---

## Chunk 5: Video + Stories + How It Works

### Task 11: Charlotte Office Video Section

**Files:**
- Modify: `100yards/coinfully/index.html`
- Modify: `100yards/coinfully/css/style.css`

- [ ] Add Charlotte video HTML (replace `<!-- CHARLOTTE VIDEO -->` comment):
```html
<section class="section section--black charlotte-video">
  <div class="container">
    <p class="label" style="color:rgba(255,255,255,0.4)">Where the work happens</p>
    <h2 class="headline-lg" style="color:var(--white);margin:var(--space-sm) 0 var(--space-lg);">
      Behind every collection<br>is a team that actually cares.
    </h2>
    <div class="video-placeholder">
      <div class="video-placeholder__inner">
        <div class="video-placeholder__icon">▶</div>
        <p class="video-placeholder__label">Charlotte Office — Coming Soon</p>
      </div>
    </div>
  </div>
</section>
```

- [ ] Add video placeholder CSS:
```css
/* VIDEO SECTIONS */
.video-placeholder {
  width: 100%;
  aspect-ratio: 16/9;
  background: rgba(255,255,255,0.06);
  border-radius: var(--radius-lg);
  border: 2px dashed rgba(255,255,255,0.15);
  display: flex;
  align-items: center;
  justify-content: center;
}
.video-placeholder__inner { text-align: center; color: rgba(255,255,255,0.3); }
.video-placeholder__icon { font-size: 48px; margin-bottom: var(--space-sm); }
.video-placeholder__label { font-size: 14px; font-weight: 600; }

/* For real video embed, replace .video-placeholder with: */
/* <div class="video-embed"><iframe src="..." ...></iframe></div> */
.video-embed {
  width: 100%;
  aspect-ratio: 16/9;
  border-radius: var(--radius-lg);
  overflow: hidden;
}
.video-embed iframe { width: 100%; height: 100%; border: none; }
```

- [ ] Commit: `git commit -m "feat: charlotte office video section placeholder"`

---

### Task 12: Home Visit Stories Section

**Files:**
- Modify: `100yards/coinfully/index.html`
- Modify: `100yards/coinfully/css/style.css`

- [ ] Add stories HTML (replace `<!-- HOME VISIT STORIES -->` comment):
```html
<section class="section section--cream" id="stories">
  <div class="container">
    <p class="label">Real Stories</p>
    <h2 class="headline-lg" style="margin:var(--space-sm) 0 var(--space-xs);">Every collection has a story.</h2>
    <p class="subhead" style="margin-bottom:var(--space-lg);">The people behind them trusted us with something that mattered.</p>
    <div class="stories-grid">
      <div class="story-card">
        <div class="story-card__thumb video-placeholder" style="aspect-ratio:4/3;">
          <div class="video-placeholder__inner">
            <div class="video-placeholder__icon" style="font-size:32px;">▶</div>
          </div>
        </div>
        <div class="story-card__body">
          <p class="story-card__name">Margaret, Dallas TX</p>
          <p class="story-card__teaser">"I had no idea what my father left behind. Coinfully changed everything."</p>
        </div>
      </div>
      <div class="story-card">
        <div class="story-card__thumb video-placeholder" style="aspect-ratio:4/3;">
          <div class="video-placeholder__inner">
            <div class="video-placeholder__icon" style="font-size:32px;">▶</div>
          </div>
        </div>
        <div class="story-card__body">
          <p class="story-card__name">Robert, Charlotte NC</p>
          <p class="story-card__teaser">"I'd been sitting on my dad's collection for three years. I finally made the call."</p>
        </div>
      </div>
      <div class="story-card">
        <div class="story-card__thumb video-placeholder" style="aspect-ratio:4/3;">
          <div class="video-placeholder__inner">
            <div class="video-placeholder__icon" style="font-size:32px;">▶</div>
          </div>
        </div>
        <div class="story-card__body">
          <p class="story-card__name">Linda, Houston TX</p>
          <p class="story-card__teaser">"My parents bought coins for years. I needed someone I could actually trust."</p>
        </div>
      </div>
    </div>
  </div>
</section>
```

- [ ] Add stories CSS:
```css
/* STORIES */
.stories-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-md);
}
.story-card {
  background: var(--white);
  border-radius: var(--radius-md);
  overflow: hidden;
  border: 1px solid rgba(0,0,0,0.07);
}
.story-card__thumb { margin: 0; border-radius: 0; border: none; background: var(--gray-light); }
.story-card__body { padding: var(--space-md); }
.story-card__name { font-size: 13px; font-weight: 700; color: var(--gray-mid); margin-bottom: 6px; letter-spacing: 0.5px; text-transform: uppercase; }
.story-card__teaser { font-size: 16px; font-weight: 600; line-height: 1.5; color: var(--black); font-style: italic; }

@media (max-width: 768px) {
  .stories-grid { grid-template-columns: 1fr; }
}
```

- [ ] Commit: `git commit -m "feat: coinfully home visit stories section"`

---

### Task 13: How It Works

**Files:**
- Modify: `100yards/coinfully/index.html`
- Modify: `100yards/coinfully/css/style.css`

- [ ] Add how it works HTML (replace `<!-- HOW IT WORKS -->` comment):
```html
<section class="section" id="how-it-works">
  <div class="container">
    <p class="label">Simple Process</p>
    <h2 class="headline-lg" style="margin:var(--space-sm) 0 var(--space-lg);">Three steps. No surprises.</h2>
    <div class="steps">
      <div class="step">
        <div class="step__num">1</div>
        <h3 class="headline-sm">Tell us about your collection</h3>
        <p>A few photos. A quick description. That's all we need to get started. No expertise required on your end.</p>
      </div>
      <div class="step__arrow">→</div>
      <div class="step">
        <div class="step__num">2</div>
        <h3 class="headline-sm">We appraise, authenticate, value</h3>
        <p>Our team reviews everything. We know what we're looking at. You get a real number — not a guess.</p>
      </div>
      <div class="step__arrow">→</div>
      <div class="step">
        <div class="step__num">3</div>
        <h3 class="headline-sm">Accept the offer. Get paid.</h3>
        <p>If you're happy with the offer, payment is issued in minutes. No delays, no waiting, no chasing anyone down.</p>
      </div>
    </div>
    <p class="steps__note">For large or significant collections, we travel to you. <a href="https://coinfully.com/at-home">Learn about our at-home service →</a></p>
  </div>
</section>
```

- [ ] Add steps CSS:
```css
/* HOW IT WORKS */
.steps {
  display: flex;
  align-items: flex-start;
  gap: var(--space-md);
  margin-bottom: var(--space-lg);
}
.step {
  flex: 1;
  padding: var(--space-md);
  background: var(--cream);
  border-radius: var(--radius-md);
}
.step__num {
  font-size: 56px;
  font-weight: 900;
  color: var(--yellow-dark);
  line-height: 1;
  margin-bottom: var(--space-sm);
}
.step h3 { margin-bottom: var(--space-xs); }
.step p { font-size: 15px; color: var(--gray-dark); line-height: 1.6; }
.step__arrow {
  font-size: 32px;
  color: var(--gray-mid);
  margin-top: 56px;
  flex-shrink: 0;
}
.steps__note {
  font-size: 15px;
  color: var(--gray-mid);
}
.steps__note a { color: var(--black); font-weight: 600; }

@media (max-width: 768px) {
  .steps { flex-direction: column; }
  .step__arrow { display: none; }
}
```

- [ ] Commit: `git commit -m "feat: coinfully how it works section"`

---

## Chunk 6: Social Proof, Content, CTAs, Footer

### Task 14: Testimonials

**Files:**
- Modify: `100yards/coinfully/index.html`
- Modify: `100yards/coinfully/css/style.css`

- [ ] Add testimonials HTML (replace `<!-- TESTIMONIALS -->` comment):
```html
<section class="section section--cream">
  <div class="container">
    <p class="label">What people say after.</p>
    <div class="testimonials-grid">
      <div class="testimonial">
        <div class="testimonial__stars">★★★★★</div>
        <p class="testimonial__quote">"Kindest, most professional people I've dealt with. We were ignored everywhere else. This was the complete opposite. Common decency — person to person."</p>
        <div class="testimonial__author">
          <strong>Sandra K.</strong>
          <span>Dallas, TX — Inherited Collection</span>
        </div>
      </div>
      <div class="testimonial">
        <div class="testimonial__stars">★★★★★</div>
        <p class="testimonial__quote">"They came to my house on a Friday. By Monday it was done. I couldn't believe how easy it was. I'd been dreading this for three years."</p>
        <div class="testimonial__author">
          <strong>James R.</strong>
          <span>Charlotte, NC — At-Home Appraisal</span>
        </div>
      </div>
      <div class="testimonial">
        <div class="testimonial__stars">★★★★★</div>
        <p class="testimonial__quote">"They knew what every coin was worth before I even finished showing them. And they explained it all without making me feel stupid. That meant everything."</p>
        <div class="testimonial__author">
          <strong>Patricia M.</strong>
          <span>Houston, TX — Estate Collection</span>
        </div>
      </div>
    </div>
    <div class="testimonials-g2">
      <span class="testimonials-g2__stars">★★★★★</span>
      <strong>4.9 out of 5</strong> on G2 from 200+ verified reviews
      <a href="https://g2.com" target="_blank" style="color:var(--black);font-weight:700;">Read all reviews →</a>
    </div>
  </div>
</section>
```

- [ ] Add testimonials CSS:
```css
/* TESTIMONIALS */
.testimonials-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-md);
  margin-bottom: var(--space-lg);
}
.testimonial {
  background: var(--white);
  padding: var(--space-md);
  border-radius: var(--radius-md);
  border: 1px solid rgba(0,0,0,0.07);
  display: flex;
  flex-direction: column;
  gap: var(--space-sm);
}
.testimonial__stars { color: var(--yellow-dark); font-size: 16px; letter-spacing: 2px; }
.testimonial__quote {
  font-size: 15px;
  line-height: 1.7;
  color: var(--gray-dark);
  font-style: italic;
  flex: 1;
}
.testimonial__author { font-size: 13px; }
.testimonial__author strong { display: block; font-size: 14px; }
.testimonial__author span { color: var(--gray-mid); }
.testimonials-g2 {
  display: flex;
  align-items: center;
  gap: var(--space-sm);
  font-size: 14px;
  flex-wrap: wrap;
}
.testimonials-g2__stars { color: var(--yellow-dark); font-size: 18px; }

@media (max-width: 768px) {
  .testimonials-grid { grid-template-columns: 1fr; }
}
```

- [ ] Commit: `git commit -m "feat: coinfully testimonials section"`

---

### Task 15: Content Section + Estate Band + Footer Hero + Footer

**Files:**
- Modify: `100yards/coinfully/index.html`
- Modify: `100yards/coinfully/css/style.css`

- [ ] Add remaining sections HTML:
```html
<!-- CONTENT SECTION -->
<section class="section" id="blog">
  <div class="container">
    <p class="label">Things Worth Knowing</p>
    <h2 class="headline-md" style="margin:var(--space-sm) 0 var(--space-lg);">Answers before you need them.</h2>
    <div class="content-grid">
      <a href="https://coinfully.com/blog" class="content-card">
        <div class="content-card__tag">For Inheritors</div>
        <h3 class="content-card__title">What to do when you inherit a coin collection</h3>
        <p class="content-card__desc">Step by step — from opening the box to getting a fair offer.</p>
      </a>
      <a href="https://coinfully.com/blog" class="content-card">
        <div class="content-card__tag">For Investors</div>
        <h3 class="content-card__title">Why coin shops pay 40 cents on the dollar (and how to avoid it)</h3>
        <p class="content-card__desc">The insider math behind lowball offers — and what to do instead.</p>
      </a>
      <a href="https://coinfully.com/blog" class="content-card">
        <div class="content-card__tag">Trust & Safety</div>
        <h3 class="content-card__title">10 questions to ask before selling your coin collection to anyone</h3>
        <p class="content-card__desc">A plain-English checklist for finding someone you can actually trust.</p>
      </a>
    </div>
    <a href="https://coinfully.com/blog" class="btn btn-outline" style="margin-top:var(--space-md);">Read more on the blog</a>
  </div>
</section>

<!-- ESTATE CTA BAND -->
<section class="estate-band" id="estate">
  <div class="container estate-band__inner">
    <div>
      <p class="label" style="color:var(--gray-mid);">Estate Sales & Legal</p>
      <h3 class="headline-sm" style="margin-top:6px;">Working through an estate sale or legal process?</h3>
      <p style="font-size:15px;color:var(--gray-dark);margin-top:6px;">We help with documentation, valuation, and coordination — everything probate, insurance, and legal teams need.</p>
    </div>
    <a href="https://coinfully.com/contact" class="btn btn-outline" style="flex-shrink:0;">Let's talk</a>
  </div>
</section>

<!-- FOOTER HERO -->
<section class="footer-hero">
  <div class="container footer-hero__inner">
    <h2 class="headline-lg" style="color:var(--white);">Ready to find out<br>what yours is worth?</h2>
    <div class="footer-hero__ctas">
      <a href="https://coinfully.com/appraisal" class="btn btn-primary">Get a Free Appraisal</a>
      <button class="btn btn-outline-white travis-trigger" data-persona="inheritor">Ask Travis</button>
    </div>
  </div>
</section>

<!-- FOOTER -->
<footer class="footer">
  <div class="container footer__inner">
    <div class="footer__brand">
      <p style="font-weight:900;font-size:18px;letter-spacing:-0.5px;">COINFULLY</p>
      <p style="font-size:13px;color:var(--gray-mid);margin-top:4px;">Knowledgeable. Transparent. Fair.</p>
    </div>
    <div class="footer__links">
      <a href="#inheritors">For Inheritors</a>
      <a href="#investors">For Investors</a>
      <a href="https://coinfully.com/about">About Us</a>
      <a href="https://coinfully.com/blog">Blog</a>
      <a href="https://coinfully.com/locations">Locations</a>
      <a href="https://coinfully.com/contact">Contact</a>
    </div>
    <p class="footer__legal">© 2026 Coinfully. All rights reserved. | <a href="https://coinfully.com/privacy">Privacy Policy</a></p>
  </div>
</footer>
```

- [ ] Add CSS for remaining sections:
```css
/* CONTENT SECTION */
.content-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: var(--space-md);
}
.content-card {
  padding: var(--space-md);
  background: var(--cream);
  border-radius: var(--radius-md);
  border: 1px solid rgba(0,0,0,0.07);
  text-decoration: none;
  color: var(--black);
  display: flex;
  flex-direction: column;
  gap: var(--space-xs);
  transition: box-shadow 0.15s;
}
.content-card:hover { box-shadow: 0 4px 20px rgba(0,0,0,0.08); }
.content-card__tag {
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 1.5px;
  text-transform: uppercase;
  color: var(--yellow-dark);
}
.content-card__title { font-size: 17px; font-weight: 700; line-height: 1.3; }
.content-card__desc { font-size: 14px; color: var(--gray-mid); line-height: 1.5; }

/* ESTATE BAND */
.estate-band {
  background: var(--gray-light);
  padding: var(--space-lg) 0;
  border-top: 1px solid rgba(0,0,0,0.08);
}
.estate-band__inner {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: var(--space-lg);
}

/* FOOTER HERO */
.footer-hero {
  background: var(--black);
  padding: var(--space-2xl) 0;
}
.footer-hero__inner { text-align: center; }
.footer-hero__ctas {
  display: flex;
  gap: var(--space-sm);
  justify-content: center;
  margin-top: var(--space-lg);
  flex-wrap: wrap;
}

/* FOOTER */
.footer {
  background: #050505;
  padding: var(--space-lg) 0;
  border-top: 1px solid rgba(255,255,255,0.06);
}
.footer__inner {
  display: flex;
  flex-direction: column;
  gap: var(--space-md);
}
.footer__links {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-md);
}
.footer__links a {
  color: rgba(255,255,255,0.5);
  text-decoration: none;
  font-size: 14px;
  font-weight: 500;
}
.footer__links a:hover { color: var(--white); }
.footer__legal { font-size: 12px; color: rgba(255,255,255,0.25); }
.footer__legal a { color: rgba(255,255,255,0.35); }

@media (max-width: 768px) {
  .content-grid { grid-template-columns: 1fr; }
  .estate-band__inner { flex-direction: column; }
}
```

- [ ] Commit: `git commit -m "feat: coinfully content, estate band, footer hero, footer"`

---

## Chunk 7: JS Polish + Deploy

### Task 16: main.js — Scroll & Nav Behavior

**Files:**
- Modify: `100yards/coinfully/js/main.js`

- [ ] Write main.js:
```javascript
// main.js — Scroll behavior, nav active state, mobile menu

document.addEventListener('DOMContentLoaded', () => {

  // Nav scroll shadow
  const nav = document.querySelector('.nav');
  window.addEventListener('scroll', () => {
    nav.style.boxShadow = window.scrollY > 20
      ? '0 2px 20px rgba(0,0,0,0.1)'
      : 'none';
  });

  // Mobile burger menu (expand nav__links)
  const burger = document.querySelector('.nav__burger');
  const navLinks = document.querySelector('.nav__links');
  if (burger && navLinks) {
    burger.addEventListener('click', () => {
      const open = navLinks.style.display === 'flex';
      navLinks.style.cssText = open
        ? ''
        : 'display:flex;flex-direction:column;position:absolute;top:68px;left:0;right:0;background:white;padding:24px;gap:16px;border-bottom:1px solid rgba(0,0,0,0.08);z-index:99;';
    });
  }

  // Smooth scroll for anchor links (supplement native behavior for older browsers)
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const target = document.querySelector(a.getAttribute('href'));
      if (target) {
        e.preventDefault();
        target.scrollIntoView({ behavior: 'smooth', block: 'start' });
      }
    });
  });
});
```

- [ ] Test: Scroll down → nav gets shadow. Mobile → burger opens links. Persona cards → smooth scroll to sections.
- [ ] Commit: `git commit -m "feat: coinfully main.js — nav behavior and smooth scroll"`

---

### Task 17: Deploy to Netlify

**Files:**
- Create: `100yards/coinfully/.netlify/state.json`

- [ ] Create new Netlify site and deploy:
```bash
cd /Users/joshmait/Desktop/Claude/100yards/coinfully
npx netlify-cli sites:create --disable-linking
```

- [ ] Note the new site ID from output, then:
```bash
echo '{"siteId": "PASTE_SITE_ID_HERE"}' > .netlify/state.json
npx netlify deploy --prod --dir .
```

- [ ] Rename site to clean URL:
```bash
npx netlify-cli api updateSite --data '{"site_id": "SITE_ID", "body": {"name": "coinfully-homepage"}}'
```

- [ ] Verify live at `https://coinfully-homepage.netlify.app`
- [ ] Final commit:
```bash
git add 100yards/coinfully/
git commit -m "feat: coinfully homepage — complete build deployed to Netlify"
```

---

## QA Checklist

- [ ] Desktop: All sections render correctly, no overflow
- [ ] Mobile (375px): Nav burger works, cards stack, Travis modal fits screen
- [ ] Travis inheritor flow: 4 questions → response → CTA
- [ ] Travis investor flow: 4 questions → response → CTA
- [ ] Travis modal: close button, click-outside close, back button all work
- [ ] Persona card anchors scroll to correct sections
- [ ] All external links go to correct coinfully.com pages
- [ ] No console errors
- [ ] Page loads in under 3 seconds (check Network tab)

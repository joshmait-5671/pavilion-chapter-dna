# New Member Onboarding Wizard — Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a 15-step + 1 interlude mobile-first onboarding wizard that replaces the static joinpavilion.com/new-member-onboarding page.

**Architecture:** Static multi-file HTML/CSS/JS SPA deployed to Netlify. Step engine swaps a single container div. Google Apps Script backend receives progressive POST saves. URL params pre-populate member name/email/city from HubSpot welcome email.

**Tech Stack:** Vanilla JS (no framework), Poppins via Google Fonts, Google Apps Script (web app), Netlify CLI deploy.

**Spec:** `pavilion/docs/superpowers/specs/2026-04-09-new-member-onboarding-design.md`

---

## File Map

| File | Responsibility |
|------|---------------|
| `pavilion/new-member-onboarding/index.html` | Shell: `<head>`, font links, empty `#app` container, script/style tags |
| `pavilion/new-member-onboarding/style.css` | All CSS: variables, reset, layout, progress bar, step anatomy, all component variants (channels, events, people, text inputs, reveals) |
| `pavilion/new-member-onboarding/steps.js` | Array of 16 step config objects — each defines: id, section, headline, eyebrow, type, options/content, CTA label, skip label |
| `pavilion/new-member-onboarding/engine.js` | Core: renders steps from config, handles forward/back nav, CSS slide transitions, LocalStorage persistence, confetti on Step 1 |
| `pavilion/new-member-onboarding/params.js` | Parses URL params (name, email, city), exports `member` object with graceful fallbacks |
| `pavilion/new-member-onboarding/submit.js` | Sends progressive POST to Apps Script on each step advance; queues failed sends for retry |
| `pavilion/new-member-onboarding/confetti.js` | Minimal canvas confetti implementation (self-contained, ~80 lines) |
| `apps-script/onboarding-backend.js` | Google Apps Script: receives POST, appends row to "Pavilion Onboarding Responses" Sheet |

---

## Chunk 1: Foundation — Shell, CSS, Step Engine

### Task 1: Create project scaffold

**Files:**
- Create: `pavilion/new-member-onboarding/index.html`
- Create: `pavilion/new-member-onboarding/style.css`

- [ ] **Step 1: Create the directory and index.html shell**

```bash
mkdir -p /Users/joshmait/Desktop/Claude/pavilion/new-member-onboarding
```

Write `index.html`:
```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0">
  <title>Welcome to Pavilion</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="style.css">
</head>
<body>
  <div id="app">
    <div id="progress-bar"></div>
    <div id="step-container"></div>
  </div>

  <script src="confetti.js"></script>
  <script src="params.js"></script>
  <script src="steps.js"></script>
  <script src="submit.js"></script>
  <script src="engine.js"></script>
</body>
</html>
```

- [ ] **Step 2: Write the base CSS**

Write `style.css` — full content:

```css
/* =========================================
   CSS VARIABLES — Pavilion Brand
   ========================================= */
:root {
  --pink:       #DF285B;
  --pink-lt:    #F14972;
  --navy:       #2B1887;
  --navy-dk:    #180A5C;
  --navy-xdk:   #080122;
  --blue-100:   #EDEAFF;
  --white:      #ffffff;
  --slate:      #64748b;
  --slate-lt:   #94a3b8;

  --radius-pill: 100px;
  --radius-card: 10px;
  --transition-step: 220ms ease-out;
}

/* =========================================
   RESET + BASE
   ========================================= */
*, *::before, *::after {
  margin: 0; padding: 0; box-sizing: border-box;
}

html, body {
  height: 100%;
  background: #f0f0f3;
  font-family: 'Poppins', sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

/* =========================================
   APP SHELL — centered phone-width container
   ========================================= */
#app {
  min-height: 100vh;
  max-width: 420px;
  margin: 0 auto;
  background: var(--white);
  display: flex;
  flex-direction: column;
  position: relative;
  overflow: hidden;
  box-shadow: 0 0 40px rgba(0,0,0,0.08);
}

/* =========================================
   PROGRESS BAR
   ========================================= */
#progress-bar {
  display: flex;
  gap: 3px;
  padding: 0;
  height: 3px;
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  z-index: 10;
}

.prog-seg {
  flex: 1;
  height: 100%;
  background: rgba(43,24,135,0.10);
  transition: background 0.3s ease;
}
.prog-seg.done   { background: var(--navy); }
.prog-seg.active { background: var(--pink); }

/* =========================================
   STEP ANATOMY
   ========================================= */
.step {
  display: flex;
  flex-direction: column;
  min-height: 100vh;
  position: absolute;
  inset: 0;
  will-change: transform, opacity;
}

/* Slide transitions */
.step.entering  { transform: translateX(100%); opacity: 0; }
.step.active    { transform: translateX(0);    opacity: 1; transition: transform var(--transition-step), opacity var(--transition-step); }
.step.exiting   { transform: translateX(-100%); opacity: 0; transition: transform var(--transition-step), opacity var(--transition-step); }
.step.back-entering { transform: translateX(-100%); opacity: 0; }
.step.back-exiting  { transform: translateX(100%); opacity: 0; transition: transform var(--transition-step), opacity var(--transition-step); }

/* Top band */
.step-top {
  background: var(--blue-100);
  padding: 32px 24px 22px;
  flex-shrink: 0;
}

.step-eyebrow {
  font-size: 9px;
  font-weight: 700;
  letter-spacing: 0.24em;
  text-transform: uppercase;
  color: var(--pink);
  margin-bottom: 10px;
}

.step-headline {
  font-size: 24px;
  font-weight: 800;
  color: var(--navy-dk);
  line-height: 1.15;
  letter-spacing: -0.02em;
}

/* Body */
.step-body {
  padding: 22px 24px 32px;
  flex: 1;
  display: flex;
  flex-direction: column;
}

.step-note {
  font-size: 11px;
  font-weight: 300;
  color: var(--slate);
  line-height: 1.7;
  margin-bottom: 20px;
}

/* =========================================
   INTERACTIONS AREA
   ========================================= */
.options-list {
  display: flex;
  flex-direction: column;
  gap: 7px;
  flex: 1;
}

/* Selectable card (channels, prefs, benchmarks, etc.) */
.option-card {
  display: flex;
  align-items: center;
  gap: 11px;
  padding: 11px 14px;
  border-radius: var(--radius-card);
  background: var(--blue-100);
  border: 1.5px solid transparent;
  cursor: pointer;
  transition: background 0.12s, border-color 0.12s;
  user-select: none;
  -webkit-tap-highlight-color: transparent;
}
.option-card.selected {
  background: var(--white);
  border-color: var(--navy);
}

.option-indicator {
  width: 18px;
  height: 18px;
  border-radius: 50%;
  border: 1.5px solid rgba(43,24,135,0.2);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  transition: background 0.12s, border-color 0.12s;
}
.option-card.selected .option-indicator {
  background: var(--navy);
  border-color: var(--navy);
}
.option-check {
  display: none;
  font-size: 9px;
  font-weight: 900;
  color: var(--white);
  line-height: 1;
}
.option-card.selected .option-check { display: block; }

.option-body { flex: 1; min-width: 0; }
.option-name {
  font-size: 12px;
  font-weight: 600;
  color: var(--navy-dk);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.option-sub {
  font-size: 10px;
  font-weight: 400;
  color: var(--slate-lt);
  margin-top: 1px;
}

/* =========================================
   TEXT INPUT
   ========================================= */
.text-input {
  width: 100%;
  padding: 14px 16px;
  border-radius: var(--radius-card);
  border: 1.5px solid rgba(43,24,135,0.15);
  font-family: 'Poppins', sans-serif;
  font-size: 14px;
  font-weight: 400;
  color: var(--navy-dk);
  background: var(--blue-100);
  outline: none;
  transition: border-color 0.15s;
  resize: none;
}
.text-input:focus { border-color: var(--navy); background: var(--white); }
.text-input::placeholder { color: var(--slate-lt); font-weight: 300; }

/* =========================================
   CTA + SKIP
   ========================================= */
.cta-area {
  margin-top: auto;
  padding-top: 20px;
}

.btn-primary {
  display: block;
  width: 100%;
  background: var(--pink);
  color: var(--white);
  border: none;
  border-radius: var(--radius-pill);
  padding: 15px;
  font-family: 'Poppins', sans-serif;
  font-size: 13px;
  font-weight: 700;
  letter-spacing: 0.01em;
  cursor: pointer;
  transition: transform 0.1s, background 0.15s;
  -webkit-tap-highlight-color: transparent;
}
.btn-primary:active { transform: scale(0.97); background: var(--pink-lt); }

.btn-back {
  position: absolute;
  top: 14px;
  left: 18px;
  background: none;
  border: none;
  font-family: 'Poppins', sans-serif;
  font-size: 11px;
  font-weight: 500;
  color: var(--slate-lt);
  cursor: pointer;
  padding: 4px;
  z-index: 20;
  display: none;
}
.btn-back.visible { display: block; }

.skip-link {
  text-align: center;
  font-size: 10px;
  font-weight: 400;
  color: var(--slate-lt);
  margin-top: 12px;
  cursor: pointer;
  letter-spacing: 0.04em;
}

/* =========================================
   PHONE INPUT (Step 4)
   ========================================= */
.phone-wrap {
  display: flex;
  flex-direction: column;
  gap: 12px;
  flex: 1;
}

.sms-consent {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  padding: 12px 14px;
  background: var(--blue-100);
  border-radius: var(--radius-card);
  cursor: pointer;
  user-select: none;
}
.sms-checkbox {
  width: 16px;
  height: 16px;
  border-radius: 4px;
  border: 1.5px solid rgba(43,24,135,0.2);
  background: var(--white);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
  margin-top: 1px;
  transition: background 0.12s, border-color 0.12s;
}
.sms-consent.checked .sms-checkbox {
  background: var(--navy);
  border-color: var(--navy);
}
.sms-check-icon { display: none; font-size: 10px; color: #fff; font-weight: 900; }
.sms-consent.checked .sms-check-icon { display: block; }
.sms-label { font-size: 11px; color: var(--slate); line-height: 1.6; font-weight: 300; }

/* =========================================
   EVENT CARDS (Step 5)
   ========================================= */
.event-card {
  display: flex;
  gap: 14px;
  align-items: center;
  padding: 12px 14px;
  border-radius: var(--radius-card);
  background: var(--blue-100);
  border: 1.5px solid transparent;
  cursor: pointer;
  transition: background 0.12s, border-color 0.12s;
  user-select: none;
}
.event-card.selected { background: var(--white); border-color: var(--navy); }
.event-card.featured { background: var(--navy-dk); border-color: transparent; }
.event-card.featured .ev-day { color: var(--white); }
.event-card.featured .ev-name { color: var(--white); }
.event-card.featured .ev-loc { color: rgba(255,255,255,0.45); }
.event-card.featured .ev-action { color: var(--pink-lt); }

.ev-date { display: flex; flex-direction: column; align-items: center; min-width: 32px; }
.ev-month { font-size: 8px; font-weight: 700; letter-spacing: 0.15em; text-transform: uppercase; color: var(--pink); }
.ev-day { font-size: 22px; font-weight: 800; color: var(--navy-dk); line-height: 1; letter-spacing: -0.02em; }
.ev-info { flex: 1; }
.ev-name { font-size: 12px; font-weight: 600; color: var(--navy-dk); }
.ev-loc { font-size: 10px; color: var(--slate-lt); margin-top: 2px; }
.ev-action { font-size: 10px; font-weight: 700; color: var(--pink); white-space: nowrap; }

/* =========================================
   PEOPLE CARDS (Step 8)
   ========================================= */
.people-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
  flex: 1;
}
.person-card {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  padding: 14px 10px;
  border-radius: 12px;
  background: var(--blue-100);
  border: 1.5px solid transparent;
  cursor: pointer;
  text-align: center;
  transition: background 0.12s, border-color 0.12s;
  user-select: none;
}
.person-card.selected { background: var(--white); border-color: var(--navy); }
.person-avatar {
  width: 44px;
  height: 44px;
  border-radius: 50%;
  background: var(--navy);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  color: var(--white);
  font-weight: 700;
}
.person-name { font-size: 11px; font-weight: 700; color: var(--navy-dk); }
.person-role { font-size: 9px; color: var(--slate-lt); line-height: 1.4; }

/* =========================================
   VIDEO INTERLUDE
   ========================================= */
.video-interlude {
  flex: 1;
  background: var(--navy-xdk);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 16px;
  position: relative;
  padding: 32px 24px;
}
.vi-skip {
  position: absolute;
  top: 16px;
  right: 20px;
  font-size: 11px;
  font-weight: 500;
  color: rgba(255,255,255,0.3);
  cursor: pointer;
  opacity: 0;
  transition: opacity 0.5s;
}
.vi-skip.visible { opacity: 1; }
.vi-tag {
  font-size: 9px;
  font-weight: 600;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: rgba(255,255,255,0.3);
}
.vi-play-btn {
  width: 64px;
  height: 64px;
  border-radius: 50%;
  background: var(--pink);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  cursor: pointer;
  box-shadow: 0 6px 24px rgba(223,40,91,0.4);
  transition: transform 0.15s;
}
.vi-play-btn:active { transform: scale(0.94); }
.vi-meta { text-align: center; }
.vi-name { font-size: 15px; font-weight: 700; color: var(--white); }
.vi-role { font-size: 11px; color: rgba(255,255,255,0.4); margin-top: 3px; }
.vi-duration {
  font-size: 10px;
  font-weight: 600;
  color: rgba(255,255,255,0.3);
  background: rgba(0,0,0,0.4);
  padding: 3px 10px;
  border-radius: 4px;
}
.vi-continue {
  width: 100%;
  background: rgba(255,255,255,0.08);
  color: rgba(255,255,255,0.6);
  border: 1px solid rgba(255,255,255,0.12);
  border-radius: var(--radius-pill);
  padding: 14px;
  font-family: 'Poppins', sans-serif;
  font-size: 13px;
  font-weight: 500;
  cursor: pointer;
  margin-top: 8px;
  transition: background 0.15s;
}
.vi-continue:active { background: rgba(255,255,255,0.14); }

/* =========================================
   WELCOME SCREEN (Step 1)
   ========================================= */
.welcome-screen {
  flex: 1;
  background: var(--blue-100);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 40px 28px 48px;
  text-align: center;
  gap: 20px;
}
.welcome-emoji { font-size: 36px; }
.welcome-hed {
  font-size: 28px;
  font-weight: 800;
  color: var(--navy-dk);
  letter-spacing: -0.02em;
  line-height: 1.15;
}
.welcome-sub {
  font-size: 13px;
  font-weight: 300;
  color: var(--slate);
  line-height: 1.7;
  max-width: 280px;
}
.avatar-row {
  display: flex;
  align-items: center;
  gap: 6px;
  background: var(--white);
  border-radius: var(--radius-pill);
  padding: 8px 16px;
  border: 1px solid rgba(43,24,135,0.08);
}
.avatar-stack { display: flex; }
.av {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  border: 2px solid var(--white);
  margin-left: -8px;
  background: var(--navy);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  color: #fff;
  font-weight: 700;
}
.av:first-child { margin-left: 0; }
.avatar-text {
  font-size: 11px;
  font-weight: 600;
  color: var(--navy);
}
.welcome-cta {
  background: var(--pink);
  color: var(--white);
  border: none;
  border-radius: var(--radius-pill);
  padding: 16px 32px;
  font-family: 'Poppins', sans-serif;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  width: 100%;
  max-width: 300px;
  transition: transform 0.1s;
}
.welcome-cta:active { transform: scale(0.97); }

/* =========================================
   REVEAL SCREEN (Step 15)
   ========================================= */
.reveal-screen {
  flex: 1;
  background: var(--navy-xdk);
  display: flex;
  flex-direction: column;
  padding: 48px 24px 40px;
  gap: 24px;
}
.reveal-hed {
  font-size: 28px;
  font-weight: 800;
  color: var(--white);
  letter-spacing: -0.02em;
  line-height: 1.15;
}
.reveal-items {
  display: flex;
  flex-direction: column;
  gap: 8px;
  flex: 1;
}
.reveal-item {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  background: rgba(255,255,255,0.05);
  border-radius: 10px;
  padding: 13px 14px;
}
.reveal-icon { font-size: 16px; flex-shrink: 0; margin-top: 1px; }
.reveal-text {
  font-size: 12px;
  font-weight: 400;
  color: rgba(255,255,255,0.7);
  line-height: 1.55;
}
.reveal-text strong { color: var(--white); font-weight: 600; }
.reveal-cta {
  background: var(--pink);
  color: var(--white);
  border: none;
  border-radius: var(--radius-pill);
  padding: 16px;
  font-family: 'Poppins', sans-serif;
  font-size: 14px;
  font-weight: 700;
  cursor: pointer;
  transition: transform 0.1s;
}
.reveal-cta:active { transform: scale(0.97); }
.reveal-cta.pulse {
  animation: reveal-pulse 0.6s ease-out;
}
@keyframes reveal-pulse {
  0%   { transform: scale(1); }
  40%  { transform: scale(1.04); }
  100% { transform: scale(1); }
}

/* =========================================
   CONFETTI CANVAS
   ========================================= */
#confetti-canvas {
  position: fixed;
  inset: 0;
  pointer-events: none;
  z-index: 100;
}
```

- [ ] **Step 3: Open in browser and verify layout renders (white page, correct font loads)**

```bash
open /Users/joshmait/Desktop/Claude/pavilion/new-member-onboarding/index.html
```

Expected: blank white page with Poppins font loaded (no errors in console).

- [ ] **Step 4: Commit**

```bash
cd /Users/joshmait/Desktop/Claude
git add pavilion/new-member-onboarding/
git commit -m "feat(onboarding): scaffold — shell HTML + full CSS system"
```

---

### Task 2: URL param parser

**Files:**
- Create: `pavilion/new-member-onboarding/params.js`

- [ ] **Step 1: Write params.js**

```javascript
// params.js — Parse URL params; export `member` with safe fallbacks.
// URL format: ?name=Sarah&email=sarah@co.com&city=San+Francisco
// Fallbacks: name='' (reveal shows generic), city='' (city-aware steps degrade gracefully).

(function () {
  const p = new URLSearchParams(window.location.search);

  const raw = {
    name:  p.get('name')  || '',
    email: p.get('email') || '',
    city:  p.get('city')  || '',
  };

  // Sanitize — strip any HTML to prevent XSS
  function clean(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML.slice(0, 120); // cap length
  }

  const name  = clean(raw.name);
  const email = clean(raw.email);
  const city  = clean(raw.city);

  window.member = {
    name,
    firstName:  name.split(' ')[0],   // '' if name is empty — engine checks hasName before using
    email,
    city,
    hasName:    name.trim().length > 0,
    hasCity:    city.trim().length > 0,
  };
  // Fallback behavior:
  // - Welcome screen: shows "Welcome to Pavilion." (no name) if hasName=false
  // - Reveal screen: omits name from headline if hasName=false
  // - City steps: show generic events/members if hasCity=false
  // - Slack city channel: shows #local-members if hasCity=false
})();
```

- [ ] **Step 2: Verify in console**

Open `index.html` with `?name=Sarah+Chen&email=test@co.com&city=San+Francisco` appended to the file URL. Open DevTools console, type `member` — expect: `{name: "Sarah Chen", firstName: "Sarah", email: "test@co.com", city: "San Francisco", hasName: true, hasCity: true}`.

Test missing params: open without any query string, type `member` — expect: `{name: "", firstName: "", email: "", city: "", hasName: false, hasCity: false}`.

- [ ] **Step 3: Commit**

```bash
git add pavilion/new-member-onboarding/params.js
git commit -m "feat(onboarding): URL param parser with XSS sanitization + fallbacks"
```

---

### Task 3: Confetti

**Files:**
- Create: `pavilion/new-member-onboarding/confetti.js`

- [ ] **Step 1: Write confetti.js**

```javascript
// confetti.js — Minimal canvas confetti. Call window.launchConfetti() to fire.

window.launchConfetti = function () {
  const canvas = document.createElement('canvas');
  canvas.id = 'confetti-canvas';
  canvas.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:999;width:100%;height:100%;';
  document.body.appendChild(canvas);
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight;

  const ctx = canvas.getContext('2d');
  const colors = ['#DF285B', '#2B1887', '#EDEAFF', '#F14972', '#180A5C', '#ffffff'];
  const pieces = Array.from({ length: 90 }, () => ({
    x:   Math.random() * canvas.width,
    y:   Math.random() * canvas.height * -1,
    r:   Math.random() * 6 + 3,
    d:   Math.random() * 2 + 1,
    c:   colors[Math.floor(Math.random() * colors.length)],
    tilt: Math.random() * 10 - 10,
    ts:  Math.random() * 0.2 - 0.1,
  }));

  let frame;
  let start = null;
  const duration = 1800;

  function draw(ts) {
    if (!start) start = ts;
    const elapsed = ts - start;

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    pieces.forEach(p => {
      p.y  += p.d + 0.5;
      p.tilt += p.ts;
      ctx.beginPath();
      ctx.ellipse(p.x, p.y, p.r, p.r * 0.5, p.tilt, 0, Math.PI * 2);
      ctx.fillStyle = p.c;
      ctx.globalAlpha = Math.max(0, 1 - elapsed / duration);
      ctx.fill();
    });

    if (elapsed < duration) {
      frame = requestAnimationFrame(draw);
    } else {
      canvas.remove();
    }
  }

  frame = requestAnimationFrame(draw);
};
```

- [ ] **Step 2: Verify confetti fires**

Add `<button onclick="launchConfetti()">Test</button>` temporarily to index.html, open in browser, click button — expect: pink/navy confetti burst for ~1.8 seconds, canvas self-removes. Remove the test button after verifying.

- [ ] **Step 3: Commit**

```bash
git add pavilion/new-member-onboarding/confetti.js
git commit -m "feat(onboarding): canvas confetti for welcome screen"
```

---

### Task 4: Step definitions

**Files:**
- Create: `pavilion/new-member-onboarding/steps.js`

This file defines the content of all 16 screens (15 steps + 1 interlude) as a data structure. The engine reads this to render — no logic here, only content config.

- [ ] **Step 1: Write steps.js**

```javascript
// steps.js — All step content. Loaded before engine.js.
// `member` (from params.js) is available at load time.

window.STEPS = [

  // ── STEP 1: WELCOME ──────────────────────────────
  {
    id: 'welcome',
    type: 'welcome',
    // Rendered entirely by engine as a special case
  },

  // ── STEP 2: SLACK CHANNELS ───────────────────────
  {
    id: 'slack-channels',
    type: 'multi-select',
    eyebrow: 'Your Community',
    headline: 'Pick channels\nbuilt for you.',
    note: 'Curated for revenue leaders at your stage. Choose 3–5. You can change these any time.',
    cta: 'Add these channels',
    skip: 'Skip for now',
    options: [
      { id: 'revenue-strategy',    label: '#revenue-strategy',    sub: 'Pipeline · GTM · Forecasting' },
      { id: 'intros-referrals',    label: '#intros-and-referrals', sub: 'Warm connections, fast' },
      { id: 'benchmark-data',      label: '#benchmark-data',       sub: 'Comp · Team size · GTM' },
      { id: 'ai-in-gtm',           label: '#ai-in-gtm',            sub: 'Tools · Experiments' },
      { id: 'exec-leadership',     label: '#exec-leadership',      sub: 'Peer conversations' },
      { id: 'city',                label: () => member.hasCity ? `#${member.city.toLowerCase().replace(/\s+/g,'-')}` : '#local-members', sub: 'Local events · Meetups' },
    ],
    key: 'slack_channels',
  },

  // ── STEP 3: EMAIL PREFS ──────────────────────────
  {
    id: 'email-prefs',
    type: 'multi-select',
    eyebrow: 'Your Community',
    headline: 'How should we\nstay in touch?',
    note: 'Pick what feels right. You can always unsubscribe from individual lists.',
    cta: 'Save preferences',
    skip: 'Skip for now',
    options: [
      { id: 'weekly-digest',    label: 'Weekly digest',      sub: 'The best of Pavilion, every Monday' },
      { id: 'event-alerts',     label: 'Event alerts',       sub: 'New events in your area + online' },
      { id: 'member-spotlight', label: 'Member spotlights',  sub: 'Who to know and why' },
      { id: 'ai-newsletter',    label: 'AI + GTM roundup',   sub: 'Weekly AI-for-revenue-leaders brief' },
    ],
    key: 'email_prefs',
  },

  // ── STEP 4: SMS OPT-IN ───────────────────────────
  {
    id: 'sms-optin',
    type: 'phone',
    eyebrow: 'Your Community',
    headline: 'Can we text you?',
    note: 'Intros, event reminders, when someone asks about you. Short messages. Never spam.',
    cta: 'Yes — text me',
    skip: 'No thanks',
    key: 'sms',
  },

  // ── STEP 5: EVENTS ───────────────────────────────
  {
    id: 'events',
    type: 'events',
    eyebrow: 'Your Calendar',
    headline: () => member.hasCity ? `Events in\n${member.city}.` : 'Events near\nyou.',
    note: 'RSVP now or save for later. We'll remind you either way.',
    cta: 'Save my picks',
    skip: 'Nothing looks right',
    key: 'events_rsvp',
  },

  // ── STEP 6: TRAVEL CITY ──────────────────────────
  {
    id: 'travel-city',
    type: 'text-input',
    eyebrow: 'Your Calendar',
    headline: 'Do you travel\nto another city?',
    note: 'Tell us where and we'll add those events to your radar too.',
    placeholder: 'e.g. New York, Chicago, Austin',
    cta: 'Add this city',
    skip: 'I stay put',
    key: 'travel_city',
  },

  // ── STEP 7: CLASSES ──────────────────────────────
  {
    id: 'classes',
    type: 'multi-select',
    eyebrow: 'Your Calendar',
    headline: 'Classes on\nyour radar.',
    note: 'Enroll now or we'll remind you closer to the start date.',
    cta: 'Save these classes',
    skip: 'Not right now',
    options: [
      { id: 'sales-leadership',   label: 'Sales Leadership Intensive',  sub: 'Starts May 12 · 6 weeks' },
      { id: 'revops-101',         label: 'RevOps Fundamentals',         sub: 'Starts Apr 28 · 4 weeks' },
      { id: 'cs-excellence',      label: 'CS Excellence Program',       sub: 'Starts May 5 · 6 weeks' },
      { id: 'exec-presence',      label: 'Executive Presence',          sub: 'Starts Apr 30 · 3 weeks' },
      { id: 'ai-for-gtm',         label: 'AI for GTM Leaders',          sub: 'Starts May 1 · 2 weeks' },
    ],
    key: 'classes',
  },

  // ── STEP 8: PEOPLE ───────────────────────────────
  {
    id: 'people',
    type: 'people',
    eyebrow: 'Meet Someone',
    headline: () => member.hasCity ? `Members in\n${member.city}.` : 'Members near\nyou.',
    note: 'Pick 1–2 people to be introduced to. We'll send a warm note this week.',
    cta: 'Intro me to these people',
    skip: 'Not ready yet',
    key: 'intro_requests',
  },

  // ── VIDEO INTERLUDE ───────────────────────────────
  {
    id: 'video-interlude',
    type: 'video-interlude',
    // Rendered as special case
  },

  // ── STEP 9: VOICE ────────────────────────────────
  {
    id: 'your-voice',
    type: 'multi-select',
    eyebrow: 'Your Voice',
    headline: 'Where would you\nlike to be heard?',
    note: 'We\'ll promote your insights and ideas in the channels you choose. Or not at all — your call.',
    cta: 'Save my preferences',
    skip: 'Not right now',
    options: [
      { id: 'linkedin',    label: 'LinkedIn',         sub: 'Pavilion reposts your content' },
      { id: 'slack',       label: 'Slack shoutouts',  sub: 'Featured in member channels' },
      { id: 'newsletter',  label: 'Newsletter',       sub: 'Member spotlight feature' },
      { id: 'podcast',     label: 'Podcast guest',    sub: 'Pavilion podcast interview' },
    ],
    key: 'promote_channels',
  },

  // ── STEP 10: BENCHMARKS ──────────────────────────
  {
    id: 'benchmarks',
    type: 'multi-select',
    eyebrow: 'Your Data',
    headline: 'Benchmarks\nyou care about.',
    note: 'We\'ll make sure you get the data reports most relevant to your role.',
    cta: 'Send me these reports',
    skip: 'Skip',
    options: [
      { id: 'team-size',    label: 'Team size benchmarks',  sub: 'GTM team structure by ARR' },
      { id: 'gtm-data',     label: 'GTM metrics',           sub: 'CAC, NRR, win rates by segment' },
      { id: 'hiring-plans', label: 'Hiring plans',          sub: 'Who\'s growing what function' },
      { id: 'tech-stack',   label: 'Tech stack trends',     sub: 'What revenue leaders are buying' },
    ],
    key: 'benchmarks',
  },

  // ── STEP 11: COMP PACKAGE ────────────────────────
  {
    id: 'comp-package',
    type: 'single-select',
    eyebrow: 'Your Data',
    headline: 'Looking for comp\npackage expertise?',
    note: 'We have coaches and benchmark data specifically for executive compensation.',
    cta: 'Continue',
    skip: null,
    options: [
      { id: 'yes',  label: 'Yes — connect me to resources', sub: 'Coaching, benchmarks, negotiation guides' },
      { id: 'maybe', label: 'Tell me more first',           sub: 'Send me an overview' },
      { id: 'no',   label: 'Not right now',                 sub: '' },
    ],
    key: 'comp_interest',
  },

  // ── STEP 12: ONE THING ───────────────────────────
  {
    id: 'one-thing',
    type: 'textarea',
    eyebrow: 'The Human Part',
    headline: 'One thing the\ncommunity should know.',
    note: 'What makes you you? Keep it short. Members will see this.',
    placeholder: 'e.g. I\'ve built three sales teams from scratch. I love the chaos.',
    cta: 'That\'s me',
    skip: 'Skip this one',
    key: 'one_thing',
  },

  // ── STEP 13: COMMITMENT ──────────────────────────
  {
    id: 'commitment',
    type: 'textarea',
    eyebrow: 'The Human Part',
    headline: '12 months from now,\nwhat does success look like?',
    note: 'Your answer stays with your profile. It\'s not a contract — it\'s a north star.',
    placeholder: 'e.g. My team hits 120% of plan and I\'m sleeping again.',
    cta: 'That\'s my goal',
    skip: 'Skip this one',
    key: 'commitment',
  },

  // ── STEP 14: FAVORITE SONG ───────────────────────
  {
    id: 'favorite-song',
    type: 'text-input',
    eyebrow: 'The Human Part',
    headline: 'Favorite song\nright now.',
    note: 'We\'re building a Pavilion Spotify playlist. What\'s on repeat?',
    placeholder: 'Song · Artist',
    cta: 'Add to the playlist',
    skip: 'Skip',
    key: 'favorite_song',
  },

  // ── STEP 15: REVEAL ──────────────────────────────
  {
    id: 'reveal',
    type: 'reveal',
    // Rendered as special case using saved state
  },

];
```

- [ ] **Step 2: Verify steps loaded**

Open index.html in browser, open console, type `STEPS.length` — expect: `16`.

- [ ] **Step 3: Commit**

```bash
git add pavilion/new-member-onboarding/steps.js
git commit -m "feat(onboarding): step definitions — 16 screens as data config"
```

---

## Chunk 2: Engine, Steps 1–8, Video Interlude

### Task 5: Step engine (core)

**Files:**
- Create: `pavilion/new-member-onboarding/engine.js`

This is the largest file. It reads `STEPS`, renders each step, manages state, handles navigation, and persists to localStorage.

- [ ] **Step 1: Write engine.js**

```javascript
// engine.js — Wizard engine. Reads STEPS, renders to #step-container,
// manages navigation, state persistence, and submit triggers.

(function () {

  // ── STATE ──────────────────────────────────────────
  const STORAGE_KEY = 'pavilion-onboarding-v1';

  let currentIndex = 0;
  let state = loadState();

  function loadState() {
    try {
      return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {};
    } catch (_) { return {}; }
  }

  function saveState() {
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(state));
    } catch (_) {}
  }

  function setState(key, value) {
    if (!key) return;
    state[key] = value;
    saveState();
  }

  // ── PROGRESS BAR ─────────────────────────────────
  const progressBar = document.getElementById('progress-bar');
  const NUMBERED_STEPS = 15; // Interlude doesn't count

  function renderProgress(index) {
    const interludeIdx = STEPS.findIndex(s => s.type === 'video-interlude');

    // Hide progress bar during video interlude — it's not a numbered step
    if (index === interludeIdx) {
      progressBar.innerHTML = '';
      return;
    }

    // Map wizard array index → 1-based step number (skipping the interlude slot)
    // Indices 0–(interludeIdx-1) → step numbers 1–interludeIdx
    // Indices (interludeIdx+1)–end → step numbers interludeIdx+1…15
    const stepNum = index < interludeIdx ? index + 1 : index; // interlude slot removed from count

    progressBar.innerHTML = Array.from({ length: NUMBERED_STEPS }, (_, i) => {
      const seg = i + 1;
      let cls = 'prog-seg';
      if (seg < stepNum) cls += ' done';
      else if (seg === stepNum) cls += ' active';
      return `<div class="${cls}"></div>`;
    }).join('');
  }

  // ── RENDER ────────────────────────────────────────
  const container = document.getElementById('step-container');

  function renderStep(index, direction) {
    const step = STEPS[index];
    if (!step) return;

    renderProgress(index);

    // Remove old step with exit animation
    const old = container.querySelector('.step');
    if (old) {
      old.classList.remove('active');
      old.classList.add(direction === 'back' ? 'back-exiting' : 'exiting');
      setTimeout(() => old.remove(), 240);
    }

    // Build new step element
    const el = document.createElement('div');
    el.className = 'step entering';
    el.innerHTML = buildStepHTML(step, index);
    container.appendChild(el);

    // Trigger enter animation
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        el.classList.remove('entering', 'back-entering');
        el.classList.add('active');
        if (direction === 'back') {
          el.classList.add('back-entering');
          requestAnimationFrame(() => {
            el.classList.remove('back-entering');
          });
        }
      });
    });

    // Back button
    const backBtn = document.createElement('button');
    backBtn.className = 'btn-back' + (index > 0 ? ' visible' : '');
    backBtn.textContent = '← Back';
    backBtn.onclick = () => navigate(currentIndex - 1, 'back');
    container.appendChild(backBtn);

    // Wire interactions
    wireStep(el, step);
  }

  // ── HTML BUILDERS ──────────────────────────────────

  function resolveVal(v) {
    return typeof v === 'function' ? v() : v;
  }

  function buildStepHTML(step, index) {
    switch (step.type) {
      case 'welcome':         return buildWelcome();
      case 'video-interlude': return buildVideoInterlude();
      case 'reveal':          return buildReveal();
      case 'multi-select':    return buildMultiSelect(step);
      case 'single-select':   return buildSingleSelect(step);
      case 'phone':           return buildPhone(step);
      case 'text-input':      return buildTextInput(step);
      case 'textarea':        return buildTextarea(step);
      case 'events':          return buildEvents(step);
      case 'people':          return buildPeople(step);
      default: return '<div class="step-body"><p>Unknown step type.</p></div>';
    }
  }

  function stepShell(step, bodyContent) {
    const hl = resolveVal(step.headline).replace('\n', '<br>');
    return `
      <div class="step-top">
        ${step.eyebrow ? `<div class="step-eyebrow">${step.eyebrow}</div>` : ''}
        <div class="step-headline">${hl}</div>
      </div>
      <div class="step-body">
        ${step.note ? `<p class="step-note">${step.note}</p>` : ''}
        ${bodyContent}
        <div class="cta-area">
          <button class="btn-primary" data-action="cta">${step.cta}</button>
          ${step.skip ? `<div class="skip-link" data-action="skip">${step.skip}</div>` : ''}
        </div>
      </div>
    `;
  }

  function buildWelcome() {
    const name = member.hasName ? `Welcome,<br>${member.firstName}.` : 'Welcome to<br>Pavilion.';
    const cityText = member.hasCity ? `8 members in ${member.city}` : '10,000+ members worldwide';
    return `
      <div class="welcome-screen">
        <div class="welcome-emoji">🎉</div>
        <div class="welcome-hed">${name}</div>
        <p class="welcome-sub">You're joining revenue leaders who figured out they don't have to do this alone.</p>
        <div class="avatar-row">
          <div class="avatar-stack">
            <div class="av">👩</div><div class="av">👨</div><div class="av">👩</div><div class="av">👨</div>
          </div>
          <span class="avatar-text">${cityText}</span>
        </div>
        <button class="welcome-cta" data-action="cta">Let's set you up →</button>
      </div>
    `;
  }

  function buildMultiSelect(step) {
    const saved = state[step.key] || [];
    const options = step.options.map(opt => {
      const label = resolveVal(opt.label);
      const isSel = saved.includes(opt.id);
      return `
        <div class="option-card${isSel ? ' selected' : ''}" data-id="${opt.id}">
          <div class="option-indicator"><span class="option-check">✓</span></div>
          <div class="option-body">
            <div class="option-name">${label}</div>
            ${opt.sub ? `<div class="option-sub">${opt.sub}</div>` : ''}
          </div>
        </div>
      `;
    }).join('');
    return stepShell(step, `<div class="options-list">${options}</div>`);
  }

  function buildSingleSelect(step) {
    const saved = state[step.key] || null;
    const options = step.options.map(opt => {
      const isSel = saved === opt.id;
      return `
        <div class="option-card${isSel ? ' selected' : ''}" data-id="${opt.id}" data-single="true">
          <div class="option-indicator"><span class="option-check">✓</span></div>
          <div class="option-body">
            <div class="option-name">${opt.label}</div>
            ${opt.sub ? `<div class="option-sub">${opt.sub}</div>` : ''}
          </div>
        </div>
      `;
    }).join('');
    return stepShell(step, `<div class="options-list">${options}</div>`);
  }

  function buildPhone(step) {
    const saved = state['phone'] || '';
    const optedIn = state['sms_opt_in'] || false;
    return stepShell(step, `
      <div class="phone-wrap">
        <input type="tel" class="text-input" placeholder="(555) 555-5555"
          value="${saved}" id="phone-input" autocomplete="tel">
        <div class="sms-consent${optedIn ? ' checked' : ''}" id="sms-consent">
          <div class="sms-checkbox"><span class="sms-check-icon">✓</span></div>
          <span class="sms-label">I agree to receive text messages from Pavilion. Reply STOP to opt out at any time.</span>
        </div>
      </div>
    `);
  }

  function buildTextInput(step) {
    const saved = state[step.key] || '';
    return stepShell(step, `
      <input type="text" class="text-input" placeholder="${step.placeholder || ''}"
        value="${saved}" id="text-field">
    `);
  }

  function buildTextarea(step) {
    const saved = state[step.key] || '';
    return stepShell(step, `
      <textarea class="text-input" rows="4" placeholder="${step.placeholder || ''}"
        id="textarea-field">${saved}</textarea>
    `);
  }

  function buildEvents(step) {
    const saved = state[step.key] || [];
    const events = getEvents();
    const cards = events.map((ev, i) => {
      const isFeatured = i === 0;
      const isSel = saved.includes(ev.id);
      return `
        <div class="event-card${isFeatured ? ' featured' : ''}${isSel ? ' selected' : ''}" data-id="${ev.id}">
          <div class="ev-date">
            <div class="ev-month">${ev.month}</div>
            <div class="ev-day">${ev.day}</div>
          </div>
          <div class="ev-info">
            <div class="ev-name">${ev.name}</div>
            <div class="ev-loc">📍 ${ev.location}</div>
          </div>
          <div class="ev-action">${isSel ? '✓' : 'Save →'}</div>
        </div>
      `;
    }).join('');
    return stepShell(step, `<div class="options-list">${cards}</div>`);
  }

  function buildPeople(step) {
    const saved = state[step.key] || [];
    const people = getPeople();
    const cards = people.map(p => {
      const isSel = saved.includes(p.id);
      return `
        <div class="person-card${isSel ? ' selected' : ''}" data-id="${p.id}">
          <div class="person-avatar">${p.initials}</div>
          <div class="person-name">${p.name}</div>
          <div class="person-role">${p.role}</div>
        </div>
      `;
    }).join('');
    return stepShell(step, `<div class="people-grid">${cards}</div>`);
  }

  function buildVideoInterlude() {
    // V1 stub — placeholder until real videos exist
    const members = getVideoMembers();
    const vm = members[Math.floor(Math.random() * members.length)];
    return `
      <div class="video-interlude">
        <div class="vi-skip" id="vi-skip">Skip</div>
        <div class="vi-tag">📱 Member Story</div>
        <div class="vi-play-btn">▶</div>
        <div class="vi-meta">
          <div class="vi-name">${vm.name}</div>
          <div class="vi-role">${vm.role}</div>
        </div>
        <div class="vi-duration">${vm.duration}</div>
        <button class="vi-continue" data-action="cta">Continue →</button>
      </div>
    `;
  }

  function buildReveal() {
    const channels  = state['slack_channels'] || [];
    const events    = state['events_rsvp']    || [];
    const intros    = state['intro_requests'] || [];
    const benchmarks = state['benchmarks']    || [];
    const comp      = state['comp_interest'];

    const introText = intros.length > 0
      ? `Expect a message this week from <strong>${getPersonName(intros[0])}</strong>`
      : `We're working on your first intro. Expect a message within the week.`;

    const eventText = events.length > 0
      ? `Saved for <strong>${getEventName(events[0])}</strong>`
      : `Your local events are on your radar`;

    const chText = channels.length > 0
      ? `<strong>${channels.length} channel${channels.length > 1 ? 's' : ''} added</strong> — ${channels.slice(0,2).join(', ')}${channels.length > 2 ? ' + more' : ''}`
      : `Channels ready when you open Slack`;

    const items = [
      { icon: '💬', text: chText },
      { icon: '📅', text: eventText },
      { icon: '🤝', text: introText },
      benchmarks.length > 0 ? { icon: '📊', text: `<strong>Benchmark reports</strong> being prepared` } : null,
      comp === 'yes' || comp === 'maybe' ? { icon: '💼', text: `<strong>Exec comp resources</strong> on their way` } : null,
    ].filter(Boolean);

    const itemsHTML = items.map(item => `
      <div class="reveal-item">
        <div class="reveal-icon">${item.icon}</div>
        <div class="reveal-text">${item.text}</div>
      </div>
    `).join('');

    // If name is missing, headline reads "Your Pavilion is ready." (no dangling comma or blank)
    const nameSuffix = member.hasName ? `,<br>${member.firstName}` : '';

    return `
      <div class="reveal-screen">
        <div class="reveal-hed">Your Pavilion<br>is ready${nameSuffix}.</div>
        <div class="reveal-items">${itemsHTML}</div>
        <button class="reveal-cta" data-action="cta">Go to Slack →</button>
      </div>
    `;
  }

  // ── WIRING ─────────────────────────────────────────

  function wireStep(el, step) {
    // Multi-select toggling
    el.querySelectorAll('.option-card:not([data-single])').forEach(card => {
      card.addEventListener('click', () => {
        card.classList.toggle('selected');
      });
    });

    // Single-select
    el.querySelectorAll('.option-card[data-single]').forEach(card => {
      card.addEventListener('click', () => {
        el.querySelectorAll('.option-card[data-single]').forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
      });
    });

    // Event cards
    el.querySelectorAll('.event-card').forEach(card => {
      card.addEventListener('click', () => { card.classList.toggle('selected'); });
    });

    // Person cards
    el.querySelectorAll('.person-card').forEach(card => {
      card.addEventListener('click', () => {
        const selectedCount = el.querySelectorAll('.person-card.selected').length;
        if (!card.classList.contains('selected') && selectedCount >= 2) return; // max 2
        card.classList.toggle('selected');
      });
    });

    // SMS consent
    const consent = el.querySelector('#sms-consent');
    if (consent) {
      consent.addEventListener('click', () => consent.classList.toggle('checked'));
    }

    // Video interlude skip (appears after 5s)
    const viSkip = el.querySelector('#vi-skip');
    if (viSkip) {
      setTimeout(() => viSkip.classList.add('visible'), 5000);
      viSkip.addEventListener('click', () => navigate(currentIndex + 1, 'forward'));
    }

    // CTA
    el.querySelectorAll('[data-action="cta"]').forEach(btn => {
      btn.addEventListener('click', () => handleCta(el, step));
    });

    // Skip
    el.querySelectorAll('[data-action="skip"]').forEach(link => {
      link.addEventListener('click', () => navigate(currentIndex + 1, 'forward'));
    });

    // Reveal CTA → Pavilion Slack
    const revealCta = el.querySelector('.reveal-cta');
    if (revealCta) {
      revealCta.addEventListener('click', () => {
        revealCta.classList.add('pulse');
        setTimeout(() => {
          window.location.href = 'https://joinpavilion.slack.com';
        }, 600);
      });
    }

    // Welcome CTA
    const welCta = el.querySelector('.welcome-cta');
    if (welCta) {
      welCta.addEventListener('click', () => navigate(currentIndex + 1, 'forward'));
    }
  }

  function handleCta(el, step) {
    const collected = collectStepData(el, step);
    if (collected !== null) {
      setState(step.key, collected);
      window.submitStep && window.submitStep(step.key, collected);
    }
    navigate(currentIndex + 1, 'forward');
  }

  function collectStepData(el, step) {
    if (!step.key) return null;

    switch (step.type) {
      case 'multi-select':
        return [...el.querySelectorAll('.option-card.selected')].map(c => c.dataset.id);

      case 'single-select':
        const sel = el.querySelector('.option-card.selected');
        return sel ? sel.dataset.id : null;

      case 'phone': {
        // Store only under the step key ('sms') to avoid duplicated keys in state.
        // The reveal and submit both read from state['sms'].phone / state['sms'].sms_opt_in.
        const phone = el.querySelector('#phone-input')?.value.trim() || '';
        const sms_opt_in = el.querySelector('#sms-consent')?.classList.contains('checked') || false;
        return { phone, sms_opt_in };
      }

      case 'text-input':
        return el.querySelector('#text-field')?.value.trim() || '';

      case 'textarea':
        return el.querySelector('#textarea-field')?.value.trim() || '';

      case 'events':
      case 'people':
        return [...el.querySelectorAll('.event-card.selected, .person-card.selected')]
          .map(c => c.dataset.id);

      default:
        return null;
    }
  }

  // ── NAVIGATION ────────────────────────────────────

  function navigate(index, direction) {
    if (index < 0 || index >= STEPS.length) return;
    currentIndex = index;
    renderStep(currentIndex, direction);
  }

  // ── CONTENT DATA (placeholder until API-driven) ───

  function getEvents() {
    const city = member.city || 'your city';
    return [
      { id: 'ev1', month: 'Apr', day: '17', name: 'Revenue Leaders Dinner',    location: `The Battery · ${city}` },
      { id: 'ev2', month: 'Apr', day: '24', name: 'GTM Masterclass: AI in the Stack', location: 'Virtual · 12pm PT' },
      { id: 'ev3', month: 'May', day: '6',  name: 'Pavilion Summit · NYC',     location: 'Convene · Midtown' },
    ];
  }

  function getPeople() {
    return [
      { id: 'p1', initials: 'SC', name: 'Sarah Chen',    role: 'VP Sales · Series B' },
      { id: 'p2', initials: 'MR', name: 'Marcus Reyes',  role: 'CRO · SaaS' },
      { id: 'p3', initials: 'AK', name: 'Anya Kim',      role: 'Head of CS' },
      { id: 'p4', initials: 'JT', name: 'James Torres',  role: 'VP Marketing' },
      { id: 'p5', initials: 'LP', name: 'Lisa Park',     role: 'RevOps Lead' },
      { id: 'p6', initials: 'DW', name: 'David Wu',      role: 'VP Sales · PLG' },
    ];
  }

  function getVideoMembers() {
    return [
      { name: 'Sarah Chen',   role: 'VP of Sales · Attentive · San Francisco', duration: '0:28' },
      { name: 'Marcus Reyes', role: 'CRO · Rippling · New York',               duration: '0:32' },
      { name: 'Anya Kim',     role: 'Head of CS · Notion · Remote',            duration: '0:24' },
    ];
  }

  function getPersonName(id) {
    return getPeople().find(p => p.id === id)?.name || 'your new connection';
  }

  function getEventName(id) {
    return getEvents().find(e => e.id === id)?.name || 'your saved event';
  }

  // ── BOOT ──────────────────────────────────────────

  function boot() {
    // Step 1 (welcome) gets confetti
    const welcomeIdx = STEPS.findIndex(s => s.type === 'welcome');
    if (currentIndex === welcomeIdx) {
      setTimeout(() => window.launchConfetti && window.launchConfetti(), 400);
    }
    renderStep(currentIndex, 'forward');
  }

  document.addEventListener('DOMContentLoaded', boot);

})();
```

- [ ] **Step 2: Open in browser, verify Step 1 renders**

Open `index.html?name=Sarah+Chen&city=San+Francisco`. Expected:
- Welcome screen with "Welcome, Sarah." headline
- Confetti burst after ~400ms
- Avatar row with "8 members in San Francisco"
- "Let's set you up →" button visible

- [ ] **Step 3: Click through to Step 2, verify channels render**

Click the CTA. Expected: Slack channels step slides in, progress bar shows 2 active, 5 channel options visible.

- [ ] **Step 4: Test back navigation**

Click "← Back". Expected: Welcome screen slides back in from left, Step 2 slides out right.

- [ ] **Step 5: Test localStorage persistence**

On Step 2, select 2 channels, advance to Step 3. Reload page. Navigate forward — selected channels on Step 2 should still be highlighted.

- [ ] **Step 6: Commit**

```bash
git add pavilion/new-member-onboarding/engine.js
git commit -m "feat(onboarding): step engine — render, nav, state, transitions, 16 screens"
```

---

### Task 6: Walk all 16 steps in browser

Manual verification pass — no code changes, just confirming every screen renders.

- [ ] Navigate all 16 steps forward: Welcome → Slack → Email → SMS → Events → Travel → Classes → People → Video → Voice → Benchmarks → Comp → One Thing → Commitment → Song → Reveal
- [ ] Verify: progress bar updates correctly on each step
- [ ] Verify: Reveal screen correctly shows selected channels, event name, intro name
- [ ] Verify: Video interlude Skip button appears after 5 seconds
- [ ] Verify: on Step 11 (comp), selecting an option auto-advances when CTA tapped
- [ ] Verify: Step 15 CTA pulses on click

If anything looks wrong, fix it in engine.js before committing. No new commit needed for this task — it's a verification pass only.

---

## Chunk 3: Submission Backend, Deploy, Memory

### Task 7: Apps Script backend

**Files:**
- Create: `pavilion/new-member-onboarding/apps-script/onboarding-backend.js` (reference copy — actual deploy is via Apps Script editor)

- [ ] **Step 1: Write the Apps Script**

This code runs as a Google Apps Script Web App, receives POST requests, and appends to a Sheet.

Save this to `pavilion/new-member-onboarding/apps-script/onboarding-backend.js` for reference:

```javascript
// Google Apps Script — Pavilion Onboarding Backend
// Deploy as Web App: Execute as Me, Anyone can access.

const SHEET_NAME = 'Pavilion Onboarding Responses';

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const ss = SpreadsheetApp.getActiveSpreadsheet();
    let sheet = ss.getSheetByName(SHEET_NAME);

    // Create sheet + headers if first time
    if (!sheet) {
      sheet = ss.insertSheet(SHEET_NAME);
      sheet.appendRow([
        'timestamp', 'session_id', 'member_name', 'member_email', 'city',
        'step_key', 'step_value', 'completed',
      ]);
      sheet.setFrozenRows(1);
    }

    const sessionId = data.session_id || '';
    const stepKey   = data.key || '';

    // Deduplication: overwrite existing row for same session_id + step_key
    // (handles user going back and re-submitting a step)
    if (sessionId && stepKey) {
      const values = sheet.getDataRange().getValues();
      for (let i = 1; i < values.length; i++) {
        if (values[i][1] === sessionId && values[i][5] === stepKey) {
          const row = i + 1; // 1-indexed
          sheet.getRange(row, 1, 1, 8).setValues([[
            new Date().toISOString(), sessionId,
            data.member_name || '', data.member_email || '', data.member_city || '',
            stepKey, JSON.stringify(data.value), data.completed ? 'TRUE' : '',
          ]]);
          return ContentService.createTextOutput(JSON.stringify({ ok: true, action: 'updated' }))
            .setMimeType(ContentService.MimeType.JSON);
        }
      }
    }

    // No existing row — append new
    sheet.appendRow([
      new Date().toISOString(), sessionId,
      data.member_name || '', data.member_email || '', data.member_city || '',
      stepKey, JSON.stringify(data.value), data.completed ? 'TRUE' : '',
    ]);

    return ContentService.createTextOutput(JSON.stringify({ ok: true, action: 'appended' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({ ok: false, error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService.createTextOutput('Pavilion Onboarding Backend — POST only');
}
```

- [ ] **Step 2: Deploy the Apps Script**

Deploy settings matter — do this exactly:

1. Create a Google Sheet named "Pavilion Onboarding Responses" (this will be the container)
2. Inside the sheet: Extensions → Apps Script → opens script editor
3. Delete the default `function myFunction()` and paste the full code above
4. Save (Cmd+S), name the project "Pavilion Onboarding"
5. Deploy → New deployment → Type: Web app
6. **Execute as: Me** (josh.mait@joinpavilion.com)
7. **Who has access: Anyone** (required for CORS — unauthenticated cross-origin POSTs)
8. Click Deploy → Authorize → Grant permissions
9. Copy the deployment URL: `https://script.google.com/macros/s/AKf.../exec`
10. **IMPORTANT:** After each code change, you must Deploy → New deployment (not "Manage deployments") to get an updated URL, OR redeploy to the same deployment ID.

- [ ] **Step 3: Test the endpoint manually**

```bash
curl -s -X POST "YOUR_APPS_SCRIPT_URL" \
  -H "Content-Type: application/json" \
  -d '{"session_id":"test-001","member_name":"Test User","member_email":"test@test.com","member_city":"San Francisco","key":"slack_channels","value":["revenue-strategy","intros-referrals"]}'
```

Expected response: `{"ok":true}`. Check the Sheet — a new row should appear.

- [ ] **Step 4: Commit the reference copy**

```bash
git add pavilion/new-member-onboarding/apps-script/
git commit -m "feat(onboarding): Apps Script backend reference — progressive step save"
```

---

### Task 8: Submit.js — progressive save

**Files:**
- Create: `pavilion/new-member-onboarding/submit.js`

- [ ] **Step 1: Write submit.js**

Replace `YOUR_APPS_SCRIPT_URL` with the actual deployment URL from Task 7.

```javascript
// submit.js — Sends each step's data to Apps Script on advance.
// Fails silently (doesn't block the wizard).

(function () {
  const ENDPOINT = 'YOUR_APPS_SCRIPT_URL'; // Replace after deploy

  // Stable session ID for this wizard run
  const SESSION_ID = (() => {
    const key = 'pav-session-id';
    let id = sessionStorage.getItem(key);
    if (!id) {
      id = 'sess-' + Date.now() + '-' + Math.random().toString(36).slice(2, 8);
      sessionStorage.setItem(key, id);
    }
    return id;
  })();

  window.submitStep = function (key, value) {
    if (!ENDPOINT || ENDPOINT === 'YOUR_APPS_SCRIPT_URL') return; // Skip until configured

    const payload = {
      session_id:   SESSION_ID,
      member_name:  window.member?.name  || '',
      member_email: window.member?.email || '',
      member_city:  window.member?.city  || '',
      key,
      value,
      completed: false,
    };

    // Fire-and-forget — no await, no error UI
    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }).catch(() => {}); // Silently swallow network errors
  };

  window.submitComplete = function () {
    window.submitStep('__completed__', true);
  };
})();
```

- [ ] **Step 2: Update engine.js to call submitComplete on Step 15 CTA**

In `engine.js`, find the reveal CTA click handler and add `window.submitComplete && window.submitComplete()` before the redirect:

```javascript
// In the reveal-cta click handler in wireStep():
revealCta.addEventListener('click', () => {
  revealCta.classList.add('pulse');
  window.submitComplete && window.submitComplete(); // ADD THIS LINE
  setTimeout(() => {
    window.location.href = 'https://joinpavilion.slack.com';
  }, 600);
});
```

- [ ] **Step 3: Verify submit fires**

Open DevTools → Network tab → Filter for "script.google.com". Advance through 2 steps. Expect: 2 POST requests appear in Network tab (may show as "preflight" OPTIONS + POST).

- [ ] **Step 4: Commit**

```bash
git add pavilion/new-member-onboarding/submit.js
git commit -m "feat(onboarding): progressive step submission → Apps Script"
```

---

### Task 9: Netlify deploy

- [ ] **Step 1: Create netlify.toml**

```bash
cat > /Users/joshmait/Desktop/Claude/pavilion/new-member-onboarding/netlify.toml << 'EOF'
[build]
  publish = "."

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200
EOF
```

- [ ] **Step 2: Replace Apps Script URL in submit.js before deploying**

In `submit.js`, replace `YOUR_APPS_SCRIPT_URL` with the actual URL from Task 7 Step 2:

```javascript
const ENDPOINT = 'https://script.google.com/macros/s/AKf.../exec'; // actual URL here
```

Verify: open index.html locally, advance 2 steps, check DevTools Network tab — expect POST requests to script.google.com.

- [ ] **Step 3: Deploy to Netlify**

```bash
PATH="/usr/local/bin:$PATH" /Users/joshmait/.local/node_modules/.bin/netlify deploy \
  --auth $NETLIFY_AUTH_TOKEN \
  --dir /Users/joshmait/Desktop/Claude/pavilion/new-member-onboarding \
  --prod
```

This creates a new Netlify site. Copy the resulting URL (format: `https://xxxx-xxxx-xxxx.netlify.app`).

- [ ] **Step 4: Test live URL**

Open the Netlify URL in a browser on your phone. Verify:
- Welcome screen loads with confetti
- Font renders correctly (Poppins)
- All 16 screens reachable by tapping through
- Pink CTA pills render correctly on mobile
- Progress bar advances on each step, hides during video interlude

- [ ] **Step 5: Test personalized URL**

Open `[netlify-url]?name=Josh+Mait&email=josh.mait@joinpavilion.com&city=New+York`. Verify Welcome screen shows "Welcome, Josh."

Test missing params: open `[netlify-url]` (no params). Verify Welcome shows "Welcome to Pavilion." with no comma. Verify Reveal shows "Your Pavilion is ready." with no dangling comma.

- [ ] **Step 6: Commit + update MEMORY.md**

```bash
cd /Users/joshmait/Desktop/Claude
git add pavilion/new-member-onboarding/
git commit -m "feat(onboarding): Netlify deploy config — wizard live"
```

Update `MEMORY.md` with:
- Live URL
- Netlify site ID (from deploy output)
- Apps Script endpoint URL
- Local path: `pavilion/new-member-onboarding/`

---

## Quick Reference

**Local preview:**
```bash
cd /Users/joshmait/Desktop/Claude/pavilion/new-member-onboarding
python3 -m http.server 3456
# Open: http://localhost:3456?name=Sarah&city=San+Francisco
```

**Test personalized URL pattern:**
`[base-url]?name=FirstName+LastName&email=email@company.com&city=City+Name`

**Apps Script deploy steps (summary):**
1. script.google.com → New project
2. Paste onboarding-backend.js
3. Deploy → Web app → Execute as Me → Anyone
4. Copy URL → paste into submit.js ENDPOINT constant

**Files to update when real data is available:**
- `engine.js` → `getEvents()`, `getPeople()`, `getVideoMembers()` — replace stub arrays with API calls or updated hardcoded content
- `submit.js` → update `ENDPOINT` with real Apps Script URL

// engine.js — Wizard engine. Reads STEPS, renders to #step-container,
// manages navigation, state persistence, and submit triggers.

(function () {

  // ── CONSTANTS ─────────────────────────────────────────────────
  const STORAGE_KEY    = 'pavilion-onboarding-v1';
  const NUMBERED_STEPS = 15;

  // ── STATE ─────────────────────────────────────────────────────
  let currentIndex = 0;
  let state = loadState();

  function loadState() {
    try { return JSON.parse(localStorage.getItem(STORAGE_KEY)) || {}; }
    catch (_) { return {}; }
  }

  function saveLocalState() {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); }
    catch (_) {}
  }

  function setState(key, value) {
    if (!key) return;
    state[key] = value;
    saveLocalState();
  }

  // ── ELEMENTS ──────────────────────────────────────────────────
  const progressBar = document.getElementById('progress-bar');
  const container   = document.getElementById('step-container');

  // ── PROGRESS BAR ──────────────────────────────────────────────
  function renderProgress(index) {
    const interludeIdx = STEPS.findIndex(s => s.type === 'video-interlude');

    // Hide bar during video interlude — it's not a numbered step
    if (index === interludeIdx) {
      progressBar.innerHTML = '';
      return;
    }

    // Map array index → 1-based step number (interlude slot removed from count)
    // Indices 0..(interludeIdx-1)  → steps 1..interludeIdx
    // Indices (interludeIdx+1)..end → steps interludeIdx+1..15
    const stepNum = index < interludeIdx ? index + 1 : index;

    progressBar.innerHTML = Array.from({ length: NUMBERED_STEPS }, (_, i) => {
      const seg = i + 1;
      let cls = 'prog-seg';
      if (seg < stepNum)      cls += ' done';
      else if (seg === stepNum) cls += ' active';
      return `<div class="${cls}"></div>`;
    }).join('');
  }

  // ── RENDER ────────────────────────────────────────────────────
  function renderStep(index, direction) {
    const step = STEPS[index];
    if (!step) return;

    renderProgress(index);

    // Exit old steps — remove ALL to prevent orphans from double-navigation
    container.querySelectorAll('.step').forEach(old => {
      old.classList.remove('active');
      old.classList.add(direction === 'back' ? 'back-exiting' : 'exiting');
      setTimeout(() => old.remove(), 250);
    });

    // Build new step element
    const el = document.createElement('div');
    el.className = direction === 'back' ? 'step back-entering' : 'step entering';
    el.innerHTML = buildStepHTML(step);
    container.appendChild(el);

    // Trigger enter animation on next frame
    requestAnimationFrame(() => {
      requestAnimationFrame(() => {
        el.classList.remove('entering', 'back-entering');
        el.classList.add('active');
      });
    });

    // Back button (rendered outside the step, floating)
    const existingBack = container.querySelector('.btn-back');
    if (existingBack) existingBack.remove();
    if (index > 0) {
      const backBtn = document.createElement('button');
      backBtn.className = 'btn-back visible';
      backBtn.textContent = '← Back';
      backBtn.addEventListener('click', () => navigate(currentIndex - 1, 'back'));
      container.appendChild(backBtn);
    }

    // Wire up interactions
    wireStep(el, step);

    // Welcome gets confetti
    if (step.type === 'welcome') {
      setTimeout(() => window.launchConfetti && window.launchConfetti(), 450);
    }
  }

  // ── HTML BUILDERS ─────────────────────────────────────────────

  function resolveVal(v) {
    return typeof v === 'function' ? v() : v;
  }

  function buildStepHTML(step) {
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
      default:                return '<div class="step-body"><p>Unknown step type.</p></div>';
    }
  }

  function stepShell(step, bodyContent) {
    const hl = resolveVal(step.headline).replace('\n', '<br>');
    const skipHtml = step.skip
      ? `<div class="skip-link" data-action="skip">${step.skip}</div>`
      : '';
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
          ${skipHtml}
        </div>
      </div>
    `;
  }

  // ── WELCOME ───────────────────────────────────────────────────
  function buildWelcome() {
    const hed  = member.hasName ? `Welcome,<br>${member.firstName}.` : 'Welcome to<br>Pavilion.';
    const city = member.hasCity ? `8 members in ${member.city}` : '10,000+ members worldwide';
    return `
      <div class="welcome-screen">
        <div class="welcome-emoji">🎉</div>
        <div class="welcome-hed">${hed}</div>
        <p class="welcome-sub">You're joining revenue leaders who figured out they don't have to do this alone.</p>
        <div class="avatar-row">
          <div class="avatar-stack">
            <div class="av">👩</div><div class="av">👨</div><div class="av">👩</div><div class="av">👨</div>
          </div>
          <span class="avatar-text">${city}</span>
        </div>
        <button class="welcome-cta">Let's set you up →</button>
      </div>
    `;
  }

  // ── MULTI-SELECT ──────────────────────────────────────────────
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

  // ── SINGLE-SELECT ─────────────────────────────────────────────
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

  // ── PHONE ─────────────────────────────────────────────────────
  function buildPhone(step) {
    const saved    = state['sms'] || {};
    const phone    = saved.phone    || '';
    const optedIn  = saved.sms_opt_in || false;
    return stepShell(step, `
      <div class="phone-wrap">
        <input type="tel" class="text-input" id="phone-input"
          placeholder="(555) 555-5555" value="${phone}" autocomplete="tel">
        <div class="sms-consent${optedIn ? ' checked' : ''}" id="sms-consent">
          <div class="sms-checkbox"><span class="sms-check-icon">✓</span></div>
          <span class="sms-label">I agree to receive text messages from Pavilion. Reply STOP to opt out at any time.</span>
        </div>
      </div>
    `);
  }

  // ── TEXT INPUT ────────────────────────────────────────────────
  function buildTextInput(step) {
    const saved = state[step.key] || '';
    return stepShell(step, `
      <input type="text" class="text-input" id="text-field"
        placeholder="${step.placeholder || ''}" value="${saved}">
    `);
  }

  // ── TEXTAREA ──────────────────────────────────────────────────
  function buildTextarea(step) {
    const saved = state[step.key] || '';
    return stepShell(step, `
      <textarea class="text-input" rows="5" id="textarea-field"
        placeholder="${step.placeholder || ''}">${saved}</textarea>
    `);
  }

  // ── EVENTS ────────────────────────────────────────────────────
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

  // ── PEOPLE ────────────────────────────────────────────────────
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

  // ── VIDEO INTERLUDE ───────────────────────────────────────────
  function buildVideoInterlude() {
    const vids = getVideoMembers();
    const vm = vids[Math.floor(Math.random() * vids.length)];
    return `
      <div class="video-interlude">
        <div class="vi-skip" id="vi-skip">Skip ›</div>
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

  // ── REVEAL ────────────────────────────────────────────────────
  function buildReveal() {
    const channels   = state['slack_channels'] || [];
    const events     = state['events_rsvp']    || [];
    const intros     = state['intro_requests'] || [];
    const benchmarks = state['benchmarks']     || [];
    const comp       = state['comp_interest'];

    const introText = intros.length > 0
      ? `Expect a message this week from <strong>${getPersonName(intros[0])}</strong>`
      : `We're working on your first intro. Expect a message within the week.`;

    const eventText = events.length > 0
      ? `Saved for <strong>${getEventName(events[0])}</strong>`
      : `Your local events are on your radar`;

    const chText = channels.length > 0
      ? `<strong>${channels.length} channel${channels.length > 1 ? 's' : ''} added</strong>${channels.length > 0 ? ' — ' + channels.slice(0, 2).join(', ') + (channels.length > 2 ? ' + more' : '') : ''}`
      : `Channels ready when you open Slack`;

    const items = [
      { icon: '💬', text: chText },
      { icon: '📅', text: eventText },
      { icon: '🤝', text: introText },
      benchmarks.length > 0 ? { icon: '📊', text: `<strong>Benchmark reports</strong> being prepared` } : null,
      (comp === 'yes' || comp === 'maybe') ? { icon: '💼', text: `<strong>Exec comp resources</strong> on their way` } : null,
    ].filter(Boolean);

    const itemsHTML = items.map(item => `
      <div class="reveal-item">
        <div class="reveal-icon">${item.icon}</div>
        <div class="reveal-text">${item.text}</div>
      </div>
    `).join('');

    // No dangling comma when name is missing
    const nameSuffix = member.hasName ? `,<br>${member.firstName}` : '';

    return `
      <div class="reveal-screen">
        <div class="reveal-hed">Your Pavilion<br>is ready${nameSuffix}.</div>
        <div class="reveal-items">${itemsHTML}</div>
        <button class="reveal-cta" data-action="reveal-cta">Go to Slack →</button>
      </div>
    `;
  }

  // ── WIRING ────────────────────────────────────────────────────
  function wireStep(el, step) {

    // Multi-select toggle
    el.querySelectorAll('.option-card:not([data-single])').forEach(card => {
      card.addEventListener('click', () => card.classList.toggle('selected'));
    });

    // Single-select (radio behaviour)
    el.querySelectorAll('.option-card[data-single]').forEach(card => {
      card.addEventListener('click', () => {
        el.querySelectorAll('.option-card[data-single]').forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
      });
    });

    // Event cards
    el.querySelectorAll('.event-card').forEach(card => {
      card.addEventListener('click', () => {
        card.classList.toggle('selected');
        // Update action label
        const action = card.querySelector('.ev-action');
        if (action) action.textContent = card.classList.contains('selected') ? '✓' : 'Save →';
      });
    });

    // Person cards (max 2)
    el.querySelectorAll('.person-card').forEach(card => {
      card.addEventListener('click', () => {
        const alreadySelected = el.querySelectorAll('.person-card.selected').length;
        if (!card.classList.contains('selected') && alreadySelected >= 2) return;
        card.classList.toggle('selected');
      });
    });

    // SMS consent checkbox
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

    // Welcome CTA
    const welCta = el.querySelector('.welcome-cta');
    if (welCta) {
      welCta.addEventListener('click', () => navigate(currentIndex + 1, 'forward'));
    }

    // Reveal CTA
    const revealCta = el.querySelector('[data-action="reveal-cta"]');
    if (revealCta) {
      revealCta.addEventListener('click', () => {
        revealCta.classList.add('pulse');
        window.submitComplete && window.submitComplete();
        setTimeout(() => {
          window.location.href = 'https://joinpavilion.slack.com';
        }, 650);
      });
    }
  }

  // ── CTA HANDLER ───────────────────────────────────────────────
  function handleCta(el, step) {
    const value = collectStepData(el, step);
    if (value !== null && step.key) {
      setState(step.key, value);
      window.submitStep && window.submitStep(step.key, value);
    }
    navigate(currentIndex + 1, 'forward');
  }

  function collectStepData(el, step) {
    if (!step.key) return null;

    switch (step.type) {
      case 'multi-select':
        return [...el.querySelectorAll('.option-card.selected')].map(c => c.dataset.id);

      case 'single-select': {
        const sel = el.querySelector('.option-card.selected');
        return sel ? sel.dataset.id : null;
      }

      case 'phone': {
        // Store only under step.key ('sms') — no separate top-level keys
        const phone     = el.querySelector('#phone-input')?.value.trim() || '';
        const sms_opt_in = el.querySelector('#sms-consent')?.classList.contains('checked') || false;
        return { phone, sms_opt_in };
      }

      case 'text-input':
        return el.querySelector('#text-field')?.value.trim() || '';

      case 'textarea':
        return el.querySelector('#textarea-field')?.value.trim() || '';

      case 'events':
        return [...el.querySelectorAll('.event-card.selected')].map(c => c.dataset.id);

      case 'people':
        return [...el.querySelectorAll('.person-card.selected')].map(c => c.dataset.id);

      default:
        return null;
    }
  }

  // ── NAVIGATION ────────────────────────────────────────────────
  function navigate(index, direction) {
    if (index < 0 || index >= STEPS.length) return;
    currentIndex = index;
    renderStep(currentIndex, direction);
  }

  // ── CONTENT DATA (stub — replace with API calls for production) ──

  function getEvents() {
    const city = member.hasCity ? member.city : 'your city';
    return [
      { id: 'ev1', month: 'Apr', day: '17', name: 'Revenue Leaders Dinner',          location: `The Battery · ${city}` },
      { id: 'ev2', month: 'Apr', day: '24', name: 'GTM Masterclass: AI in the Stack', location: 'Virtual · 12pm PT' },
      { id: 'ev3', month: 'May', day: '6',  name: 'Pavilion Summit · NYC',           location: 'Convene · Midtown' },
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
      { name: 'Sarah Chen',   role: 'VP of Sales · Attentive\nSan Francisco',  duration: '0:28' },
      { name: 'Marcus Reyes', role: 'CRO · Rippling\nNew York',                 duration: '0:32' },
      { name: 'Anya Kim',     role: 'Head of CS · Notion\nRemote',              duration: '0:24' },
    ];
  }

  function getPersonName(id) {
    return getPeople().find(p => p.id === id)?.name || 'your new connection';
  }

  function getEventName(id) {
    return getEvents().find(e => e.id === id)?.name || 'your saved event';
  }

  // ── BOOT ──────────────────────────────────────────────────────
  document.addEventListener('DOMContentLoaded', () => {
    renderStep(currentIndex, 'forward');
  });

})();

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
      small: "Smaller collections are handled quickly — usually a photo inventory is all we need to get you a real number.",
      medium: "At this size, we can often do a full assessment remotely. Get us a list or photos and we'll come back with an offer within 24 hours.",
      large: "Collections at $50K+ typically qualify for our at-home service — we come to you, assess on-site, and can make an offer the same day.",
      unknown: "That's why we start with an appraisal — so you know what you're working with before any decisions get made.",
      final: "The fastest path is to get us a photo inventory or fill out our contact form — we'll come back to you with a real number, usually within 24 hours. For larger collections, we can schedule a visit."
    }
  }
};

// Build response summary based on answers
function buildResponse(persona, answers) {
  const tree = TRAVIS[persona];
  const msgs = [];

  // First question response (situation or type)
  if (answers.situation) msgs.push(tree.responses[answers.situation]);
  if (answers.type) msgs.push(tree.responses[answers.type]);

  // Size context
  if (answers.size && tree.responses[answers.size]) {
    msgs.push(tree.responses[answers.size]);
  }

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
          <img src="assets/travis-avatar.svg" alt="Travis" onerror="this.style.display='none';this.parentNode.innerHTML='🪙'">
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

  // Keyboard close
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') closeTravis();
  });
}

function openTravis(persona) {
  currentPersona = persona;
  currentStep = 0;
  answers = {};

  if (!document.getElementById('travis-modal')) createModal();

  document.getElementById('travis-modal').classList.add('active');
  document.body.style.overflow = 'hidden';
  renderStep();
}

function closeTravis() {
  const modal = document.getElementById('travis-modal');
  if (modal) modal.classList.remove('active');
  document.body.style.overflow = '';
}

function renderStep() {
  const tree = TRAVIS[currentPersona];
  const body = document.getElementById('travis-body');

  if (currentStep >= tree.questions.length) {
    renderResponse();
    return;
  }

  const q = tree.questions[currentStep];
  const progress = `Question ${currentStep + 1} of ${tree.questions.length}`;

  body.innerHTML = `
    <p class="travis-modal__progress">${progress}</p>
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
    <div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:8px;align-items:center;">
      ${cta}
      <button class="btn btn-outline" id="travis-restart" style="font-size:14px;padding:10px 20px;">Start over</button>
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

  // Load Travis avatar into inline placeholders
  document.querySelectorAll('.travis-placeholder').forEach(el => {
    const img = document.createElement('img');
    img.src = 'assets/travis-avatar.svg';
    img.alt = 'Travis';
    img.style.cssText = 'width:100%;height:100%;border-radius:50%;object-fit:cover;';
    img.onerror = () => { el.textContent = '🪙'; el.style.fontSize = '48px'; el.style.display = 'flex'; el.style.alignItems = 'center'; el.style.justifyContent = 'center'; };
    el.replaceWith(img);
  });
});

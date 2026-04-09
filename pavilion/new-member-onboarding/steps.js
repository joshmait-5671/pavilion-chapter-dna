// steps.js — All 16 screen definitions (15 steps + 1 video interlude).
// Content only — no logic. `member` from params.js is available at runtime.

window.STEPS = [

  // ── STEP 1: WELCOME ──────────────────────────────────────────
  {
    id: 'welcome',
    type: 'welcome',
  },

  // ── STEP 2: SLACK CHANNELS ────────────────────────────────────
  {
    id: 'slack-channels',
    type: 'multi-select',
    eyebrow: 'Your Community',
    headline: 'Pick channels\nbuilt for you.',
    note: 'Curated for revenue leaders at your stage. Choose 3–5. You can change these any time.',
    cta: 'Add these channels',
    skip: 'Skip for now',
    options: [
      { id: 'revenue-strategy',  label: '#revenue-strategy',     sub: 'Pipeline · GTM · Forecasting' },
      { id: 'intros-referrals',  label: '#intros-and-referrals',  sub: 'Warm connections, fast' },
      { id: 'benchmark-data',    label: '#benchmark-data',        sub: 'Comp · Team size · GTM' },
      { id: 'ai-in-gtm',         label: '#ai-in-gtm',             sub: 'Tools · Experiments' },
      { id: 'exec-leadership',   label: '#exec-leadership',       sub: 'Peer conversations' },
      {
        id: 'city-channel',
        label: () => member.hasCity
          ? `#${member.city.toLowerCase().replace(/\s+/g, '-')}`
          : '#local-members',
        sub: 'Local events · Meetups',
      },
    ],
    key: 'slack_channels',
  },

  // ── STEP 3: EMAIL PREFERENCES ─────────────────────────────────
  {
    id: 'email-prefs',
    type: 'multi-select',
    eyebrow: 'Your Community',
    headline: 'How should we\nstay in touch?',
    note: 'Pick what feels right. You can unsubscribe from individual lists any time.',
    cta: 'Save preferences',
    skip: 'Skip for now',
    options: [
      { id: 'weekly-digest',    label: 'Weekly digest',        sub: 'The best of Pavilion, every Monday' },
      { id: 'event-alerts',     label: 'Event alerts',         sub: 'New events in your area + online' },
      { id: 'member-spotlight', label: 'Member spotlights',    sub: 'Who to know and why' },
      { id: 'ai-newsletter',    label: 'AI + GTM roundup',     sub: 'Weekly AI-for-revenue-leaders brief' },
    ],
    key: 'email_prefs',
  },

  // ── STEP 4: SMS OPT-IN ────────────────────────────────────────
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

  // ── STEP 5: EVENTS NEAR YOU ───────────────────────────────────
  {
    id: 'events',
    type: 'events',
    eyebrow: 'Your Calendar',
    headline: () => member.hasCity ? `Events in\n${member.city}.` : 'Events near\nyou.',
    note: 'RSVP now or save for later. We\'ll remind you either way.',
    cta: 'Save my picks',
    skip: 'Nothing looks right',
    key: 'events_rsvp',
  },

  // ── STEP 6: TRAVEL CITY ───────────────────────────────────────
  {
    id: 'travel-city',
    type: 'text-input',
    eyebrow: 'Your Calendar',
    headline: 'Do you travel\nto another city?',
    note: 'Tell us where and we\'ll add those events to your radar too.',
    placeholder: 'e.g. New York, Chicago, Austin',
    cta: 'Add this city',
    skip: 'I stay put',
    key: 'travel_city',
  },

  // ── STEP 7: CLASSES ───────────────────────────────────────────
  {
    id: 'classes',
    type: 'multi-select',
    eyebrow: 'Your Calendar',
    headline: 'Classes on\nyour radar.',
    note: 'Enroll now or we\'ll remind you closer to the start date.',
    cta: 'Save these classes',
    skip: 'Not right now',
    options: [
      { id: 'sales-leadership',  label: 'Sales Leadership Intensive', sub: 'Starts May 12 · 6 weeks' },
      { id: 'revops-101',        label: 'RevOps Fundamentals',        sub: 'Starts Apr 28 · 4 weeks' },
      { id: 'cs-excellence',     label: 'CS Excellence Program',      sub: 'Starts May 5 · 6 weeks' },
      { id: 'exec-presence',     label: 'Executive Presence',         sub: 'Starts Apr 30 · 3 weeks' },
      { id: 'ai-for-gtm',        label: 'AI for GTM Leaders',         sub: 'Starts May 1 · 2 weeks' },
    ],
    key: 'classes',
  },

  // ── STEP 8: PEOPLE NEAR YOU ───────────────────────────────────
  {
    id: 'people',
    type: 'people',
    eyebrow: 'Meet Someone',
    headline: () => member.hasCity ? `Members in\n${member.city}.` : 'Members near\nyou.',
    note: 'Pick 1–2 people to be introduced to. We\'ll send a warm note this week.',
    cta: 'Intro me to these people',
    skip: 'Not ready yet',
    key: 'intro_requests',
  },

  // ── VIDEO INTERLUDE ───────────────────────────────────────────
  {
    id: 'video-interlude',
    type: 'video-interlude',
  },

  // ── STEP 9: YOUR VOICE ────────────────────────────────────────
  {
    id: 'your-voice',
    type: 'multi-select',
    eyebrow: 'Your Voice',
    headline: 'Where would you\nlike to be heard?',
    note: 'We\'ll promote your insights and ideas in the channels you choose. Or not at all — your call.',
    cta: 'Save my preferences',
    skip: 'Not right now',
    options: [
      { id: 'linkedin',   label: 'LinkedIn',         sub: 'Pavilion reposts your content' },
      { id: 'slack',      label: 'Slack shoutouts',  sub: 'Featured in member channels' },
      { id: 'newsletter', label: 'Newsletter',        sub: 'Member spotlight feature' },
      { id: 'podcast',    label: 'Podcast guest',     sub: 'Pavilion podcast interview' },
    ],
    key: 'promote_channels',
  },

  // ── STEP 10: BENCHMARKS ───────────────────────────────────────
  {
    id: 'benchmarks',
    type: 'multi-select',
    eyebrow: 'Your Data',
    headline: 'Benchmarks\nyou care about.',
    note: 'We\'ll make sure you get the data reports most relevant to your role.',
    cta: 'Send me these reports',
    skip: 'Skip',
    options: [
      { id: 'team-size',    label: 'Team size benchmarks', sub: 'GTM team structure by ARR' },
      { id: 'gtm-data',     label: 'GTM metrics',          sub: 'CAC, NRR, win rates by segment' },
      { id: 'hiring-plans', label: 'Hiring plans',         sub: 'Who\'s growing what function' },
      { id: 'tech-stack',   label: 'Tech stack trends',    sub: 'What revenue leaders are buying' },
    ],
    key: 'benchmarks',
  },

  // ── STEP 11: COMP PACKAGE ─────────────────────────────────────
  {
    id: 'comp-package',
    type: 'single-select',
    eyebrow: 'Your Data',
    headline: 'Looking for comp\npackage expertise?',
    note: 'We have coaches and benchmark data specifically for executive compensation.',
    cta: 'Continue',
    skip: null,
    options: [
      { id: 'yes',   label: 'Yes — connect me to resources', sub: 'Coaching, benchmarks, negotiation guides' },
      { id: 'maybe', label: 'Tell me more first',            sub: 'Send me an overview' },
      { id: 'no',    label: 'Not right now',                 sub: '' },
    ],
    key: 'comp_interest',
  },

  // ── STEP 12: ONE THING ────────────────────────────────────────
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

  // ── STEP 13: COMMITMENT ───────────────────────────────────────
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

  // ── STEP 14: FAVORITE SONG ────────────────────────────────────
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

  // ── STEP 15: REVEAL ───────────────────────────────────────────
  {
    id: 'reveal',
    type: 'reveal',
  },

];

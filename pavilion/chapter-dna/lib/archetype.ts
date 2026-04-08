import { Answers } from '@/types'

export type ArchetypeId =
  | 'inner_circle'
  | 'operators'
  | 'insurgents'
  | 'climbers'
  | 'intelligentsia'
  | 'builders'

export interface Archetype {
  id: ArchetypeId
  name: string
  tagline: string
  description: string
  traits: [string, string, string]
  manifesto: [string, string, string]
  moodPhoto: string
}

export interface ArchetypeResult {
  archetype: Archetype
  drink: string
  spot: string
  says: string
}

// ── Archetype definitions ───────────────────────────────────────────────────

export const ARCHETYPES: Record<ArchetypeId, Archetype> = {
  inner_circle: {
    id: 'inner_circle',
    name: 'INNER CIRCLE',
    tagline: 'Where trust is the currency.',
    description: 'This chapter runs on genuine connection. People show up for each other — not just for the agenda.',
    traits: ['Relationship-first', 'Deeply welcoming', 'High trust'],
    manifesto: [
      'The relationship IS the strategy.',
      'We remember who showed up.',
      'Trust takes years. We\'re building it anyway.',
    ],
    moodPhoto: 'https://images.unsplash.com/photo-1529156069898-49953e39b3ac?w=800&q=80&auto=format&fit=crop',
  },
  operators: {
    id: 'operators',
    name: 'OPERATORS',
    tagline: 'Execution over everything.',
    description: 'This chapter is allergic to fluff. Show up with a real problem and leave with a real answer.',
    traits: ['Tactically sharp', 'Low ego', 'High output'],
    manifesto: [
      'Real problems. Real answers. No theatre.',
      'Good enough ships. Perfect doesn\'t.',
      'We don\'t workshop it. We fix it.',
    ],
    moodPhoto: 'https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800&q=80&auto=format&fit=crop',
  },
  insurgents: {
    id: 'insurgents',
    name: 'INSURGENTS',
    tagline: 'Say the thing. Mean it.',
    description: 'This chapter has no patience for performance. The most useful thing you\'ll hear is the thing nobody else will say.',
    traits: ['Radically direct', 'No filter', 'High standards'],
    manifesto: [
      'Polished is overrated.',
      'The truth has an edge. Good.',
      'We say the thing nobody else will.',
    ],
    moodPhoto: 'https://images.unsplash.com/photo-1543269865-cbf427effbad?w=800&q=80&auto=format&fit=crop',
  },
  climbers: {
    id: 'climbers',
    name: 'CLIMBERS',
    tagline: 'Ambition is the entry fee.',
    description: 'This chapter attracts people who are going somewhere and want to be around others doing the same.',
    traits: ['Relentlessly ambitious', 'Competitive edge', 'High ceiling'],
    manifesto: [
      'Every room is an opportunity.',
      'Ambition isn\'t a dirty word here.',
      'We\'re going somewhere. Join us.',
    ],
    moodPhoto: 'https://images.unsplash.com/photo-1515187029135-18ee286d815b?w=800&q=80&auto=format&fit=crop',
  },
  intelligentsia: {
    id: 'intelligentsia',
    name: 'INTELLIGENTSIA',
    tagline: 'The sharpest room in the city.',
    description: 'This chapter raises the bar by asking harder questions. Expect to be challenged. Expect to leave smarter.',
    traits: ['Intellectually rigorous', 'High signal', 'Discerning'],
    manifesto: [
      'The hardest question in the room is ours.',
      'Frameworks first. Always.',
      'We leave smarter. Every time.',
    ],
    moodPhoto: 'https://images.unsplash.com/photo-1524178232363-1fb2b075b655?w=800&q=80&auto=format&fit=crop',
  },
  builders: {
    id: 'builders',
    name: 'BUILDERS',
    tagline: 'Playing the long game.',
    description: 'This chapter invests in people before they need something. The network compounds quietly and pays off big.',
    traits: ['Collaborative', 'Thoughtful', 'Long-term minded'],
    manifesto: [
      'Ship it. Learn. Ship it better.',
      'We invest before we need something.',
      'The network compounds quietly.',
    ],
    moodPhoto: 'https://images.unsplash.com/photo-1517048676732-d65bc937f952?w=800&q=80&auto=format&fit=crop',
  },
}

// ── Answer → flavor text lookups ────────────────────────────────────────────

const DRINK_LABELS: Record<string, string> = {
  q9_a: '🍸 Martini',
  q9_b: '🥃 Whiskey neat',
  q9_c: '🌶️ Spicy margarita',
  q9_d: '🍺 IPA',
  q9_e: '🍷 Natural wine',
  q9_f: '☕ Black coffee',
}

const SPOT_LABELS: Record<string, string> = {
  q10_a: 'Steakhouse private room',
  q10_b: 'Neighborhood bar',
  q10_c: 'Hotel lobby',
  q10_d: 'Great coffee shop',
  q10_e: "Someone's office",
  q10_f: "Dinner party at a member's house",
}

const SAY_LABELS: Record<string, string> = {
  q8_a: '"Get to the point"',
  q8_b: '"Who do you need to meet?"',
  q8_c: '"Sounds good, but will it work?"',
  q8_d: '"Let\'s make it useful"',
  q8_e: '"Say the thing you really mean"',
  q8_f: '"Someone here has solved this"',
}

// ── Answer → archetype score mapping ────────────────────────────────────────

const ANSWER_SCORES: Record<string, Partial<Record<ArchetypeId, number>>> = {
  // Q1 — what do you expect most?
  q1_a: { insurgents: 1, intelligentsia: 1 },
  q1_b: { operators: 2 },
  q1_c: { inner_circle: 1, builders: 1 },
  q1_d: { climbers: 2 },
  q1_e: { insurgents: 1, climbers: 1 },
  q1_f: { inner_circle: 2 },

  // Q2 — best at?
  q2_a: { inner_circle: 2 },
  q2_b: { operators: 2 },
  q2_c: { insurgents: 2 },
  q2_d: { inner_circle: 1, builders: 1 },
  q2_e: { climbers: 2 },
  q2_f: { insurgents: 1, intelligentsia: 1 },

  // Q3 — people type?
  q3_a: { operators: 2 },
  q3_b: { inner_circle: 2 },
  q3_c: { climbers: 2 },
  q3_d: { builders: 2 },
  q3_e: { insurgents: 1, climbers: 1 },
  q3_f: { operators: 1, builders: 1 },

  // Q4 — energy?
  q4_a: { insurgents: 1, climbers: 1 },
  q4_b: { inner_circle: 2 },
  q4_c: { intelligentsia: 2 },
  q4_d: { operators: 1, builders: 1 },
  q4_e: { intelligentsia: 1, builders: 1 },
  q4_f: { operators: 1, intelligentsia: 1 },

  // Q5 — what makes it different?
  q5_a: { insurgents: 1, operators: 1 },
  q5_b: { inner_circle: 2 },
  q5_c: { operators: 2 },
  q5_d: { inner_circle: 1, builders: 1 },
  q5_e: { intelligentsia: 2 },
  q5_f: { operators: 1, builders: 1 },

  // Q6 — event type? (lighter weight)
  q6_a: { intelligentsia: 1 },
  q6_b: { operators: 1 },
  q6_c: { insurgents: 1 },
  q6_d: { inner_circle: 1 },
  q6_e: { builders: 1 },
  q6_f: { intelligentsia: 1 },

  // Q7 — secretly proud of?
  q7_a: { intelligentsia: 2 },
  q7_b: { inner_circle: 2 },
  q7_c: { insurgents: 2 },
  q7_d: { inner_circle: 1, builders: 1 },
  q7_e: { climbers: 2 },
  q7_f: { builders: 1, inner_circle: 1 },

  // Q8 — what we say? (higher weight — most direct signal)
  q8_a: { insurgents: 3 },
  q8_b: { inner_circle: 3 },
  q8_c: { intelligentsia: 2, operators: 1 },
  q8_d: { operators: 2, builders: 1 },
  q8_e: { insurgents: 2, intelligentsia: 1 },
  q8_f: { operators: 2, builders: 1 },

  // Q9 — drink? (vibe, lighter)
  q9_a: { intelligentsia: 1 },
  q9_b: { insurgents: 1 },
  q9_c: { climbers: 1 },
  q9_d: { builders: 1 },
  q9_e: { inner_circle: 1 },
  q9_f: { operators: 1 },

  // Q10 — meeting spot? (vibe, lighter)
  q10_a: { intelligentsia: 1 },
  q10_b: { insurgents: 1 },
  q10_c: { climbers: 1 },
  q10_d: { builders: 1 },
  q10_e: { operators: 1 },
  q10_f: { inner_circle: 1 },
}

// ── Scoring function ─────────────────────────────────────────────────────────

export function calculateArchetype(answers: Answers): ArchetypeResult {
  const scores: Record<ArchetypeId, number> = {
    inner_circle: 0,
    operators: 0,
    insurgents: 0,
    climbers: 0,
    intelligentsia: 0,
    builders: 0,
  }

  for (const answerId of Object.values(answers)) {
    const pts = ANSWER_SCORES[answerId]
    if (!pts) continue
    for (const [id, points] of Object.entries(pts)) {
      scores[id as ArchetypeId] += points
    }
  }

  const winnerId = (
    Object.entries(scores).sort(([, a], [, b]) => b - a)[0][0]
  ) as ArchetypeId

  return {
    archetype: ARCHETYPES[winnerId],
    drink: DRINK_LABELS[answers.q9] ?? '',
    spot: SPOT_LABELS[answers.q10] ?? '',
    says: SAY_LABELS[answers.q8] ?? '',
  }
}

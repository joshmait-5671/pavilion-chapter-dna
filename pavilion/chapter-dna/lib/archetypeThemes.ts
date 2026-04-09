// chapter-dna/lib/archetypeThemes.ts
import { ArchetypeId } from '@/lib/archetype'

export interface ArchetypeTheme {
  primary:  string            // dominant color (borders, highlights)
  accent:   string            // high-contrast color (eyebrows, pills, canvas accents)
  cardBg:   string            // darkest bg — top of gradient
  gradient: [string, string]  // [top, bottom] top-to-bottom linear gradient
}

export const ARCHETYPE_THEMES: Record<ArchetypeId, ArchetypeTheme> = {
  inner_circle:   { primary: '#8B1A1A', accent: '#C9A84C', cardBg: '#1a0a0a', gradient: ['#1a0a0a', '#0a0a0f'] },
  operators:      { primary: '#1A3A5C', accent: '#E8EEF4', cardBg: '#0a1220', gradient: ['#0a1220', '#0a0a0f'] },
  insurgents:     { primary: '#CC1A1A', accent: '#FF6B6B', cardBg: '#1a0505', gradient: ['#1a0505', '#0a0a0f'] },
  climbers:       { primary: '#1A5C2A', accent: '#D4E84C', cardBg: '#061208', gradient: ['#061208', '#0a0a0f'] },
  intelligentsia: { primary: '#2D1A5C', accent: '#C4C4D4', cardBg: '#0d0a1a', gradient: ['#0d0a1a', '#0a0a0f'] },
  builders:       { primary: '#8B4A1A', accent: '#F0A050', cardBg: '#1a0e05', gradient: ['#1a0e05', '#0a0a0f'] },
}

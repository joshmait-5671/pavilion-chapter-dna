// chapter-dna/lib/archetypeThemes.ts
import { ArchetypeId } from '@/lib/archetype'

export interface ArchetypeTheme {
  /** Full-bleed solid bg color for result card */
  bg: string
  /** Text color for on-color content (almost always white) */
  text: string
  /** Accent for secondary elements (share button outlines, etc.) */
  accent: string
}

export const ARCHETYPE_THEMES: Record<ArchetypeId, ArchetypeTheme> = {
  inner_circle:   { bg: '#FF0080', text: '#FFFFFF', accent: 'rgba(255,255,255,0.25)' },
  operators:      { bg: '#1246FF', text: '#FFFFFF', accent: 'rgba(255,255,255,0.25)' },
  insurgents:     { bg: '#FF4D00', text: '#FFFFFF', accent: 'rgba(255,255,255,0.25)' },
  climbers:       { bg: '#FFE135', text: '#111111', accent: 'rgba(0,0,0,0.15)'        },
  intelligentsia: { bg: '#9B00FF', text: '#FFFFFF', accent: 'rgba(255,255,255,0.25)' },
  builders:       { bg: '#00C853', text: '#111111', accent: 'rgba(0,0,0,0.15)'        },
}

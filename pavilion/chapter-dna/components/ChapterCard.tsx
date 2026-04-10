'use client'

import { useState } from 'react'
import { ArchetypeResult } from '@/lib/archetype'
import { ARCHETYPE_THEMES } from '@/lib/archetypeThemes'
import { Chapter } from '@/types'

interface ChapterCardProps {
  result: ArchetypeResult
  chapter: Chapter
  onRestart: () => void
}

export default function ChapterCard({ result, chapter, onRestart }: ChapterCardProps) {
  const { archetype, drink, spot, says } = result
  const theme = ARCHETYPE_THEMES[archetype.id]
  const [sharingIG, setSharingIG] = useState(false)
  const [sharingLI, setSharingLI] = useState(false)

  const handleInstagram = async () => {
    if (sharingIG) return
    setSharingIG(true)
    try {
      const { downloadCard } = await import('@/components/SocialCardExport')
      await downloadCard(result, chapter, 'instagram')
    } catch { /* silent */ } finally { setSharingIG(false) }
  }

  const handleLinkedIn = async () => {
    if (sharingLI) return
    setSharingLI(true)
    try {
      const { downloadCard } = await import('@/components/SocialCardExport')
      await downloadCard(result, chapter, 'linkedin')
    } catch { /* silent */ } finally { setSharingLI(false) }
  }

  return (
    <div
      className="flex flex-col min-h-dvh px-5 pt-12 pb-10"
      style={{ background: theme.bg, position: 'relative', overflow: 'hidden' }}
    >

      {/* Concentric circles bg texture */}
      <svg
        aria-hidden
        style={{ position: 'absolute', inset: 0, width: '100%', height: '100%', opacity: 0.07, pointerEvents: 'none' }}
        viewBox="0 0 400 800"
        preserveAspectRatio="xMidYMid slice"
      >
        {[100, 190, 290, 400, 520, 650].map(r => (
          <circle key={r} cx="200" cy="500" r={r} fill="none" stroke="white" strokeWidth="1.5" />
        ))}
      </svg>

      {/* Top label */}
      <p style={{
        fontSize: '10px',
        fontWeight: 800,
        letterSpacing: '0.25em',
        textTransform: 'uppercase',
        color: `${theme.text}99`,
        marginBottom: '4px',
        position: 'relative',
        zIndex: 1,
      }}>
        {chapter.name} is —
      </p>

      {/* Archetype eyebrow */}
      <p style={{
        fontSize: '11px',
        fontWeight: 700,
        letterSpacing: '0.14em',
        textTransform: 'uppercase',
        color: `${theme.text}66`,
        marginBottom: '8px',
        position: 'relative',
        zIndex: 1,
      }}>
        Your archetype
      </p>

      {/* THE [ARCHETYPE NAME] — giant */}
      <h1 style={{
        fontSize: 'clamp(48px, 14vw, 64px)',
        fontWeight: 900,
        color: theme.text,
        lineHeight: 0.87,
        letterSpacing: '-0.04em',
        marginBottom: '24px',
        fontFamily: 'var(--font-space-grotesk)',
        position: 'relative',
        zIndex: 1,
      }}>
        THE<br />{archetype.name.toUpperCase().replace('THE ', '')}
      </h1>

      {/* Rule */}
      <div style={{ width: '40px', height: '3px', background: `${theme.text}50`, marginBottom: '20px', position: 'relative', zIndex: 1 }} />

      {/* Tagline */}
      <p style={{
        fontSize: '16px',
        color: `${theme.text}CC`,
        lineHeight: 1.55,
        fontWeight: 500,
        marginBottom: '28px',
        maxWidth: '300px',
        position: 'relative',
        zIndex: 1,
      }}>
        {archetype.tagline}
      </p>

      {/* Trait pills */}
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px', marginBottom: '28px', position: 'relative', zIndex: 1 }}>
        {archetype.traits.map(trait => (
          <span
            key={trait}
            style={{
              fontSize: '11px',
              fontWeight: 700,
              padding: '6px 14px',
              borderRadius: '999px',
              border: `1.5px solid ${theme.text}40`,
              color: theme.text,
              background: `${theme.text}15`,
            }}
          >
            {trait}
          </span>
        ))}
      </div>

      {/* Flavor */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '10px', marginBottom: '32px', position: 'relative', zIndex: 1 }}>
        {[{ emoji: '🥃', value: drink }, { emoji: '📍', value: spot }, { emoji: '💬', value: says }].map(({ emoji, value }) => (
          <div key={emoji} style={{ display: 'flex', alignItems: 'flex-start', gap: '12px' }}>
            <span style={{ fontSize: '16px', flexShrink: 0, lineHeight: 1.4 }}>{emoji}</span>
            <span style={{ fontSize: '14px', color: `${theme.text}BB`, lineHeight: 1.45, fontWeight: 500 }}>{value}</span>
          </div>
        ))}
      </div>

      {/* Share buttons */}
      <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '10px', marginBottom: '16px', position: 'relative', zIndex: 1 }}>
        <button
          onClick={handleInstagram}
          disabled={sharingIG}
          style={{
            padding: '14px 8px',
            background: `${theme.text}20`,
            border: `1.5px solid ${theme.text}40`,
            borderRadius: '8px',
            fontSize: '12px',
            fontWeight: 800,
            color: theme.text,
            cursor: 'pointer',
            letterSpacing: '0.04em',
            opacity: sharingIG ? 0.6 : 1,
          }}
        >
          {sharingIG ? 'Saving…' : '📸 Instagram'}
        </button>
        <button
          onClick={handleLinkedIn}
          disabled={sharingLI}
          style={{
            padding: '14px 8px',
            background: theme.text,
            border: `1.5px solid ${theme.text}`,
            borderRadius: '8px',
            fontSize: '12px',
            fontWeight: 800,
            color: theme.bg,
            cursor: 'pointer',
            letterSpacing: '0.04em',
            opacity: sharingLI ? 0.6 : 1,
          }}
        >
          {sharingLI ? 'Saving…' : '💼 LinkedIn'}
        </button>
      </div>

      {/* Restart */}
      <button
        onClick={onRestart}
        style={{
          width: '100%',
          padding: '14px',
          background: 'transparent',
          border: `1.5px solid ${theme.text}30`,
          borderRadius: '8px',
          fontSize: '13px',
          fontWeight: 600,
          color: `${theme.text}80`,
          cursor: 'pointer',
          position: 'relative',
          zIndex: 1,
        }}
      >
        Try a Different City
      </button>
    </div>
  )
}

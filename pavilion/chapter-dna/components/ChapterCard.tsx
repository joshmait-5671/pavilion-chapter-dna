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
    } catch {
      // silent fail
    } finally {
      setSharingIG(false)
    }
  }

  const handleLinkedIn = async () => {
    if (sharingLI) return
    setSharingLI(true)
    try {
      const { downloadCard } = await import('@/components/SocialCardExport')
      await downloadCard(result, chapter, 'linkedin')
    } catch {
      // silent fail
    } finally {
      setSharingLI(false)
    }
  }

  return (
    <div
      className="flex flex-col min-h-dvh px-5 pt-12 pb-10"
      style={{
        background: `linear-gradient(to bottom, ${theme.gradient[0]}, ${theme.gradient[1]})`,
      }}
    >
      {/* Eyebrow */}
      <p
        className="text-[10px] font-bold tracking-[0.28em] uppercase mb-3"
        style={{ color: theme.accent }}
      >
        Your Chapter Is
      </p>

      {/* Archetype name */}
      <h1
        className="font-display font-bold text-white leading-[1.0] tracking-[-0.03em] mb-3"
        style={{ fontSize: 'clamp(48px, 14vw, 64px)' }}
      >
        {archetype.name}
      </h1>

      {/* Tagline */}
      <p className="text-[18px] text-white/55 italic mb-6 leading-snug">
        {archetype.tagline}
      </p>

      {/* Trait pills */}
      <div className="flex flex-wrap gap-2 mb-6">
        {archetype.traits.map(trait => (
          <span
            key={trait}
            className="text-[11px] font-semibold px-3 py-1.5 rounded-full"
            style={{
              background: theme.accent,
              color: '#0a0a0f',
            }}
          >
            {trait}
          </span>
        ))}
      </div>

      {/* Divider */}
      <div className="h-px bg-white/10 mb-6" />

      {/* Manifesto */}
      <div className="flex flex-col gap-3 mb-6">
        {archetype.manifesto.map((line, i) => (
          <div key={i} className="flex items-baseline gap-3">
            <span
              className="text-[10px] font-bold flex-shrink-0"
              style={{ color: theme.accent }}
            >
              {String(i + 1).padStart(2, '0')}
            </span>
            <p className="text-[15px] font-semibold text-white/85 leading-snug italic">
              {line}
            </p>
          </div>
        ))}
      </div>

      {/* Divider */}
      <div className="h-px bg-white/10 mb-6" />

      {/* Flavor text */}
      <div className="flex flex-col gap-3 mb-8">
        {[
          { emoji: '🥃', value: drink },
          { emoji: '📍', value: spot },
          { emoji: '💬', value: says },
        ].map(({ emoji, value }) => (
          <div key={emoji} className="flex items-center gap-3">
            <span className="text-[18px]">{emoji}</span>
            <span className="text-[14px] text-white/70">{value}</span>
          </div>
        ))}
      </div>

      {/* Share section */}
      <div className="mb-2">
        <p className="text-[9px] font-bold tracking-[0.22em] uppercase text-white/25 text-center mb-4">
          Share Your Result
        </p>

        {/* Instagram button */}
        <button
          onClick={handleInstagram}
          disabled={sharingIG}
          className="w-full py-4 bg-pav-pink text-white font-semibold text-[15px] rounded-full
                     hover:bg-pav-pink-800 active:scale-[0.98] transition-all duration-150 mb-3
                     disabled:opacity-50"
        >
          {sharingIG ? 'Saving…' : '📸  Save for Instagram'}
        </button>

        {/* LinkedIn button */}
        <button
          onClick={handleLinkedIn}
          disabled={sharingLI}
          className="w-full py-4 text-white font-semibold text-[15px] rounded-full
                     border border-white/20 hover:border-white/40
                     active:scale-[0.98] transition-all duration-150 mb-6
                     disabled:opacity-50"
          style={{ background: 'rgba(255,255,255,0.05)' }}
        >
          {sharingLI ? 'Saving…' : '💼  Save for LinkedIn'}
        </button>

        {/* iOS note */}
        <p className="text-[11px] text-white/25 text-center mb-6 leading-relaxed">
          On iPhone: tap and hold the image to save.
        </p>
      </div>

      {/* Take it again */}
      <button
        onClick={onRestart}
        className="text-[13px] text-white/30 hover:text-white/60 transition-colors duration-150 mx-auto"
      >
        Take it again
      </button>
    </div>
  )
}

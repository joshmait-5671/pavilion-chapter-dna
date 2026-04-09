'use client'

import { Chapter } from '@/types'
import { COMPETITION_LABEL } from '@/lib/config'

interface ChapterSelectProps {
  chapters: Chapter[]
  onSelect: (chapter: Chapter) => void
}

export default function ChapterSelect({ chapters, onSelect }: ChapterSelectProps) {
  return (
    <div className="flex flex-col min-h-dvh bg-cw-bg px-5 pb-10">

      {/* Hero section with radial glow */}
      <div
        className="relative pt-14 pb-10 text-center"
        style={{
          background: 'radial-gradient(ellipse 80% 50% at 50% 40%, rgba(223,40,91,0.15) 0%, transparent 70%)',
        }}
      >
        {/* Eyebrow */}
        <p className="text-[10px] font-bold tracking-[0.28em] uppercase text-pav-pink mb-5">
          Pavilion Chapter Wars
        </p>

        {/* Headline */}
        <h1 className="font-display font-bold text-white leading-[1.05] tracking-[-0.03em] mb-4"
            style={{ fontSize: 'clamp(48px, 12vw, 68px)' }}>
          15 cities.<br />
          6 archetypes.<br />
          One winner.
        </h1>

        {/* Competition dates */}
        <p className="text-[13px] text-white/40 mb-6 tracking-wide">
          {COMPETITION_LABEL}
        </p>

        {/* Divider */}
        <div className="w-12 h-px bg-white/10 mx-auto mb-6" />

        {/* Setup paragraph */}
        <p className="text-[14px] text-white/55 leading-[1.75] max-w-[320px] mx-auto mb-8">
          Every Pavilion chapter has a personality. Some rooms run on ambition.
          Others run on execution. This is your chance to find out what yours
          is made of — and prove it.
        </p>

        {/* Scroll CTA */}
        <button
          onClick={() => {
            document.getElementById('city-grid')?.scrollIntoView({ behavior: 'smooth' })
          }}
          className="w-full max-w-[320px] py-4 bg-pav-pink text-white font-semibold text-[15px] rounded-full
                     hover:bg-pav-pink-800 active:scale-[0.98] transition-all duration-150"
        >
          Find Your Archetype →
        </button>
      </div>

      {/* City grid */}
      <div id="city-grid" className="pt-4">
        <p className="text-[10px] font-bold tracking-[0.24em] uppercase text-white/25 text-center mb-4">
          Select Your City
        </p>

        <div className="grid grid-cols-3 gap-2">
          {chapters.map(chapter => (
            <button
              key={chapter.id}
              onClick={() => onSelect(chapter)}
              className="
                relative py-3 px-2 rounded-xl text-center
                bg-cw-surface border border-white/[0.06]
                text-[13px] font-semibold text-white/80
                hover:border-pav-pink/50 hover:bg-cw-surface2 hover:text-white hover:scale-[1.03]
                active:scale-[0.97]
                transition-all duration-150
              "
            >
              {chapter.name}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

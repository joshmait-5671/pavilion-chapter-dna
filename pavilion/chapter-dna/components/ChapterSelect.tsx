'use client'

import { useState } from 'react'
import { Chapter } from '@/types'

interface ChapterSelectProps {
  chapters: Chapter[]
  onSelect: (chapter: Chapter) => void
}

export default function ChapterSelect({ chapters, onSelect }: ChapterSelectProps) {
  const [selected, setSelected] = useState<Chapter | null>(null)

  const handlePick = (chapter: Chapter) => {
    setSelected(chapter)
  }

  const handleContinue = () => {
    if (selected) onSelect(selected)
  }

  return (
    <div className="flex flex-col min-h-dvh bg-[#180A5C] px-5 pt-14 pb-8">
      {/* Wordmark */}
      <div className="mb-10">
        <p className="text-[11px] font-semibold tracking-[0.18em] uppercase text-pav-purple-400">
          Pavilion
        </p>
        <h1 className="mt-2 text-[28px] font-display font-bold text-white leading-[1.15] tracking-tight">
          Chapter DNA
        </h1>
      </div>

      {/* Prompt */}
      <p className="text-[16px] text-white/60 mb-6 leading-relaxed">
        Which chapter are you in?
      </p>

      {/* Chapter grid */}
      <div className="flex flex-wrap gap-2 flex-1">
        {chapters.map((chapter) => {
          const isSelected = selected?.id === chapter.id
          return (
            <button
              key={chapter.id}
              onClick={() => handlePick(chapter)}
              className={`
                px-4 py-2.5 rounded-lg border text-sm font-medium
                transition-all duration-150 active:scale-95
                ${isSelected
                  ? 'bg-pav-pink text-white border-pav-pink'
                  : 'bg-white/8 text-white/80 border-white/12 hover:border-white/30 hover:text-white hover:bg-white/12'
                }
              `}
            >
              {chapter.name}
            </button>
          )
        })}
      </div>

      {/* Continue */}
      <div
        className={`
          mt-8 transition-all duration-300
          ${selected ? 'opacity-100 translate-y-0' : 'opacity-0 translate-y-2 pointer-events-none'}
        `}
      >
        <button
          onClick={handleContinue}
          className="w-full py-4 bg-pav-pink text-white font-semibold text-[15px] rounded-xl
                     hover:bg-pav-pink-800 active:scale-[0.98] transition-all duration-150"
        >
          Continue
        </button>
      </div>
    </div>
  )
}

'use client'

import { Chapter } from '@/types'

interface CompletionScreenProps {
  chapter: Chapter
  totalQuestions: number
  onRestart: () => void
}

export default function CompletionScreen({
  chapter,
  totalQuestions,
  onRestart,
}: CompletionScreenProps) {
  return (
    <div className="flex flex-col min-h-dvh bg-[#111111] px-5 py-12">
      {/* Top spacer */}
      <div className="flex-1" />

      {/* Check mark */}
      <div className="flex justify-center mb-8 animate-fade-in">
        <div
          className="w-16 h-16 rounded-full flex items-center justify-center"
          style={{ background: 'rgba(255,255,255,0.06)', border: '1px solid rgba(255,255,255,0.1)' }}
        >
          <svg width="28" height="28" viewBox="0 0 28 28" fill="none">
            <path
              d="M6 14L11.5 20L22 8"
              stroke="#f5f4ef"
              strokeWidth="2"
              strokeLinecap="round"
              strokeLinejoin="round"
            />
          </svg>
        </div>
      </div>

      {/* Heading */}
      <div className="text-center animate-slide-in" style={{ animationDelay: '60ms' }}>
        <h1 className="text-[32px] sm:text-[38px] font-bold text-[#f5f4ef] leading-[1.15] tracking-tight mb-3">
          You're done.
        </h1>
        <p className="text-[15px] text-white/40 leading-relaxed max-w-[280px] mx-auto">
          Thanks for completing Chapter DNA for{' '}
          <span className="text-white/70">{chapter.name}</span>.
        </p>
      </div>

      {/* Stats row */}
      <div
        className="flex items-center justify-center gap-8 mt-10 animate-fade-in"
        style={{ animationDelay: '160ms' }}
      >
        <div className="text-center">
          <p className="text-[28px] font-bold text-[#f5f4ef] tabular-nums">{totalQuestions}</p>
          <p className="text-[11px] text-white/30 tracking-wider uppercase mt-0.5">Questions</p>
        </div>
        <div className="w-px h-8 bg-white/10" />
        <div className="text-center">
          <p className="text-[28px] font-bold text-[#f5f4ef]">~2</p>
          <p className="text-[11px] text-white/30 tracking-wider uppercase mt-0.5">Minutes</p>
        </div>
        <div className="w-px h-8 bg-white/10" />
        <div className="text-center">
          <p className="text-[28px] font-bold text-[#f5f4ef]">✓</p>
          <p className="text-[11px] text-white/30 tracking-wider uppercase mt-0.5">Complete</p>
        </div>
      </div>

      {/* Bottom spacer */}
      <div className="flex-1" />

      {/* CTA */}
      <div className="animate-fade-in" style={{ animationDelay: '240ms' }}>
        <p className="text-center text-[13px] text-white/25 mb-6">
          Your responses have been recorded.
        </p>
        <button
          onClick={onRestart}
          className="w-full py-4 rounded-2xl text-[15px] font-semibold
                     active:scale-[0.98] transition-transform duration-100"
          style={{
            background: 'rgba(255,255,255,0.07)',
            color: 'rgba(255,255,255,0.5)',
            border: '1px solid rgba(255,255,255,0.08)',
          }}
        >
          Start over
        </button>
      </div>
    </div>
  )
}

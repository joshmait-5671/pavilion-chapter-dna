'use client'

interface WelcomeScreenProps {
  chapterName: string
  onStart: () => void
}

export default function WelcomeScreen({ chapterName, onStart }: WelcomeScreenProps) {
  return (
    <div className="flex flex-col min-h-dvh bg-cw-bg px-5 pt-14 pb-10">

      {/* Eyebrow */}
      <p className="text-[10px] font-bold tracking-[0.28em] uppercase text-pav-pink mb-3">
        Chapter Wars
      </p>

      {/* Chapter name */}
      <p className="text-[13px] font-semibold text-white/50 mb-10 tracking-wide">
        {chapterName} Chapter
      </p>

      {/* Hero copy */}
      <div className="flex-1">
        <h1 className="font-display font-bold text-white leading-[1.1] tracking-[-0.025em] mb-6"
            style={{ fontSize: 'clamp(32px, 9vw, 42px)' }}>
          You&apos;re representing<br />
          <span className="text-pav-pink">{chapterName}.</span>
        </h1>

        <p className="text-[15px] text-white/55 leading-relaxed max-w-sm mb-8">
          Answer 10 questions about your chapter&apos;s personality. We&apos;ll tell you exactly
          what archetype defines it — and where you rank against every other city.
        </p>

        <p className="text-[13px] text-white/35">
          Takes 90 seconds. Results are meant to be shared.
        </p>
      </div>

      {/* CTA */}
      <button
        onClick={onStart}
        className="w-full py-4 bg-pav-pink text-white font-semibold text-[15px] rounded-full
                   hover:bg-pav-pink-800 active:scale-[0.98] transition-all duration-150 mt-10"
      >
        Start the Assessment →
      </button>
    </div>
  )
}

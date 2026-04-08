'use client'

interface WelcomeScreenProps {
  chapterName: string
  onStart: () => void
}

export default function WelcomeScreen({ chapterName, onStart }: WelcomeScreenProps) {
  return (
    <div className="flex flex-col min-h-dvh bg-[#180A5C] px-5 pt-14 pb-10">
      {/* Label */}
      <p className="text-[11px] font-semibold tracking-[0.18em] uppercase text-pav-purple-400 mb-2">
        Chapter DNA
      </p>

      {/* Chapter name */}
      <p className="text-[13px] font-medium text-white/60 mb-10">
        {chapterName} Chapter
      </p>

      {/* Hero copy */}
      <div className="flex-1">
        <h1 className="text-[36px] font-display font-bold text-white leading-[1.1] tracking-tight mb-6">
          10 questions.<br />
          Under 3 minutes.<br />
          No right answers.
        </h1>

        <p className="text-[15px] text-white/60 leading-relaxed max-w-sm">
          Your answers will be combined with your chapter&rsquo;s responses
          to generate a unique chapter identity — and eventually, head-to-head
          comparisons with other chapters.
        </p>

        <div className="mt-8 flex flex-col gap-3">
          {[
            'One question at a time',
            'Tap to select, auto-advances',
            'Takes about 2 minutes',
          ].map((hint) => (
            <div key={hint} className="flex items-center gap-3">
              <span className="w-1.5 h-1.5 rounded-full bg-pav-pink/40 flex-shrink-0" />
              <p className="text-[13px] text-white/50">{hint}</p>
            </div>
          ))}
        </div>
      </div>

      {/* CTA */}
      <button
        onClick={onStart}
        className="w-full py-4 bg-pav-pink text-white font-semibold text-[15px] rounded-xl
                   hover:bg-pav-pink-800 active:scale-[0.98] transition-all duration-150 mt-10"
      >
        Start
      </button>
    </div>
  )
}

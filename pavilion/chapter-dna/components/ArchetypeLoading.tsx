'use client'

import { useEffect, useState } from 'react'

interface ArchetypeLoadingProps {
  chapterName: string
  onComplete: () => void
}

const MESSAGES = [
  'Reading the room…',
  'Analyzing chapter energy…',
  'Cross-referencing 847 chapters…',
  'Calculating your DNA…',
]

export default function ArchetypeLoading({ chapterName, onComplete }: ArchetypeLoadingProps) {
  const [messageIndex, setMessageIndex] = useState(0)
  const [progress, setProgress] = useState(0)

  useEffect(() => {
    // Cycle through messages
    const msgInterval = setInterval(() => {
      setMessageIndex(i => Math.min(i + 1, MESSAGES.length - 1))
    }, 500)

    // Animate progress bar over 1.8s
    const startTime = Date.now()
    const duration = 1800

    const progressInterval = setInterval(() => {
      const elapsed = Date.now() - startTime
      const pct = Math.min(elapsed / duration, 1)
      // Ease out cubic
      const eased = 1 - Math.pow(1 - pct, 3)
      setProgress(eased * 100)

      if (pct >= 1) {
        clearInterval(progressInterval)
        clearInterval(msgInterval)
        setTimeout(onComplete, 100)
      }
    }, 16)

    return () => {
      clearInterval(msgInterval)
      clearInterval(progressInterval)
    }
  }, [onComplete])

  return (
    <div className="flex flex-col items-center justify-center min-h-dvh bg-[#111111] px-8">
      {/* Chapter name */}
      <p
        className="text-[11px] font-semibold tracking-[0.22em] uppercase mb-12 text-white/40 animate-fade-in"
      >
        {chapterName}
      </p>

      {/* Main label */}
      <h2 className="text-[22px] font-display font-bold text-white mb-2 text-center leading-tight animate-slide-in">
        Calculating your
        <br />
        Chapter DNA
      </h2>

      {/* Cycling message */}
      <p
        className="text-[13px] mb-10 h-5 text-center text-white/40 transition-all duration-300"
      >
        {MESSAGES[messageIndex]}
      </p>

      {/* Progress bar */}
      <div className="w-48 h-[3px] rounded-full overflow-hidden bg-white/10">
        <div
          className="h-full rounded-full bg-white transition-all duration-75"
          style={{ width: `${progress}%` }}
        />
      </div>
    </div>
  )
}

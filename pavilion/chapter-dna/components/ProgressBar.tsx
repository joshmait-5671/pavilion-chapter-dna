'use client'

interface ProgressBarProps {
  current: number // 1-based
  total: number
}

export default function ProgressBar({ current, total }: ProgressBarProps) {
  const pct = Math.round((current / total) * 100)

  return (
    <div className="w-full h-[3px] bg-white/10 overflow-hidden">
      <div
        className="h-full bg-pav-pink transition-all duration-500 ease-out"
        style={{ width: `${pct}%` }}
      />
    </div>
  )
}

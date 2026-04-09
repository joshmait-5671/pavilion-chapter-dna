'use client'

interface ProgressBarProps {
  current: number
  total: number
}

export default function ProgressBar({ current, total }: ProgressBarProps) {
  const pct = (current / total) * 100

  return (
    <div className="w-full h-[2px] bg-white/[0.06]">
      <div
        className="h-full bg-pav-pink transition-all duration-300 ease-out"
        style={{
          width: `${pct}%`,
          boxShadow: '0 0 8px #DF285B, 0 0 16px rgba(223,40,91,0.4)',
        }}
      />
    </div>
  )
}

'use client'

interface ProgressBarProps {
  current: number
  total: number
}

export default function ProgressBar({ current, total }: ProgressBarProps) {
  const pct = (current / total) * 100

  return (
    <div style={{ width: '100%', height: '3px', background: 'rgba(255,255,255,0.12)' }}>
      <div
        style={{
          height: '100%',
          width: `${pct}%`,
          background: '#FFFFFF',
          borderRadius: '0 2px 2px 0',
          transition: 'width 300ms ease-out',
        }}
      />
    </div>
  )
}

'use client'

import { CardType, AnswerOption } from '@/types'

interface AnswerCardProps {
  option: AnswerOption
  cardType: CardType
  isSelected: boolean
  isDisabled: boolean
  onSelect: () => void
}

export default function AnswerCard({
  option,
  cardType,
  isSelected,
  isDisabled,
  onSelect,
}: AnswerCardProps) {
  const baseCard = `
    relative cursor-pointer rounded-xl transition-all duration-150 select-none
    border outline-none focus-visible:ring-2 focus-visible:ring-pav-pink/40
    ${isDisabled ? 'pointer-events-none' : ''}
  `

  // ── Variant: text ──────────────────────────────────────────────────────────
  if (cardType === 'text') {
    return (
      <button
        onClick={onSelect}
        style={{
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          padding: '16px 20px',
          minHeight: '72px',
          borderRadius: '12px',
          border: isSelected ? '2px solid rgba(255,255,255,0.9)' : '1.5px solid rgba(255,255,255,0.12)',
          background: isSelected ? 'rgba(255,255,255,0.95)' : 'rgba(255,255,255,0.08)',
          cursor: isDisabled ? 'default' : 'pointer',
          transition: 'background 0.12s, border-color 0.12s',
          width: '100%',
          textAlign: 'left',
          pointerEvents: isDisabled ? 'none' : 'auto',
        }}
      >
        <span style={{
          fontSize: '15px',
          fontWeight: 500,
          lineHeight: 1.35,
          color: isSelected ? '#111111' : 'rgba(255,255,255,0.8)',
        }}>
          {option.text}
        </span>
        <span style={{ marginLeft: '12px', flexShrink: 0, opacity: isSelected ? 1 : 0, transition: 'opacity 0.12s' }}>
          <CheckIcon color={isSelected ? '#111111' : '#ffffff'} />
        </span>
      </button>
    )
  }

  // ── Variant: icon-text ─────────────────────────────────────────────────────
  if (cardType === 'icon-text') {
    return (
      <button
        onClick={onSelect}
        style={{
          display: 'flex',
          alignItems: 'center',
          gap: '12px',
          padding: '16px',
          minHeight: '72px',
          borderRadius: '12px',
          border: isSelected ? '2px solid rgba(255,255,255,0.9)' : '1.5px solid rgba(255,255,255,0.12)',
          background: isSelected ? 'rgba(255,255,255,0.95)' : 'rgba(255,255,255,0.08)',
          cursor: isDisabled ? 'default' : 'pointer',
          transition: 'background 0.12s, border-color 0.12s',
          width: '100%',
          textAlign: 'left',
          pointerEvents: isDisabled ? 'none' : 'auto',
        }}
      >
        <span style={{ fontSize: '20px', flexShrink: 0, lineHeight: 1 }} role="img" aria-label="">
          {option.icon}
        </span>
        <span style={{
          fontSize: '14px',
          fontWeight: 500,
          lineHeight: 1.35,
          color: isSelected ? '#111111' : 'rgba(255,255,255,0.8)',
        }}>
          {option.text}
        </span>
        {isSelected && (
          <span style={{ marginLeft: 'auto', flexShrink: 0 }}>
            <CheckIcon color="#111111" />
          </span>
        )}
      </button>
    )
  }

  // ── Variant: image-text ────────────────────────────────────────────────────
  return (
    <button
      onClick={onSelect}
      className={`
        ${baseCard}
        overflow-hidden h-[160px]
        ${isSelected ? 'border-white/90 ring-1 ring-white/30 animate-pulse-select' : 'border-white/10 hover:border-white/25 active:scale-[0.98]'}
      `}
      style={{
        backgroundImage: `url(${option.image})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundColor: '#111111',
      }}
    >
      {/* Dark overlay */}
      <div
        className="absolute inset-0"
        style={{
          background: isSelected
            ? 'linear-gradient(to top, rgba(10,10,15,0.92) 0%, rgba(10,10,15,0.35) 60%, rgba(10,10,15,0.15) 100%)'
            : 'linear-gradient(to top, rgba(10,10,15,0.85) 0%, rgba(10,10,15,0.3) 60%, rgba(10,10,15,0.1) 100%)',
        }}
      />

      {/* Selected ring overlay */}
      {isSelected && (
        <div className="absolute inset-0 bg-white/10" />
      )}

      {/* Check badge */}
      {isSelected && (
        <div className="absolute top-2.5 right-2.5 bg-white rounded-full p-0.5">
          <CheckIcon color="#111111" size={12} />
        </div>
      )}

      {/* Label */}
      <div className="absolute bottom-0 left-0 right-0 px-3 pb-3 pt-6">
        <p className="text-[13px] font-semibold text-white leading-tight text-left">
          {option.text}
        </p>
      </div>
    </button>
  )
}

// ── Internal check icon ────────────────────────────────────────────────────────
function CheckIcon({ color = '#ffffff', size = 14 }: { color?: string; size?: number; className?: string }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 14 14"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
    >
      <path
        d="M2.5 7L5.5 10L11.5 4"
        stroke={color}
        strokeWidth="1.75"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

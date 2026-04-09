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
        className={`
          ${baseCard}
          flex items-center justify-between
          px-5 py-5 min-h-[72px]
          ${isSelected
            ? 'bg-pav-pink/15 border-pav-pink animate-pulse-select'
            : 'bg-white/8 border-white/10 hover:bg-white/12 hover:border-white/20 active:scale-[0.98]'
          }
        `}
      >
        <span className={`text-[15px] font-medium leading-snug text-left ${isSelected ? 'text-white' : 'text-white/80'}`}>
          {option.text}
        </span>
        <span className={`ml-3 flex-shrink-0 transition-opacity duration-150 ${isSelected ? 'opacity-100' : 'opacity-0'}`}>
          <CheckIcon />
        </span>
      </button>
    )
  }

  // ── Variant: icon-text ─────────────────────────────────────────────────────
  if (cardType === 'icon-text') {
    return (
      <button
        onClick={onSelect}
        className={`
          ${baseCard}
          flex items-center gap-3
          px-4 py-5 min-h-[72px]
          ${isSelected
            ? 'bg-pav-pink/15 border-pav-pink animate-pulse-select'
            : 'bg-white/8 border-white/10 hover:bg-white/12 hover:border-white/20 active:scale-[0.98]'
          }
        `}
      >
        <span className="text-xl flex-shrink-0 leading-none" role="img" aria-label="">
          {option.icon}
        </span>
        <span className={`text-[14px] font-medium leading-snug text-left ${isSelected ? 'text-white' : 'text-white/80'}`}>
          {option.text}
        </span>
        {isSelected && (
          <span className="ml-auto flex-shrink-0">
            <CheckIcon />
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
        ${isSelected ? 'border-pav-pink ring-1 ring-pav-pink/30 animate-pulse-select' : 'border-white/10 hover:border-white/25 active:scale-[0.98]'}
      `}
      style={{
        backgroundImage: `url(${option.image})`,
        backgroundSize: 'cover',
        backgroundPosition: 'center',
        backgroundColor: '#0a0a0f',
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
        <div className="absolute inset-0 bg-pav-pink/8" />
      )}

      {/* Check badge */}
      {isSelected && (
        <div className="absolute top-2.5 right-2.5 bg-pav-pink rounded-full p-0.5">
          <CheckIcon className="text-white" size={12} />
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
function CheckIcon({ className = 'text-white', size = 14 }: { className?: string; size?: number }) {
  return (
    <svg
      width={size}
      height={size}
      viewBox="0 0 14 14"
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      className={className}
    >
      <path
        d="M2.5 7L5.5 10L11.5 4"
        stroke="currentColor"
        strokeWidth="1.75"
        strokeLinecap="round"
        strokeLinejoin="round"
      />
    </svg>
  )
}

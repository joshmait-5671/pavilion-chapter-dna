'use client'

import { Chapter } from '@/types'

interface ChapterSelectProps {
  chapters: Chapter[]
  onSelect: (chapter: Chapter) => void
}

export default function ChapterSelect({ chapters, onSelect }: ChapterSelectProps) {
  return (
    <div className="flex flex-col min-h-dvh px-5 pb-10 relative overflow-hidden"
         style={{ background: '#FFE135' }}>

      {/* Ghost letter bg decoration */}
      <div
        aria-hidden
        style={{
          position: 'absolute',
          bottom: '-40px',
          right: '-20px',
          fontSize: 'clamp(200px, 55vw, 280px)',
          fontWeight: 900,
          color: 'rgba(0,0,0,0.05)',
          lineHeight: 1,
          letterSpacing: '-0.05em',
          pointerEvents: 'none',
          userSelect: 'none',
          fontFamily: 'var(--font-space-grotesk)',
        }}
      >
        W
      </div>

      {/* Pavilion eyebrow */}
      <p style={{
        fontSize: '10px',
        fontWeight: 800,
        letterSpacing: '0.22em',
        textTransform: 'uppercase',
        color: 'rgba(0,0,0,0.4)',
        paddingTop: '48px',
        marginBottom: 'auto',
      }}>
        Pavilion
      </p>

      {/* Hero type */}
      <div style={{ marginTop: 'auto', position: 'relative', zIndex: 1 }}>
        <h1 style={{
          fontSize: 'clamp(52px, 14vw, 72px)',
          fontWeight: 900,
          color: '#111111',
          lineHeight: 0.88,
          letterSpacing: '-0.04em',
          marginBottom: '16px',
          fontFamily: 'var(--font-space-grotesk)',
        }}>
          CHAPTER<br />WARS
        </h1>
        <p style={{
          fontSize: '14px',
          fontWeight: 500,
          color: 'rgba(0,0,0,0.5)',
          lineHeight: 1.5,
          marginBottom: '28px',
        }}>
          Which archetype is your chapter?
        </p>

        {/* City grid */}
        <div style={{
          display: 'grid',
          gridTemplateColumns: 'repeat(3, 1fr)',
          gap: '8px',
          marginBottom: '16px',
        }}>
          {chapters.map(chapter => (
            <button
              key={chapter.id}
              onClick={() => onSelect(chapter)}
              style={{
                padding: '10px 6px',
                background: 'rgba(0,0,0,0.08)',
                border: '2px solid rgba(0,0,0,0.12)',
                borderRadius: '8px',
                fontSize: '12px',
                fontWeight: 700,
                color: '#111111',
                cursor: 'pointer',
                transition: 'background 0.12s, border-color 0.12s, transform 0.12s',
                fontFamily: 'var(--font-space-grotesk)',
              }}
              onMouseEnter={e => {
                ;(e.currentTarget as HTMLButtonElement).style.background = 'rgba(0,0,0,0.15)'
                ;(e.currentTarget as HTMLButtonElement).style.borderColor = 'rgba(0,0,0,0.3)'
              }}
              onMouseLeave={e => {
                ;(e.currentTarget as HTMLButtonElement).style.background = 'rgba(0,0,0,0.08)'
                ;(e.currentTarget as HTMLButtonElement).style.borderColor = 'rgba(0,0,0,0.12)'
              }}
            >
              {chapter.name}
            </button>
          ))}
        </div>
      </div>
    </div>
  )
}

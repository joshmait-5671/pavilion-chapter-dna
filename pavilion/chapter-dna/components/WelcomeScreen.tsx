'use client'

interface WelcomeScreenProps {
  chapterName: string
  onStart: () => void
}

export default function WelcomeScreen({ chapterName, onStart }: WelcomeScreenProps) {
  return (
    <div className="flex flex-col min-h-dvh px-5 pb-10 relative overflow-hidden"
         style={{ background: '#FFE135' }}>

      {/* Ghost letter — first letter of city name */}
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
        {chapterName.charAt(0).toUpperCase()}
      </div>

      {/* Eyebrow */}
      <p style={{
        fontSize: '10px',
        fontWeight: 800,
        letterSpacing: '0.22em',
        textTransform: 'uppercase',
        color: 'rgba(0,0,0,0.4)',
        paddingTop: '48px',
        marginBottom: '8px',
      }}>
        Chapter Wars
      </p>

      {/* Chapter name badge */}
      <p style={{
        fontSize: '13px',
        fontWeight: 700,
        color: 'rgba(0,0,0,0.5)',
        marginBottom: 'auto',
      }}>
        {chapterName} Chapter
      </p>

      {/* Hero */}
      <div style={{ position: 'relative', zIndex: 1, marginTop: 'auto' }}>
        <h1 style={{
          fontSize: 'clamp(40px, 11vw, 56px)',
          fontWeight: 900,
          color: '#111111',
          lineHeight: 0.95,
          letterSpacing: '-0.04em',
          marginBottom: '20px',
          fontFamily: 'var(--font-space-grotesk)',
        }}>
          You&apos;re<br />representing<br />{chapterName}.
        </h1>

        <p style={{
          fontSize: '14px',
          fontWeight: 500,
          color: 'rgba(0,0,0,0.5)',
          lineHeight: 1.6,
          marginBottom: '32px',
          maxWidth: '280px',
        }}>
          10 questions. 90 seconds. Find out what your chapter is made of.
        </p>

        <button
          onClick={onStart}
          style={{
            width: '100%',
            padding: '16px 20px',
            background: '#111111',
            color: '#FFE135',
            border: 'none',
            borderRadius: '8px',
            fontSize: '14px',
            fontWeight: 800,
            letterSpacing: '0.04em',
            textTransform: 'uppercase',
            cursor: 'pointer',
            fontFamily: 'var(--font-space-grotesk)',
          }}
        >
          Start the Assessment →
        </button>
      </div>
    </div>
  )
}

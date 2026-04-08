'use client'

import { useEffect, useState } from 'react'
import { ARCHETYPES, ArchetypeId } from '@/lib/archetype'

const ARCHETYPE_COLORS: Record<ArchetypeId, string> = {
  insurgents:    '#DF285B',
  inner_circle:  '#C57FD9',
  operators:     '#4A9EDB',
  climbers:      '#F4A742',
  intelligentsia:'#5BB89C',
  builders:      '#8B7FD4',
}

const MIN_VOTES = 3 // raise to 10 for production

interface BreakdownItem {
  archetypeId: ArchetypeId
  count: number
  pct: number
}

interface ChapterStats {
  chapterId: string
  chapterName: string
  total: number
  breakdown: BreakdownItem[]
  leading: ArchetypeId
  locked: boolean
}

async function fetchLeaderboard(): Promise<ChapterStats[]> {
  const url = process.env.NEXT_PUBLIC_SHEETS_URL
  if (!url) return []
  try {
    const resp = await fetch(url, { cache: 'no-store' })
    const json = await resp.json()
    if (!json.success || !json.data) return []

    const byChapter: Record<string, { name: string; votes: Record<string, number> }> = {}
    for (const row of json.data) {
      if (!row.chapterId || !row.archetype) continue
      if (!byChapter[row.chapterId]) byChapter[row.chapterId] = { name: row.chapter, votes: {} }
      byChapter[row.chapterId].votes[row.archetype] =
        (byChapter[row.chapterId].votes[row.archetype] || 0) + 1
    }

    return Object.entries(byChapter)
      .map(([chapterId, { name, votes }]) => {
        const total = Object.values(votes).reduce((s, c) => s + c, 0)
        const sorted = Object.entries(votes).sort(([, a], [, b]) => b - a)
        const breakdown: BreakdownItem[] = sorted.map(([id, count]) => ({
          archetypeId: id as ArchetypeId,
          count,
          pct: Math.round((count / total) * 100),
        }))
        return {
          chapterId,
          chapterName: name,
          total,
          breakdown,
          leading: sorted[0][0] as ArchetypeId,
          locked: total >= MIN_VOTES,
        }
      })
      .sort((a, b) => b.total - a.total)
  } catch {
    return []
  }
}

function archetypeFontSize(name: string): string {
  const longest = Math.max(...name.split(' ').map(w => w.length))
  const px = Math.min(56, Math.floor(260 / (longest * 0.6)))
  return `${px}px`
}

export default function LeaderboardPage() {
  const [chapters, setChapters] = useState<ChapterStats[]>([])
  const [loading, setLoading] = useState(true)
  const [lastUpdated, setLastUpdated] = useState<Date | null>(null)

  const poppins = 'var(--font-poppins), system-ui, sans-serif'

  const load = async () => {
    const data = await fetchLeaderboard()
    setChapters(data)
    setLastUpdated(new Date())
    setLoading(false)
  }

  useEffect(() => {
    load()
    const interval = setInterval(load, 30_000)
    return () => clearInterval(interval)
  }, [])

  const totalVotes = chapters.reduce((s, c) => s + c.total, 0)

  return (
    <div style={{ minHeight: '100dvh', background: '#080808', fontFamily: poppins, color: '#fff' }}>

      {/* ── Masthead ── */}
      <div style={{ padding: '20px 20px 0', maxWidth: '860px', margin: '0 auto' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
          <p style={{ fontSize: '14px', fontWeight: 800, letterSpacing: '0.38em', color: 'rgba(255,255,255,0.95)', textTransform: 'uppercase' }}>
            Pavilion
          </p>
          <div style={{ padding: '5px 13px', borderRadius: '999px', fontSize: '9px', fontWeight: 700, letterSpacing: '0.18em', textTransform: 'uppercase', background: 'rgba(223,40,91,0.9)', color: '#fff' }}>
            Chapter DNA
          </div>
        </div>
        <div style={{ height: '1px', background: 'rgba(255,255,255,0.08)', marginTop: '11px' }} />

        <div style={{ paddingTop: '28px', paddingBottom: '4px' }}>
          <h1 style={{ fontSize: '32px', fontWeight: 900, letterSpacing: '-0.025em', lineHeight: 1 }}>
            Live Results
          </h1>
          <p style={{ fontSize: '11px', color: 'rgba(255,255,255,0.28)', marginTop: '8px', letterSpacing: '0.04em' }}>
            {chapters.length} chapter{chapters.length !== 1 ? 's' : ''} · {totalVotes} vote{totalVotes !== 1 ? 's' : ''} cast
            {lastUpdated && ` · ${lastUpdated.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`}
            {' · refreshes every 30s'}
          </p>
        </div>
      </div>

      {/* ── Chapter grid ── */}
      <div style={{
        padding: '20px 16px 60px',
        maxWidth: '860px',
        margin: '0 auto',
        display: 'grid',
        gridTemplateColumns: 'repeat(auto-fill, minmax(280px, 1fr))',
        gap: '12px',
      }}>
        {loading && (
          <p style={{ color: 'rgba(255,255,255,0.28)', fontSize: '13px', padding: '40px 4px', gridColumn: '1 / -1' }}>
            Loading results…
          </p>
        )}

        {!loading && chapters.length === 0 && (
          <p style={{ color: 'rgba(255,255,255,0.28)', fontSize: '13px', padding: '40px 4px', gridColumn: '1 / -1' }}>
            No votes yet — send members to take the survey.
          </p>
        )}

        {chapters.map(c => {
          const arch = ARCHETYPES[c.leading]
          const color = ARCHETYPE_COLORS[c.leading]

          return (
            <div
              key={c.chapterId}
              style={{
                borderRadius: '16px',
                background: '#111',
                border: `1px solid ${c.locked ? 'rgba(255,255,255,0.09)' : 'rgba(255,255,255,0.04)'}`,
                padding: '20px',
                position: 'relative',
                overflow: 'hidden',
              }}
            >
              {/* Subtle color accent behind leading archetype */}
              {c.locked && (
                <div style={{
                  position: 'absolute', top: 0, left: 0, right: 0, height: '3px',
                  background: `linear-gradient(90deg, ${color}, transparent)`,
                }} />
              )}

              {/* Chapter name + status */}
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
                <p style={{ fontSize: '10px', fontWeight: 700, letterSpacing: '0.24em', color: 'rgba(255,255,255,0.32)', textTransform: 'uppercase' }}>
                  {c.chapterName}
                </p>
                <div style={{
                  padding: '3px 10px', borderRadius: '999px', fontSize: '8px', fontWeight: 700,
                  letterSpacing: '0.12em', textTransform: 'uppercase',
                  background: c.locked ? 'rgba(91,184,156,0.12)' : 'rgba(244,167,66,0.12)',
                  color: c.locked ? '#5BB89C' : '#F4A742',
                  border: `1px solid ${c.locked ? 'rgba(91,184,156,0.25)' : 'rgba(244,167,66,0.25)'}`,
                }}>
                  {c.locked ? 'Result' : 'Voting'}
                </div>
              </div>

              {c.locked ? (
                <>
                  {/* Archetype name */}
                  <p style={{ fontSize: '10px', fontWeight: 500, letterSpacing: '0.28em', color: 'rgba(255,255,255,0.22)', textTransform: 'uppercase', marginBottom: '2px' }}>
                    The
                  </p>
                  <h2 style={{ fontSize: archetypeFontSize(arch.name), fontWeight: 900, color: '#fff', lineHeight: 0.9, letterSpacing: '-0.02em', marginBottom: '10px' }}>
                    {arch.name}
                  </h2>
                  <p style={{ fontSize: '12px', fontWeight: 600, color: '#C57FD9', fontStyle: 'italic', marginBottom: '18px', lineHeight: 1.4 }}>
                    {arch.tagline}
                  </p>

                  {/* Breakdown bar */}
                  <div style={{ display: 'flex', height: '4px', borderRadius: '999px', overflow: 'hidden', gap: '2px', marginBottom: '10px' }}>
                    {c.breakdown.map(b => (
                      <div
                        key={b.archetypeId}
                        title={`${ARCHETYPES[b.archetypeId]?.name} ${b.pct}%`}
                        style={{ flex: b.count, background: ARCHETYPE_COLORS[b.archetypeId] ?? '#444', minWidth: '2px' }}
                      />
                    ))}
                  </div>

                  {/* Top 3 breakdown labels */}
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '8px 14px', marginBottom: '16px' }}>
                    {c.breakdown.slice(0, 3).map(b => (
                      <span key={b.archetypeId} style={{ fontSize: '9px', fontWeight: 600, color: 'rgba(255,255,255,0.32)', letterSpacing: '0.03em', display: 'flex', alignItems: 'center', gap: '4px' }}>
                        <span style={{ width: '6px', height: '6px', borderRadius: '50%', background: ARCHETYPE_COLORS[b.archetypeId], display: 'inline-block', flexShrink: 0 }} />
                        {ARCHETYPES[b.archetypeId]?.name} {b.pct}%
                      </span>
                    ))}
                  </div>
                </>
              ) : (
                <div style={{ paddingBottom: '16px' }}>
                  <p style={{ fontSize: '14px', fontWeight: 700, color: 'rgba(255,255,255,0.4)', marginBottom: '6px' }}>
                    Voting in progress…
                  </p>
                  <p style={{ fontSize: '11px', color: 'rgba(255,255,255,0.2)' }}>
                    Result unlocks at {MIN_VOTES} votes
                  </p>
                </div>
              )}

              {/* Footer */}
              <div style={{ height: '1px', background: 'rgba(255,255,255,0.06)', margin: '4px 0 10px' }} />
              <p style={{ fontSize: '10px', color: 'rgba(255,255,255,0.2)', letterSpacing: '0.04em' }}>
                {c.total} member{c.total !== 1 ? 's' : ''} voted
              </p>
            </div>
          )
        })}
      </div>

      {/* Footer */}
      <div style={{ textAlign: 'center', paddingBottom: '32px' }}>
        <p style={{ fontSize: '9px', fontWeight: 600, letterSpacing: '0.2em', color: 'rgba(255,255,255,0.1)', textTransform: 'uppercase' }}>
          joinpavilion.com · 2026
        </p>
      </div>
    </div>
  )
}

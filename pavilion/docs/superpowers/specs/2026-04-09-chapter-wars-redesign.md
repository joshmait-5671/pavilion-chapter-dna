# Chapter Wars — Redesign Spec

**Date:** 2026-04-09
**Project:** `/Users/joshmait/Desktop/Claude/pavilion/chapter-dna/`
**Live:** https://chapter-dna.vercel.app

---

## Goal

Relaunch Chapter DNA as **Chapter Wars** — a timeboxed Pavilion city competition with Spotify Wrapped visual energy, per-archetype collectible cards, and social-ready exports for LinkedIn and Instagram.

---

## What Changes / What Stays

### Changes
- Brand name: Chapter DNA → **Chapter Wars**
- Landing page: full redesign (competition framing, dark, gradient, dates)
- Welcome screen: updated copy for competition context
- Survey: dark mode redesign + question reorder (images at positions 2, 5, 10)
- Loading + completion screens: dark mode treatment (prevent jarring flash)
- Result screen (`ChapterCard.tsx`): per-archetype palette, social share buttons
- Social export: canvas-rendered PNG — Square 1080×1080 (works on both Instagram + LinkedIn)

### Stays the Same
- Next.js app structure, all component files
- 10 questions, 6 archetypes, all answer IDs and scoring logic
- Google Sheets submission (`lib/submit.ts`)
- City data (15 cities, `data/chapters.json`)
- Page router (screen state machine in `app/page.tsx`)

---

## Section 0: Shared Config

`lib/config.ts` — imported by landing page, result screen, and social card export:

```ts
// lib/config.ts
export const COMPETITION_START = 'May 5, 2026'
export const COMPETITION_END   = 'May 30, 2026'
export const COMPETITION_LABEL = `Chapter Wars · ${COMPETITION_START} — ${COMPETITION_END}`
```

Update both date strings here when dates are confirmed.

---

## Section 1: Visual System

### Palette — Global
```
Background:    #0a0a0f   (near-black)
Surface:       #1a1a24   (dark cards)
Surface-2:     #242432   (elevated cards)
Pink:          #DF285B   (Pavilion, CTAs)
Pink-glow:     rgba(223,40,91,0.25)
White:         #ffffff
Muted:         rgba(255,255,255,0.45)
```

### Typography
- **Display font:** Space Grotesk (Google Fonts, weights 400–700 — **max available weight is 700, not 900**)
- **Body:** Inter or system-ui
- Headline scale: 64–72px mobile, tight letter-spacing (-0.03em)
- All-caps eyebrows at 10px / 0.25em tracking

**Font loading in app:** Add Space Grotesk via `next/font/google` in `app/layout.tsx` (same pattern as existing Inter), exposed as CSS variable `--font-space-grotesk`. Do NOT use a `globals.css` `@import` — it conflicts with the existing Next.js font pattern.

### Archetype IDs
As returned by `lib/archetype.ts` `calculateArchetype()` — used as keys in theme config and filenames:
```
inner_circle | operators | insurgents | climbers | intelligentsia | builders
```

### `lib/archetypeThemes.ts` — Full Definition

```ts
import { ArchetypeId } from '@/lib/archetype'

export interface ArchetypeTheme {
  primary:  string              // dominant color (borders, accents)
  accent:   string              // highlight (eyebrows, trait pills, canvas accents)
  cardBg:   string              // darkest card background color
  gradient: [string, string]    // [top, bottom] for top-to-bottom linear gradient
}

export const ARCHETYPE_THEMES: Record<ArchetypeId, ArchetypeTheme> = {
  inner_circle:   { primary: '#8B1A1A', accent: '#C9A84C', cardBg: '#1a0a0a', gradient: ['#1a0a0a', '#0a0a0f'] },
  operators:      { primary: '#1A3A5C', accent: '#E8EEF4', cardBg: '#0a1220', gradient: ['#0a1220', '#0a0a0f'] },
  insurgents:     { primary: '#CC1A1A', accent: '#FF6B6B', cardBg: '#1a0505', gradient: ['#1a0505', '#0a0a0f'] },
  climbers:       { primary: '#1A5C2A', accent: '#D4E84C', cardBg: '#061208', gradient: ['#061208', '#0a0a0f'] },
  intelligentsia: { primary: '#2D1A5C', accent: '#C4C4D4', cardBg: '#0d0a1a', gradient: ['#0d0a1a', '#0a0a0f'] },
  builders:       { primary: '#8B4A1A', accent: '#F0A050', cardBg: '#1a0e05', gradient: ['#1a0e05', '#0a0a0f'] },
}
```

**Note on `climbers` accent:** `#D4E84C` (yellow-green) on near-black has acceptable contrast at large sizes but should be verified at small canvas text. Bump to `#E8F46B` if readability suffers.

Gradient direction on all surfaces: **top-to-bottom linear** (`gradient[0]` at y=0, `gradient[1]` at y=height). Applied as CSS `background: linear-gradient(to bottom, ...)` on screens and as `ctx.createLinearGradient(0, 0, 0, height)` on canvas.

---

## Section 2: Landing Page (`components/ChapterSelect.tsx`)

Full redesign of existing `ChapterSelect.tsx`. Same props: `chapters`, `onSelect`.

### Layout
Full-screen dark, centered, mobile-first (max-width 480px centered on desktop).

```
┌─────────────────────────────────┐
│  PAVILION CHAPTER WARS          │  ← eyebrow, pink, 10px caps
│                                 │
│  15 cities.                     │  ← 64px Space Grotesk 700
│  6 archetypes.                  │     tight tracking, white
│  One winner.                    │
│                                 │
│  May 5 — May 30, 2026           │  ← from COMPETITION_LABEL, muted 13px
│  ─────────────────              │
│  Every Pavilion chapter has a   │  ← setup paragraph, 14px muted
│  personality. Some rooms run on │     line-height 1.75
│  ambition. Others run on        │
│  execution. This is your chance │
│  to find out what yours is made │
│  of — and prove it.             │
│                                 │
│  [FIND YOUR ARCHETYPE →]        │  ← pink pill CTA, full-width
│                                 │
│  ── SELECT YOUR CITY ──         │  ← section divider
│  [Atlanta] [Austin] [Boston]    │  ← city grid, dark cards
│  ...                            │
└─────────────────────────────────┘
```

### Gradient Burst
Large radial gradient centered behind the headline: `rgba(223,40,91,0.15)` at center → transparent at edges. Applied as CSS background on the hero section.

### City Grid
- Dark surface cards (`#1a1a24`), 3-col grid on mobile
- City name only (no photo — clean and fast)
- Hover: pink border glow, `scale(1.03)` transition
- Click calls `onSelect(chapter)` → navigates to Welcome

---

## Section 3: Welcome Screen (`components/WelcomeScreen.tsx`)

Dark mode redesign. Props unchanged: `chapterName`, `onStart`.

**Copy:**
> **You're representing [City].**
> Answer 10 questions about your chapter's personality. We'll tell you exactly what archetype defines it — and where you rank against every other city.
>
> Takes 90 seconds. Results are meant to be shared.

CTA: **"Start the Assessment →"** (pink pill, full-width)

---

## Section 4: Survey Redesign (`components/SurveyQuestion.tsx`)

### Visual
- Full dark background (`#0a0a0f`)
- Progress bar: thin 2px pink glowing line at top (`box-shadow: 0 0 8px #DF285B`), width = `(currentIndex+1)/total * 100%`
- Question text: 22px Space Grotesk 700, white
- Answer cards: `#1a1a24` bg, 1px `rgba(255,255,255,0.08)` border
- Selected state: pink border + `rgba(223,40,91,0.12)` bg + pulse keyframe (scale 1→1.03→1, 150ms)
- Auto-advance behavior: unchanged

### Question Order (images at positions 2, 5, 10)

**Do not change question `id` values** (q1, q6, etc.) — scoring keys off these. Only update the `number` display field and array order.

| New `number` | Question ID | Type |
|---|---|---|
| 1 | q1 — what do you expect most? | text |
| 2 | q6 — what event feels on-brand? | **image** |
| 3 | q2 — what is this chapter best at? | text |
| 4 | q3 — which people? | icon-text |
| 5 | q9 — chapter drink? | **image** |
| 6 | q4 — what energy? | text |
| 7 | q5 — what makes it different? | icon-text |
| 8 | q7 — secretly proud of? | icon-text |
| 9 | q8 — what does it say? | text |
| 10 | q10 — default meeting spot? | **image** |

---

## Section 5: Loading + Completion Screens

`ArchetypeLoading.tsx` and `CompletionScreen.tsx` get **dark mode treatment only** — no copy or layout changes. Apply `background: #0a0a0f`, white text, pink accent. Prevents jarring flash between the dark survey and dark result screen.

---

## Section 6: Result Screen (`components/ChapterCard.tsx`)

**Full JSX replacement.** The existing component is a two-page horizontal swipe layout with `page1Ref` (magazine cover) and `page2Ref` (editorial spread), plus `handleDownloadPDF` (jsPDF) and `handleShare` (html-to-image + Web Share API) handlers. All of this is removed. The new layout is a single scrollable vertical column. Remove: `jsPDF` import, `html-to-image` import, `handleDownloadPDF`, `handleShare`, old Share + PDF buttons, both page refs.

Props unchanged: `result`, `chapter`, `onRestart`.
**"Take it again"** calls `onRestart()` which resets to landing (clears city selection).
**Flavor text** source: `result.drink`, `result.spot`, `result.says` — already returned by `calculateArchetype()`. No new data needed.

### Layout (scrollable, archetype theme applied)

```
┌─────────────────────────────────┐
│  [archetype gradient, full bleed]
│  YOUR CHAPTER IS                │  ← 10px eyebrow, accent color
│  INSURGENTS                     │  ← 60px Space Grotesk 700, white
│  "Say the thing. Mean it."      │  ← tagline, 18px, muted white
│                                 │
│  [pill] Radically direct        │  ← 3 trait pills, accent bg
│  [pill] No filter               │
│  [pill] High standards          │
│                                 │
│  "Polished is overrated."       │  ← manifesto lines, italic 14px
│  "The truth has an edge. Good." │
│  "We say the thing..."          │
│                                 │
│  🥃 Whiskey neat                │  ← result.drink
│  📍 Neighborhood bar            │  ← result.spot
│  💬 "Get to the point"          │  ← result.says
│                                 │
│  ── SHARE YOUR RESULT ──        │
│                                 │
│  [📸  Save for Instagram]       │  ← full-width pink pill
│  [💼  Save for LinkedIn]        │  ← full-width outlined pill
│                                 │
│  [Take it again]                │  ← ghost text button
└─────────────────────────────────┘
```

Share buttons call named imports:
```ts
import { downloadCard } from '@/components/SocialCardExport'
// Instagram button:
await downloadCard(result, chapter, 'instagram')
// LinkedIn button:
await downloadCard(result, chapter, 'linkedin')
```

---

## Section 7: Social Card Export (`components/SocialCardExport.tsx`)

See also: `social-card-export` skill at `/Users/joshmait/.claude/skills/social-card-export/SKILL.md`

### Single exported function

```ts
export async function downloadCard(
  result: ArchetypeResult,
  chapter: Chapter,
  format: 'instagram' | 'linkedin'
): Promise<void>
```

### Dimensions

**Both formats use 1080×1080** (square). Research confirms 1080×1080 is the universal safe format for both Instagram feed and LinkedIn feed posts in 2026. A separate landscape format is out of scope for V1 — both share buttons produce the same square card.

### Font Loading

Space Grotesk max weight is **700** (not 900 — Google Fonts caps it). Load via Fontsource CDN (stable, versioned URL — no brittle gstatic parsing):

```ts
const font = new FontFace(
  'Space Grotesk',
  'url(https://cdn.jsdelivr.net/fontsource/fonts/space-grotesk@latest/latin-700-normal.woff2)'
)
await font.load()
document.fonts.add(font)
// ctx.font must exactly match registered family name:
ctx.font = '700 120px "Space Grotesk"'
```

Cache the font load promise — only load once per session.

### Canvas Card Design (1080×1080)

```
Background:   top-to-bottom archetype gradient (full bleed)
              ctx.createLinearGradient(0, 0, 0, 1080)
              stop 0 = theme.gradient[0], stop 1 = theme.gradient[1]

Top-left:     "PAVILION CHAPTER WARS" — 26px caps, accent color  (x:60, y:72)
Top-right:    COMPETITION_LABEL — 20px, muted  (right-aligned, y:72)

Center (y:440): Archetype name — 120px Space Grotesk 700, white, centered
Below (y:590):  Tagline — 34px italic, rgba(255,255,255,0.6), centered

Bottom band (y:880–1020):
  3 trait pills drawn as fillRect + fillText
  Centered, spaced evenly, accent color bg, dark text, 24px
  Each pill: measureText for width, +40px padding, 30px height, 15px radius

Bottom-right: "pavilion" — 20px, muted, right-aligned  (x:1020, y:1050)
```

**Text wrapping:** Archetype names are short (max "INTELLIGENTSIA" = 13 chars). No wrapping needed at 120px. Taglines fit at 34px within 900px center column — confirm with `measureText` and reduce font size if over 900px.

**Trait pill drawing pattern:**
```ts
function drawPill(ctx, text, cx, cy, theme) {
  const metrics = ctx.measureText(text)
  const pw = metrics.width + 40
  const ph = 32
  // draw rounded rect
  ctx.fillStyle = theme.accent
  roundRect(ctx, cx - pw/2, cy - ph/2, pw, ph, 16)
  ctx.fill()
  // draw text
  ctx.fillStyle = '#0a0a0f'
  ctx.font = '600 18px "Space Grotesk"'
  ctx.textAlign = 'center'
  ctx.fillText(text, cx, cy + 6)
}
```

### Export / Share

```ts
canvas.toBlob(blob => {
  const file = new File([blob], `chapter-wars-${result.archetype.id}.png`, { type: 'image/png' })

  // Mobile: use Web Share API (required on iOS — <a download> is broken)
  if (navigator.canShare?.({ files: [file] })) {
    navigator.share({ files: [file], title: 'Chapter Wars' })
    return
  }

  // Desktop: programmatic download
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = file.name
  a.click()
  URL.revokeObjectURL(url)
}, 'image/png')
```

**Must be called from a direct user gesture** — do not defer with setTimeout or inside an async chain that loses the gesture context.

---

## Section 8: `app/layout.tsx` Updates

- Add Space Grotesk via `next/font/google`, expose as `--font-space-grotesk`
- Update `metadata.title`: `'Chapter Wars by Pavilion'`
- Update `metadata.description`: `'15 cities. 6 archetypes. One winner.'`
- Update `viewport.themeColor`: `'#0a0a0f'`

---

## File Changes Summary

| File | Change |
|---|---|
| `components/ChapterSelect.tsx` | Full redesign → Chapter Wars landing |
| `components/WelcomeScreen.tsx` | Copy + dark mode redesign |
| `components/SurveyQuestion.tsx` | Dark mode, glowing progress bar, pulse animation |
| `components/ArchetypeLoading.tsx` | Dark mode only (bg + text color) |
| `components/ChapterCard.tsx` | Per-archetype palette, social share buttons |
| `components/SocialCardExport.tsx` | **New** — canvas export, single `downloadCard` function |
| `data/questions.json` | Reorder array + update `number` fields (do NOT change `id` fields) |
| `lib/archetypeThemes.ts` | **New** — per-archetype color config keyed by `ArchetypeId` |
| `lib/config.ts` | **New** — competition dates, shared across components |
| `app/layout.tsx` | Space Grotesk font, title, description, themeColor |
| `app/globals.css` | Replace existing `background-color: #180A5C` with `#0a0a0f` |

---

## Out of Scope (V1)

- Live leaderboard (which archetype leads which city) — requires backend aggregation
- Bracket/tournament bracket view — operational lift, future phase
- Landscape / Stories social formats — 1080×1080 square covers both platforms
- Animated card export (video/GIF)
- `CompletionScreen.tsx` — check if it's still in the active flow; if not used, leave untouched

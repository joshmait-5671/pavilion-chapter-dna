'use client'

import { ArchetypeResult } from '@/lib/archetype'
import { ARCHETYPE_THEMES } from '@/lib/archetypeThemes'
import { COMPETITION_LABEL } from '@/lib/config'
import { Chapter } from '@/types'

// Cache font load — only fetch once per session
let fontLoadPromise: Promise<void> | null = null

async function loadCanvasFont(): Promise<void> {
  if (fontLoadPromise) return fontLoadPromise
  fontLoadPromise = (async () => {
    const font = new FontFace(
      'Space Grotesk',
      'url(https://cdn.jsdelivr.net/fontsource/fonts/space-grotesk@latest/latin-700-normal.woff2)',
      { weight: '700', style: 'normal' }
    )
    await font.load()
    document.fonts.add(font)
  })()
  return fontLoadPromise
}

// Helper: draw rounded rectangle path
function roundedRect(
  ctx: CanvasRenderingContext2D,
  x: number, y: number,
  w: number, h: number,
  r: number
) {
  ctx.beginPath()
  ctx.moveTo(x + r, y)
  ctx.lineTo(x + w - r, y)
  ctx.quadraticCurveTo(x + w, y, x + w, y + r)
  ctx.lineTo(x + w, y + h - r)
  ctx.quadraticCurveTo(x + w, y + h, x + w - r, y + h)
  ctx.lineTo(x + r, y + h)
  ctx.quadraticCurveTo(x, y + h, x, y + h - r)
  ctx.lineTo(x, y + r)
  ctx.quadraticCurveTo(x, y, x + r, y)
  ctx.closePath()
}

// Helper: draw a trait pill centered at (cx, cy)
function drawPill(
  ctx: CanvasRenderingContext2D,
  text: string,
  cx: number,
  cy: number,
  accentColor: string
) {
  ctx.font = '600 18px "Space Grotesk", system-ui'
  const tw = ctx.measureText(text).width
  const pw = tw + 40
  const ph = 32
  const px = cx - pw / 2
  const py = cy - ph / 2

  ctx.fillStyle = accentColor
  roundedRect(ctx, px, py, pw, ph, 16)
  ctx.fill()

  ctx.fillStyle = '#0a0a0f'
  ctx.textAlign = 'center'
  ctx.textBaseline = 'middle'
  ctx.fillText(text, cx, cy + 1)
}

// Draw the 1080×1080 card onto ctx
function drawCard(
  ctx: CanvasRenderingContext2D,
  result: ArchetypeResult
) {
  const SIZE = 1080
  const theme = ARCHETYPE_THEMES[result.archetype.id]

  // Background gradient
  const grad = ctx.createLinearGradient(0, 0, 0, SIZE)
  grad.addColorStop(0, theme.gradient[0])
  grad.addColorStop(1, theme.gradient[1])
  ctx.fillStyle = grad
  ctx.fillRect(0, 0, SIZE, SIZE)

  // Subtle radial burst
  const radial = ctx.createRadialGradient(SIZE / 2, SIZE * 0.4, 0, SIZE / 2, SIZE * 0.4, SIZE * 0.5)
  radial.addColorStop(0, 'rgba(255,255,255,0.04)')
  radial.addColorStop(1, 'transparent')
  ctx.fillStyle = radial
  ctx.fillRect(0, 0, SIZE, SIZE)

  // Top-left: "PAVILION CHAPTER WARS"
  ctx.font = '700 26px "Space Grotesk", system-ui'
  ctx.fillStyle = theme.accent
  ctx.textAlign = 'left'
  ctx.textBaseline = 'alphabetic'
  ctx.fillText('PAVILION CHAPTER WARS', 60, 76)

  // Top-right: competition label
  ctx.font = '400 19px "Space Grotesk", system-ui'
  ctx.fillStyle = 'rgba(255,255,255,0.35)'
  ctx.textAlign = 'right'
  ctx.fillText(COMPETITION_LABEL, SIZE - 60, 76)

  // Center: archetype name
  ctx.font = '700 120px "Space Grotesk", system-ui'
  ctx.fillStyle = '#ffffff'
  ctx.textAlign = 'center'
  ctx.textBaseline = 'alphabetic'

  // Reduce font size if name is too wide
  let nameSize = 120
  while (ctx.measureText(result.archetype.name).width > SIZE - 120 && nameSize > 60) {
    nameSize -= 4
    ctx.font = `700 ${nameSize}px "Space Grotesk", system-ui`
  }
  ctx.fillText(result.archetype.name, SIZE / 2, 440)

  // Below: tagline
  ctx.font = 'italic 700 34px "Space Grotesk", system-ui'
  ctx.fillStyle = 'rgba(255,255,255,0.55)'
  ctx.textAlign = 'center'
  ctx.textBaseline = 'alphabetic'
  ctx.fillText(result.archetype.tagline, SIZE / 2, 590)

  // Trait pills — evenly spaced horizontally
  const traits = result.archetype.traits
  const pillY = 900
  const spacing = SIZE / (traits.length + 1)
  traits.forEach((trait, i) => {
    drawPill(ctx, trait, spacing * (i + 1), pillY, theme.accent)
  })

  // Bottom-right: pavilion wordmark
  ctx.font = '400 20px "Space Grotesk", system-ui'
  ctx.fillStyle = 'rgba(255,255,255,0.25)'
  ctx.textAlign = 'right'
  ctx.textBaseline = 'alphabetic'
  ctx.fillText('pavilion', SIZE - 60, SIZE - 40)
}

export async function downloadCard(
  result: ArchetypeResult,
  _chapter: Chapter,  // reserved for future per-city card variants
  _format: 'instagram' | 'linkedin'  // Both use 1080×1080 in V1
): Promise<void> {
  // Load font before drawing
  await loadCanvasFont()

  const SIZE = 1080
  const canvas = document.createElement('canvas')
  canvas.width = SIZE
  canvas.height = SIZE
  const ctx = canvas.getContext('2d')
  if (!ctx) throw new Error('Canvas 2D context unavailable')

  drawCard(ctx, result)

  const filename = `chapter-wars-${result.archetype.id}.png`

  return new Promise((resolve, reject) => {
    canvas.toBlob(blob => {
      if (!blob) { reject(new Error('toBlob failed')); return }

      const file = new File([blob], filename, { type: 'image/png' })

      // Mobile: Web Share API (required on iOS — <a download> is broken there)
      if (navigator.canShare?.({ files: [file] })) {
        navigator.share({ files: [file], title: 'Chapter Wars' })
          .then(resolve).catch(resolve)  // resolve on cancel too
        return
      }

      // Desktop: programmatic download
      const url = URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = filename
      a.click()
      URL.revokeObjectURL(url)
      resolve()
    }, 'image/png')
  })
}

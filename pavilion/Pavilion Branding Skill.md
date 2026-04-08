# Pavilion Branding Skill

Use this skill whenever creating or designing any Pavilion-branded output: HTML emails, landing pages, dashboards, slides, reports, or print materials.

## Color System

### Core Brand Colors

| Name | Hex | Role |
|------|-----|------|
| Pink 700 | `#DF285B` | Primary — CTAs, key accents |
| Blue 700 | `#180A5C` | Dark backgrounds, authority |
| Purple 700 | `#59146C` | Accent sections |
| White | `#FFFFFF` | Primary background (default) |

### Approved Background Colors

| Swatch | Hex | Notes |
|--------|-----|-------|
| Pink 100 | `#FEF9F9` | Subtle warm tint |
| Pink 200 | `#FFEDF2` | Soft section break |
| Pink 700 | `#DF285B` | Bold hero/CTA section |
| Blue 600 | `#2B1887` | Rich navy card/section |
| Blue 700 | `#180A5C` | Deepest navy |
| Purple 600 | `#7F2A97` | Accent/community section |
| Purple 700 | `#59146C` | Deep purple hero |

White is the **primary background** — use colored backgrounds sparingly for section breaks or emphasis.

### Typographic Color Pairings

| Background | Headline | Body |
|------------|----------|------|
| White / Pink 100 / Pink 200 | Blue 600 `#2B1887` | Gray 700 `#404040` |
| Pink 700 | White `#FFFFFF` | White `#FFFFFF` |
| Blue 600 | White `#FFFFFF` (+ Pink 400 `#C57FD9` accent) | White `#FFFFFF` |
| Blue 700 | White `#FFFFFF` (+ Pink 400 `#C57FD9` accent) | White `#FFFFFF` |
| Purple 600 | White `#FFFFFF` (+ Pink 400 `#C57FD9` accent) | White `#FFFFFF` |
| Purple 700 | White `#FFFFFF` (+ Pink 400 `#C57FD9` accent) | White `#FFFFFF` |

### Full Palette (for hover states, gradients, tints)

**Brand Pink:**
`#FEF9F9` (100) → `#FFEDF2` (200) → `#FFDDD`(300) → `#FE818F` (400) → `#FF7F8F` (500) → `#F13472` (600) → `#DF285B` (700) → `#B81C48` (800) → `#920E32` (900)

**Brand Blue:**
`#EDEAFF` (100) → `#CEC5F4` (200) → `#9998BF` (300) → `#6D69CF` (400) → `#432CAE` (500) → `#2B1887` (600) → `#180A5C` (700) → `#0D0039` (800) → `#080122` (900)

**Brand Purple:**
`#FDF5FF` (100) → `#F4E0FA` (200) → `#DEB0EB` (300) → `#C57FD9` (400) → `#A34CBB` (500) → `#7F2A97` (600) → `#59146C` (700) → `#3E044F` (800) → `#250030` (900)

**Gray:**
`#F5F5F5` (100) → `#EFEFEF` (200) → `#CCCCCC` (300) → `#A3A3A3` (400) → `#717171` (500) → `#525252` (600) → `#404040` (700) → `#262626` (800) → `#1A1A25` (900)

### Duotone Image Pairings

Primary: **Pink 700 + Blue 600** (event photography, hero images)

Secondary pairings:
- Pink 500 + Blue 600
- Pink 400 + Blue 100
- Pink 400 + Purple 700
- Pink 700 + Purple 600

---

## Typography

Single typeface system — hierarchy via weight, size, and color only.

- **Web font**: Poppins (Google Fonts) — `@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap')`
- **Email/print fallback**: Arial, sans-serif
- **CSS font-family**: `'Poppins', Arial, sans-serif`

### Type Scale

| Class | Size | Line Height | Letter Spacing | Use |
|-------|------|-------------|----------------|-----|
| `body-s` | 14px | 20px | 0 | Captions, tight spaces |
| `body-m` | 16px | 24px | 0 | Default body / email body |
| `body-l` | 20px | 28px | 0 | Pairs with XXL+ headlines |
| `headline-xxs` | 18px | 20px | 0.25px | Mobile, small labels |
| `headline-xs` | 20px | 24px | 0.25px | Small headlines |
| `headline-s` | 24px | 32px | 0.375px | h3 |
| `headline-m` | 32px | 40px | 0.5px | h2 secondary |
| `headline-l` | 40px | 48px | 0.75px | h2 primary |
| `headline-xl` | 48px | 56px | 0.75px | Section titles |
| `headline-xxl` | 72px | 74px | 0.75px | Key hero headlines |
| `headline-xxxl` | 96px | 100px | 0.75px | Top-level page headline |
| `headline-xxxxl` | 120px | 136px | 0.75px | Most important message only |

Font weight for headlines: **700 (Bold)**. Body: **400 (Regular)**. Sub-labels/captions: **600 (SemiBold)** acceptable.

---

## HTML Email Template

Pavilion sends HTML emails via HubSpot. When producing HTML email content, follow this structure and style. Email client safe: table-based layout, inline styles, Arial fallback.

### Key Email Styles

```css
/* Email-safe inline style values */
font-family: Arial, sans-serif;
font-size: 15px;
color: #23496D;           /* Pavilion dark blue — body text in email */
line-height: 175%;
background-color: #ffffff;
```

### Email Shell Structure

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body bgcolor="#ffffff" style="font-family:Arial,sans-serif;font-size:15px;
      color:#23496D;margin:0;padding:0;">
  <table role="presentation" cellpadding="0" cellspacing="0"
         style="width:100%;max-width:600px;margin:0 auto;">
    <tbody>
      <tr>
        <td style="padding:24px 24px 8px;">
          <!-- BODY CONTENT: paragraphs and bullet lists -->
          <p style="line-height:175%;font-family:Arial,sans-serif">Hi [First Name],</p>
          <p style="line-height:175%;font-family:Arial,sans-serif">
            <!-- invitation copy here -->
          </p>
        </td>
      </tr>
      <tr>
        <td style="padding:8px 24px 24px;font-size:12px;color:#23496D;">
          <!-- FOOTER -->
          <p style="font-size:12px;">
            Sent with ♥️ by Pavilion, 302A West 12th Street, #254, New York, NY 10014, USA
          </p>
          <p>
            <a href="[UNSUBSCRIBE_URL]"
               style="font-size:12px;color:#00A4BD;text-decoration:underline;">Unsubscribe</a>
            &nbsp;|&nbsp;
            <a href="[PREFERENCES_URL]"
               style="font-size:12px;color:#00A4BD;text-decoration:underline;">Manage preferences</a>
          </p>
        </td>
      </tr>
    </tbody>
  </table>
</body>
</html>
```

### Real Example (Operator Dinner Invite)

The following is a real Pavilion invitation email body (decoded from the HubSpot template):

```
Hi [First Name],

We're finalizing guest lists for the upcoming [City] dates, and I'm following
up to see if one of them might work for you:

  • [Date 1]
  • [Date 2]
  • [Date 3]

If you're interested, just reply with the date that works best and any dietary
restrictions, and I'll be happy to save you a seat.

Best,
Ben McCormick
```

Key structural notes:
- Greeting uses first name only ("Hi Caitlin,")
- Bullets for multiple dates — concise, scannable
- Single CTA: reply to this email (no button needed)
- Sign-off: "Best, Ben McCormick" (first contact) or "Best, Ben" (follow-up)

---

## Voice & Tone

See full messaging guidelines, ICP detail, writing examples, and anti-patterns in the **Pavilion Messaging Brief**: `/Users/joshmait/.claude/projects/-Users-joshmait-Desktop-Claude/memory/pavilion-messaging-brief.md`

### Quick Reference

- **Pavilion is**: a professional operator network. Never a "community," "platform," or "course library."
- **Most important positioning word**: "backup" — *the backup your board will never give you*
- **Dinners are always called**: "Operator Dinners" — never "events" or just "dinners"
- **Tone**: Direct, pressure-aware, peer-to-peer, specific, credible without bragging
- **Emails**: Under 150 words. First name greeting. Reply-based RSVP. PS lines mandatory.
- **Value prop language**: "8,000+ operators", "under 1 hour response", "operator-led learning", "give to get"
- **Scarcity**: "Seats tend to fill quickly" / "We have few of these each year in [city]"
- **Never use**: unlock, empower, transform, synergy, community, platform, next-level, world-class, game-changing, supercharge, cutting-edge, leverage (as a verb)
- No corporate jargon. No walls of text. No emojis (unless approved).

---

## Web/HTML Application

When building web interfaces with Pavilion branding, apply as CSS variables:

```css
:root {
  /* Core */
  --pav-pink: #DF285B;
  --pav-blue: #180A5C;
  --pav-purple: #59146C;
  --pav-white: #FFFFFF;

  /* Backgrounds */
  --pav-pink-100: #FEF9F9;
  --pav-pink-200: #FFEDF2;
  --pav-blue-600: #2B1887;
  --pav-blue-800: #0D0039;
  --pav-purple-600: #7F2A97;
  --pav-card-light: #F9F8FF;

  /* Text */
  --pav-body: #404040;
  --pav-headline-light: #2B1887;
  --pav-headline-dark: #1E1E1E;
  --pav-body-dark: #404040;
  --pav-pink-400: #C57FD9;

  /* Typography */
  --pav-font: 'Poppins', Arial, sans-serif;

  /* Layout */
  --pav-container-max: 1680px;
  --pav-container-padding: 40px;
  --pav-section-gap: 2rem;
  --pav-radius: 12px;
  --pav-radius-lg: 16px;
}
```

Import Poppins at the top of your `<head>`:
```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
```

---

## Web Page Design System

Reference: [joinpavilion.com/ai-in-gtm](https://www.joinpavilion.com/ai-in-gtm) — the gold standard for Pavilion page design. All landing pages, program pages, and marketing pages should follow this design language.

### Page Layout Principles

1. **Container**: Max-width 1680px, centered, 40px horizontal padding
2. **Section rhythm**: Alternate between light backgrounds (white, `#F9F8FF`, Pink 100) and dark backgrounds (Blue 700, Blue 600) to create visual breathing room
3. **Whitespace is generous**: Sections have significant vertical padding. Content never feels cramped.
4. **Content is left-aligned by default**: Headlines, body, CTAs all left-aligned. Center-alignment used only for single stat callouts or logo bars.

### Section Catalog

Build pages by assembling these section types. Every Pavilion page should use at least the Hero, a Feature section, Social Proof, and a CTA section.

---

#### 1. Hero Section (Dark)

The hero sets the tone for the entire page. Always dark background.

- **Background**: Dark image with overlay OR solid Blue 700 / Blue 800
- **Text**: White. Headline is `headline-xxl` or `headline-xxxl` (72–96px). Body is `body-l` (20px).
- **CTA placement**: Two buttons side by side — primary (Pink 700 fill) + secondary (outline or white fill)
- **Structure**: Text left-aligned in left 60% of the viewport. Right side can be empty (the dark background does the work) or contain a subtle image.
- **Headline rule**: Short. Tension-first. Under 8 words. Example: "Stop figuring out AI alone."
- **No background gradients**: Solid dark or dark image. Keep it clean.

```css
.hero {
  background-color: var(--pav-blue);
  color: white;
  padding: 120px var(--pav-container-padding) 80px;
  max-width: var(--pav-container-max);
  margin: 0 auto;
}
.hero h1 {
  font-size: 72px;
  line-height: 74px;
  font-weight: 700;
  letter-spacing: 0.75px;
  margin-bottom: 24px;
}
.hero p {
  font-size: 20px;
  line-height: 28px;
  max-width: 600px;
  opacity: 0.9;
}
```

---

#### 2. Logo Trust Bar

Immediately below the hero. Shows enterprise credibility.

- **Background**: Same dark as hero (seamless transition) OR white
- **Layout**: Horizontal scrolling row of company logos. White logos on dark, gray logos on light.
- **Logos**: Display at consistent height (~30px). Repeat the logo set for seamless scroll on mobile.
- **Label**: Optional small uppercase label above: "TRUSTED BY OPERATORS AT"
- **Count**: Show 10–14 recognizable logos (Shopify, Salesforce, Microsoft, IBM, Stripe, etc.)

---

#### 3. Founder Quote / Personal Message

A pattern unique to Pavilion — breaks the "marketing page" feel and makes it human.

- **Background**: Dark (Blue 700) or white
- **Layout**: Single-column, narrow width (~700px max), centered
- **Typography**: Body text in italic. Attribution in bold, non-italic.
- **Purpose**: Establishes authenticity. The founder (or a senior leader) speaks directly to the reader. Conversational, not polished.

---

#### 4. Feature Grid (Icon + Text Cards)

The workhorse section for explaining what's included.

- **Layout**: 2-column grid, `gap: 2rem`
- **Card background**: `#F9F8FF` (very light purple) on light pages, semi-transparent blue on dark pages
- **Card border-radius**: 12px
- **Card padding**: 32–45px
- **Card structure**: Icon (30x30, Blue 600 or white fill) → Headline (`headline-s`, 24px bold) → Body text (`body-m`, 16px regular)
- **Last card**: Spans full width (`grid-column: 1 / -1`) — use this for the most important or differentiating feature
- **Border**: Optional 1px solid Blue 500 on dark-background cards

```css
.feature-grid {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 2rem;
}
.feature-card {
  background: #F9F8FF;
  border-radius: 12px;
  padding: 40px;
}
.feature-card:last-child {
  grid-column: 1 / -1;
}
.feature-card .icon {
  width: 30px;
  height: 30px;
  fill: var(--pav-blue-600);
  margin-bottom: 16px;
}
.feature-card h3 {
  font-size: 24px;
  font-weight: 700;
  line-height: 32px;
  color: var(--pav-headline-dark);
  margin-bottom: 12px;
}
.feature-card p {
  font-size: 16px;
  line-height: 24px;
  color: var(--pav-body);
}
```

**Responsive**: Collapses to single column below 768px.

---

#### 5. Two-Column Content (60/40 Split)

Used for curriculum details, program overviews, or detailed feature explanations.

- **Layout**: 60% text column (left) + 40% detail card (right)
- **Left column**: Headline (`headline-l`, 40px) + body copy + optional bullet list
- **Right column**: Card with distinct background — semi-transparent blue (`rgba(13, 0, 57, 0.25)`) with 1px solid Blue 500 border, 12px border-radius, 45px padding
- **Right card content**: Program details (dates, duration, format, requirements) displayed as label/value pairs
- **Responsive**: Stacks vertically below 768px, right card goes full-width

```css
.two-col {
  display: flex;
  gap: 3rem;
  align-items: flex-start;
}
.two-col__content {
  flex: 3;
}
.two-col__sidebar {
  flex: 2;
  background: rgba(13, 0, 57, 0.25);
  border: 1px solid #432CAE;
  border-radius: 12px;
  padding: 45px;
}
```

---

#### 6. Stats Bar / Proof Points

Display 2–4 key metrics in a horizontal row. High visual impact.

- **Layout**: Flex row, evenly spaced, centered
- **Stat number**: `headline-xl` (48px) or `headline-xxl` (72px), bold, Pink 700 or White (on dark)
- **Stat label**: `body-s` (14px) or `body-m` (16px), Gray 700 or White
- **Background**: White with subtle Pink 100 tint, or inline within a dark section
- **Examples**: "70%" / "of members are VP+", "<1hr" / "average Slack response", "2,000+" / "Slack messages per week"
- **Border treatment**: Optional bottom border on each stat using Pink 400

```css
.stats-bar {
  display: flex;
  justify-content: space-around;
  padding: 60px var(--pav-container-padding);
  text-align: center;
}
.stat-item .number {
  font-size: 48px;
  font-weight: 700;
  color: var(--pav-pink);
  line-height: 56px;
}
.stat-item .label {
  font-size: 14px;
  color: var(--pav-body);
  margin-top: 8px;
}
```

---

#### 7. Testimonial Section

Member quotes displayed as cards. Critical for credibility.

- **Layout**: Horizontal scroll/carousel or 2–3 column grid
- **Card background**: White (on light sections) or `#F9F8FF`
- **Card border-radius**: 12px
- **Card structure**: Photo (circular, ~80px) → Quote text (italic, `body-m`) → Name (bold) + Title/Company (regular, `body-s`)
- **Quote style**: Real quotes from real members. Include first name, last name, title, company. Never anonymous.
- **No quotation mark icons**: The italic formatting signals it's a quote. Keep it clean.

```css
.testimonial-card {
  background: white;
  border-radius: 12px;
  padding: 32px;
}
.testimonial-card img {
  width: 80px;
  height: 80px;
  border-radius: 50%;
  object-fit: cover;
  margin-bottom: 16px;
}
.testimonial-card blockquote {
  font-style: italic;
  font-size: 16px;
  line-height: 24px;
  color: var(--pav-body);
  margin-bottom: 16px;
}
.testimonial-card .attribution {
  font-size: 14px;
}
.testimonial-card .attribution strong {
  display: block;
  color: var(--pav-headline-dark);
}
```

---

#### 8. Values / Principles List

A single-column list of cultural or philosophical points. Adds depth.

- **Layout**: Single column, max-width ~800px, centered
- **Structure per item**: Icon (optional, 24px) + Title (`headline-xs`, 20px bold) + Description (`body-m`, 16px regular)
- **Spacing**: `1.5rem` between items
- **Background**: White or Pink 100
- **Use for**: Pavilion values (Be open and honest, Be direct, Be a good listener, Be reasonable with your time, Be vulnerable)

---

#### 9. CTA Section (Final)

Every page ends with a strong call to action.

- **Background**: Blue 700 or Pink 700 — always bold, always dark
- **Text**: White. Headline is `headline-l` or `headline-xl` (40–48px).
- **CTA copy**: Action-oriented, specific. "Get me in the room" not "Learn more." "Talk with our Team" not "Contact us."
- **Button**: Pink 700 fill on dark blue background, or White fill on pink background
- **Qualification line**: Small text below the button identifying who this is for: "For VP and C-suite GTM leaders"

---

### Button System

All buttons use `text-transform: none` (never uppercase). Rounded corners.

| Variant | Background | Text | Border | Hover |
|---------|-----------|------|--------|-------|
| **Primary** | Pink 700 `#DF285B` | White | None | Blue 800 `#0D0039` bg, white text, 1px white border |
| **Secondary** | Transparent | White or Blue 600 | 1px solid current color | Blue 800 bg, white text |
| **White fill** | White | Blue 600 `#2B1887` | None | Blue 800 bg, white text, 1px white border |
| **Small** | Same as above | Same | Same | Same — just reduced padding |

```css
.cta-btn {
  display: inline-block;
  font-family: var(--pav-font);
  font-size: 16px;
  font-weight: 600;
  padding: 14px 32px;
  border-radius: 8px;
  text-decoration: none;
  text-transform: none;
  cursor: pointer;
  transition: all 0.2s ease;
}
.cta-btn--primary {
  background: var(--pav-pink);
  color: white;
  border: 1px solid transparent;
}
.cta-btn--primary:hover {
  background: var(--pav-blue-800, #0D0039);
  border-color: white;
}
.cta-btn--secondary {
  background: transparent;
  color: white;
  border: 1px solid white;
}
.cta-btn--secondary:hover {
  background: var(--pav-blue-800, #0D0039);
}
.cta-btn--white-fill {
  background: white;
  color: var(--pav-blue-600);
  border: 1px solid transparent;
}
.cta-btn--white-fill:hover {
  background: var(--pav-blue-800, #0D0039);
  color: white;
  border-color: white;
}
.cta-btn--small {
  font-size: 14px;
  padding: 10px 24px;
}
```

### Icon System

- Use **Material Symbols Rounded** (Google) for all icons
- Icon size: 30x30px in feature cards, 24x24px inline
- Icon color: Blue 600 `#2B1887` on light backgrounds, White on dark backgrounds
- Icons are decorative — always paired with text. Never icon-only.

```html
<link href="https://fonts.googleapis.com/css2?family=Material+Symbols+Rounded:opsz,wght,FILL,GRAD@24,400,1,0" rel="stylesheet">
```

```css
.material-symbols-rounded {
  font-size: 30px;
  color: var(--pav-blue-600);
}
```

### Responsive Breakpoints

| Breakpoint | Target | Key changes |
|------------|--------|-------------|
| `> 993px` | Desktop | Full layout — 2-column grids, 60/40 splits, side-by-side CTAs |
| `769–993px` | Tablet | Grids stay 2-column, 60/40 stacks, padding reduces |
| `569–768px` | Small tablet | Grids collapse to 1-column, images go full-width |
| `< 568px` | Mobile | Everything single column, hero headline drops to `headline-l` (40px), images 100% width, buttons stack vertically |

### Page Template (Recommended Section Order)

A typical Pavilion landing/program page follows this flow:

```
1. Hero (dark)                     — Blue 700 / dark image
2. Logo Trust Bar                  — same dark bg or white
3. Founder Quote / Personal Hook   — dark or white
4. Feature Grid (what's included)  — white / #F9F8FF cards
5. Two-Column (curriculum detail)  — white with blue sidebar card
6. Stats Bar                       — white or Pink 100
7. Testimonials                    — white or #F9F8FF
8. Values / Principles (optional)  — white
9. CTA Section (final)             — Blue 700 or Pink 700
10. Footer                         — Black bg, white text
```

**Rules:**
- Never stack two dark sections back to back
- Never stack two sections with the same background color
- The page should "breathe" — alternate light/dark, dense/sparse
- Every scroll-stop should have one clear thing to read or click
- Stats are always real, always specific (see Messaging Brief for approved numbers)

### Footer

- **Background**: Black `#000000`
- **Text**: White, `body-s` (14px)
- **Links**: White, hover → Pink 700
- **Structure**: Multi-column navigation (Membership, Why Pavilion, Insights, Who We Are)
- **Social icons**: LinkedIn, Instagram, Facebook — left-aligned
- **Bottom bar**: Copyright + legal links (Terms, Privacy, Code of Conduct)

### Design Anti-Patterns (Never Do These)

- **No gradients on backgrounds** — use solid colors or images with overlays
- **No drop shadows on cards** — use background color contrast instead
- **No rounded-pill buttons** — use 8px border-radius, not 50px
- **No stock photography** — use event photos with duotone treatment or abstract/dark backgrounds
- **No centered body text** — center-align only stat numbers, logos, or single-line CTAs
- **No thin/light font weights** — Poppins 400 minimum. Never 100, 200, or 300.
- **No icon-only navigation** — always pair icons with text labels
- **No animations/transitions on page load** — only on hover states and button interactions
- **No more than 2 CTAs per section** — one primary, one secondary max

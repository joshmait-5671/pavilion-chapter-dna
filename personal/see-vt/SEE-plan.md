# SEE — Plan

## Context

Josh wants to create a premium digital publication for the state of Vermont — but Vermont is just the first edition. **SEE is the platform. VT is the first state.** The brand, design system, voice, and structure must be state-agnostic so it scales to SEE NH, SEE ME, SEE CO, SEE MT, etc.

Not a newsletter. Not Morning Brew. Something you sit with. Highbrow but accessible — that contradiction is the answer.

Primary audience: out-of-state second-home owners, state diaspora, and people who love a place from afar. Secondary: in-state residents. This audience model scales perfectly — every state has these people.

---

## Phase 1: Brand Foundation

### The SEE Brand (State-Agnostic)
- **SEE** is the parent brand. Clean, modern, editorial. Works everywhere.
- **SEE VT** is the first edition. Vermont content lives *inside* the SEE frame.
- The logo, typography, color system, section structure — none of it should feel Vermont-specific. It should feel like a premium publication platform that happens to be featuring Vermont right now.
- Think: HBO is the brand. The show is Vermont.

### Visual Identity (The Frame)
- Design a visual identity for **SEE** — not SEE VT
- Reference aesthetic: Kinfolk's restraint meets Monocle's editorial authority. Clean, sharp, timeless.
- Color direction: neutral foundation (black, white, warm cream) with a single accent color that can shift per state edition
- Typography: serif for headlines (authority, editorial weight), clean sans-serif for body
- The "VT" in SEE VT could be a different weight, color, or treatment — signaling it's the variable, not the constant

### Voice
- Cool. Grounded. Earned knowledge. Not trying to sell you on Vermont — assumes you already get it.
- First person plural ("we") when appropriate, but mostly lets the content speak
- Avoids: tourism-speak, Chamber of Commerce language, "hidden gems," "best kept secrets"
- Embraces: specificity, craft language, quiet confidence, occasional dry humor

### Platform: Ghost
- Maximum design control for premium visual identity
- 0% revenue share on paid subscriptions (Stripe fees only)
- Custom website + newsletter in one platform
- Self-hostable for long-term control
- Themes can be fully customized (HTML/CSS/JS)

### Delivery
- **Start: Sunday evening** — arrives like a gift before the week. You read it with wine, not coffee. It's a ritual, not a task.
- A/B test against Saturday morning after 8-12 weeks
- This is not a daily or even weekly-daily publication. One issue per week, substantial, worth the wait.

---

## Phase 2: Content Architecture

Each issue has a consistent structure. Readers know what to expect but are always surprised by the specifics.

### Sections (working names — refine in build)

**1. The View** — Opening image + short editorial
- One stunning Vermont photograph or illustration
- 2-3 sentences. Sets the tone. Seasonal, observational, grounding.
- Think: the feeling of looking out a window at the Green Mountains

**2. On Tap** — Beer & brewery section
- New releases, taproom events, brewery profiles, festival previews
- Data sources: Vermont Brewers Association events calendar, brewery social feeds, direct relationships
- 56 breweries in state = endless content pipeline
- Rotate between: new release spotlight, brewer profile, event preview, seasonal guide

**3. The Market** — Farmer's markets & local food
- What's in season, market highlights, farmer profiles, recipes
- Data sources: NOFA-VT directory, Vermont Agency of Agriculture pricing reports, Vermont Fresh Network
- Seasonal (May-Oct heavy, winter markets Nov-Mar)
- Could include: "What to buy this week" — one item, why it matters, what to do with it

**4. Good News** — Vermont economic development (2-3 items)
- Small business openings, expansions, investments, job growth
- Data sources: VEDA press releases, Vermont Business Magazine, Vermont Chamber, VTDigger
- Short, punchy items. No analysis paralysis. Just: here's something good happening.
- Keeps the publication grounded in Vermont's real economy, not just lifestyle

**5. The Calendar** — Cultural events & happenings
- Curated picks (not a comprehensive listing — that's what Seven Days is for)
- 3-5 events worth knowing about this week
- Music, art, film, food, outdoor, community
- Data sources: Vermont Tourism events, Burlington Discover Jazz, VTIFF, Flynn Theater, local venues

**6. The Scoreboard** — Sports
- UVM Catamounts (D1), Middlebury Panthers (D3), high school highlights
- Keep it tight: scores, standout performances, what to watch next week
- Data sources: uvmathletics.com, athletics.middlebury.edu, MaxPreps VT, VPA

**7. Last Word** — Closing wisdom
- A quote, a line, a thought that captures the Vermont ethos
- Could be: historical figure, local voice, seasonal observation, literary reference
- John Dewey, Robert Frost, Calvin Coolidge, Scott Nearing, anonymous farmer at the Stowe market
- This is the signature. The thing people screenshot and share.

---

## Phase 3: Data Sources & Content Engine

### Public Data (Free)
- Vermont Agency of Agriculture — market pricing, farm directories, seasonal data
- Vermont Department of Labor (vtlmi.info) — economic indicators, wage data, employment
- ACCD Tourism Research — visitor stats, economic impact
- Vermont Open Data Portal (data.vermont.gov) — various state datasets
- NOFA-VT — farmer's market directory (searchable by county, day, EBT)
- UVM Athletics / Middlebury Athletics / MaxPreps — sports schedules & scores
- Vermont Brewers Association — 56 brewery directory, events calendar
- Vermont Tourism events calendar

### Private/Paid Data (Explore later)
- Vermont Business Magazine premium content
- VTDigger membership (investigative/economic reporting)
- Direct brewery relationships (exclusive release info, early access)
- Vermont Fresh Network membership (farm-to-table database)

### Content Tools
- **Ghost** — publishing platform + website + email
- **Figma or Canva Pro** — visual design, templates, illustrations
- **Unsplash / local photographers** — imagery (eventually commission original photography)
- **Claude** — content drafting, data synthesis, economic summaries
- **Instagram** — brand presence, visual identity, audience growth
- **NotebookLM** — potential audio companion (podcast-style deep dives on specific stories)

---

## Phase 4: Visual & Design System

### Photography Style
- Natural light. Real places. No stock.
- Landscape, craft, food, people at work — not posed
- Seasonal palette shifts (green/gold in summer, white/blue in winter, amber/red in fall)
- Commission 2-3 Vermont-based photographers for original work (long-term)

### Illustration
- Consider hand-drawn spot illustrations for recurring sections (a beer glass for On Tap, a basket for The Market, etc.)
- Gives warmth and personality that photography alone can't
- Reference: Kinfolk's use of illustration alongside photography

### Email Design
- Ghost's custom theme system allows full HTML/CSS control
- Design a custom email template that matches the website aesthetic
- Generous whitespace. Editorial layout. Not a "newsletter" — a publication in your inbox.
- Mobile-first (most opens will be mobile)

---

## Phase 5: Instagram Strategy

### Handle: @seevt
- Check availability (likely available or negotiable)

### Visual Identity
- Same palette and typography as the publication
- Photography-forward feed
- Mix: landscape (Vermont beauty), close-ups (craft/food/beer), people (community), text cards (quotes/wisdom)

### Cadence
- 3-4 posts/week to start
- Daily Stories during peak content (events, market season, ski season)
- Reels for discovery (brewery visits, market walks, seasonal beauty)

### Growth Strategy
- Tag every Vermont business, brewery, market, venue featured
- Use location tags aggressively (Vermont Explore page)
- Cross-promote with local accounts
- Feature reader/follower photos (UGC builds community)
- Link in bio → Ghost signup page

---

## Phase 6: Monetization Path

### Year 1: Build the Audience (Months 1-12)
- Free publication to build subscriber base
- Target: 3,000 email subscribers, 2,000 Instagram followers
- Revenue: minimal (maybe 1-2 small local sponsors at $250-500/placement)
- Focus: quality, consistency, voice, visual identity

### Year 2: Introduce Revenue (Months 13-24)
- Launch paid tier on Ghost (exclusive content, early access, community)
- Native advertising: $500-$1,500 per placement (target: breweries, real estate, outdoor brands, restaurants, resorts)
- Farmer's market presence: branded tent/table at 5-10 top markets (spring/summer)
- Target: 5,000 email subscribers, 500 paid subscribers, 5,000 Instagram followers

### Year 3+: Scale
- Premium sponsorship packages: $1,500-$3,000 per placement
- Events: curated experiences (brewery tours, farm dinners, cultural events)
- Physical products: annual print edition, Vermont calendar, curated gift boxes
- Target: 10,000+ email subscribers, 1,000+ paid subscribers

### Advertiser Targets
- Vermont breweries & distilleries
- Ski resorts (Stowe, Killington, Sugarbush)
- Real estate (second-home market)
- Fine dining & hospitality
- Outdoor recreation brands
- Vermont artisan goods
- Tourism boards
- UVM / Middlebury (alumni engagement)

---

## Phase 7: Farmer's Market Presence

### Top Markets to Target (Spring/Summer)
1. Burlington Farmers Market (Saturdays, May-Oct)
2. Stowe Farmers Market
3. Montpelier Farmers Market
4. Middlebury Farmers Market
5. Brattleboro Farmers Market
6. Woodstock Farmers Market
7. Manchester Farmers Market
8. Shelburne Farmers Market
9. Waterbury Farmers Market
10. Rutland Farmers Market

### Presence Model
- Branded table/tent with SEE VT visual identity
- QR code to subscribe (free)
- Print copies of the latest issue (collector's value)
- "Last Word" quote cards (people take them home — organic brand building)
- Local product recommendations (cross-promote with market vendors)

---

## Build Steps (What Claude Actually Builds)

### Step 1: Ghost Setup
- Set up Ghost instance (Ghost Pro or self-hosted)
- Custom theme design matching SEE VT brand identity
- Configure email templates for the publication
- Set up subscription tiers (free to start, paid tier structure ready)

### Step 2: Brand Assets
- Logo design (SEE VT wordmark)
- Color palette and typography system
- Section icons/illustrations
- Email template design
- Instagram templates

### Step 3: Website
- Ghost-powered website at seevt.com (or similar domain — check availability)
- Homepage: brand statement, latest issue, subscribe CTA
- Archive: past issues browsable
- About: the story, the people, the mission

### Step 4: First Issue
- Design and write Issue #1 as a proof of concept
- All 7 sections populated with real Vermont content
- Full visual treatment — this is the pitch deck for the brand

### Step 5: Instagram Launch
- Set up @seevt account
- Create first 9 posts (grid aesthetic)
- Bio with subscribe link
- First batch of Stories

---

## Competitive Positioning

| | Seven Days | 6AM City | Morning Brew | SEE VT |
|---|---|---|---|---|
| Audience | In-state | Local professionals | National biz | VT lovers everywhere |
| Voice | Journalistic | Upbeat/efficient | Bro-casual | Grounded/elevated |
| Design | Newspaper | Template | Template | Editorial/premium |
| Cadence | Weekly | Daily | Daily | Weekly (Sunday) |
| Revenue | Ads | Ads + affiliate | Ads + sponsorship | Subs + native ads + events |
| Vibe | Read it | Skim it | Skim it | Sit with it |

---

## The Scale Play

SEE is designed to be a franchise from day one. Every design decision, section name, and structural choice must pass the test: "Does this work in Vermont AND Montana AND Maine?"

- **SEE** = the brand, the platform, the design system, the voice
- **VT** = the first edition, the content, the local relationships, the proof of concept
- Section names (On Tap, The Market, The Calendar, Good News, The Scoreboard, Last Word) are intentionally universal
- The Ghost theme/template is built once, content swaps per state
- Instagram: @seevt is the first account. @seenh, @seeme, @seeco follow.
- Revenue model replicates: every state has breweries, farmer's markets, sports, cultural events, economic news, and wisdom

### Expansion Criteria (When to Launch State #2)
- SEE VT hits 5,000+ email subscribers
- Revenue model proven (sponsors + paid subs covering costs)
- Content engine systematized (templates, data sources, contributor network)
- Pick State #2 based on: second-home owner density, craft culture, tourism spend, diaspora size (Maine, New Hampshire, Colorado, Montana are obvious candidates)

---

## What SEE Is Not
- Not a news publication (that's Seven Days / VTDigger)
- Not a tourism guide (that's the state tourism board)
- Not a daily briefing (that's 6AM City / Morning Brew)
- Not a beer blog (that's Untappd)
- Not an events calendar (that's Front Porch Forum)

## What SEE Is
A weekly publication that makes you feel something about a place. Whether you live there, used to live there, or wish you did. Vermont is first. It won't be last.

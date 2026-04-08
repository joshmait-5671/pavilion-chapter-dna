# Session 3 — March 19, 2026

## New Brainstorm Items Added

### 1. Three-Tier Question Routing (detailed)
- **Tier A — Bot answers autonomously:**
  - Routine weather questions with clear answers ("What's the weather tomorrow?", "Rain this weekend?")
  - Questions where weather models are in strong agreement
  - Anything the corpus has strong precedent for (Lloyd has answered similar questions many times)
  - Low-stakes decisions ("Do I need an umbrella today?")

- **Tier B — Bot drafts, Lloyd approves:**
  - High-stakes planning questions ("Should we cancel the outdoor birthday party Saturday?")
  - When models meaningfully disagree on the outcome
  - Multi-day forecasts where confidence drops (4+ days out)
  - Beach/ski weekend trip decisions involving travel

- **Tier C — Lloyd answers directly:**
  - Major storm events (nor'easters, blizzards, hurricanes)
  - When a user explicitly asks to hear from Lloyd himself
  - Anything the bot flags as low-confidence
  - Easter egg territory (theme parks, strip clubs)

- **Routing logic:** A confidence score based on model agreement + question stakes + time horizon. Short-range + routine + models agree = Tier A. Longer-range + high stakes + model disagreement = escalates to B or C.

- **Lloyd's experience:**
  - Dashboard shows a queue: Tier B items have the bot's draft answer ready for him to approve/edit/reject. Tier C items are blank, waiting for his input.
  - Push notification (SMS) when a Tier B or C question arrives. He can approve a Tier B draft right from the text.
  - If Lloyd doesn't respond within a time window (say 2 hours), Tier B auto-sends with a "Lloyd's best guess" disclaimer. Tier C tells the user Lloyd will get back to them.

### 2. Meteorologist Framework Research
- 10 dimensions completed and saved to meteorologist-framework.md
- Purpose: map Lloyd's specific tendencies against a professional framework before analyzing his data
- Will use to identify Lloyd's voice AND his forecasting patterns

### 3. Lloyd Avatar/Character
- Photo received: Lloyd in snowflake jacket, glasses on head, big smile, approachable energy
- Will create stylized avatar/character for branding

## Vision Restated (for context preservation)
"Only Lloyd Knows" is a subscription weather service for people in the NYC tri-state suburbs. For $6/month, you text or chat a question like "is my kid's soccer game getting rained out Saturday?" and you get an answer back from Lloyd — not a generic weather bot, but something that sounds exactly like your friend Lloyd who lives and breathes this stuff. His excitement when a nor'easter is coming. His specific way of referencing models. His humor. The reason it works is that Lloyd is genuinely obsessed with weather and people who know him already trust his calls — we're just scaling that to strangers who want the same thing.

Under the hood, we're feeding Claude with Lloyd's years of emails, his Twitter commentary, and his WhatsApp messages to nail his voice. We're pulling real-time weather data so the forecasts are accurate. And we have a routing system so Lloyd himself stays in the loop on the calls that matter — big storms, high-stakes questions — while the bot handles the routine stuff autonomously.

The website is the storefront — fun, on-brand, Lloyd's personality front and center. Sign up, pay, start asking.

## Key Details Captured
- **Lloyd's full name:** Lloyd Mallah
- **Lloyd's email:** lloydm5678@icloud.com
- **Lloyd's Twitter:** @lloydm1234
- **Target customer:** Affluent suburban parents (35-50), young kids to early teens, tri-state area, may have beach/ski homes
- **Lloyd's buy-in level:** Intrigued but skeptical — needs to see it to believe it
- **Lloyd's existing audience:** 500+ email list, Twitter followers
- **Goal:** Build the FULL product (not a demo) so Lloyd sees it and commits
- **Budget:** Lean to start, no tradeoffs on quality
- **Lloyd involvement:** Semi-active (dashboard + push notifications)
- **Name (placeholder):** "Only Lloyd Knows"

## Design Sections Presented & Approved

### Section 2: Question Routing (Three Tiers)
See above for full detail. APPROVED.

### Section 3: Chat Experience (Web + SMS)
- Web chat is the main event on the site, not a tiny chat bubble
- User types plain English questions
- Bot responds in Lloyd's voice with forecast + clear recommendation
- Conversation history preserved for context
- SMS via Twilio: same pipeline, shorter/punchier format
- Both channels feed the same backend

**Sample Lloyd response:**
> "Saturday at Jones Beach? You're golden. High of 82, light breeze out of the southwest, maybe some clouds rolling in by 4 but nothing that ruins your day. Sunday's the one I'd worry about — front coming through late Saturday night. Go Saturday, trust me."

APPROVED.

### Section 4: Website
- **Home** — Hero with Lloyd's avatar, tagline, value prop, sample response, CTA
- **How It Works** — Three steps: sign up, ask, get Lloyd's take
- **Meet Lloyd** — His story, fun quotes from real emails/tweets, "greatest calls" section
- **Chat** — Authenticated subscribers, full chat interface (the product)
- **Pricing** — $6/month, one tier, Stripe Checkout
- **Lloyd's Dashboard** — separate authenticated route, question queue, approve/edit/reject, stats

Brand tone: Fun, confident, a little irreverent. Like a friend who happens to be obsessed with weather.

APPROVED.

### Section 5: Payments & Subscriptions
- Stripe Checkout, $6/month, one plan
- No free trial (Lloyd's personality does the selling via "Meet Lloyd" page)
- Supabase stores user record linked to Stripe customer ID
- SMS verified by matching phone number to active subscription

APPROVED.

### Section 6: Infrastructure & Data Flow
```
User asks question (web or SMS)
        |
Twilio (SMS) or Next.js API route (web)
        |
Question Router (confidence score)
        |
   A    B    C
   |    |    |
  Bot  Bot   Queue for Lloyd
  auto drafts
        |
Claude API + weather data + Lloyd corpus (semantic search)
        |
Response in Lloyd's voice
        |
Delivered via same channel
```

**Services:**
- Vercel — Next.js site + API routes
- Supabase — Postgres (users, subscriptions, conversations, Lloyd corpus with embeddings), auth
- Claude API — generates all responses
- Weather API — Open-Meteo (free) or Weather.gov
- Stripe — payments
- Twilio — SMS
- Gmail API — ingests Lloyd's emails
- Twitter/X API — ingests Lloyd's tweets

**Cost at launch:** ~$0 fixed. Pay-per-use on Claude, Twilio, Stripe.

APPROVED.

## Top 5 Unconsidered Items (Operational)

1. **Lloyd's legal exposure** — Need disclaimer ("for entertainment/informational purposes"). Josh says YES.
2. **Response time for Tier B/C** — Need interim messages while waiting for Lloyd. Josh says YES, build messages to cover when Lloyd is sleeping.
3. **Off-season engagement** — What keeps people paying in mild months? Josh says THIS IS HARD, wants to discuss more. Notes: winter, summer, fall (foliage?) are strong. His Snowlogy newsletter is $29.99/year but winter-only. OPEN ITEM.
4. **Lloyd's content rights** — Simple licensing agreement needed. Josh says YES, don't worry about it for now.
5. **Onboarding the 500** — Launch email to Lloyd's existing list. Josh says we'll figure out once built.

## Top 5 Unconsidered Items (Product/UX)

1. **Location awareness** — Users need to specify WHERE. Josh's solution: location selector fields in the chat prompt. Users set locations once (home, beach house, ski house), pick which applies. Defaults to home. APPROVED.
2. **Proactive alerts** — Lloyd texts YOU first when weather threatens your plans. Josh says incorporate but don't over-index. APPROVED as value-add.
3. **First-time experience** — Suggested starter questions + welcome message in Lloyd's voice after signup. Josh says LOVE. APPROVED.
4. **Family sharing** — One subscription covers the household (multiple phone numbers). Josh says YES. APPROVED.
5. **Feedback loop** — "Was this helpful?" after each answer. Trains system + tracks Lloyd's accuracy over time. Josh says YES. APPROVED.

## Status
- All 6 design sections APPROVED
- All 10 product/UX items addressed (1 open: off-season engagement)
- Ready for: formal spec document

## Next Session
- Discuss off-season engagement model (seasonal pricing? annual? proactive content?)
- Write formal spec document
- Spec review loop
- Implementation plan

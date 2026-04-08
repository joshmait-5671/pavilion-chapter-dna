# Travel Nurse Stipend Clarity Tool

**Date:** 2026-04-07
**Status:** SCORED
**Source:** Josh ideation

---

## WHO

**Active travel nurses in the US receiving tax-free stipends.**

- **Size:** ~175,000 active travel nurses (surged from 33K in 2018 to 175K+ by 2024; post-pandemic correction but still massive)
- **Income:** $88K-$166K/year. National average ~$2,165/week ($101K/year). Tax-free stipends often $1,000-$1,250/week on top of taxable hourly rate
- **Demographics:** Predominantly women (85%+), 25-45, mobile, tech-savvy (manage contracts, housing, licensing across states constantly). Many are solo operators managing their own finances for the first time at real income levels
- **Psychographic:** Independent, adventurous, financially motivated (they chose travel nursing for the money). But also anxious — they're making more than they ever have, the tax rules are confusing, and they know they're doing something the IRS might question. Many gave up a permanent home to travel and now aren't sure if they still qualify for tax-free stipends
- **Behavioral:** Heavy TikTok/Instagram users. Active on r/TravelNursing, r/nursing. Join Facebook groups (Travel Nurse Network, Gypsy Nurse). Trust peer recommendations over institutions. Google "travel nurse tax home" constantly during tax season

## WHAT (Value Point)

**Relief + Money.** This is fear-of-loss, not aspiration.

The core value: **"Do I owe the IRS $30,000-$50,000 I don't know about?"**

Travel nurses receive $50K-$65K/year in tax-free stipends. Those stipends are only legal if you maintain a valid "tax home" under the IRS 3-factor test. If you fail the test, you're an "itinerant worker" and ALL stipends become retroactively taxable — plus 20-25% accuracy penalties plus interest. That's a potential $30K-$50K surprise bill going back multiple years.

Here's the kicker: **most agencies don't verify tax home status.** They pay the stipends regardless. The nurse assumes it's fine. The IRS disagrees later.

This tool answers one burning question: **"Am I protected, or am I sitting on a time bomb?"**

Then it tells them exactly what to fix if they're not.

## HOW (Build)

### Product Form
Single-page self-service tool. Not an app. Not a dashboard. A guided questionnaire (10-15 questions) that evaluates the IRS 3-factor test, scores the nurse's risk level (green/yellow/red), and generates a personalized protection checklist + audit-ready documentation template.

### The 3-Factor Test (What We're Evaluating)
1. **Regular employment in the area** — do you work part of the year near your permanent home?
2. **Duplicate living expenses** — are you paying for a home AND temporary housing simultaneously?
3. **Ties to the area** — voter registration, driver's license, vehicle registration, church membership, etc.

Must meet 2 of 3 to qualify. The tool walks them through each one with plain-English questions, not IRS jargon.

### Output
- **Risk Score** (Protected / At Risk / Danger Zone)
- **Plain-English explanation** of where they stand and why
- **Fix-it checklist** — exactly what to do if they're not compliant (e.g., "Register to vote at your tax home address," "Keep receipts for mortgage/rent at your permanent residence")
- **Audit-ready documentation template** — a PDF they can hand to their CPA or keep in their files
- **Estimated tax exposure** — "If audited, you could owe approximately $X based on your stipend level"

### Stack
- Josh builds the front-end (HTML/CSS/JS, single page)
- AI-powered logic layer (Claude API for personalized recommendations)
- Stripe checkout ($29 one-time)
- No backend needed beyond Stripe. All computation client-side or single API call
- No licenses required. This is education/information, not tax advice (clear disclaimers)

### The Medvi Test
**Hard thing we're NOT building:** Tax preparation, CPA services, legal advice, multi-state filing. All of that already exists ($285-$595 from specialists like TravelNurseTaxes.com, TravelTax.com). We own the FRONT DOOR — the moment of panic — and either resolve it or hand them off to the specialists.

## Competitive Landscape

| Competitor | What They Offer | Price | Gap |
|---|---|---|---|
| **Excursion Health** | Free 7-question tax home quiz + paid Tax Home Tracker tool | Quiz free, Tracker ~$29-49 (one-time) | Quiz is too simple (7 Qs). Tracker is ongoing documentation, not instant clarity. No emotional payoff. |
| **YourTaxBase** | Free tax calculator with tax home verification | Free | Calculator-focused, not fear-resolution focused. Leads to their FL tax home service. |
| **TravelNurseTaxes.com** | Full tax prep | $285-$595 | Way overkill for "am I OK?" question. High friction. |
| **TravelTax.com** | Phone consults + tax prep | $75/hr consult, $400+ prep | Requires scheduling, talking to a human, waiting |
| **TravelNurseTaxPro.com** | CPA services | $300+ | Same — full service, high friction |
| **BluePipes** | Pay calculator | Free | Pay comparison only, no tax home evaluation |
| **Blog posts / guides** | Every agency publishes tax guides | Free | Generic, not personalized. Nurse reads it and still doesn't know if THEY'RE ok. |

**The gap:** Everyone either gives you a generic quiz/article OR sells you full tax prep. Nobody gives you a **personalized, instant, $29 answer to "am I protected?"** with a clear action plan. The free quizzes are lead magnets. The paid services are $300+. The $29 middle is wide open.

Excursion Health is the closest competitor and the most interesting one. They clearly understand the problem space. But their quiz is a lead gen tool (7 questions, email required), and their tracker is an ongoing documentation system. Neither one delivers the emotional payoff of **"here's your risk score, here's what to fix, here's your audit documentation — done."**

## Channel

**Primary: TikTok (organic + paid)**

- Travel nurse TikTok is massive. Multiple nurse influencers with 1M+ followers (Miki Rai: 2.5M, Nurse Tara: 1.3M, Nurse Blake: 925K)
- Travel nurse content performs well: lifestyle, money, housing tips
- The hook writes itself: "I just found out I might owe the IRS $40,000 from my travel nurse stipends" — that's a viral TikTok
- **Harper can run this.** She's 17, TikTok-native, AI-fluent. This is her lane.
- Micro-influencer partnerships: pay 3-5 mid-tier travel nurse TikTokers ($500-$1,000 each) for authentic "I just took this quiz and..." content

**Secondary: Facebook Groups**
- Travel Nurse Network, Gypsy Nurse Community, Highway Hypodermics — these groups have 50K-200K+ members
- Tax questions are the #1 anxiety topic every Q1-Q4
- Drop value (free tax home tips) then link to tool

**Tertiary: SEO**
- "travel nurse tax home" / "travel nurse stipend taxable" / "travel nurse IRS audit" — high intent, moderate competition
- One strong landing page could rank within 90 days

## Revenue Math

### Conservative (200 customers = a business)
- 200 sales x $29 = **$5,800**
- With upsell (audit documentation bundle at $49): 200 x $39 avg = **$7,800**
- Timeline: achievable in 60-90 days with TikTok + FB groups

### Moderate (Year 1)
- 1,000 sales x $29 = **$29,000**
- Tax season spike (Jan-Apr) drives 60% of sales
- With documentation upsell: **$39,000-$45,000**

### Aggressive (Year 1 with paid + influencers)
- 3,000 sales x $35 avg = **$105,000**
- If even 2% of 175K active travel nurses buy, that's 3,500 sales

### Costs
- Build: $0 (Josh builds in Claude Code)
- Stripe fees: 2.9% + $0.30 per transaction
- TikTok ads: $500-$1,000/month test budget
- Influencer partnerships: $2,000-$5,000 initial batch
- Ongoing: near-zero marginal cost (no API calls if logic is client-side; minimal if using Claude API for personalization)

### Expansion Plays (After Validation)
- **Annual re-check** ($19/year) — "Tax laws change. Re-run your assessment for 2027."
- **Audit defense kit** ($79) — deeper documentation package
- **CPA referral partnerships** — 15-20% rev share for warm handoffs to travel nurse CPAs
- **Agency partnerships** — white-label the tool for staffing agencies to offer their nurses

## Josh Score

### 1. Do I feel something for these people? — 8/10
These are mostly women, working brutal shifts, away from home, doing genuinely hard work — and the government might come after them for money they thought was legally theirs. The agencies that profit from them don't even bother to tell them they might not qualify for the stipends. That's messed up. Real empathy here.

### 2. Is this overlooked or dismissed? — 7/10
Travel nurses are a known market, but the *tax compliance anxiety* sub-niche is invisible to anyone outside it. VCs see "travel nurse" and think "post-COVID correction." CPAs see it and think "niche tax prep." Nobody is building a fast, self-service clarity tool for the panic moment. The "that's a CPA problem" dismissal is exactly the signal DMF looks for.

### 3. Is there a mashup or stolen idea angle? — 7/10
This is basically **TurboTax's "Am I getting audited?" anxiety + credit score monitoring psychology** applied to travel nurse stipends. The risk score concept (green/yellow/red) is stolen straight from credit monitoring. The "here's what to fix" action plan is stolen from security compliance tools. Nobody has mashed these UX patterns into this problem.

### 4. How simple is the solution? — 9/10
10-15 questions. One score. One checklist. One PDF. Done. No account needed. No ongoing commitment. No dashboard to maintain. This is closer to keychain than app. The IRS 3-factor test is actually simple — it's just buried in jargon. We translate it.

### 5. Can I nail the positioning in one sentence? — 9/10
**"Find out in 5 minutes if your tax-free stipends are legally protected — before the IRS finds out they're not."**
That's it. Fear + clarity + speed. The positioning is almost too easy.

### 6. Is the price below the "do I really need this?" threshold? — 9/10
$29 for someone earning $100K+/year who's worried about a $30K-$50K tax bill? That's not even a decision. It's a stress-relief impulse buy. It costs less than their lunch on assignment. The alternative is a $75/hr phone call with a CPA or $400+ tax prep.

### 7. Do I see the person paying? — 9/10
She's scrolling TikTok at 11pm after a 12-hour shift. She sees a video: "I almost got hit with a $38,000 tax bill because I didn't have a tax home. Here's how I found out in 5 minutes." She clicks. She reads the landing page. $29. She doesn't even think twice. She's already imagining the IRS letter. She pays. She takes the assessment. She either breathes a sigh of relief or gets a clear fix-it list. Either way, she texts her travel nurse friends about it.

### 8. Would I tell someone about this at dinner? — 7/10
"Did you know travel nurses get like $60K a year in tax-free money, but most of them don't actually qualify for it, and the IRS is starting to crack down? There's a massive hidden tax bomb sitting under an entire profession." Yeah, that's a good dinner conversation. It's not as inherently *fun* as some ideas, but the "hidden financial time bomb" angle is genuinely interesting to anyone who likes understanding how money works.

### OVERALL JOSH SCORE: 65/80 (81%)

**This is a strong score.** The simplicity (9), positioning (9), pricing (9), and payment visualization (9) are all near-perfect. The empathy pull (8) is real. The mashup angle (7) and overlooked factor (7) are solid but not extraordinary — travel nurses are a known group, even if this specific problem isn't being served well. Dinner test (7) is the weakest — it's interesting but not irresistible as a story.

## Recommendation: GO

### Why GO:
1. **Radical simplicity.** This can be built in a weekend. Single HTML page + Stripe + optional Claude API call. No backend, no accounts, no infrastructure, no licenses.
2. **2-week launch is realistic.** Week 1: build tool + landing page. Week 2: TikTok content + FB group seeding + 2-3 influencer DMs. Live and selling by day 14.
3. **The channel is obvious and accessible.** Harper can create TikTok content. Travel nurse FB groups are free to post in. The hook is visceral and shareable.
4. **Price-to-pain ratio is perfect.** $29 against a potential $30K-$50K liability. This is the most lopsided value prop in the pipeline.
5. **No competition in the $29 middle.** Free quizzes exist (lead gen). $300+ services exist (full prep). Nobody owns the instant-clarity layer.
6. **Expansion paths are clear.** Annual re-checks, audit defense kits, CPA referrals, agency white-labeling. This $29 tool can become the front door to a $200K/year travel nurse financial brand.
7. **Team fit.** Josh builds. Harper does TikTok. Kira (post-June) handles customer questions/support if volume grows.

### Key Risks:
- **Liability/disclaimer management.** Must be crystal clear this is educational, not tax advice. "Consult a CPA" on every output. Standard practice for tools like this, but get the disclaimer right.
- **Seasonality.** Tax anxiety peaks Jan-Apr. Need to figure out year-round positioning (new contract decision moments, mid-year check-ins).
- **Excursion Health could copy.** If they turn their free quiz into a paid assessment, they have the SEO and audience. Speed matters — get there first with better positioning.
- **Market correction.** Travel nursing shrunk post-COVID. 175K is lower than the pandemic peak. But it's still a massive audience for a $29 product — you only need 200 buyers.

### Name Ideas (Riffing):
- **StipendShield** — protection-forward
- **TaxHomeCheck** — literal, SEO-friendly
- **NurseGuard** — broader, could expand beyond stipends
- **StipendSafe** — simple, implies safety
- **The Stipend Test** — plain, memorable

### 2-Week Launch Plan:
**Days 1-3:** Build assessment logic (IRS 3-factor test questions + scoring algorithm + risk tiers)
**Days 4-5:** Design landing page + results page + PDF output
**Days 6-7:** Stripe integration + disclaimers + legal review of language
**Days 8-10:** Create 5-7 TikTok scripts + record first batch (Harper)
**Days 11-12:** Seed 3-5 Facebook groups with value posts (tax home tips, link to tool)
**Days 13-14:** DM 5-10 mid-tier travel nurse TikTokers for partnerships. Go live.

---

*Scored by Dr. Money Fingers on 2026-04-07.*
*Research sources: Excursion Health, YourTaxBase, TravelNurseTaxes.com, TravelTax.com, BluePipes, Advantis Medical, BetterNurse.org, Nurse.org, TLC Nursing, Staffing Industry Analysts, Prolink, Aequor, Vivian, NurseMagic AI, The Gypsy Nurse, inBeat Agency.*

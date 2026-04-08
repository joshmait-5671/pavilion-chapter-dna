# Opportunity Brief: Barn Manager Boarder Vetting

**Date:** 2026-04-07
**Source:** Josh idea + industry signal (Facebook group drama, equine forums)
**Status:** SCORED

---

## WHO

**Small horse boarding facility owner-operators.** 5-30 stalls. Mostly women, 35-60. Running the barn themselves or with 1-2 part-time helpers. Revenue $5K-$25K/month in boarding fees. Located rural/semi-rural, every state but concentrated in TX, FL, CA, OH, PA, KY, VA, NC.

**How many exist?** The ~35,000 estimate is plausible but soft. USDA 2022 data shows 370,000 equine-dedicated farms in the US. Pennsylvania alone has 30,000 horse operations with ~6,000 commercial. Nationally, dedicated *boarding* facilities (not breeding, training-only, or personal) likely fall in the 25,000-50,000 range. The 35K number is reasonable as a working estimate for commercial boarding operations that take outside boarders.

**Psychographic profile:**
- Passionate about horses, running the business out of love not optimization
- Burned out by the people side of boarding, not the horse side
- Zero business sophistication in most cases — no CRM, no screening process, contracts are a Word doc they found online
- Deep distrust after getting burned by non-paying boarders
- Active in local/regional Facebook groups, Chronicle of the Horse forums, Horse Forum
- Word-of-mouth network is everything — reputation travels fast in a small community

**Behavioral:**
- Currently vet boarders by gut feel, maybe a phone call to a previous barn
- No standardized process. Some ask for references but rarely check them
- When burned, they post in Facebook groups warning others — but it's scattered, unsearchable, and dies in the feed
- Already paying $750-$1,000+/month per stall in costs (feed, bedding, labor, insurance) — a single non-paying boarder is a $3K-$5K hit before they can even legally act

---

## WHAT (Value Point)

**Relief + Money.** The core value is: *never take on a deadbeat boarder again.*

A single non-paying boarder costs a facility $3,000-$10,000+ in unpaid board, feed costs, legal fees, and emotional drain. The legal remedy (horseman's lien / stablemen's lien) exists in all 50 states but requires you to physically keep the horse — once the boarder trailers out at 2am, you're stuck eating the loss. Small claims court is slow and rarely worth it.

The pain is real and well-documented:
- [Equine Legal Solutions: Warning Signs of Problem Boarders](https://equinelegalsolutions.com/warning-signs-of-problem-boarders/) — entire practice area built around this problem
- [Horse Network: Barn Owner with Unpaid Boarding Bills](https://horsenetwork.com/2020/12/im-a-barn-owner-with-unpaid-boarding-bills-now-what/) — common enough to warrant dedicated editorial
- [Chronicle of the Horse Forums](https://forum.chronofhorse.com/t/boarder-stops-paying-for-horse-wwyd/782786) — recurring threads, high engagement
- [Horse Forum: Evicting Boarder for Non-Payment](https://www.horseforum.com/threads/evicting-boarder-for-non-payment.118838/) — years of active discussion
- [The Plaid Horse: Tips for Boarding Agreements](https://www.theplaidhorse.com/2021/04/19/tips-for-every-boarding-agreement-to-protect-facility-owners-from-boarders-who-dont-pay/) — industry publication covering the problem

**What they get:**
- Before accepting a new boarder: run a check, see if they have unpaid history at other facilities
- After getting burned: report the boarder so the next barn knows
- Peace of mind that the $800/month stall they're filling won't become a $4,000 loss

---

## HOW (Build)

### The Product: BarnCheck (working name)

**A boarder reputation registry for horse boarding facilities.** Think tenant screening for barns — but radically simpler. No credit checks, no SSNs, no legal complexity. Just a shared record of boarding history reported by facility operators.

**V1 — The Minimum:**
1. **Landing page** — positioning, waitlist, $9/month or $79/year pricing
2. **Simple web app** (no native app) — barn owner creates account, reports boarders (name, dates, facility, outcome: good standing / left owing / evicted / abandoned horse)
3. **Search** — barn owner types in a name + state, gets back any reports filed on that person
4. **Report** — barn owner files a report after a boarder leaves (positive or negative)

**What Josh builds vs. outsources:**
- Josh owns: brand, positioning, landing page, checkout (Stripe), marketing
- Claude Code builds: the web app (simple CRUD — could be a single-page app with Supabase backend)
- No deep infrastructure needed. No licenses. No regulated data (no SSNs, no credit reports — this is NOT a consumer reporting agency under FCRA as long as it's structured as a peer review/reference network, not a credit check)

**Legal note:** Structure this as a "reference sharing network among facility operators" — similar to how landlords share info in local landlord associations. Barn owners are sharing their own first-party experience. This is protected speech / opinion. NOT a consumer reporting agency. Still worth a $500 legal review before launch to confirm FCRA doesn't apply.

**Tech stack:**
- Landing page: static HTML (Josh's wheelhouse)
- App: Supabase (auth + database) + simple frontend (HTML/JS or lightweight framework)
- Payments: Stripe
- Total build time: 5-7 days for V1

---

## Competitive Landscape

**Nobody does this.** That's the whole point.

The existing horse management software market is focused on barn operations:
- **BarnManager** — horse profiles, medical records, scheduling. No boarder vetting.
- **Stablebuzz** — customer service and task management for boarding stables. No vetting.
- **Stables.co** — comprehensive management software with AI billing features. Can flag late-paying *current* boarders but has no cross-facility reputation sharing.
- **EquineM** — stable administration. No vetting.
- **Equestria.ai** — free barn management. No vetting.
- **eSoft Planner** — boarding payments and scheduling. No vetting.

**Legal solutions exist but are reactive:**
- **Equine Legal Solutions** — sells boarding contract templates ($50-$200). Defensive, not preventive.
- **Stablemen's lien laws** — exist in all 50 states but only work if you still have the horse

**The informal system:** Facebook groups. Barn owners post "watch out for [name]" warnings. These are:
- Unsearchable (Facebook search is terrible for this)
- Ephemeral (buried in feed within days)
- Legally risky for the poster (defamation claims)
- Fragmented by region (you'd have to be in 20 groups to catch everything)

**BarnCheck replaces the Facebook warning post with a structured, searchable, persistent record.** That's it.

---

## Channel

**Primary channel: Facebook groups.** This is where barn owners already congregate and already discuss this exact problem. The channel IS the pain point.

**Campaign sketch:**
1. Join 10-15 of the largest horse boarding / barn owner Facebook groups
2. Don't spam — participate genuinely for 1-2 weeks, then share the product when a relevant thread appears (and they appear weekly)
3. Kira (post-June) or Josh posts: "We built the thing everyone keeps asking for — a way to check if a new boarder has unpaid history at other facilities. $9/month. [link]"
4. One-time viral potential: this solves a problem people have been complaining about publicly for years. The first 50 sign-ups come from pent-up demand.

**Secondary channels:**
- Chronicle of the Horse forums (chronofhorse.com) — the most active equestrian forum
- Horse Forum (horseforum.com) — large general community
- Local equestrian associations and chapters
- Equine Legal Solutions could be a referral partner (they already field these questions)

**Content play:** "The 5 Warning Signs of a Problem Boarder" — SEO article linking to BarnCheck. This content already exists everywhere but nobody owns it with a product behind it.

---

## Revenue Math

**Pricing:** $9/month or $79/year (impulse range, below "do I need this?" threshold)

| Milestone | Customers | MRR | ARR |
|-----------|-----------|-----|-----|
| Launch month | 20 | $180 | $2,160 |
| 3 months | 75 | $675 | $8,100 |
| 6 months | 200 | $1,800 | $21,600 |
| 12 months | 500 | $4,500 | $54,000 |
| 18 months | 1,000 | $9,000 | $108,000 |

**200 customers = $21,600/year.** That's a business by Josh's definition.

**Unit economics:**
- Supabase free tier covers first 500+ users easily
- Stripe fees: ~3%
- No COGS beyond hosting
- 95%+ margin at scale

**Expansion plays (later, not V1):**
- Boarding contract templates ($29 one-time add-on)
- "Verified Facility" badge for barn listings ($19/month premium tier)
- Boarder-side product: "BarnCheck Verified" portable good-standing certificate boarders can show new facilities ($4.99/year)
- Regional barn directory with ratings

---

## Josh Score

### 1. Do I feel something for these people? — 7/10
These are small operators running a labor-of-love business, getting financially hammered by bad actors with no recourse. The empathy is real — they're the underdog getting screwed by people gaming the system. Not Josh's world, but the dynamic is instantly relatable. Loses a few points because Josh has no personal connection to horses or this community.

### 2. Is this overlooked or dismissed? — 9/10
This is textbook "that's not a real market." VCs would never touch horse boarding. The big equine software companies are focused on operations, not trust. Facebook groups have been the de facto solution for years, which means the industry has literally been trying to solve this with the wrong tool. Nobody has productized it because nobody respects this audience enough.

### 3. Is there a mashup or stolen idea angle? — 9/10
Tenant screening for horse barns. That's the whole pitch. TransUnion/Experian for the equestrian world, but without the regulatory burden because it's peer-reported experience, not credit data. Also borrows from: Yelp (reviews), Carfax (vehicle history report), and landlord blacklist networks. Multiple proven models from other industries, zero application to this one.

### 4. How simple is the solution? — 8/10
Search a name, see if they have history. Report a boarder when they leave. That's it. V1 is a database with a search bar and a form. No AI needed. No complex workflows. No integrations. The only complexity is getting the initial data seeded (chicken-and-egg: need reports to be useful, need users to get reports). Loses 2 points for that cold-start challenge.

### 5. Can I nail the positioning in one sentence? — 9/10
"Check a boarder before they cost you thousands." Or: "The boarding history every barn owner deserves to see." Or: "Stop inheriting someone else's deadbeat." Clean, visceral, immediate. Multiple strong angles. This positions itself.

### 6. Is the price below the "do I really need this?" threshold? — 9/10
$9/month is nothing when a single bad boarder costs $3,000-$10,000. One prevented deadbeat pays for 30+ years of the subscription. The ROI story is absurdly obvious. Nobody will agonize over $9/month to protect against a $5,000 loss.

### 7. Do I see the person paying? — 8/10
Yes. The barn owner just had a boarder skip out owing $2,400. She's venting in a Facebook group. Someone links BarnCheck. She clicks, reads "never again," enters her card in 90 seconds. She also immediately reports the deadbeat who just screwed her — seeding the database with real data out of pure catharsis. Loses 2 points because the card-pull moment depends on timing (you need to catch them when they're angry or screening someone new).

### 8. Would I tell someone about this at dinner? — 8/10
"There are 35,000 horse barns in America and deadbeat boarders just hop from barn to barn with no accountability. We built a blacklist. $9 a month." That's a dinner story. It's unexpected, it's a world most people know nothing about, and the injustice is immediately graspable. People lean in when you describe a problem they've never heard of that has an obvious solution nobody built.

### OVERALL JOSH SCORE: 67/80 (83.75%)

---

## Risk Factors

1. **Cold-start problem.** The database is empty on day one. First users search, find nothing, and may churn before enough reports accumulate. **Mitigation:** Offer free first 3 months to any barn owner who files 3+ reports. Incentivize seeding.

2. **Defamation / legal exposure.** Barn owners reporting boarders could face pushback. **Mitigation:** Structure as "facility experience reports" with factual fields (dates, amounts owed, outcome) rather than free-text reviews. Include a dispute process. Get a $500 legal review pre-launch confirming FCRA non-applicability.

3. **Identity verification.** How do you confirm the person being searched is the same person? Common names are a problem. **Mitigation:** Name + state + approximate dates. Not perfect, but barn owners in a 50-mile radius usually know the players. V2 could add phone number as optional identifier.

4. **Josh has no equestrian network.** He's entering cold. **Mitigation:** Facebook groups ARE the network. The pain is so visible and discussed so publicly that you don't need insider access — you just need to show up where the conversation is already happening. Kira could own the community presence post-June.

5. **Low switching cost / easy to copy.** Once the model is proven, a barn management platform (BarnManager, Stables.co) could add this feature. **Mitigation:** Network effects. The database IS the moat. First mover with 1,000+ reports is hard to unseat. Also: Liquid Death principle — brand > product. If BarnCheck becomes the name people say when they mean "check a boarder," the brand is the moat.

---

## Team Fit

- **Josh:** Brand, positioning, landing page, Stripe setup, marketing copy, Facebook group seeding. 80% of V1 work.
- **Claude Code:** Build the web app (Supabase + frontend). 2-3 day build.
- **Kira (post-June):** Community manager in Facebook groups, customer support, boarder dispute resolution. This is PERFECT for Kira — customer-facing, relationship-driven, requires empathy.
- **Harper:** Could manage a BarnCheck social media presence (Instagram, TikTok horse community is massive).

---

## The Medvi Test

**What's the hard thing we're NOT building?** We're not building barn management software. We're not building a payments system. We're not building a legal platform. We're building one feature — the shared boarder record — that none of the existing platforms offer.

**Can Josh own just the brand/marketing/checkout layer?** Yes. The tech is trivial (database + search + forms). The value is in the network (data) and the brand (trust). Josh owns the two things that matter.

**Does it need licenses or deep infrastructure?** No. Not a credit reporting agency. Not a financial product. No regulated data. Just barn owners sharing their own experiences.

---

## 2-Week Launch Plan

**Days 1-3:** Brand + positioning. Name, domain, logo, one-page landing page with waitlist. Join 10+ barn owner Facebook groups.
**Days 4-7:** Build V1 app. Supabase backend, simple search + report UI, Stripe checkout. Deploy to Netlify/Vercel.
**Days 8-10:** Seed database. Reach out to 20 barn owners from Facebook groups, offer free lifetime access in exchange for filing their first 3 reports.
**Days 11-14:** Launch in Facebook groups. Post in 5-10 groups where the problem is being discussed. First paying customers.

---

## Recommendation

### GO

**Reasoning:** This scores 67/80 on the Josh Score — well above the action threshold. It hits nearly every DMF thesis criterion: overlooked audience, "too small" market that VCs ignore, clear mashup angle (tenant screening for barns), radical simplicity, impulse pricing, and a visible, vocal community where the pain is expressed weekly.

The cold-start risk is real but manageable — angry barn owners will seed the database for free just for the satisfaction of reporting a deadbeat. The legal risk is low with proper structuring. The build is trivial. The channel is clear and free (Facebook groups). And the team fit is excellent, especially with Kira coming online in June for the community/support role.

This is a 2-week build, $0 startup cost (Supabase free tier + Stripe), with a clear path to 200 paying customers ($21K ARR) within 6 months. If it works, the network effect creates a real moat. If it doesn't, Josh loses 2 weeks of evenings.

**The one thing that could kill it:** If barn owners won't file reports (fear of retaliation, laziness, apathy). The entire product depends on user-generated data. The Facebook group behavior suggests they WILL — they're already doing it in an inferior format. But this is the assumption to validate first.

**First move:** Buy the domain. Build the landing page. Join the groups. See if 50 people sign up for a waitlist in 2 weeks. If yes, build V1. If no, kill it fast.

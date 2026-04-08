# Opportunity Brief: Home Health Aide Worker Tools

**Date:** 2026-04-07
**Stage:** Scored
**Source:** Josh seed idea (Run 1) + DMF research

---

## WHO

**3.7 million home health and personal care aides** — the single largest occupation in U.S. healthcare (BLS 2024). Growing 17% over the next decade with 765,800 openings projected per year.

Demographics that matter:
- **87% women**
- **62% people of color** (Black women alone are 43% of the workforce in the South)
- **31% immigrants** (vs. 17% of overall U.S. workforce)
- **Median age: 46**
- **Median pay: $16.78/hr** ($34,900/year) — up 4.93% in 2025, still poverty-adjacent
- **49% rely on public assistance** despite working full-time (PHI National)
- **36% live in or near poverty** (household income < 200% federal poverty level)
- **~80% annual turnover rate** — the workforce churns almost entirely every year

This is a workforce that is essential, enormous, growing fast, overwhelmingly female and non-white, and systematically underpaid. They are invisible to Silicon Valley.

---

## WHAT (The Value Point)

**The core pain: these workers are getting robbed and they can't prove it.**

Agencies bill $25-$50/hr to Medicaid/private pay clients. Workers see $12-$18/hr. The spread is the agency's margin — but the math is opaque to the worker. Common abuses documented in DOL enforcement actions and the $45M Americare settlement (NY AG, 2025):

1. **Pay inaccuracy** — missed overtime, wrong hours logged, "straight time" for 50+ hour weeks. A single worker can have a dozen different pay codes on one check, making verification nearly impossible.
2. **Schedule chaos** — last-minute changes, overbooking, no-shows communicated by text or not at all. Workers plan childcare and second jobs around schedules that evaporate.
3. **No documentation power** — when disputes arise, the agency has the system of record. The worker has nothing. No independent log of hours worked, clients visited, or miles driven.
4. **Benefits vacuum** — no health insurance, no PTO, no retirement. Many are misclassified as independent contractors to avoid these obligations entirely.

**What exists today: nothing for the worker.** A 2022 NIH scoping review found only 4 apps in existence focused on supporting HHAs — and those were research prototypes, not products. Every piece of home health software (Alora, AlayaCare, AxisCare, WellSky, HHAeXchange) is built for and sold to agencies. The worker is a row in someone else's database.

CareLinx and similar platforms (Honor, HomeTeam) tried to disintermediate agencies entirely — a VC-scale play that mostly failed or pivoted. Nobody has tried building a simple tool that sits alongside the agency relationship, giving the worker independent visibility into their own work life.

---

## HOW (The Build)

### The Product: **ShiftProof** (working name)

A dead-simple mobile-first web tool (not an app — no app store, no download friction) that does three things:

1. **Shift Logger** — Worker taps "start" and "stop" for each shift. GPS-stamped. Creates an independent record of hours worked, separate from whatever the agency tracks. End of week: generates a clean summary the worker can compare against their pay stub.

2. **Pay Check-Up** — Worker enters their hourly rate and uploads/photos their pay stub. Tool highlights discrepancies: "You logged 47 hours this week. At $16/hr with overtime, you should see $X. Your stub shows $Y. That's a $Z difference." Simple math, massive clarity.

3. **Know Your Rights** — One-page, plain-language (English + Spanish + Haitian Creole) summary of: overtime rules, minimum wage by state, what counts as work time, how to file a wage complaint. Not legal advice — a flashlight.

### What Josh builds vs. what exists:
- **Josh builds:** Brand, landing page, the shift logger (simple JS/HTML), pay calculator logic, rights content, checkout, distribution
- **Josh does NOT build:** A full scheduling system, EVV compliance, agency integrations, anything that requires healthcare licensing or HIPAA compliance
- **The Medvi test:** Josh owns the customer-facing layer. The "hard thing" (payroll systems, agency software, legal services) already exists — ShiftProof just gives the worker a mirror to hold up against it.

### Technical complexity: LOW
- Mobile-first responsive web page with localStorage or simple backend (Supabase free tier)
- No accounts required for basic use (reduce friction for a population that is not tech-forward)
- SMS-based shift reminders via Twilio ($0.0079/msg) for paid tier
- PDF export of weekly shift log for disputes
- Claude Code can build the V1 in a weekend

---

## Competitive Landscape

| Player | What They Do | Who Pays | Worker-Focused? |
|--------|-------------|----------|-----------------|
| AxisCare | Agency management, scheduling, EVV | Agency | No — worker is managed |
| AlayaCare | Full home care platform | Agency | No |
| HHAeXchange | Billing, payroll, EVV for agencies | Agency | No |
| CareLinx | Marketplace connecting workers to families | Families (platform fee) | Partially — but it's a job board, not a tool |
| Honor | Tech-enabled home care company | Families/insurance | Employer model — worker is employee |
| Help at Home (Caregiver Connect) | Agency app for their own workers | Agency | Portal, not advocate |
| TripLog | Mileage tracking | Worker (freemium) | Yes but single-purpose |
| **ShiftProof** | **Independent shift/pay verification** | **Worker** | **Yes — built for the worker, period** |

**The gap is real and validated:** Every tool in this space is sold to agencies. The worker has no independent tooling. The NIH literature review confirmed it. The $45M Americare settlement proves the pain is not theoretical.

---

## Channel

**Primary: TikTok / Instagram Reels (Harper runs this)**

This is a 87%-female, median-age-46 workforce. They are on social media. They share work frustrations. The content writes itself:

- "POV: your agency owes you $127 this week and you didn't even know"
- "I tracked my shifts for one month. Here's what my agency shorted me."
- "3 things every home health aide should know about overtime"
- Before/after of a shift log vs. a confusing pay stub

**Secondary: Facebook Groups** — there are dozens of large HHA/CNA/caregiver groups. Kira (post-June) can seed these with genuine participation, not spam.

**Tertiary: CNA/HHA training programs** — many states require certification. Partner with training schools to include ShiftProof in their "what you need to know" materials.

---

## Revenue Math

**Pricing: Freemium**
- **Free tier:** Shift logger (up to 10 shifts/month), basic pay calculator, Know Your Rights page
- **Pro tier: $4.99/month** ($59.88/year) — unlimited shifts, SMS reminders, PDF export, pay stub photo analysis, Spanish/Creole interface

**Why $4.99:** This is a population making $16/hr. The price must be invisible. $4.99/month is one Dunkin' run. Below the "do I really need this?" line. And the tool can pay for itself if it catches a single $20 payroll error.

| Milestone | Subscribers | MRR | ARR |
|-----------|------------|-----|-----|
| 200 customers | 200 | $998 | $11,976 |
| 500 customers | 500 | $2,495 | $29,940 |
| 1,000 customers | 1,000 | $4,990 | $59,880 |
| 5,000 customers | 5,000 | $24,950 | $299,400 |

**200 paying users = a business.** And 200 out of 3.7 million is 0.005% penetration.

**Cost structure:** Near-zero. Hosting (Netlify free or $19/mo), Supabase free tier, Twilio SMS (~$40/mo at 1K users). Margin is 95%+ until real scale.

---

## JOSH SCORE

### 1. Do I feel something for these people? **9/10**

Almost entirely women. Majority people of color and immigrants. Working full-time and still on public assistance. Getting shorted on pay by agencies that bill 2-3x what they pay. 80% turnover because the job is brutal and the system treats them as disposable. This is the definition of an overlooked, disrespected workforce. The empathy pull is immediate and real.

### 2. Is this overlooked or dismissed? **10/10**

Nobody in tech is building for this audience. VCs funded the agency-disruption play (Honor, CareLinx, HomeHero) and most of those failed or pivoted. The worker-side tool market literally has 4 research prototypes and zero commercial products (NIH, 2022). When you say "I'm building software for home health aides," people's first reaction is confusion. That's the signal.

### 3. Is there a mashup or stolen idea angle? **8/10**

This is the **bank statement analyzer for hourly workers.** Apps like Rocket Money and Truebill built entire businesses helping people see where their money goes. ShiftProof does the same thing but for where your money *should be coming from*. It's also borrowing from the gig-worker tools world (Gridwise for rideshare drivers, Stride for freelancer tax tracking) and applying it to a non-gig workforce that has zero tooling. The mashup is: gig-economy worker empowerment tools applied to a W-2/1099 workforce that predates the gig economy by decades.

### 4. How simple is the solution? **8/10**

Tap start. Tap stop. See your hours. Compare to your check. That's it. No onboarding flow, no account required for basic use, no integrations. The complexity ceiling is deliberately low. One risk: the pay stub analysis feature could get complicated (different agency formats, different pay codes). Keep V1 manual — worker enters their rate and hours, tool does the math. Photo-scan of pay stubs is a V2 feature.

### 5. Can I nail the positioning in one sentence? **9/10**

*"Your agency tracks your hours for them. ShiftProof tracks your hours for you."*

That's it. The positioning is the product. The name is the value prop. It's adversarial in the right way — not anti-agency, but pro-worker. "We're not saying they're cheating you. We're saying you should know for yourself."

### 6. Is the price below the "do I really need this?" threshold? **9/10**

$4.99/month for a workforce making $2,800/month. That's 0.18% of gross income. And the product pays for itself if it catches one missed overtime hour per month (~$25 in recovered wages). The free tier removes all friction for trial. The upgrade is a no-brainer once someone sees their first discrepancy.

### 7. Do I see the person paying? **8/10**

Yes. She's 42, Black, lives in Atlanta. She just finished a 10-hour shift and she's sitting in her car in the Kroger parking lot before picking up her kid. She opens her phone, sees the weekly summary email from ShiftProof: "You worked 48.5 hours this week. At your rate with overtime, you're owed $X." She opens her direct deposit notification. It's $67 less. She screenshots both. She upgrades to Pro so she can export the PDF and show her supervisor. $4.99. Done.

The moment is real. The card comes out because the tool just proved its value in dollars.

### 8. Would I tell someone about this at dinner? **8/10**

"Did you know there are 3.7 million home health aides in America and not a single app exists that's built for them? Agencies bill $50/hr to Medicare and pay the worker $14. The worker has no way to verify their own hours. I built a tool that lets them track their shifts independently and compare against their paycheck. It's $5 a month and it's already caught $X in underpayments."

That's a dinner conversation. It has the Liquid Death quality — "wait, nobody's doing this?" The social proof angle is strong too. People want to root for the underdog.

---

## OVERALL JOSH SCORE: 8.6 / 10

| Dimension | Score |
|-----------|-------|
| Empathy pull | 9 |
| Overlooked/dismissed | 10 |
| Mashup angle | 8 |
| Solution simplicity | 8 |
| One-sentence positioning | 9 |
| Impulse pricing | 9 |
| See the person paying | 8 |
| Dinner test | 8 |
| **Average** | **8.6** |

---

## Risk Factors

1. **Reach:** This workforce skews older (median 46), lower-income, and immigrant. Digital literacy and comfort with new tools varies. The product must be radically simple and multilingual from day one. SMS-first may beat web-first.

2. **Payment friction:** $4.99/month is cheap but this population has high financial stress. Free tier must be genuinely useful, not a teaser. Conversion will be lower than typical SaaS — plan for 2-5% free-to-paid.

3. **Agency backlash:** If ShiftProof gets traction, agencies may discourage workers from using it. This is actually a feature, not a bug — it validates the product. But it means distribution can't rely on agency cooperation.

4. **Legal surface area:** ShiftProof is NOT providing legal advice, NOT filing claims, NOT accessing agency systems. It's a calculator and a logger. Keep it there. The moment you touch dispute resolution or legal services, you need licenses.

5. **Language:** English-only is a non-starter. Spanish and Haitian Creole are table stakes for V1.

---

## 2-Week Launch Plan

**Days 1-3:** Brand + landing page. Name, logo, one-page site explaining the value prop. "Your agency tracks your hours for them. ShiftProof tracks your hours for you." Email capture. Josh builds this in Claude Code.

**Days 4-7:** Build the shift logger (mobile-first web). Start/stop with timestamp. Weekly summary view. Basic pay calculator (enter rate, see what you should earn vs. what you got). No login required. Deploy to Netlify.

**Days 8-10:** Know Your Rights content in English, Spanish, Haitian Creole. Stripe checkout for Pro tier ($4.99/mo). PDF export for Pro users.

**Days 11-14:** Harper creates 5-7 TikTok/Reels. Josh seeds 3-5 Facebook groups (CNA communities, home health aide support groups). Launch post. First users.

**Team fit:**
- **Josh:** Builds everything, positioning, brand, checkout
- **Harper:** TikTok/Reels content, ongoing social
- **Kira (post-June):** Facebook group seeding, customer support, community building

---

## Recommendation: **GO**

This is one of the highest-scoring opportunities DMF has surfaced. Here's why:

**Why GO:**
- The audience is massive (3.7M), growing (17% over decade), and has literally zero worker-side tooling
- The pain is documented, litigated ($45M settlements), and visceral
- The product is simple enough to build in a weekend and launch in two weeks
- The positioning writes itself — adversarial but not aggressive, empowering but not preachy
- Josh owns just the brand/marketing/checkout layer — no healthcare licensing, no HIPAA, no agency integrations needed
- $4.99/month at 200 users is already a small business; at 5,000 users it's $300K/year
- The Liquid Death principle applies: in a space full of agency software with names like "HHAeXchange" and "WellSky," a worker-first brand with personality and attitude will stand out by existing

**What would make me pause:**
- If digital adoption in this population proves lower than expected (mitigate with SMS-first approach)
- If the free-to-paid conversion is below 2% (mitigate with strong free tier that demonstrates value before paywall)
- If agencies actively block workers from using it (mitigate by not requiring any agency cooperation — this is the worker's personal tool)

**The Medvi test:** Josh builds brand, site, shift logger, pay calculator, checkout. He does NOT build agency integrations, EVV compliance, scheduling systems, or legal services. The hard infrastructure already exists on the agency side. ShiftProof is the mirror the worker holds up to it.

**Bottom line:** 3.7 million people, growing fast, no one building for them, pain that's been proven in court, a product simple enough to ship in two weeks, and a price point that pays for itself the first time it catches a $20 error. This is what DMF was built to find.

---

## Sources

- [BLS Occupational Outlook: Home Health and Personal Care Aides](https://www.bls.gov/ooh/healthcare/home-health-aides-and-personal-care-aides.htm)
- [PHI National: Understanding the Direct Care Workforce](https://www.phinational.org/policy-research/key-facts-faq/)
- [BLS: Majority of Home Health Aides Were Women in 2023](https://www.bls.gov/opub/ted/2024/in-2023-the-majority-of-home-health-aides-and-personal-care-aides-were-women.htm)
- [EPI: State Policy Solutions for Home Health Care Jobs](https://www.epi.org/blog/state-policy-solutions-for-good-home-health-care-jobs-nearly-half-held-by-black-women-in-the-south-should-address-the-legacy-of-racism-sexism-and-xenophobia-in-the-workforce/)
- [KFF: Payment Rates for Medicaid Home Care (2025)](https://www.kff.org/medicaid/payment-rates-for-medicaid-home-care-ahead-of-the-2025-reconciliation-law/)
- [NY AG: $45M Settlement for Underpaid Home Health Aides](https://ag.ny.gov/press-release/2025/attorney-general-james-secures-45-million-underpaid-home-health-aides)
- [NIH: Technological Landscape of Home Health Aides (2022)](https://pmc.ncbi.nlm.nih.gov/articles/PMC9700235/)
- [LeadingAge: Home Care Aides 4.93% Pay Increase in 2025](https://leadingage.org/home-care-aides-receive-4-93-pay-increase-in-2025/)
- [The New Republic: Crisis in Home Health Care](https://newrepublic.com/article/161087/home-health-care-crisis-lhc-group-overtime-wage-fraud)
- [Whirks: 6 Biggest Home Care Payroll Problems](https://www.whirks.com/blog/home-care-payroll-problems)
- [IntelyCare: Home Health Aide Salary 2025-26](https://www.intelycare.com/career-advice/home-health-aide-salary-facts-figures-and-salaries-by-state/)
- [KFF: Role of Immigrants in Direct Long-Term Care Workforce](https://www.kff.org/medicaid/issue-brief/what-role-do-immigrants-play-in-the-direct-long-term-care-workforce/)

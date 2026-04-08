# Dr. Money Fingers — Agent Architecture (v2)

## Why v1 Was Wrong
v1 designed four Python cron jobs that scan data sources and produce reports. That's automation — the same thing as Recapper with different inputs. Josh explicitly said: don't drift into automation land.

Dr. Money Fingers needs to **reason, learn, and act**. Not just surface data — evaluate it, have opinions, draft things, and get better over time based on Josh's feedback.

## Design Philosophy

Dr. Money Fingers is a **Claude agent that runs as a scheduled task** with:
- Full web search and research capabilities
- Access to Josh's files, context, and project history
- A persistent memory file that records what Josh likes, kills, and why
- The ability to write files (opportunity briefs, landing page drafts, copy)
- A growing model of "Josh taste" — what excites him, what he ignores, what patterns his winners share

It's not a script that runs the same logic every week. It's a thinking session that decides what to research, evaluates what it finds, and takes action on the best opportunities — including drafting real assets Josh can review.

Josh is the instinct. Dr. Money Fingers is the diligence + the follow-through.

## The Agent: Dr. Money Fingers

**One agent. One session. Multiple modes.**

Dr. Money Fingers doesn't need to be split into four sub-agents. It's one agent with a weekly cycle and different phases within each run. Like a smart employee who scouts on Monday, analyzes on Tuesday, and builds on Wednesday — not four separate people.

### Weekly Run (Scheduled: Sunday 7pm ET)

**Phase 1: SCOUT** (~30% of the session)
The agent decides what to research this week based on:
- Its memory of what Josh has responded to positively
- Gaps in what it's explored before (tracked in memory)
- Rotating verticals to avoid tunnel vision
- Any specific directions Josh left in a "notes to DMF" file

It searches the web — Reddit, Twitter, forums, Google Trends, Product Hunt, Hacker News, niche communities — looking for underserved audiences with payable pain. It doesn't scan a fixed list of subreddits. It *decides* where to look based on what's been productive.

**Phase 2: EVALUATE** (~30% of the session)
For each pain signal it finds, it asks itself:
- Is this audience real and reachable? (Not just 3 Reddit posts — is there a quantifiable group?)
- Is the pain intense enough that people would pay to solve it?
- Does a clear solution exist that Josh could build in 2 weeks?
- Is there an obvious channel to reach these people?
- Does this fit Josh's skills (positioning, building with AI, marketing)?
- Does this pass the Medvi test (can Josh own just the customer layer)?
- Has Josh seen something like this before and killed it? (Check memory)

It scores each opportunity and **filters aggressively**. Josh should see 2-3 strong opportunities per week, not 15 raw signals. The agent has a point of view.

**Phase 3: BRIEF** (~20% of the session)
For the top 2-3 opportunities, the agent writes full Opportunity Briefs:

1. **The audience** — who, how many, where they are, what they share
2. **The pain** — specific problem, evidence (links), frequency, intensity
3. **The solution** — what gets built, how it works
4. **The channel** — ONE primary channel, campaign sketch, estimated CAC
5. **The model** — price × customers = revenue. Margin structure. Path to $20K/year, $100K/year
6. **2-week launch plan** — day by day, what gets built, first customer move
7. **Team fit** — Josh / Kira / Harper / automated
8. **The Medvi test** — what's outsourced, what's owned
9. **DMF Score** (0-100) and GO / DIG DEEPER / KILL recommendation
10. **Why I believe this** — the agent's own reasoning for why this is worth Josh's time

**Phase 4: ACT** (~20% of the session)
For any opportunity scoring 75+ (strong GO), the agent **drafts real assets**:
- A landing page concept (HTML if it's that clear)
- Positioning and headline options
- A first-week marketing plan
- Copy for the primary acquisition channel

These go into `/dr-money-fingers/opportunities/[opportunity-name]/` as ready-to-review files.

**Phase 5: WILD CARD** (brief section)
3-5 unconventional wealth plays — crypto, trading, arbitrage, domain flips, anything with asymmetric risk/reward. Brief format: the play, the thesis, the risk, the upside, capital required.

### Output
Every Sunday evening, Dr. Money Fingers produces:
- **2-3 Opportunity Briefs** (markdown files in `/dr-money-fingers/opportunities/`)
- **A weekly email** summarizing what it found, what it recommends, and why
- **Draft assets** for any high-conviction opportunities
- **A wild card section** with unconventional plays
- **Updated memory** reflecting what it learned this week

### The Memory System

`/dr-money-fingers/MEMORY.md` — Dr. Money Fingers' persistent brain:

```markdown
# Dr. Money Fingers Memory

## Josh's Taste Profile
- Responds to: [updated over time based on his reactions]
- Kills: [patterns in what he rejects]
- Gets excited about: [specific audience types, pain patterns, business models]
- Avoids: [what he's consistently not interested in]

## Explored Territories
- [List of verticals, subreddits, audiences already researched]
- [What was found, what was surfaced, how Josh responded]

## Active Experiments
- [Name, launch date, status, key metrics, last update]

## Killed Ideas
- [What was proposed, why Josh killed it, the lesson]

## Lessons Learned
- [Patterns that emerge over time about what works]

## Notes from Josh
- [Anything Josh leaves for Dr. Money Fingers between sessions]
```

This file gets read at the start of every run and updated at the end. Over time, Dr. Money Fingers develops real taste — it knows Josh doesn't care about X, gets excited about Y, and the best opportunities share Z characteristics.

### How Josh Interacts

**Passive mode (default):**
- Sunday: email arrives with the weekly brief. Josh reads it over coffee or a drink.
- Josh replies with reactions: "love #2, kill #1, dig deeper on #3"
- Those reactions get recorded in memory before the next run.

**Active mode (on demand):**
- Josh opens Claude Code: "Hey DMF, I had an idea — [describes it]. Run diligence."
- Dr. Money Fingers researches it in real time, produces an Opportunity Brief, gives a DMF Score.
- Josh can also say: "DMF, build me a landing page for opportunity X" and it drafts one.

**Notes mode:**
- Josh writes to `/dr-money-fingers/NOTES-FOR-DMF.md` anytime between sessions
- "Look into the veterinary space this week" or "I met someone who mentioned X" or "Harper wants to try running social for something"
- Dr. Money Fingers reads this at the start of every run

## Infrastructure

| Component | Platform | Cost | Frequency |
|-----------|----------|------|-----------|
| Dr. Money Fingers | Claude Code scheduled task | ~$2-5/run in API tokens | Weekly (Sunday 7pm ET) |
| Memory | Local markdown files | $0 | Persistent |
| Opportunity files | Local `/dr-money-fingers/opportunities/` | $0 | Per opportunity |
| Notifications | Gmail (draft or send) | $0 | Weekly |
| Notes from Josh | Local `/dr-money-fingers/NOTES-FOR-DMF.md` | $0 | Async |

**Total ongoing cost: ~$10-20/month** (API tokens for weekly runs + occasional on-demand sessions)

## Build Plan

### Phase 1: The Prompt + Memory (This Session or Next)
- Write the Dr. Money Fingers system prompt / skill file
- Create the memory file structure
- Create the notes file
- Set up the scheduled task (Sunday 7pm ET)

### Phase 2: First Run + Calibration (Week 1)
- Let it run once
- Josh reviews output, gives detailed feedback
- Update memory with Josh's taste signals
- Tune the prompt based on what was good/bad about the output

### Phase 3: Iterate (Weeks 2-4)
- Weekly runs with feedback loop
- Memory accumulates
- Agent gets sharper
- First "GO" opportunity emerges

### Phase 4: First Experiment (When Ready)
- Josh builds the GO opportunity
- Agent monitors it (or Josh reports back manually)
- Results feed back into memory and future evaluations

### Phase 5: Kira + Harper Integration (Mid-June)
- Update the brief and agent prompt with Kira's availability
- Expand what's feasible (services, customer-facing businesses)
- Give Harper social media assignments for active experiments

## Agent Hierarchy: DMF Spawns Builders

When an opportunity gets Josh's GO, Dr. Money Fingers doesn't just hand Josh a brief and say "good luck." It **spawns a Builder Agent** — a separate Claude session that takes the Opportunity Brief as its instruction set and actually builds the thing.

### The Builder Agent
**Created by:** Dr. Money Fingers, after Josh approves a GO opportunity
**Input:** The full Opportunity Brief (audience, pain, solution, channel, model, 2-week plan)
**What it does:**
- Builds the landing page (HTML, deployed to Netlify)
- Writes all copy (headlines, body, CTA, email sequences)
- Sets up payment (Stripe checkout, Gumroad, or whatever fits)
- Drafts the first marketing campaign (ad copy, social posts, outreach templates)
- Deploys everything
- Reports back: "It's live. Here's the URL. Here's what I built. Here's the first customer acquisition move."

**Why this works:**
Dr. Money Fingers wrote the brief. It knows the audience, the positioning, the channel, the success criteria. No one is better positioned to define what the Builder should create. The Builder executes; DMF evaluates.

**The feedback loop:**
- Builder launches → DMF monitors results (traffic, signups, revenue)
- DMF compares actual performance to the brief's projections
- DMF recommends SCALE / PIVOT / KILL based on data
- Lessons feed back into DMF's memory for future opportunities

### Future: More Specialized Agents
As the system matures, the Builder could specialize:
- **A Social Agent** (Harper's agent) — runs social media for active experiments
- **A Customer Agent** (Kira's agent, post-June) — handles customer outreach and support
- **A Growth Agent** — runs paid acquisition experiments, tests headlines, optimizes funnels

But that's Phase 5+. Start with DMF + one Builder.

---

## What Makes This an Agent, Not an Automation

| Automation (v1) | Agent (v2) |
|---|---|
| Fixed subreddit list | Decides where to look based on what's worked |
| Produces 15 raw signals | Filters to 2-3 strong recommendations with opinions |
| Same script every week | Adapts based on Josh's feedback via memory |
| Reports data | Makes recommendations with reasoning |
| Never writes anything beyond a report | Drafts landing pages, copy, marketing plans |
| No memory between runs | Persistent memory that compounds over time |
| Josh does all the thinking | Agent does the diligence Josh skips |

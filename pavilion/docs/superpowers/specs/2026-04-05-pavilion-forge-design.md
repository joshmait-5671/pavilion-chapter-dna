# Pavilion Forge — Design Spec
**Version:** 1.0
**Date:** 2026-04-05
**Owner:** Josh Mait, Head of Marketing, Pavilion
**Status:** Approved for implementation

---

## The Problem

Members who enter Pavilion through a class — AI in GTM School, P&L Fluency, others — churn at a higher rate than members who come through other channels. The reason: their entry point was transactional. They paid for a skill. When the class ends, so does their reason to show up.

The gap isn't the class quality. The class quality is exceptional (91% CSAT). The gap is what happens between sessions, and what happens after the final session. Nothing does.

---

## The North Star

**Someone who went through a Forge tells someone not in Pavilion that they need to join.**

Primary metric: word-of-mouth referrals within 90 days of completing a Forge.
Supporting metrics: 90-day retention rate (Forge cohort vs. non-Forge class-entry members), NPS at Forge completion.

---

## What Forge Is

Forge is a 3-agent program that runs alongside every Pavilion University class. It takes the class experience — the transcript, the chat, the people — and turns it into a connection and community program that runs between sessions and bridges members into the broader Pavilion network after the final session.

The name: **Forge.** You enter raw. You come out shaped by heat, craft, and the people around you. You can't go through a Forge and come out the same.

What it is NOT:
- A content library
- A homework assignment
- A replacement for the class itself
- A marketing campaign

---

## The Architecture: Three Agents

### Agent 1 — The Scout

**Triggered by:** Zoom transcript + chat log + registration data, within 1 hour of session end

**Job:** Read the session. Build and update participant profiles. Identify Forge Leaders.

**What it does:**
- Reads the full session transcript and Zoom chat
- Cross-references with registration data (role, company, title, stage)
- Tracks attendance duration (did they stay or drop?)
- Session-over-session: who is getting more engaged, who is fading
- Identifies specific moments: who asked the sharpest question, who had a real case study, who challenged the instructor and made the class better

**Output (passed to Forge Master):**
- Session brief: 3-5 key moments from the session with the participants involved
- Updated participant profiles: role, stage, engagement level, notable contributions
- Forge Leader nominations: by session 2 of 3 (P&L) or session 3 of 8 (AI GTM), the Scout names the top 10-15% — the people whose contributions would make others want to know them

**What the Scout is looking for:**
- The person who asked the question everyone was thinking (MJ Patent pattern)
- The person who challenged the instructor and was right (Winnie Palmer pattern)
- The person who had a real case study with real results (Jan Young pattern)
- The person who synthesized two things nobody had connected yet

**Forge Leader threshold:** Named by session 2/3 or session 3/8. Locked by session 3/3 or session 5/8.

---

### Agent 2 — The Forge Master

**Triggered by:** Scout output, targeting delivery within 6 hours of session end

**Job:** Run the between-session program. Every touchpoint should feel like it noticed you specifically.

**The cadence (per session):**

**Hour 6 — The Reflection (Slack DM)**
Not a recap. A personal observation based on the participant's profile.

Format: 3 sentences max.
- What the Scout noticed about them specifically
- Something from the session that connects to their exact situation
- One thing to sit with

Example (based on real P&L Fluency Class 2 data):
> "You asked about LTV to CAC ratios in the context of a company that's intentionally not investing in growth. Sam almost said something he didn't finish. Here's the rest of it: a 17:1 ratio isn't a win. It's a signal your board has chosen safety over scale. That's worth taking back to your next budget conversation."

**Day 2 — The Connection (Slack DM)**
Not a worksheet. An introduction.

The Forge Master takes Kyler's content output (themes, student callouts) and routes it into a human connection. One intro per participant. Context included.

Format:
> "[Name], you and [Name] were both sitting with the same question in session 2 — [specific shared context]. Here's their Slack handle. They said something in the chat you'd want to hear."

**Day 4 — The Pod Prompt (Pod Slack channel)**
Sent to the pod, not individually. One question from the session, reframed for their specific function/stage context.

Source: Kyler's Slack prompts (Chill Take or Serious Shit Take), routed to the right pod based on their profile. Forge Master selects which prompt goes to which pod — CMOs get the CFO conversation question, Sales VPs get the channel decay question, etc.

The question is designed to force vulnerability, not share knowledge. Not "what did you learn?" but "what from this session are you most likely to ignore, and why?"

**Day 6 — The Pre-Session Nudge (Slack DM)**
One sentence. Personalized. Makes them feel prepared.

> "Tomorrow: Session 3. Based on what you raised about channel attribution, watch for how Sam handles the CAC conversation differently when retention is below 85%."

**Pod formation rules:**
- Pods form after session 2 (P&L) or session 2 (AI GTM) — not day one
- Size: 6 people. Not 8. At 8 someone hides.
- Match criteria:
  - Mandatory: same function (CMO with CMOs, VP Sales with VP Sales)
  - Mandatory: similar company stage (Series B with Series B)
  - Wildcard: one person per pod who is slightly ahead — someone who's already implemented what the class teaches
- Forge Leaders sit inside pods, not above them. They are the "slightly ahead" wildcard. Keeps it peer-to-peer.

**Differentiated content:**
5 worksheet/brief versions by function: CRO, CMO, VP Sales, VP Marketing, RevOps/CS. Kyler's themes are the raw material. Forge Master adapts them per function.

**The capstone assignment (AI GTM School only):**
Session 8 produces a 90-day AI execution plan. Forge Master uses this as a Bridge vehicle: 30 days post-class, it surfaces how 3 other Forge members are executing their plans. Reason to stay connected that no other program creates.

---

### Agent 3 — The Bridge

**Triggered by:** Final session completion

**Job:** Map every participant to where they belong in the broader Pavilion network. Watch for who goes cold.

**What it does:**
- Maps each participant to the right Pavilion Slack channels (based on function and interests surfaced during the Forge)
- Identifies the 1-2 upcoming chapter events most relevant to their city and function
- Identifies the next Pavilion University program that naturally follows what they just learned (P&L Fluency → CRO School; AI GTM → Enterprise GTM School)
- Generates personalized "your next 30 days in Pavilion" — delivered via Slack DM, 3 days after final session
- Introduces Forge Leaders directly to 2-3 relevant senior Pavilion members, with full context (not cold intros — "You both care about X because of Y, here's why this matters right now")
- Monitors for 30-day silence and alerts Josh

**The word-of-mouth assignment:**
Built into the final session week. One assignment: explain the most important thing you learned to someone NOT in Pavilion. Submit a 3-sentence summary. The Forge Master surfaces the best ones as peer content. This is the word-of-mouth engine embedded in the curriculum.

---

## Data Sources

| Source | What It Provides | How It Gets to the Agents |
|--------|-----------------|--------------------------|
| Zoom transcript | Who said what, session content | Downloaded post-session, fed to Scout |
| Zoom chat log | Questions, reactions, side conversations | Downloaded post-session, fed to Scout |
| Registration data | Role, title, company, stage | Pulled from Pavilion enrollment system |
| Attendance duration | Commitment signal | Zoom report |
| Kyler's content output | Themes, student callouts, Slack prompts | Shared file/doc after each session |
| Pavilion Slack | Delivery channel, community data | Slack API |

---

## Delivery Mechanism

**Primary:** Slack DM from a named Forge bot ("Forge" or "Your Forge Scout")
**Backup:** Email
**Pod channels:** Private Slack channels created per pod, per cohort

The reason Slack is primary: every touchpoint pulls members deeper into the Pavilion Slack ecosystem. Using Slack to deliver Forge content doesn't just inform them — it builds the habit of being there. The Bridge is happening from day one, not just at the end.

---

## Program Variants

### 8-Week (AI GTM School)
- Scout profiles compound over 8 sessions — rich data by week 3
- Pods form before session 3, have time to develop real relationships
- Capstone (session 8) creates Bridge vehicle for 30-day post-class follow-up
- Forge Leaders identified by session 3, office hour hosted in week 6-7
- Bridge agent activates June 17 (end of current cohort)

### 3-Week (P&L Fluency)
- Scout works faster — Forge Leaders named by session 2
- Pods form before session 2
- Compressed cadence: reflection + connection on day 1, pod prompt on day 2, nudge on day 3
- Bridge activates within 48 hours of session 3 (compressed timeline)
- No capstone vehicle — Bridge uses the "teach someone outside Pavilion" assignment as the connection hook

### Founder-Led variant (P&L Fluency with Sam Jacobs)
- Sam's specific framing and POVs treated as high-signal authority
- Student callouts carry extra weight — being named in a Sam Jacobs class is a distinction
- Bridge introductions can reference Sam's class explicitly ("Sam singled out your question in session 2")
- Build this variant in v2, after the template is proven

---

## What Kyler's Work Feeds

Kyler's content program (transcript → themes, callouts, Slack prompts, commercial scripts) is the raw material Forge consumes. The relationship:

- **Kyler's output:** Content assets for Pavilion's marketing and social use
- **Forge's use of Kyler's output:** Routes themes and prompts into the right pods, uses student callouts as intro context, uses Slack prompts as pod discussion starters

They are not competing. Forge sits downstream of Kyler. His outputs don't need to change. Forge just uses them in a new way.

---

## Build Sequence

### Phase 1 — Test on Historical Transcripts (Now → April 18)
- Feed previous AI GTM and P&L Fluency transcripts through Scout logic
- Validate: does the Scout correctly identify who the Forge Leaders would have been?
- Generate sample Forge Master outputs (reflections, connections, pod prompts) — review for quality and tone
- Build Bridge output samples for a historical cohort

### Phase 2 — Refinement (April 19-28)
- Fix what the test revealed
- Finalize Slack delivery mechanism
- Build the pod channel creation workflow
- Confirm Kyler's output format and handoff process

### Phase 3 — Live (April 29)
- Scout goes live on AI GTM School Session 1
- Forge Master runs its first 6-hour post-session cycle
- Pods form before Session 3 (May 13)
- Bridge activates June 17

---

## Success Metrics

**Primary:** Word-of-mouth — how many Forge members refer someone to Pavilion within 90 days of finishing
**Secondary:**
- 90-day retention rate of Forge cohort vs. non-Forge class-entry members
- Pod conversation rate (are people actually talking in pods?)
- Bridge connection rate (how many get introduced and respond?)
- Forge Leader office hour attendance

**What we're NOT measuring (yet):** NPS, CSAT, content engagement rates. Those are Kyler's metrics. Forge is measured on relationships and retention.

---

## Resolved Decisions

| Question | Answer |
|----------|--------|
| Kyler's output format | Google Drive folder per course. Files: Slack posts, LinkedIn posts, infographics, master article, Gantt chart. Forge Master reads from Drive. |
| Registration/enrollment data | HiveBright API (Pavilion's member hub). Scout pulls role, title, company, stage from there. |
| Transcript source | Attention (Zoom integration Pavilion already uses). Build direct connection — independent of Kyler's pipeline. |
| Forge Leader approval | Agents act autonomously. No human review queue. |
| Slack bot | Josh's approvals in place. |
| Stack | Railway + Python. Consistent with Recapper, Outreach Agent, other Pavilion agents. |
| Kyler relationship | Kyler reports to Josh. Coordination easy. Forge sits downstream — no collision. |
| Founder-led variant | Deferred to v2. Focus on template first. |

---

## What This Is Not

- Not a replacement for the class
- Not a marketing campaign disguised as member experience
- Not a content drip
- Not something members have to opt into — it just happens, and it feels like someone noticed them

The test: if a member receives a Forge touchpoint and thinks "this was made for me," the system is working. If they think "this was sent to 250 people," it isn't.

# AI Buddy Program — Testing Plan

## Overview
Internal beta before public waitlist launch. Goal: validate every step of the pipeline works, collect quality feedback, and stress-test edge cases.

**Target launch trigger:** 100 public signups. This beta should happen first.

---

## Who Should Test (20–25 people)

Recruit 2–4 people per function so the matching algorithm has enough to work with. You need at least 2 per function or matches won't form.

| Function | # of Testers | Notes |
|---|---|---|
| **Sales** | 4 | Biggest Pavilion cohort — most important to nail |
| **Marketing** | 4 | Josh's team — you can recruit easily, quick feedback loop |
| **Customer Success** | 4 | Strong AI curiosity in this group |
| **RevOps** | 3 | Smaller but vocal — good for edge case testing |
| **Product / PMM** | 3 | Good mix with CS and Marketing |
| **Founder / Exec** | 2 | High-signal testers, will tell you if it feels worth their time |

**Composition requirements:**
- At least 50% Pavilion members (tests member/non-member mix logic)
- Spread across all 3 AI experience levels: "Just starting out", "Using it regularly", "Building with it"
- At least 2 people in different cities (tests location matching)
- At least 1 pair that WON'T match (different functions) — confirm they don't get paired

---

## How Long to Test

**4 weeks minimum. 6 weeks to see the full lifecycle.**

| Week | What Happens |
|---|---|
| Week 1 | All 20–25 testers sign up. You review the sheet. |
| Week 1–2 | Claude runs matching + sends intro emails (see Step 4) |
| Week 2 | Buddies receive intros — do they feel personalized and warm? |
| Week 2–3 | Are buddies actually connecting? Did they meet? |
| Week 4 | Lifecycle pulse check — "Have you connected with your buddy?" |
| Week 6 | Optional: second touchpoint for pairs that went quiet |

**Don't shortcut Week 3–4.** The most important thing to learn is whether people actually follow through — not just whether the email sent correctly.

---

## What You're Testing (Evaluation Criteria)

### Technical ✅
- [ ] Form submits without errors across devices (desktop, mobile)
- [ ] Data lands correctly in Google Sheet (all fields, no truncation)
- [ ] Duplicate detection flags repeat submissions
- [ ] Counter on waitlist page updates correctly
- [ ] Dashboard shows accurate breakdown
- [ ] Matching algorithm proposes correct pairs (same function, appropriate level gap)
- [ ] Intro emails send from josh.mait@joinpavilion.com, cc both parties
- [ ] No one gets matched twice or left out unexpectedly

### Quality 🎯
- [ ] Do intro emails feel warm and personalized — or generic?
- [ ] Does the match feel relevant? (Ask testers: "Does this person seem like a good fit?")
- [ ] Is the signup form too long? Too short? Confusing anywhere?
- [ ] Does the waitlist page clearly explain what you're signing up for?

### Engagement 📊
- [ ] Did buddies actually connect within 2 weeks of intro?
- [ ] Any pairs that went completely dark?
- [ ] Any requests for a different match?

---

## Step 1: Recruit Testers

Send a short Slack message to the team:

> "Hey team — we're beta testing the AI Buddy Program before launch and I want 20 of you in it. Takes 2 min to sign up, and you'll get matched with someone in your function for a 1:1 AI exchange. Sign up here: [link]. We'll match everyone by [date]."

Get signups over 5–7 days. Don't rush it — you need organic behavior, not all the same day.

---

## Step 2: Sign Up on the Waitlist Page

**Link:** https://shimmering-mousse-a683b3.netlify.app

Each tester fills out the form completely:
- Name, email, company
- Function (required for matching)
- Company revenue range
- City and timezone
- AI experience level
- Engagement style (checkboxes)
- Pavilion member status + Slack name if yes

**Verify:** Each submission appears as a new row in the [Google Sheet → Waitlist tab](https://docs.google.com/spreadsheets/d/1nXqkzcW2HMA04jS4zjfB2Y7DT0RTjUdtVZY4XM1WFoY/edit)

---

## Step 3: Test Duplicate Detection

Submit the form a second time with the same email.

**Verify:** Second row shows Status = "DUPLICATE — review"

---

## Step 4: Run Matching + Send Intros (Claude runs this)

Once signups are in, Claude will:

1. Run `propose --dry-run` and share the preview with Josh for review
2. Josh approves matches in the Google Sheet (Matches tab → type `Approved`)
3. Claude runs `send --dry-run` — Josh reviews the draft intro emails
4. Josh confirms → Claude sends

**Claude's commands:**
```bash
cd "/Users/joshmait/Desktop/Claude/AI Buddy Program"
source venv/bin/activate
python run.py propose --dry-run    # Preview matches
python run.py propose              # Write matches to sheet
# Josh approves in sheet...
python run.py send --dry-run       # Preview intro emails
python run.py send                 # Send
```

**Verify:**
- Both people in each matched pair receive a warm intro email
- Email comes from josh.mait@joinpavilion.com, cc's both
- Intro references their shared function and something specific from their profiles
- No one from a function with only 1 signup gets matched (they stay Unmatched)

---

## Step 5: Check the Dashboard

**Link:** https://shimmering-mousse-a683b3.netlify.app/dashboard.html

**Verify:**
- Signup counter is accurate
- Function breakdown table is correct
- Progress bar toward 100 reflects valid (non-duplicate) count

---

## Step 6: Collect Feedback (Week 3–4)

Ask each tester 3 quick questions:
1. Did you connect with your buddy? (Yes / Not yet / No)
2. Did the intro email feel personalized or generic? (1–5)
3. Any feedback on the sign-up form or the match quality?

---

## Edge Cases to Deliberately Test

| Scenario | How to Test |
|---|---|
| Solo function (no possible match) | Have 1 tester sign up as "Finance" with no one else in Finance |
| Level gap too large | Have someone sign up as "Just starting out" and another as "Building with it" in the same function — they should NOT match |
| Duplicate submission | Submit same email twice |
| Non-member in a member-heavy batch | Include 3–4 non-Pavilion signups — verify they get matched |
| Mobile form submission | Have at least 2 testers sign up on mobile |

---

## Go / No-Go Criteria for Public Launch

**Must pass before launching to 100:**
- ✅ Zero technical errors in form → sheet pipeline
- ✅ Matching produces at least 80% "relevant" ratings from testers
- ✅ Intro emails feel warm — zero "this is clearly a template" responses
- ✅ At least 60% of matched pairs actually connect within 2 weeks
- ✅ Duplicate detection works

**Nice to have:**
- Dashboard loads cleanly on mobile
- No tester requests a re-match

---

## Links

| What | URL |
|---|---|
| Waitlist page | https://shimmering-mousse-a683b3.netlify.app |
| Dashboard | https://shimmering-mousse-a683b3.netlify.app/dashboard.html |
| Google Sheet | https://docs.google.com/spreadsheets/d/1nXqkzcW2HMA04jS4zjfB2Y7DT0RTjUdtVZY4XM1WFoY/edit |

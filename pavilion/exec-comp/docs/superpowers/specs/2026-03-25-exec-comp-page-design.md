# Executive Compensation & Negotiation — Page Design

## Overview

A single-page marketing asset for Pavilion's Executive Compensation & Negotiation offering. Replicates the structure and brand quality of the AI GTM Bundle page but with its own identity. Primary audience: current Pavilion members who don't know this benefit exists. Secondary: prospects evaluating membership.

## Emotional Core

"Get paid what you've earned — and when the exit comes, make sure you're at the table."

This is not just salary negotiation. It's about total compensation: cash, equity, benefits, and positioning yourself for wealth creation events (exits, acquisitions, IPOs).

## Page Flow

### 1. Hero Section

- **Headline:** "Know your number. Then go get it." (or similar — empowering, confident)
- **Subhead:** One line connecting comp negotiation + wealth creation. Something like: "Your compensation defines your career. We make sure you never negotiate alone."
- **Bullets (4):**
  - 1-on-1 coaching with former operating executives
  - 3-week live class, runs every quarter
  - Executive comp benchmark reports from real member data
  - A community of peers navigating the same conversations
- **CTA:** "Book a Call" button (Calendly link — TBD from Josh)
- **Layout:** Single-column hero with CTA button. No form card — clean and action-oriented.
- **Design:** Pavilion brand colors (deep blue hero, pink accents). Nav bar with Pavilion logo + CTA button (same pattern as AI GTM Bundle).

### 2. Quick Truth — The Stakes

- One short section. Not fear-based, just honest.
- Something like: "Most executives negotiate their compensation alone, without data, without coaching, without preparation. The difference between good and great negotiation isn't talent — it's process."
- No more than 2-3 sentences. Sets up why the offering matters.

### 3. The Coaching (Star Section)

- **Section label:** "1-ON-1 COACHING"
- **Headline:** Something like "A former exec in your corner."
- **Body:** Sam Jacobs and fellow coaches (Russ Macowski, Fred Mather, Butch Langwa) have personally coached hundreds of Pavilion members through comp negotiations. These aren't career coaches — they're former operating executives who've been in the seat, negotiated their own packages, and know what good looks like.
- **What a session covers:** Review your offer/situation, help you script the ask, model out equity vs. base tradeoffs, prepare you for the conversation.
- **CTA:** "Book Your Session" (Calendly)
- **Design:** Premium feel. Card-based layout with coach names or clean text block with strong typography.

### 4. Sam Founder Note

- **Positioned right after coaching** to reinforce Sam's credibility while it's top of mind.
- **Format:** Same as AI GTM Bundle — handwritten signature, pink left border, warm personal tone.
- **Content:** Pulled from Sam's video transcript. Emphasis on: he's personally coached hundreds of members, this is about wealth creation not just salary, and the named coaches are real operators.
- **Video placeholder:** Build a video embed container that's hidden by default. When Josh has a hosted video URL, swap it in. Founder note stays as the default.

### 5. The Class

- **Section label:** "THE CLASS"
- **Headline:** Something like "Three weeks that change how you think about money."
- **Body:** Executive Compensation & Negotiation is a 3-week live cohort that runs every quarter. Led by Sam Jacobs and the coaching team.
- **Curriculum (complete list from Sam's video):**
  - Calibrate your success based on your market value
  - The essence of negotiation — how to take yes for an answer
  - Cash compensation and benefits aligned to outcomes you'll drive
  - The role of equity and how to increase the likelihood it turns into cash
  - Role play to stress test your approach
- **Next cohort date:** TBD (Josh to provide)
- **CTA:** "Enroll in the Next Cohort" or "Join the Next Class"
- **Design:** Clean card or structured list. Similar to how AI GTM School was presented.

### 6. Benchmark Reports

- **Section label:** "THE DATA"
- **Headline:** Something like "Know your number before you walk in the room."
- **Body:** Pavilion produces executive compensation benchmark reports based on direct survey data from members. Real numbers from people in the same roles, at the same stage companies, facing the same decisions.
- **What it includes:** Comp ranges by role, stage, geography. Equity benchmarks. Benefits benchmarks.
- **CTA:** Placeholder button ("Coming Soon" or "Get the Report") — report is currently being built.
- **Design:** Could feature a mockup/preview of the report cover or a few sample data points.

### 7. Peer Support

- **Section label:** "THE COMMUNITY"
- **Headline:** Something like "You're not the only one having this conversation."
- **Body:** Pavilion members support each other through comp negotiations, role transitions, and career decisions. When you're preparing for a big conversation, you have hundreds of peers who've been there.
- **Design:** Keep it light — this is a supporting section, not a pillar. A short paragraph, maybe a quote or two from members.

### 8. Urgency Closer

- **Headline:** "Your next negotiation is coming."
- **Subhead:** "Whether it's a new role, an annual review, or an exit — the preparation starts now."
- **Secondary CTA for prospects:** Small text link below the main CTA — "Not a member? Join Pavilion →" linking to joinpavilion.com.
- **CTA:** "Book a Call" (Calendly)
- **Design:** Dark background section (like AI GTM final CTA). Clean, punchy, one CTA button.

## Technical Approach

- **Single HTML file** — self-contained, same as AI GTM Bundle
- **Pavilion brand system** — same CSS variables, fonts (Poppins), colors (--pav-blue, --pav-pink)
- **Responsive** — mobile-first, follows same CSS grid collapse pattern as AI GTM Bundle
- **CTA:** Calendly link (single shared link for all Book a Call buttons)
- **Video:** Hidden embed container ready for a hosted URL; founder note visible by default
- **Deploy:** Netlify via CLI

## Open Items

- [ ] Calendly link for coaching sessions
- [ ] Next cohort date for the class
- [ ] Benchmark report URL (currently being built — placeholder CTA for now)
- [ ] Video hosting URL when available (founder note is the default until then)

## Design References

- **Primary template:** AI GTM Bundle page (`/Users/joshmait/Desktop/Claude/AI Offer/index.html`)
- **Brand:** Pavilion brand guidelines (deep blue, pink, Poppins font, clean/premium feel)
- **Tone:** Highbrow but accessible. Empowering, not fear-based. Confident, not salesy.

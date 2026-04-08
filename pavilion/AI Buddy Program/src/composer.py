"""Claude-powered email composer for AI Buddy Program.

Handles: intro emails, check-in emails, no-match-yet emails, and launch emails.
"""

from __future__ import annotations
import anthropic
from src.matcher import ProposedMatch, BuddyRequest


def compose_intro(match: ProposedMatch, program_description: str, client: anthropic.Anthropic) -> str:
    """Write a warm, personalized intro email for a matched pair."""
    a = match.person_a
    b = match.person_b

    # Member context
    member_context = ""
    if not a.is_member and not b.is_member:
        member_context = "Neither person is currently a Pavilion member. Include a single natural, non-pushy line at the end mentioning that this program gives them a taste of the Pavilion community."
    elif a.is_member != b.is_member:
        non_member = a if not a.is_member else b
        member_context = f"{non_member.first_name} is not yet a Pavilion member. Include a single natural, non-pushy line at the end mentioning that this program gives non-members a feel for the Pavilion community."

    # Location context
    if a.city.lower() == b.city.lower() and a.city:
        geo_line = f"Both are based in {a.city}."
    elif a.timezone == b.timezone:
        geo_line = f"Both are in the {a.timezone} timezone. {a.first_name} is in {a.city}, {b.first_name} is in {b.city}."
    else:
        geo_line = f"{a.first_name} is in {a.city} ({a.timezone}), {b.first_name} is in {b.city} ({b.timezone})."

    # Engagement context
    shared_eng = set(s.lower() for s in a.engagement_styles) & set(s.lower() for s in b.engagement_styles)
    if shared_eng:
        eng_line = f"Both prefer: {', '.join(shared_eng)}."
    else:
        eng_line = f"{a.first_name} prefers {', '.join(a.engagement_styles) or 'flexible'}. {b.first_name} prefers {', '.join(b.engagement_styles) or 'flexible'}."

    prompt = f"""You are writing a short, warm introduction email on behalf of Josh Mait, Head of Marketing at Pavilion.

You are introducing two people matched through Pavilion's AI Buddy Program.

WHAT THE PROGRAM IS:
{program_description}

PERSON A:
Name: {a.name}
Function: {a.function}
Company: {a.company} ({a.revenue_stage} revenue)
AI Experience: {a.ai_level}
{"Notes: " + a.notes if a.notes else ""}

PERSON B:
Name: {b.name}
Function: {b.function}
Company: {b.company} ({b.revenue_stage} revenue)
AI Experience: {b.ai_level}
{"Notes: " + b.notes if b.notes else ""}

GEO CONTEXT:
{geo_line}

ENGAGEMENT PREFERENCES:
{eng_line}

MATCH BASIS:
{match.match_basis} (Tier {match.match_tier} match, score: {match.match_score})

{member_context}

WRITING INSTRUCTIONS:
- Address both people by first name in the opening (e.g. "Hey Sarah and Marcus,")
- 3-4 short paragraphs maximum
- Explain what they have in common and why the match makes sense (function, company stage, shared interests)
- Mention their shared engagement preference and suggest a concrete first step based on it
- Describe the program vibe in 1-2 sentences: peer-to-peer, no pressure, no stupid questions
- End with a short handoff line like "Over to you two."
- Sign off as Josh Mait, Head of Marketing, Pavilion
- Tone: warm but not gushing. Direct. Human. Not corporate.
- No em dashes. Short sentences. Active voice.
- Do not mention money, pricing, or membership costs.

Output ONLY the email body. No subject line. No extra commentary."""

    msg = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=600,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text.strip()


def make_subject(match: ProposedMatch) -> str:
    """Generate subject line for intro email."""
    return f"Introducing {match.person_a.first_name} and {match.person_b.first_name} — Pavilion AI Buddy"


def compose_check_in(
    person: BuddyRequest,
    buddy_name: str,
    check_type: str,
    day: int,
    client: anthropic.Anthropic,
) -> tuple[str, str]:
    """Write a check-in email. Returns (subject, body).

    check_type: 'connection_check' | 'pulse_check' | 'decision_point'
    """
    templates = {
        "connection_check": {
            "subject": f"Quick check — did you connect with {buddy_name}?",
            "prompt": f"""Write a very short (3-4 sentences) check-in email from Josh Mait at Pavilion.

It's been about a week since {person.first_name} was matched with {buddy_name} in the AI Buddy Program.

Ask if they've had a chance to connect. If not, encourage them to send a quick message. Keep it light and casual. No pressure.

Include a simple call to action: reply "Yes" if they've connected, "Not yet" if they haven't, or "Need help" if something's off.

Sign off as Josh. Tone: friendly, brief, human."""
        },
        "pulse_check": {
            "subject": f"How's it going with {buddy_name}?",
            "prompt": f"""Write a very short (3-4 sentences) check-in email from Josh Mait at Pavilion.

It's been about 4 weeks since {person.first_name} was matched with {buddy_name} in the AI Buddy Program.

Ask how it's going. Quick 1-5 rating (1 = not great, 5 = awesome). Any feedback is welcome.

Sign off as Josh. Tone: casual, brief. Not a survey — a human checking in."""
        },
        "decision_point": {
            "subject": f"Your AI Buddy — keep, switch, or add?",
            "prompt": f"""Write a short (4-5 sentences) email from Josh Mait at Pavilion.

It's been 8 weeks since {person.first_name} was matched with {buddy_name} in the AI Buddy Program.

Present three options:
1. Keep your buddy — you're vibing, stay together
2. New match — try someone different
3. Add a second buddy — keep {buddy_name} AND get matched with someone new

Make it clear there's no wrong answer. This isn't a breakup — it's a checkpoint.

Sign off as Josh. Tone: light, no pressure, encouraging."""
        },
    }

    template = templates.get(check_type, templates["connection_check"])

    msg = client.messages.create(
        model="claude-sonnet-4-20250514",
        max_tokens=400,
        messages=[{"role": "user", "content": template["prompt"]}],
    )
    return template["subject"], msg.content[0].text.strip()


def compose_quarterly_pulse(person_name: str, buddy_name: str) -> tuple[str, str]:
    """Quarterly check-in for long-term pairs."""
    first_name = person_name.split()[0] if person_name else "there"
    subject = f"Quick check-in — how's it going with {buddy_name}?"
    body = f"""Hey {first_name},

Just a quick quarterly pulse on your AI Buddy pairing with {buddy_name}.

Still getting value from the connection? Want to keep going, add a second buddy, or try someone new?

Reply with:
• "Keep" — all good, carry on
• "New" — match me with someone different
• "Add" — keep {buddy_name} AND get a second buddy

No wrong answer. Just want to make sure this stays useful for you.

Josh Mait
Head of Marketing, Pavilion"""
    return subject, body


def compose_no_match_email(person: BuddyRequest) -> tuple[str, str]:
    """Static email for when no match is available yet."""
    subject = f"We're finding the right match for you, {person.first_name}"
    body = f"""Hey {person.first_name},

Thanks for signing up for the AI Buddy Program. We want to make sure your match is a great one — not just a quick one.

We're looking for someone in {person.function} at a similar company stage who wants to engage the same way you do. We haven't found the right person yet, but every new signup makes the pool stronger.

As soon as we have a match, you'll hear from us. Shouldn't be long.

Josh Mait
Head of Marketing, Pavilion"""
    return subject, body


def compose_launch_email(person: BuddyRequest) -> tuple[str, str]:
    """Email sent when waitlist hits 100 and program launches."""
    subject = "Your AI Buddy match is coming"
    body = f"""Hey {person.first_name},

We hit our target — the AI Buddy Program is live.

You were one of the first to sign up, which means you're getting matched first. Over the next few days, we'll run the matching algorithm and pair you with a peer in {person.function} at a similar company stage.

You'll get an intro email from me connecting you with your buddy. From there, it's yours to run with.

Thanks for being early.

Josh Mait
Head of Marketing, Pavilion"""
    return subject, body


def compose_nonmember_nurture(person_name: str, buddy_name: str) -> tuple[str, str]:
    """Week 8 email for non-members — tasteful path to membership."""
    first_name = person_name.split()[0] if person_name else "there"
    subject = f"{first_name}, a quick note from Pavilion"
    body = f"""Hey {first_name},

It's been about two months since you and {buddy_name} got connected through the AI Buddy Program. Hope it's been useful.

The buddy program is one small piece of what Pavilion members get access to. The full membership includes executive compensation coaching, live classes, benchmark data, local events, and a community of 10,000+ GTM leaders who share what's actually working.

If you've gotten value from the buddy program, membership is where it goes deeper.

No pressure. Just wanted you to know the door is open.

https://www.joinpavilion.com

Josh Mait
Head of Marketing, Pavilion"""
    return subject, body


def compose_ghost_alert(alerts: list[dict]) -> tuple[str, str]:
    """Weekly digest email to Josh flagging unresponsive matches."""
    subject = f"AI Buddy Program — {len(alerts)} unresponsive match(es) need review"
    lines = ["The following people haven't responded to their check-in emails after 14+ days:\n"]
    for a in alerts:
        lines.append(f"• {a['person_name']} ({a['person_email']}) — buddy: {a['buddy_name']}")
        lines.append(f"  Check-in type: {a['check_type']} · {a['days_since_checkin']} days since sent")
        lines.append("")
    lines.append("Review these and decide: nudge them manually, rematch, or leave alone.")
    lines.append("\n— AI Buddy System")
    body = "\n".join(lines)
    return subject, body

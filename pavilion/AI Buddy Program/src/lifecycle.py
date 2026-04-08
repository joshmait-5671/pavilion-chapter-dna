"""Lifecycle manager for AI Buddy Program.

Handles scheduled check-ins at Week 1, 4, and 8.
Processes responses and triggers rematching when needed.
"""

from __future__ import annotations
from datetime import datetime, timedelta
from src.matcher import BuddyRequest
import anthropic


def get_pending_check_ins(
    matches: list[dict],
    lifecycle_records: list[dict],
    check_in_schedule: list[dict],
) -> list[dict]:
    """Find all check-ins that are due but haven't been sent yet.

    Args:
        matches: All rows from the Matches tab (with Intro Sent = Yes)
        lifecycle_records: All rows from the Lifecycle tab
        check_in_schedule: From config — list of {day, type, message, options}

    Returns list of dicts with: match_id, person_email, person_name, buddy_name,
    check_type, day
    """
    # Build set of already-sent check-ins: (match_id, person_email, check_type)
    sent = set()
    for rec in lifecycle_records:
        key = (
            rec.get("Match ID", "").strip(),
            rec.get("Person Email", "").strip().lower(),
            rec.get("Check Type", "").strip(),
        )
        sent.add(key)

    pending = []
    today = datetime.utcnow().date()

    for match in matches:
        if match.get("Intro Sent", "").strip().lower() != "yes":
            continue

        match_date_str = match.get("Date Sent", "").strip()
        if not match_date_str:
            continue

        try:
            match_date = datetime.strptime(match_date_str[:10], "%Y-%m-%d").date()
        except ValueError:
            continue

        match_id = match.get("Match ID", "").strip()
        days_since_match = (today - match_date).days

        # Check each person in the match
        for person_key, buddy_key in [("Person A", "Person B"), ("Person B", "Person A")]:
            person_email = match.get(f"{person_key} Email", "").strip()
            person_name = match.get(f"{person_key} Name", "").strip()
            buddy_name = match.get(f"{buddy_key} Name", "").strip()

            for check in check_in_schedule:
                if days_since_match >= check["day"]:
                    key = (match_id, person_email.lower(), check["type"])
                    if key not in sent:
                        pending.append({
                            "match_id": match_id,
                            "person_email": person_email,
                            "person_name": person_name,
                            "buddy_name": buddy_name,
                            "check_type": check["type"],
                            "day": check["day"],
                        })

    return pending


def process_response(
    response: str,
    check_type: str,
    match_id: str,
    person_email: str,
) -> dict:
    """Process a check-in response and determine next action.

    Returns dict with:
        action: 'none' | 'flag_for_help' | 'rematch' | 'add_buddy' | 'keep'
        notes: str
    """
    response_lower = response.strip().lower()

    if check_type == "connection_check":
        if response_lower in ("yes", "y"):
            return {"action": "none", "notes": "Connected successfully"}
        elif "help" in response_lower:
            return {"action": "flag_for_help", "notes": "Requested help connecting"}
        else:
            return {"action": "none", "notes": "Not yet connected — will follow up"}

    elif check_type == "pulse_check":
        try:
            rating = int(response_lower[0])
            if rating <= 2:
                return {"action": "flag_for_help", "notes": f"Rating: {rating}/5 — may need rematch"}
            else:
                return {"action": "none", "notes": f"Rating: {rating}/5"}
        except (ValueError, IndexError):
            return {"action": "none", "notes": f"Response: {response}"}

    elif check_type == "decision_point":
        if "keep" in response_lower:
            return {"action": "keep", "notes": "Keeping current buddy"}
        elif "new" in response_lower or "switch" in response_lower:
            return {"action": "rematch", "notes": "Wants a new match"}
        elif "add" in response_lower or "second" in response_lower:
            return {"action": "add_buddy", "notes": "Wants to add a second buddy"}
        else:
            return {"action": "none", "notes": f"Response: {response}"}

    return {"action": "none", "notes": f"Unknown check type: {check_type}"}


def get_ghost_alerts(
    matches: list[dict],
    lifecycle_records: list[dict],
    ghost_threshold_days: int = 14,
) -> list[dict]:
    """Find matches where a Week 1 check-in was sent but got no response
    after ghost_threshold_days. These need human review.

    Returns list of dicts with: match_id, person_email, person_name,
    buddy_name, days_since_checkin, check_type
    """
    # Build lookup: (match_id, person_email, check_type) → sent_date
    sent_checkins = {}
    responded = set()

    for rec in lifecycle_records:
        key = (
            rec.get("Match ID", "").strip(),
            rec.get("Person Email", "").strip().lower(),
            rec.get("Check Type", "").strip(),
        )
        sent_date = rec.get("Sent Date", "").strip()
        response = rec.get("Response", "").strip()

        if sent_date:
            sent_checkins[key] = {
                "sent_date": sent_date,
                "person_name": rec.get("Person Name", "").strip(),
                "buddy_name": rec.get("Buddy Name", "").strip(),
                "match_id": rec.get("Match ID", "").strip(),
                "person_email": rec.get("Person Email", "").strip(),
                "check_type": rec.get("Check Type", "").strip(),
            }
        if response:
            responded.add(key)

    alerts = []
    today = datetime.utcnow().date()

    for key, info in sent_checkins.items():
        if key in responded:
            continue

        try:
            sent_date = datetime.strptime(info["sent_date"][:10], "%Y-%m-%d").date()
        except ValueError:
            continue

        days_since = (today - sent_date).days
        if days_since >= ghost_threshold_days:
            alerts.append({
                "match_id": info["match_id"],
                "person_email": info["person_email"],
                "person_name": info["person_name"],
                "buddy_name": info["buddy_name"],
                "days_since_checkin": days_since,
                "check_type": info["check_type"],
            })

    return alerts


def get_quarterly_pulse_due(
    matches: list[dict],
    lifecycle_records: list[dict],
) -> list[dict]:
    """Find long-term pairs that need a quarterly check-in.

    These are pairs where:
    - Intro was sent
    - The Week 8 decision_point was sent AND responded to with 'keep'
    - It's been 90+ days since the last check-in of any kind
    """
    today = datetime.utcnow().date()

    # Build lookup of decision_point responses
    kept_pairs = set()  # (match_id, person_email) that chose "keep"
    last_checkin_date = {}  # (match_id, person_email) → most recent sent date

    for rec in lifecycle_records:
        match_id = rec.get("Match ID", "").strip()
        person_email = rec.get("Person Email", "").strip().lower()
        check_type = rec.get("Check Type", "").strip()
        response = rec.get("Response", "").strip().lower()
        sent_date = rec.get("Sent Date", "").strip()

        key = (match_id, person_email)

        # Track if they chose to keep
        if check_type == "decision_point" and "keep" in response:
            kept_pairs.add(key)

        # Track latest check-in date
        if sent_date:
            try:
                d = datetime.strptime(sent_date[:10], "%Y-%m-%d").date()
                if key not in last_checkin_date or d > last_checkin_date[key]:
                    last_checkin_date[key] = d
            except ValueError:
                pass

    # Also check for quarterly_pulse already sent
    sent_quarterly = set()
    for rec in lifecycle_records:
        if rec.get("Check Type", "").strip() == "quarterly_pulse":
            sent_date = rec.get("Sent Date", "").strip()
            if sent_date:
                key = (rec.get("Match ID", "").strip(), rec.get("Person Email", "").strip().lower())
                try:
                    d = datetime.strptime(sent_date[:10], "%Y-%m-%d").date()
                    if key not in last_checkin_date or d > last_checkin_date[key]:
                        last_checkin_date[key] = d
                except ValueError:
                    pass

    pending = []
    for match in matches:
        if match.get("Intro Sent", "").strip().lower() != "yes":
            continue

        match_id = match.get("Match ID", "").strip()

        for person_key, buddy_key in [("Person A", "Person B"), ("Person B", "Person A")]:
            person_email = match.get(f"{person_key} Email", "").strip().lower()
            key = (match_id, person_email)

            if key not in kept_pairs:
                continue

            last_date = last_checkin_date.get(key)
            if not last_date:
                continue

            days_since = (today - last_date).days
            if days_since >= 90:
                pending.append({
                    "match_id": match_id,
                    "person_email": match.get(f"{person_key} Email", "").strip(),
                    "person_name": match.get(f"{person_key} Name", "").strip(),
                    "buddy_name": match.get(f"{buddy_key} Name", "").strip(),
                    "days_since_last": days_since,
                })

    return pending

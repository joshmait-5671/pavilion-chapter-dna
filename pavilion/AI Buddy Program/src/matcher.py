"""AI Buddy matching algorithm v2.

Matches on: function (required), revenue stage (required), location/timezone,
engagement style, AI experience level. Supports tiered fallback matching
and multiple buddy accumulation.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional
import uuid


@dataclass
class BuddyRequest:
    row_index: int
    first_name: str
    last_name: str
    email: str
    function: str
    company: str
    revenue_stage: str
    revenue_rank: int          # 1-4
    city: str
    timezone: str
    ai_level: str
    ai_level_rank: int         # 1-3
    engagement_styles: list[str] = field(default_factory=list)
    is_member: bool = False
    notes: str = ""
    status: str = "Unmatched"
    existing_buddies: list[str] = field(default_factory=list)  # emails of current buddies
    entered_pool_date: str = ""  # ISO date when they entered/re-entered the pool

    @property
    def name(self) -> str:
        return f"{self.first_name} {self.last_name}".strip()


@dataclass
class ProposedMatch:
    match_id: str
    person_a: BuddyRequest
    person_b: BuddyRequest
    match_basis: str
    match_score: int
    match_tier: int            # 1-4
    approval_status: str = "Pending Approval"


# ── LEVEL / STAGE RANKS ──────────────────────────────────────

_AI_LEVEL_RANKS = {
    "Getting started": 1,
    "Just starting out": 1,  # backward compat
    "Using it regularly": 2,
    "Building with it": 3,
}

_REVENUE_RANKS = {
    "Less than $10M": 1,
    "$10M – $25M": 2,
    "$25M – $50M": 3,
    "$50M+": 4,
}

# Timezone groupings for "same timezone" matching
_TIMEZONE_GROUPS = {
    "Eastern (ET)": "US_East",
    "Central (CT)": "US_East",
    "Mountain (MT)": "US_West",
    "Pacific (PT)": "US_West",
    "Other US": "US_Other",
    "Europe": "International",
    "Asia-Pacific": "International",
    "Other": "International",
}


# ── PARSING ───────────────────────────────────────────────────

def parse_requests(rows: list[dict], include_statuses: list[str] = None) -> list[BuddyRequest]:
    """Convert sheet rows into BuddyRequest objects.

    By default, only includes rows with status 'Unmatched' or 'Seeking New Buddy'.
    Pass include_statuses to override.
    """
    if include_statuses is None:
        include_statuses = ["unmatched", "seeking new buddy", "seeking additional buddy"]

    requests = []
    for i, row in enumerate(rows, start=2):
        status = row.get("Status", "Unmatched").strip().lower()
        if status not in include_statuses:
            continue

        ai_level = row.get("AI Experience Level", "Getting started").strip()
        revenue = row.get("Company Revenue", "Less than $10M").strip()

        # Parse engagement styles (comma-separated in sheet)
        eng_raw = row.get("Engagement Style", "").strip()
        engagement = [s.strip() for s in eng_raw.split(",") if s.strip()] if eng_raw else []

        # Parse existing buddies (comma-separated emails)
        buddies_raw = row.get("Current Buddies", "").strip()
        existing = [e.strip() for e in buddies_raw.split(",") if e.strip()] if buddies_raw else []

        requests.append(BuddyRequest(
            row_index=i,
            first_name=row.get("First Name", "").strip(),
            last_name=row.get("Last Name", "").strip(),
            email=row.get("Email", "").strip(),
            function=row.get("Function", "").strip(),
            company=row.get("Company", "").strip(),
            revenue_stage=revenue,
            revenue_rank=_REVENUE_RANKS.get(revenue, 1),
            city=row.get("City", "").strip(),
            timezone=row.get("Timezone", "").strip(),
            ai_level=ai_level,
            ai_level_rank=_AI_LEVEL_RANKS.get(ai_level, 1),
            engagement_styles=engagement,
            is_member=row.get("Pavilion Member?", "No").strip().lower() in ("yes", "y", "true", "1"),
            notes=row.get("Notes", "").strip(),
            status=row.get("Status", "Unmatched").strip(),
            existing_buddies=existing,
            entered_pool_date=row.get("Pool Entry Date", "").strip(),
        ))
    return requests


# ── SCORING ───────────────────────────────────────────────────

def _same_function(a: BuddyRequest, b: BuddyRequest) -> bool:
    return a.function.strip().lower() == b.function.strip().lower()


def _same_revenue(a: BuddyRequest, b: BuddyRequest) -> bool:
    return a.revenue_rank == b.revenue_rank


def _same_city(a: BuddyRequest, b: BuddyRequest) -> bool:
    if not a.city or not b.city:
        return False
    return a.city.strip().lower() == b.city.strip().lower()


def _same_timezone(a: BuddyRequest, b: BuddyRequest) -> bool:
    group_a = _TIMEZONE_GROUPS.get(a.timezone, a.timezone)
    group_b = _TIMEZONE_GROUPS.get(b.timezone, b.timezone)
    return group_a == group_b and group_a != ""


def _engagement_overlap(a: BuddyRequest, b: BuddyRequest) -> int:
    """Return count of shared engagement preferences."""
    set_a = set(s.lower() for s in a.engagement_styles)
    set_b = set(s.lower() for s in b.engagement_styles)
    return len(set_a & set_b)


def _ai_level_gap(a: BuddyRequest, b: BuddyRequest) -> int:
    return abs(a.ai_level_rank - b.ai_level_rank)


def _already_buddies(a: BuddyRequest, b: BuddyRequest) -> bool:
    """Check if these two are already matched."""
    return (b.email.lower() in [e.lower() for e in a.existing_buddies] or
            a.email.lower() in [e.lower() for e in b.existing_buddies])


def score_pair(a: BuddyRequest, b: BuddyRequest, tier: int = 1) -> tuple[int, str, int]:
    """Score a potential pair at a given matching tier.

    Returns (score, match_basis, tier). Score of -1 means disqualified.

    Tier 1: All criteria
    Tier 2: Relax location to timezone
    Tier 3: Relax AI level to adjacent
    Tier 4: Function + revenue only
    """
    # Hard disqualifiers
    if a.email.lower() == b.email.lower():
        return -1, "", 0
    if not _same_function(a, b):
        return -1, "", 0
    if not _same_revenue(a, b):
        return -1, "", 0
    if _already_buddies(a, b):
        return -1, "", 0

    score = 0
    basis_parts = []
    matched_tier = 4  # Start at lowest, upgrade as criteria are met

    # Function (required) — 40 pts
    score += 40
    basis_parts.append(f"Function ({a.function})")

    # Revenue stage (required) — 30 pts
    score += 30
    basis_parts.append(f"Revenue ({a.revenue_stage})")

    # Location — city (20) or timezone (10)
    if _same_city(a, b):
        score += 20
        basis_parts.append(f"City ({a.city})")
    elif _same_timezone(a, b):
        score += 10
        basis_parts.append(f"Timezone ({a.timezone})")
    else:
        # No location match — can't be Tier 1 or 2
        if tier <= 2:
            # At tier 1-2, we need at least timezone
            pass  # Don't disqualify, just lower tier

    # Engagement style overlap — 15 pts if any overlap
    eng_overlap = _engagement_overlap(a, b)
    if eng_overlap > 0:
        score += 15
        basis_parts.append(f"Engagement overlap ({eng_overlap})")

    # AI level — same (15) or adjacent (5)
    gap = _ai_level_gap(a, b)
    if gap == 0:
        score += 15
        basis_parts.append("Same AI level")
    elif gap == 1:
        score += 5
        basis_parts.append("Adjacent AI level")
    else:
        # Gap of 2 — only allowed at Tier 4
        if tier <= 3:
            pass  # Don't disqualify, just can't be high tier

    # Member mix bonus — 5 pts
    if a.is_member != b.is_member:
        score += 5
        basis_parts.append("Member + non-member")

    # Determine actual tier based on what matched
    has_location = _same_city(a, b) or _same_timezone(a, b)
    has_city = _same_city(a, b)
    has_engagement = eng_overlap > 0
    has_same_ai = gap == 0
    has_close_ai = gap <= 1

    if has_city and has_engagement and has_same_ai:
        matched_tier = 1
    elif has_location and has_engagement and has_same_ai:
        matched_tier = 2
    elif has_location and has_close_ai:
        matched_tier = 3
    else:
        matched_tier = 4

    # Only return if this match meets the requested tier threshold
    if matched_tier > tier:
        return -1, "", 0

    return score, " · ".join(basis_parts), matched_tier


def run_matching(
    requests: list[BuddyRequest],
    max_tier: int = 4,
) -> list[ProposedMatch]:
    """Greedy matching: find highest-scoring pairs, respecting tier limits.

    Args:
        requests: List of unmatched buddy requests
        max_tier: Maximum tier to match at (1=perfect only, 4=accept anything)
    """
    matched_emails: set[str] = set()
    proposed: list[ProposedMatch] = []

    # Score all valid pairs
    scored_pairs: list[tuple[int, str, int, BuddyRequest, BuddyRequest]] = []
    for i, a in enumerate(requests):
        for b in requests[i + 1:]:
            score, basis, tier = score_pair(a, b, tier=max_tier)
            if score > 0:
                scored_pairs.append((score, basis, tier, a, b))

    # Sort by score descending
    scored_pairs.sort(key=lambda x: x[0], reverse=True)

    # Greedy assign
    for score, basis, tier, a, b in scored_pairs:
        a_key = a.email.lower()
        b_key = b.email.lower()

        # For "seeking additional buddy", allow matching even if already matched
        # For regular matching, skip if already matched this round
        if a.status.lower() != "seeking additional buddy" and a_key in matched_emails:
            continue
        if b.status.lower() != "seeking additional buddy" and b_key in matched_emails:
            continue

        matched_emails.add(a_key)
        matched_emails.add(b_key)

        proposed.append(ProposedMatch(
            match_id=str(uuid.uuid4())[:8].upper(),
            person_a=a,
            person_b=b,
            match_basis=basis,
            match_score=score,
            match_tier=tier,
        ))

    return proposed


def get_unmatched(requests: list[BuddyRequest], matched_emails: set[str]) -> list[BuddyRequest]:
    """Return people who couldn't be matched this round."""
    return [r for r in requests if r.email.lower() not in matched_emails]

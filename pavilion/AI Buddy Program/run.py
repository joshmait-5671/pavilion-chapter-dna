#!/usr/bin/env python3
"""
Pavilion AI Buddy Program — CLI Runner

Commands:
  setup     — Create Google Sheet tabs with correct headers
  status    — Show current program stats (waitlist, pool, matches)
  launch    — Move waitlist to active pool and run first matching batch
  propose   — Scan pool and propose new matches
  send      — Send intro emails for approved matches
  check-ins — Send due lifecycle check-ins (Week 1/4/8)
  daily     — Run the daily scan (propose for anyone waiting > tier threshold)
"""

import os
import sys
import click
import yaml
from dotenv import load_dotenv
from rich.console import Console
from rich.table import Table
from datetime import datetime

load_dotenv(override=True)
console = Console()


def _load_config() -> dict:
    config_path = os.path.join(os.path.dirname(__file__), "config", "buddy_program.yaml")
    with open(config_path) as f:
        return yaml.safe_load(f)


def _get_sheets():
    from src.sheets import get_sheets_client, open_spreadsheet
    sa_path = os.getenv("GOOGLE_SERVICE_ACCOUNT_PATH", "auth/service_account.json")
    gc = get_sheets_client(sa_path)
    sheet_id = os.getenv("SPREADSHEET_ID")
    sh = open_spreadsheet(gc, sheet_id)
    return gc, sh


@click.group()
def cli():
    """Pavilion AI Buddy Program"""
    pass


# ── SETUP ─────────────────────────────────────────────────────

@cli.command()
def setup():
    """Create Google Sheet with all required tabs."""
    from src.sheets import setup_all_tabs
    _, sh = _get_sheets()
    tabs = setup_all_tabs(sh)
    console.print(f"\n[bold green]Setup complete.[/]")
    console.print(f"Spreadsheet: https://docs.google.com/spreadsheets/d/{sh.id}")
    for name in tabs:
        console.print(f"  ✓ {name}")


# ── STATUS ────────────────────────────────────────────────────

@cli.command()
def status():
    """Show current program statistics."""
    _, sh = _get_sheets()
    cfg = _load_config()

    try:
        waitlist = sh.worksheet("Waitlist").get_all_records()
    except Exception:
        waitlist = []

    try:
        requests = sh.worksheet("Requests").get_all_records()
    except Exception:
        requests = []

    try:
        matches = sh.worksheet("Matches").get_all_records()
    except Exception:
        matches = []

    waitlisted = len([r for r in waitlist if r.get("Status", "").strip().lower() in ("waitlisted", "")])
    unmatched = len([r for r in requests if r.get("Status", "").strip().lower() == "unmatched"])
    matched = len([r for r in requests if r.get("Status", "").strip().lower() == "matched"])
    seeking_new = len([r for r in requests if "seeking" in r.get("Status", "").strip().lower()])
    total_matches = len([m for m in matches if m.get("Intro Sent", "").strip().lower() == "yes"])
    pending_approval = len([m for m in matches if m.get("Approval", "").strip().lower() == "pending approval"])

    target = cfg["launch"]["target_signups"]
    program_status = cfg["launch"]["status"]

    console.print(f"\n[bold]AI Buddy Program Status[/]")
    console.print(f"  Program: [{'green' if program_status == 'live' else 'yellow'}]{program_status}[/]")
    console.print(f"  Waitlist: {waitlisted} / {target} target")
    console.print(f"  Active pool: {unmatched} unmatched, {seeking_new} seeking new/additional")
    console.print(f"  Matched: {matched} people in active pairs")
    console.print(f"  Total matches sent: {total_matches}")
    if pending_approval:
        console.print(f"  [yellow]Pending approval: {pending_approval}[/]")
    console.print()


# ── LAUNCH ────────────────────────────────────────────────────

@cli.command()
@click.option("--force", is_flag=True, help="Launch even if under target signups")
def launch(force):
    """Move waitlist to active pool and run first matching batch."""
    from src.sheets import move_waitlist_to_requests
    _, sh = _get_sheets()
    cfg = _load_config()

    waitlist = sh.worksheet("Waitlist").get_all_records()
    waitlisted = len([r for r in waitlist if r.get("Status", "").strip().lower() in ("waitlisted", "")])
    target = cfg["launch"]["target_signups"]

    if waitlisted < target and not force:
        console.print(f"[yellow]Only {waitlisted}/{target} signups. Use --force to launch anyway.[/]")
        return

    console.print(f"[bold]Launching AI Buddy Program![/]")
    console.print(f"  Moving {waitlisted} waitlist entries to active pool...")

    moved = move_waitlist_to_requests(sh)
    console.print(f"  [green]✓[/] Moved {moved} people to active pool.")

    # Send launch emails to everyone who was just promoted
    from src.composer import compose_launch_email
    from src.matcher import parse_requests, BuddyRequest
    from src.emailer import get_gmail_service, send_email

    requests_ws = sh.worksheet("Requests")
    all_rows = requests_ws.get_all_records()
    all_requests = parse_requests(all_rows, include_statuses=["unmatched"])

    if all_requests:
        gmail = get_gmail_service(
            os.getenv("GMAIL_TOKEN_PATH", "auth/gmail_token.json"),
            os.getenv("GMAIL_CREDENTIALS_PATH", "auth/client_secrets.json"),
        )
        console.print(f"\n  Sending launch emails to {len(all_requests)} people...")
        for req in all_requests:
            try:
                subject, body = compose_launch_email(req)
                send_email(
                    service=gmail,
                    from_address=cfg["intro"]["sender_email"],
                    to_address=req.email,
                    subject=subject,
                    body=body,
                )
                console.print(f"    [green]✓[/] {req.name}")
            except Exception as e:
                console.print(f"    [red]✗[/] {req.name}: {e}")

    console.print(f"\n  Next: run [bold]python run.py propose[/] to generate matches.")


# ── PROPOSE ───────────────────────────────────────────────────

@cli.command()
@click.option("--tier", default=4, type=int, help="Max matching tier (1-4, default: 4)")
@click.option("--dry-run", is_flag=True, help="Preview matches without writing")
def propose(tier, dry_run):
    """Scan pool and propose new matches."""
    from src.matcher import parse_requests, run_matching

    _, sh = _get_sheets()
    requests_ws = sh.worksheet("Requests")
    matches_ws = sh.worksheet("Matches")

    all_rows = requests_ws.get_all_records()
    requests = parse_requests(all_rows)

    console.print(f"\n[bold]AI Buddy Matching[/]")
    console.print(f"  Pool size: {len(requests)}")
    console.print(f"  Max tier: {tier}")

    if len(requests) < 2:
        console.print("[yellow]  Not enough people in pool to match.[/]")
        return

    matches = run_matching(requests, max_tier=tier)
    console.print(f"  Proposed: {len(matches)} matches")

    if not matches:
        console.print("[yellow]  No matches found at this tier.[/]")
        return

    # Display
    table = Table(title="Proposed Matches", show_lines=True)
    table.add_column("ID", style="cyan", width=10)
    table.add_column("Person A", width=24)
    table.add_column("Person B", width=24)
    table.add_column("Basis", width=40)
    table.add_column("Tier", justify="center", width=5)
    table.add_column("Score", justify="right", width=7)

    for m in matches:
        table.add_row(
            m.match_id,
            f"{m.person_a.name}\n[dim]{m.person_a.function} · {m.person_a.revenue_stage}[/]",
            f"{m.person_b.name}\n[dim]{m.person_b.function} · {m.person_b.revenue_stage}[/]",
            m.match_basis,
            str(m.match_tier),
            str(m.match_score),
        )
    console.print(table)

    if dry_run:
        console.print("[yellow][DRY RUN] — not writing to sheet.[/]")
        return

    # Write to Matches tab
    existing_ids = set(row.get("Match ID", "") for row in matches_ws.get_all_records())
    new_rows = []
    for m in matches:
        if m.match_id in existing_ids:
            continue
        new_rows.append([
            m.match_id,
            m.person_a.name, m.person_a.email, m.person_a.function,
            m.person_b.name, m.person_b.email, m.person_b.function,
            m.match_basis, m.match_score, m.match_tier,
            "Pending Approval", "", "",
            datetime.utcnow().strftime("%Y-%m-%d"), "",
        ])

    if new_rows:
        matches_ws.append_rows(new_rows, value_input_option="USER_ENTERED")
        console.print(f"\n[green]✓[/] {len(new_rows)} matches written to sheet.")
        console.print(f"  Review in Google Sheet → change Approval to 'Approved'")
        console.print(f"  Then run: [bold]python run.py send[/]")


# ── SEND ──────────────────────────────────────────────────────

@cli.command()
@click.option("--dry-run", is_flag=True, help="Preview emails without sending")
def send(dry_run):
    """Send intro emails for approved matches."""
    from src.matcher import parse_requests, BuddyRequest
    from src.composer import compose_intro, make_subject
    from src.emailer import get_gmail_service, send_email
    import anthropic

    cfg = _load_config()
    _, sh = _get_sheets()

    requests_ws = sh.worksheet("Requests")
    matches_ws = sh.worksheet("Matches")

    client = anthropic.Anthropic()
    gmail = get_gmail_service(
        os.getenv("GMAIL_TOKEN_PATH", "auth/gmail_token.json"),
        os.getenv("GMAIL_CREDENTIALS_PATH", "auth/client_secrets.json"),
    )

    match_rows = matches_ws.get_all_records()
    request_rows = requests_ws.get_all_records()

    # Build lookup
    all_requests = parse_requests(request_rows, include_statuses=None)  # Include all
    # Re-parse without status filter for lookup
    email_to_request = {}
    for req in all_requests:
        email_to_request[req.email.lower()] = req
    # Also parse all rows regardless of status for email lookup
    for i, row in enumerate(request_rows, start=2):
        email = row.get("Email", "").strip().lower()
        if email and email not in email_to_request:
            from src.matcher import BuddyRequest, _AI_LEVEL_RANKS, _REVENUE_RANKS
            ai_level = row.get("AI Experience Level", "Getting started").strip()
            revenue = row.get("Company Revenue", "Less than $10M").strip()
            eng_raw = row.get("Engagement Style", "").strip()
            engagement = [s.strip() for s in eng_raw.split(",") if s.strip()] if eng_raw else []
            email_to_request[email] = BuddyRequest(
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
                is_member=row.get("Pavilion Member?", "No").strip().lower() in ("yes", "y"),
                notes=row.get("Notes", "").strip(),
                status=row.get("Status", "").strip(),
            )

    email_to_row_index = {
        row.get("Email", "").strip().lower(): i + 2
        for i, row in enumerate(request_rows)
    }

    approved = [
        (i + 2, row) for i, row in enumerate(match_rows)
        if row.get("Approval", "").strip().lower() == "approved"
        and not row.get("Intro Sent", "").strip()
    ]

    if not approved:
        console.print("[yellow]No approved matches pending intro emails.[/]")
        return

    console.print(f"\n[bold]Sending {len(approved)} intro email(s)...[/]\n")

    for sheet_row_idx, match_row in approved:
        email_a = match_row["Person A Email"].strip().lower()
        email_b = match_row["Person B Email"].strip().lower()
        match_id = match_row["Match ID"]

        req_a = email_to_request.get(email_a)
        req_b = email_to_request.get(email_b)

        if not req_a or not req_b:
            console.print(f"  [red]{match_id}:[/] Missing request records — skipping")
            continue

        from src.matcher import ProposedMatch
        match = ProposedMatch(
            match_id=match_id,
            person_a=req_a,
            person_b=req_b,
            match_basis=match_row.get("Match Basis", ""),
            match_score=int(match_row.get("Match Score", 0)),
            match_tier=int(match_row.get("Match Tier", 4)),
        )

        console.print(f"  [{match_id}] {req_a.name} ↔ {req_b.name}")

        try:
            body = compose_intro(match, cfg["intro"]["program_description"], client)
            subject = make_subject(match)
        except Exception as e:
            console.print(f"    [red]Compose error:[/] {e}")
            continue

        if dry_run:
            console.print(f"    [yellow][DRY RUN][/] Subject: {subject}")
            console.print(f"    Preview: {body[:200]}...")
            continue

        try:
            send_email(
                service=gmail,
                from_address=cfg["intro"]["sender_email"],
                to_address=req_a.email,
                cc_address=req_b.email,
                subject=subject,
                body=body,
            )

            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M")

            # Update Matches tab
            from src.sheets import MATCHES_HEADERS
            intro_sent_col = MATCHES_HEADERS.index("Intro Sent") + 1
            date_sent_col = MATCHES_HEADERS.index("Date Sent") + 1
            matches_ws.update_cell(sheet_row_idx, intro_sent_col, "Yes")
            matches_ws.update_cell(sheet_row_idx, date_sent_col, now)

            # Update Requests tab for both people
            from src.sheets import REQUESTS_HEADERS
            status_col = REQUESTS_HEADERS.index("Status") + 1
            match_id_col = REQUESTS_HEADERS.index("Match ID") + 1
            date_matched_col = REQUESTS_HEADERS.index("Date Matched") + 1
            for email in (email_a, email_b):
                req_row = email_to_row_index.get(email)
                if req_row:
                    requests_ws.update_cell(req_row, status_col, "Matched")
                    requests_ws.update_cell(req_row, match_id_col, match_id)
                    requests_ws.update_cell(req_row, date_matched_col, now)

            console.print(f"    [green]✓[/] Intro sent")

        except Exception as e:
            console.print(f"    [red]Send error:[/] {e}")

    if not dry_run:
        console.print(f"\n[bold green]Done.[/]")


# ── CHECK-INS ─────────────────────────────────────────────────

@cli.command(name="check-ins")
@click.option("--dry-run", is_flag=True, help="Preview without sending")
def check_ins(dry_run):
    """Send due lifecycle check-ins (Week 1/4/8)."""
    from src.lifecycle import get_pending_check_ins
    from src.composer import compose_check_in
    from src.emailer import get_gmail_service, send_email
    import anthropic

    cfg = _load_config()
    _, sh = _get_sheets()

    matches = sh.worksheet("Matches").get_all_records()
    try:
        lifecycle_ws = sh.worksheet("Lifecycle")
        lifecycle_records = lifecycle_ws.get_all_records()
    except Exception:
        from src.sheets import ensure_tab, LIFECYCLE_HEADERS
        lifecycle_ws = ensure_tab(sh, "Lifecycle", LIFECYCLE_HEADERS)
        lifecycle_records = []

    schedule = cfg["lifecycle"]["check_ins"]
    pending = get_pending_check_ins(matches, lifecycle_records, schedule)

    if not pending:
        console.print("[green]No check-ins due.[/]")
        return

    console.print(f"\n[bold]{len(pending)} check-in(s) due[/]\n")

    client = anthropic.Anthropic()
    gmail = get_gmail_service(
        os.getenv("GMAIL_TOKEN_PATH", "auth/gmail_token.json"),
        os.getenv("GMAIL_CREDENTIALS_PATH", "auth/client_secrets.json"),
    )

    for item in pending:
        console.print(f"  {item['check_type']} → {item['person_name']} (buddy: {item['buddy_name']})")

        try:
            from src.matcher import BuddyRequest
            person = BuddyRequest(
                row_index=0, first_name=item["person_name"].split()[0],
                last_name=" ".join(item["person_name"].split()[1:]),
                email=item["person_email"], function="", company="",
                revenue_stage="", revenue_rank=0, city="", timezone="",
                ai_level="", ai_level_rank=0,
            )
            subject, body = compose_check_in(
                person, item["buddy_name"], item["check_type"], item["day"], client,
            )
        except Exception as e:
            console.print(f"    [red]Compose error:[/] {e}")
            continue

        if dry_run:
            console.print(f"    [yellow][DRY RUN][/] Subject: {subject}")
            continue

        try:
            send_email(
                service=gmail,
                from_address=cfg["intro"]["sender_email"],
                to_address=item["person_email"],
                subject=subject,
                body=body,
            )

            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
            lifecycle_ws.append_row([
                item["match_id"],
                item["person_email"],
                item["person_name"],
                item["buddy_name"],
                item["check_type"],
                item["day"],
                now,
                "",  # Response (filled when they reply)
                "",  # Response Date
            ], value_input_option="USER_ENTERED")

            console.print(f"    [green]✓[/] Sent")
        except Exception as e:
            console.print(f"    [red]Send error:[/] {e}")

    if not dry_run:
        console.print(f"\n[bold green]Done.[/]")


# ── DAILY ─────────────────────────────────────────────────────

@cli.command()
@click.option("--dry-run", is_flag=True)
def daily(dry_run):
    """Daily scan: check pool, propose matches at appropriate tier based on wait time."""
    from src.matcher import parse_requests, run_matching

    cfg = _load_config()
    _, sh = _get_sheets()
    requests_ws = sh.worksheet("Requests")

    all_rows = requests_ws.get_all_records()
    requests = parse_requests(all_rows)

    if len(requests) < 2:
        console.print("[yellow]Not enough people in pool.[/]")
        return

    today = datetime.utcnow().date()
    tier_schedule = cfg["matching"]["tier_schedule"]

    # Group by how long they've been waiting → determine max tier
    max_tier = 1
    for req in requests:
        if req.entered_pool_date:
            try:
                entry = datetime.strptime(req.entered_pool_date, "%Y-%m-%d").date()
                days_waiting = (today - entry).days
            except ValueError:
                days_waiting = 0
        else:
            days_waiting = 0

        if days_waiting >= tier_schedule.get("tier_4", 4):
            max_tier = max(max_tier, 4)
        elif days_waiting >= tier_schedule.get("tier_3", 2):
            max_tier = max(max_tier, 3)
        elif days_waiting >= tier_schedule.get("tier_2", 1):
            max_tier = max(max_tier, 2)

    console.print(f"\n[bold]Daily Scan[/]")
    console.print(f"  Pool: {len(requests)} · Max tier today: {max_tier}")

    matches = run_matching(requests, max_tier=max_tier)

    if matches:
        console.print(f"  Found: {len(matches)} new match(es)")
        # Delegate to propose logic
        if not dry_run:
            matches_ws = sh.worksheet("Matches")
            existing_ids = set(row.get("Match ID", "") for row in matches_ws.get_all_records())
            new_rows = []
            for m in matches:
                if m.match_id not in existing_ids:
                    new_rows.append([
                        m.match_id,
                        m.person_a.name, m.person_a.email, m.person_a.function,
                        m.person_b.name, m.person_b.email, m.person_b.function,
                        m.match_basis, m.match_score, m.match_tier,
                        "Pending Approval", "", "",
                        datetime.utcnow().strftime("%Y-%m-%d"), "",
                    ])
            if new_rows:
                matches_ws.append_rows(new_rows, value_input_option="USER_ENTERED")
                console.print(f"  [green]✓[/] {len(new_rows)} matches written.")
        else:
            console.print(f"  [yellow][DRY RUN][/]")
            for m in matches:
                console.print(f"    {m.person_a.name} ↔ {m.person_b.name} (T{m.match_tier}, {m.match_score}pts)")
    else:
        console.print(f"  No new matches at tier {max_tier}.")

    # Send no-match emails to people waiting 5+ days with no match
    from src.matcher import get_unmatched
    from src.composer import compose_no_match_email
    matched_emails = set()
    for m in matches:
        matched_emails.add(m.person_a.email.lower())
        matched_emails.add(m.person_b.email.lower())
    unmatched = get_unmatched(requests, matched_emails)

    # Check lifecycle tab for already-sent no-match emails
    try:
        lifecycle_ws = sh.worksheet("Lifecycle")
        lifecycle_records = lifecycle_ws.get_all_records()
    except Exception:
        from src.sheets import ensure_tab, LIFECYCLE_HEADERS
        lifecycle_ws = ensure_tab(sh, "Lifecycle", LIFECYCLE_HEADERS)
        lifecycle_records = []

    no_match_sent = set(
        rec.get("Person Email", "").strip().lower()
        for rec in lifecycle_records
        if rec.get("Check Type", "").strip() == "no_match_yet"
    )

    no_match_pending = []
    for req in unmatched:
        if req.email.lower() in no_match_sent:
            continue
        if req.entered_pool_date:
            try:
                entry = datetime.strptime(req.entered_pool_date, "%Y-%m-%d").date()
                if (today - entry).days >= 5:
                    no_match_pending.append(req)
            except ValueError:
                pass

    if no_match_pending and not dry_run:
        from src.emailer import get_gmail_service, send_email
        gmail = get_gmail_service(
            os.getenv("GMAIL_TOKEN_PATH", "auth/gmail_token.json"),
            os.getenv("GMAIL_CREDENTIALS_PATH", "auth/client_secrets.json"),
        )
        console.print(f"\n  Sending {len(no_match_pending)} 'still looking' email(s)...")
        for req in no_match_pending:
            try:
                subject, body = compose_no_match_email(req)
                send_email(
                    service=gmail,
                    from_address=cfg["intro"]["sender_email"],
                    to_address=req.email,
                    subject=subject,
                    body=body,
                )
                lifecycle_ws.append_row([
                    "", req.email, req.name, "",
                    "no_match_yet", 5,
                    datetime.utcnow().strftime("%Y-%m-%d %H:%M"), "", "",
                ], value_input_option="USER_ENTERED")
                console.print(f"    [green]✓[/] {req.name}")
            except Exception as e:
                console.print(f"    [red]✗[/] {req.name}: {e}")


# ── ALERTS ────────────────────────────────────────────────────

@cli.command()
@click.option("--dry-run", is_flag=True)
def alerts(dry_run):
    """Check for ghosted matches and email Josh a digest."""
    from src.lifecycle import get_ghost_alerts
    from src.composer import compose_ghost_alert
    from src.emailer import get_gmail_service, send_email

    cfg = _load_config()
    _, sh = _get_sheets()

    matches = sh.worksheet("Matches").get_all_records()
    try:
        lifecycle_records = sh.worksheet("Lifecycle").get_all_records()
    except Exception:
        lifecycle_records = []

    ghost_alerts = get_ghost_alerts(matches, lifecycle_records)

    if not ghost_alerts:
        console.print("[green]No ghost alerts. Everyone's responsive.[/]")
        return

    console.print(f"\n[bold yellow]{len(ghost_alerts)} unresponsive match(es) found[/]\n")
    for a in ghost_alerts:
        console.print(f"  ⚠ {a['person_name']} — {a['check_type']} sent {a['days_since_checkin']}d ago, no response")

    if dry_run:
        console.print("\n[yellow][DRY RUN] — not sending alert email.[/]")
        return

    subject, body = compose_ghost_alert(ghost_alerts)
    gmail = get_gmail_service(
        os.getenv("GMAIL_TOKEN_PATH", "auth/gmail_token.json"),
        os.getenv("GMAIL_CREDENTIALS_PATH", "auth/client_secrets.json"),
    )
    send_email(
        service=gmail,
        from_address=cfg["intro"]["sender_email"],
        to_address=cfg["intro"]["sender_email"],  # Send to Josh
        subject=subject,
        body=body,
    )
    console.print(f"\n[green]✓[/] Alert digest sent to {cfg['intro']['sender_email']}")


# ── NURTURE ───────────────────────────────────────────────────

@cli.command()
@click.option("--dry-run", is_flag=True)
def nurture(dry_run):
    """Send membership nurture emails to non-members at Week 8."""
    from src.composer import compose_nonmember_nurture
    from src.emailer import get_gmail_service, send_email

    cfg = _load_config()
    _, sh = _get_sheets()

    matches = sh.worksheet("Matches").get_all_records()
    requests = sh.worksheet("Requests").get_all_records()

    # Build member lookup
    email_is_member = {}
    for row in requests:
        email = row.get("Email", "").strip().lower()
        is_member = row.get("Pavilion Member?", "No").strip().lower() in ("yes", "y")
        email_is_member[email] = is_member

    try:
        lifecycle_records = sh.worksheet("Lifecycle").get_all_records()
    except Exception:
        lifecycle_records = []

    # Check which non-members have already received nurture
    nurtured = set()
    for rec in lifecycle_records:
        if rec.get("Check Type", "").strip() == "nonmember_nurture":
            nurtured.add(rec.get("Person Email", "").strip().lower())

    today = datetime.utcnow().date()
    pending = []

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

        days_since = (today - match_date).days
        if days_since < 56:  # Week 8
            continue

        for person_key, buddy_key in [("Person A", "Person B"), ("Person B", "Person A")]:
            email = match.get(f"{person_key} Email", "").strip().lower()
            if not email_is_member.get(email, True) and email not in nurtured:
                pending.append({
                    "match_id": match.get("Match ID", ""),
                    "person_email": match.get(f"{person_key} Email", "").strip(),
                    "person_name": match.get(f"{person_key} Name", "").strip(),
                    "buddy_name": match.get(f"{buddy_key} Name", "").strip(),
                })

    if not pending:
        console.print("[green]No non-member nurture emails due.[/]")
        return

    console.print(f"\n[bold]{len(pending)} non-member nurture email(s) due[/]\n")

    gmail = get_gmail_service(
        os.getenv("GMAIL_TOKEN_PATH", "auth/gmail_token.json"),
        os.getenv("GMAIL_CREDENTIALS_PATH", "auth/client_secrets.json"),
    )

    lifecycle_ws = sh.worksheet("Lifecycle")

    for item in pending:
        console.print(f"  {item['person_name']} ({item['person_email']})")
        subject, body = compose_nonmember_nurture(item["person_name"], item["buddy_name"])

        if dry_run:
            console.print(f"    [yellow][DRY RUN][/] Subject: {subject}")
            continue

        try:
            send_email(
                service=gmail,
                from_address=cfg["intro"]["sender_email"],
                to_address=item["person_email"],
                subject=subject,
                body=body,
            )

            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
            lifecycle_ws.append_row([
                item["match_id"], item["person_email"], item["person_name"],
                item["buddy_name"], "nonmember_nurture", 56, now, "", "",
            ], value_input_option="USER_ENTERED")

            console.print(f"    [green]✓[/] Sent")
        except Exception as e:
            console.print(f"    [red]Send error:[/] {e}")

    if not dry_run:
        console.print(f"\n[bold green]Done.[/]")


# ── QUARTERLY PULSE ───────────────────────────────────────────

@cli.command(name="quarterly-pulse")
@click.option("--dry-run", is_flag=True)
def quarterly_pulse(dry_run):
    """Send quarterly check-ins to long-term buddy pairs."""
    from src.lifecycle import get_quarterly_pulse_due
    from src.composer import compose_quarterly_pulse
    from src.emailer import get_gmail_service, send_email

    cfg = _load_config()
    _, sh = _get_sheets()

    matches = sh.worksheet("Matches").get_all_records()
    try:
        lifecycle_ws = sh.worksheet("Lifecycle")
        lifecycle_records = lifecycle_ws.get_all_records()
    except Exception:
        from src.sheets import ensure_tab, LIFECYCLE_HEADERS
        lifecycle_ws = ensure_tab(sh, "Lifecycle", LIFECYCLE_HEADERS)
        lifecycle_records = []

    pending = get_quarterly_pulse_due(matches, lifecycle_records)

    if not pending:
        console.print("[green]No quarterly pulses due.[/]")
        return

    console.print(f"\n[bold]{len(pending)} quarterly pulse(s) due[/]\n")

    if not dry_run:
        gmail = get_gmail_service(
            os.getenv("GMAIL_TOKEN_PATH", "auth/gmail_token.json"),
            os.getenv("GMAIL_CREDENTIALS_PATH", "auth/client_secrets.json"),
        )

    for item in pending:
        console.print(f"  {item['person_name']} ↔ {item['buddy_name']} ({item['days_since_last']}d since last check-in)")
        subject, body = compose_quarterly_pulse(item["person_name"], item["buddy_name"])

        if dry_run:
            console.print(f"    [yellow][DRY RUN][/] Subject: {subject}")
            continue

        try:
            send_email(
                service=gmail,
                from_address=cfg["intro"]["sender_email"],
                to_address=item["person_email"],
                subject=subject,
                body=body,
            )

            now = datetime.utcnow().strftime("%Y-%m-%d %H:%M")
            lifecycle_ws.append_row([
                item["match_id"], item["person_email"], item["person_name"],
                item["buddy_name"], "quarterly_pulse", 90,
                now, "", "",
            ], value_input_option="USER_ENTERED")

            console.print(f"    [green]✓[/] Sent")
        except Exception as e:
            console.print(f"    [red]Send error:[/] {e}")

    if not dry_run:
        console.print(f"\n[bold green]Done.[/]")


# ── PROCESS RESPONSES ────────────────────────────────────────

@cli.command(name="process-responses")
@click.option("--dry-run", is_flag=True)
def process_responses(dry_run):
    """Process check-in responses and take action (rematch, add buddy, etc.)."""
    from src.lifecycle import process_response
    from src.sheets import REQUESTS_HEADERS

    _, sh = _get_sheets()

    try:
        lifecycle_ws = sh.worksheet("Lifecycle")
        lifecycle_records = lifecycle_ws.get_all_records()
    except Exception:
        console.print("[yellow]No lifecycle records found.[/]")
        return

    requests_ws = sh.worksheet("Requests")

    # Find rows with responses that haven't been processed
    actionable = []
    for i, rec in enumerate(lifecycle_records, start=2):
        response = rec.get("Response", "").strip()
        response_date = rec.get("Response Date", "").strip()
        check_type = rec.get("Check Type", "").strip()

        # Skip if no response, already processed, or non-actionable types
        if not response or check_type in ("no_match_yet", "nonmember_nurture", "quarterly_pulse"):
            continue

        result = process_response(
            response=response,
            check_type=check_type,
            match_id=rec.get("Match ID", "").strip(),
            person_email=rec.get("Person Email", "").strip(),
        )

        if result["action"] != "none":
            actionable.append({
                "row_index": i,
                "match_id": rec.get("Match ID", "").strip(),
                "person_email": rec.get("Person Email", "").strip(),
                "person_name": rec.get("Person Name", "").strip(),
                "check_type": check_type,
                "response": response,
                "action": result["action"],
                "notes": result["notes"],
            })

    if not actionable:
        console.print("[green]No responses needing action.[/]")
        return

    console.print(f"\n[bold]{len(actionable)} response(s) need action[/]\n")

    email_to_row = {}
    request_rows = requests_ws.get_all_records()
    for i, row in enumerate(request_rows, start=2):
        email_to_row[row.get("Email", "").strip().lower()] = i

    status_col = REQUESTS_HEADERS.index("Status") + 1

    for item in actionable:
        action = item["action"]
        console.print(f"  {item['person_name']}: {action} — {item['notes']}")

        if dry_run:
            console.print(f"    [yellow][DRY RUN][/]")
            continue

        req_row = email_to_row.get(item["person_email"].lower())
        if not req_row:
            console.print(f"    [red]Can't find request row for {item['person_email']}[/]")
            continue

        if action == "rematch":
            requests_ws.update_cell(req_row, status_col, "Seeking New Buddy")
            console.print(f"    [green]✓[/] Status → Seeking New Buddy (will be matched in next daily run)")
        elif action == "add_buddy":
            requests_ws.update_cell(req_row, status_col, "Seeking Additional Buddy")
            console.print(f"    [green]✓[/] Status → Seeking Additional Buddy")
        elif action == "keep":
            console.print(f"    [dim]No action needed — keeping current buddy[/]")
        elif action == "flag_for_help":
            console.print(f"    [yellow]⚠ FLAGGED — needs human review: {item['notes']}[/]")

    if not dry_run:
        console.print(f"\n[bold green]Done.[/] Run [bold]python run.py daily[/] to match anyone seeking a new buddy.")


if __name__ == "__main__":
    cli()

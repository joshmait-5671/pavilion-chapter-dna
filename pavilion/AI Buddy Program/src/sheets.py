"""Google Sheets integration for AI Buddy Program."""

from __future__ import annotations
import gspread
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://spreadsheets.google.com/feeds",
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

# Sheet column headers
WAITLIST_HEADERS = [
    "Timestamp", "First Name", "Last Name", "Email", "Company",
    "Function", "Company Revenue", "City", "Timezone",
    "AI Experience Level", "Engagement Style", "Pavilion Member?",
    "Slack Name", "Notes", "Status",
]

REQUESTS_HEADERS = [
    "First Name", "Last Name", "Email", "Company",
    "Function", "Company Revenue", "City", "Timezone",
    "AI Experience Level", "Engagement Style", "Pavilion Member?",
    "Slack Name", "Notes", "Status", "Match ID", "Date Matched",
    "Current Buddies", "Pool Entry Date",
]

MATCHES_HEADERS = [
    "Match ID", "Person A Name", "Person A Email", "Person A Function",
    "Person B Name", "Person B Email", "Person B Function",
    "Match Basis", "Match Score", "Match Tier",
    "Approval", "Intro Sent", "Date Sent",
    "Match Date", "Notes",
]

LIFECYCLE_HEADERS = [
    "Match ID", "Person Email", "Person Name", "Buddy Name",
    "Check Type", "Day", "Sent Date", "Response", "Response Date",
]


def get_sheets_client(service_account_path: str) -> gspread.Client:
    """Authenticate and return a gspread client."""
    creds = Credentials.from_service_account_file(service_account_path, scopes=SCOPES)
    return gspread.authorize(creds)


def open_spreadsheet(gc: gspread.Client, spreadsheet_id: str) -> gspread.Spreadsheet:
    """Open spreadsheet by ID."""
    return gc.open_by_key(spreadsheet_id)


def ensure_tab(sh: gspread.Spreadsheet, tab_name: str, headers: list[str]) -> gspread.Worksheet:
    """Ensure a tab exists with correct headers. Create if missing."""
    try:
        ws = sh.worksheet(tab_name)
        return ws
    except gspread.exceptions.WorksheetNotFound:
        ws = sh.add_worksheet(title=tab_name, rows=500, cols=len(headers))
        ws.append_row(headers, value_input_option="USER_ENTERED")
        return ws


def setup_all_tabs(sh: gspread.Spreadsheet) -> dict[str, gspread.Worksheet]:
    """Create all required tabs. Returns dict of tab_name -> worksheet."""
    tabs = {
        "Waitlist": ensure_tab(sh, "Waitlist", WAITLIST_HEADERS),
        "Requests": ensure_tab(sh, "Requests", REQUESTS_HEADERS),
        "Matches": ensure_tab(sh, "Matches", MATCHES_HEADERS),
        "Lifecycle": ensure_tab(sh, "Lifecycle", LIFECYCLE_HEADERS),
    }

    # Remove default Sheet1 if empty
    try:
        default = sh.worksheet("Sheet1")
        sh.del_worksheet(default)
    except Exception:
        pass

    return tabs


def move_waitlist_to_requests(sh: gspread.Spreadsheet) -> int:
    """Move all waitlist entries with status 'Waitlisted' to the Requests tab.

    Sets their status to 'Unmatched' in Requests. Updates Waitlist status to 'Promoted'.
    Returns count of moved entries.
    """
    waitlist_ws = sh.worksheet("Waitlist")
    requests_ws = sh.worksheet("Requests")

    rows = waitlist_ws.get_all_records()
    moved = 0

    for i, row in enumerate(rows, start=2):
        if row.get("Status", "").strip().lower() not in ("waitlisted", ""):
            continue

        # Write to Requests tab
        from datetime import datetime
        requests_ws.append_row([
            row.get("First Name", ""),
            row.get("Last Name", ""),
            row.get("Email", ""),
            row.get("Company", ""),
            row.get("Function", ""),
            row.get("Company Revenue", ""),
            row.get("City", ""),
            row.get("Timezone", ""),
            row.get("AI Experience Level", ""),
            row.get("Engagement Style", ""),
            row.get("Pavilion Member?", ""),
            row.get("Slack Name", ""),
            row.get("Notes", ""),
            "Unmatched",  # Status
            "",           # Match ID
            "",           # Date Matched
            "",           # Current Buddies
            datetime.utcnow().strftime("%Y-%m-%d"),  # Pool Entry Date
        ], value_input_option="USER_ENTERED")

        # Mark as promoted in Waitlist
        status_col = WAITLIST_HEADERS.index("Status") + 1
        waitlist_ws.update_cell(i, status_col, "Promoted")
        moved += 1

    return moved

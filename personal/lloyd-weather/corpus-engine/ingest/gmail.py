"""Ingest Lloyd's weather emails from josh.mait@gmail.com."""
import json
import base64
import re
from pathlib import Path
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from config import RAW_DIR, LLOYD_EMAIL, TOKEN_PATH


def _get_service():
    """Build Gmail API service from saved token."""
    creds = Credentials.from_authorized_user_file(str(TOKEN_PATH))
    return build("gmail", "v1", credentials=creds)


def _extract_body(payload):
    """Extract plain text body from email payload, handling multipart."""
    if payload.get("mimeType") == "text/plain" and payload.get("body", {}).get("data"):
        return base64.urlsafe_b64decode(payload["body"]["data"]).decode("utf-8", errors="replace")

    parts = payload.get("parts", [])
    for part in parts:
        if part.get("mimeType") == "text/plain" and part.get("body", {}).get("data"):
            return base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="replace")

    for part in parts:
        if part.get("mimeType") == "text/html" and part.get("body", {}).get("data"):
            html = base64.urlsafe_b64decode(part["body"]["data"]).decode("utf-8", errors="replace")
            return re.sub(r"<[^>]+>", "", html).strip()

    for part in parts:
        result = _extract_body(part)
        if result:
            return result

    return ""


def _get_header(headers, name):
    """Get a specific header value."""
    for h in headers:
        if h["name"].lower() == name.lower():
            return h["value"]
    return ""


def ingest_gmail():
    """Fetch all emails from Lloyd and save as individual JSON files.

    Resumable: skips emails already saved in data/raw/gmail/.
    Returns count of newly ingested emails.
    """
    service = _get_service()
    output_dir = RAW_DIR / "gmail"
    output_dir.mkdir(parents=True, exist_ok=True)

    existing = {f.stem for f in output_dir.glob("*.json")}

    query = f"from:{LLOYD_EMAIL}"
    new_count = 0
    page_token = None

    while True:
        results = service.users().messages().list(
            userId="me", q=query, maxResults=100, pageToken=page_token
        ).execute()

        messages = results.get("messages", [])
        if not messages:
            break

        for msg_stub in messages:
            msg_id = msg_stub["id"]
            if msg_id in existing:
                continue

            msg = service.users().messages().get(
                userId="me", id=msg_id, format="full"
            ).execute()

            headers = msg["payload"].get("headers", [])
            body = _extract_body(msg["payload"])

            if not body.strip():
                continue

            record = {
                "id": msg_id,
                "subject": _get_header(headers, "Subject"),
                "date": _get_header(headers, "Date"),
                "from": _get_header(headers, "From"),
                "body": body,
                "snippet": msg.get("snippet", ""),
            }

            out_path = output_dir / f"{msg_id}.json"
            with open(out_path, "w") as f:
                json.dump(record, f, indent=2)

            new_count += 1

        page_token = results.get("nextPageToken")
        if not page_token:
            break

    return new_count

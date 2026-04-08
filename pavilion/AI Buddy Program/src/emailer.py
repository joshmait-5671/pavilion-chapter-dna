"""Gmail sending for AI Buddy Program."""

from __future__ import annotations
import base64
from email.mime.text import MIMEText
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import json
import os


SCOPES = ["https://www.googleapis.com/auth/gmail.send"]


def get_gmail_service(token_path: str, creds_path: str):
    """Authenticate and return Gmail API service."""
    creds = None

    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(token_path, "w") as f:
            f.write(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def send_email(
    service,
    from_address: str,
    to_address: str,
    subject: str,
    body: str,
    cc_address: str = None,
) -> dict:
    """Send an email via Gmail API. Returns the sent message metadata."""
    msg = MIMEText(body)
    msg["to"] = to_address
    msg["from"] = from_address
    msg["subject"] = subject
    if cc_address:
        msg["cc"] = cc_address

    raw = base64.urlsafe_b64encode(msg.as_bytes()).decode()
    result = service.users().messages().send(
        userId="me",
        body={"raw": raw},
    ).execute()
    return result

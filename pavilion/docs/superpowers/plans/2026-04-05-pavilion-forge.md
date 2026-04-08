# Pavilion Forge Implementation Plan

> **For agentic workers:** REQUIRED: Use superpowers:subagent-driven-development (if subagents available) or superpowers:executing-plans to implement this plan. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build three Railway-deployed Python agents (Scout, Forge Master, Bridge) that turn Pavilion University class transcripts into personalized member connections and community handoffs, live for AI GTM School on April 29.

**Architecture:** Scout reads Zoom transcripts → builds participant profiles → identifies Forge Leaders. Forge Master generates personalized Slack touchpoints and pod connections using Claude API. Bridge maps members into the broader Pavilion network after the final session. All three run as Railway services triggered sequentially.

**Tech Stack:** Python 3.11, anthropic SDK, slack_sdk, sqlite3 (local profile store), requests (HiveBright + Attention APIs), google-api-python-client (Kyler's Drive outputs), Railway deployment.

**Spec:** `pavilion/docs/superpowers/specs/2026-04-05-pavilion-forge-design.md`

**Hard deadline:** April 29, 2026 — Scout goes live on AI GTM School Session 1.

---

## File Structure

```
pavilion/forge/
├── requirements.txt
├── .env.example
├── config.py                     # All env vars and constants
├── db.py                         # SQLite setup, schema, queries
├── claude_client.py              # Claude API wrapper (single prompt interface)
├── slack_client.py               # Slack bot — DM, channel create, post
├── ingestion/
│   ├── __init__.py
│   ├── transcript.py             # Load transcript from file OR Attention API
│   ├── hive_bright.py            # HiveBright member data API client
│   └── drive.py                  # Google Drive reader for Kyler's outputs
├── agents/
│   ├── __init__.py
│   ├── scout.py                  # Scout: transcript → profiles → Forge Leaders
│   ├── forge_master.py           # Forge Master: profiles → touchpoints + pod formation
│   └── bridge.py                 # Bridge: final session → community handoff
├── prompts/
│   ├── scout_analyze.txt         # Scout system prompt
│   ├── forge_reflection.txt      # Forge Master: day-1 reflection prompt
│   ├── forge_connection.txt      # Forge Master: day-2 intro prompt
│   ├── forge_pod_prompt.txt      # Forge Master: pod discussion prompt
│   ├── forge_nudge.txt           # Forge Master: pre-session nudge prompt
│   └── bridge_handoff.txt        # Bridge: community mapping prompt
├── run_scout.py                  # Entry point: python run_scout.py <session_file>
├── run_forge_master.py           # Entry point: python run_forge_master.py <session_id>
├── run_bridge.py                 # Entry point: python run_bridge.py <cohort_id>
└── tests/
    ├── fixtures/
    │   ├── sample_transcript.txt  # Real P&L Fluency transcript text for testing
    │   └── sample_registration.json
    ├── test_db.py
    ├── test_scout.py
    ├── test_forge_master.py
    └── test_bridge.py
```

---

## Chunk 1: Foundation — Data Models, DB, Config

### Task 1: Project setup

**Files:**
- Create: `pavilion/forge/requirements.txt`
- Create: `pavilion/forge/.env.example`
- Create: `pavilion/forge/config.py`

- [ ] Create the forge directory
```bash
mkdir -p pavilion/forge/ingestion pavilion/forge/agents pavilion/forge/prompts pavilion/forge/tests/fixtures
touch pavilion/forge/ingestion/__init__.py pavilion/forge/agents/__init__.py
```

- [ ] Write `requirements.txt`
```
anthropic>=0.40.0
slack_sdk>=3.27.0
google-api-python-client>=2.120.0
google-auth>=2.29.0
requests>=2.31.0
python-dotenv>=1.0.0
pytest>=8.0.0
```

- [ ] Write `.env.example`
```
ANTHROPIC_API_KEY=
SLACK_BOT_TOKEN=
SLACK_SIGNING_SECRET=
HIVE_BRIGHT_API_KEY=
HIVE_BRIGHT_BASE_URL=https://api.hivebrite.com/v1
GOOGLE_SERVICE_ACCOUNT_JSON=
KYLER_DRIVE_FOLDER_ID=
FORGE_COURSE_ID=ai-gtm-school
DATABASE_PATH=forge.db
```

- [ ] Write `config.py`
```python
import os
from dotenv import load_dotenv

load_dotenv()

ANTHROPIC_API_KEY = os.environ["ANTHROPIC_API_KEY"]
SLACK_BOT_TOKEN = os.environ["SLACK_BOT_TOKEN"]
HIVE_BRIGHT_API_KEY = os.environ.get("HIVE_BRIGHT_API_KEY", "")
HIVE_BRIGHT_BASE_URL = os.environ.get("HIVE_BRIGHT_BASE_URL", "https://api.hivebrite.com/v1")
GOOGLE_SERVICE_ACCOUNT_JSON = os.environ.get("GOOGLE_SERVICE_ACCOUNT_JSON", "")
KYLER_DRIVE_FOLDER_ID = os.environ.get("KYLER_DRIVE_FOLDER_ID", "")
DATABASE_PATH = os.environ.get("DATABASE_PATH", "forge.db")

FORGE_MODEL = "claude-opus-4-6"
POD_SIZE = 6
FORGE_LEADER_THRESHOLD = 0.12  # Top 12% of cohort
```

- [ ] Install dependencies
```bash
cd pavilion/forge && pip install -r requirements.txt
```

- [ ] Commit
```bash
git add pavilion/forge/
git commit -m "feat(forge): project scaffold and config"
```

---

### Task 2: Database schema

**Files:**
- Create: `pavilion/forge/db.py`
- Create: `pavilion/forge/tests/test_db.py`

- [ ] Write failing test
```python
# tests/test_db.py
import pytest, os, sqlite3
from db import init_db, get_connection

def test_init_creates_tables(tmp_path):
    db_path = str(tmp_path / "test.db")
    init_db(db_path)
    conn = sqlite3.connect(db_path)
    tables = {r[0] for r in conn.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()}
    assert "participants" in tables
    assert "sessions" in tables
    assert "pods" in tables
    assert "pod_members" in tables
    assert "forge_leaders" in tables
    conn.close()
```

- [ ] Run test — expect FAIL
```bash
cd pavilion/forge && pytest tests/test_db.py -v
```

- [ ] Write `db.py`
```python
import sqlite3
from config import DATABASE_PATH

def get_connection(db_path=DATABASE_PATH):
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

def init_db(db_path=DATABASE_PATH):
    conn = get_connection(db_path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS sessions (
            id TEXT PRIMARY KEY,
            course_id TEXT NOT NULL,
            session_number INTEGER NOT NULL,
            total_sessions INTEGER NOT NULL,
            session_date TEXT,
            transcript_path TEXT,
            processed_at TEXT
        );

        CREATE TABLE IF NOT EXISTS participants (
            id TEXT PRIMARY KEY,
            cohort_id TEXT NOT NULL,
            name TEXT,
            email TEXT,
            title TEXT,
            company TEXT,
            stage TEXT,
            function TEXT,
            hive_bright_id TEXT
        );

        CREATE TABLE IF NOT EXISTS session_participants (
            session_id TEXT NOT NULL,
            participant_id TEXT NOT NULL,
            attended INTEGER DEFAULT 1,
            duration_minutes INTEGER,
            contribution_score REAL DEFAULT 0.0,
            notable_moment TEXT,
            PRIMARY KEY (session_id, participant_id)
        );

        CREATE TABLE IF NOT EXISTS forge_leaders (
            participant_id TEXT PRIMARY KEY,
            cohort_id TEXT NOT NULL,
            nominated_at_session INTEGER,
            reason TEXT
        );

        CREATE TABLE IF NOT EXISTS pods (
            id TEXT PRIMARY KEY,
            cohort_id TEXT NOT NULL,
            formed_at_session INTEGER,
            function TEXT,
            stage TEXT
        );

        CREATE TABLE IF NOT EXISTS pod_members (
            pod_id TEXT NOT NULL,
            participant_id TEXT NOT NULL,
            is_wildcard INTEGER DEFAULT 0,
            PRIMARY KEY (pod_id, participant_id)
        );

        CREATE TABLE IF NOT EXISTS touchpoints (
            id TEXT PRIMARY KEY,
            participant_id TEXT NOT NULL,
            session_id TEXT NOT NULL,
            type TEXT NOT NULL,
            content TEXT,
            sent_at TEXT,
            slack_channel TEXT
        );
    """)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    init_db()
    print(f"Database initialized at {DATABASE_PATH}")
```

- [ ] Run test — expect PASS
```bash
pytest tests/test_db.py -v
```

- [ ] Commit
```bash
git add pavilion/forge/db.py pavilion/forge/tests/test_db.py
git commit -m "feat(forge): sqlite schema — participants, sessions, pods, touchpoints"
```

---

### Task 3: Claude client

**Files:**
- Create: `pavilion/forge/claude_client.py`
- Create: `pavilion/forge/tests/test_claude_client.py`

- [ ] Write failing test
```python
# tests/test_claude_client.py
import pytest
from unittest.mock import patch, MagicMock
from claude_client import ask_claude

def test_ask_claude_returns_string():
    mock_response = MagicMock()
    mock_response.content = [MagicMock(text="test response")]
    with patch("claude_client.anthropic_client.messages.create", return_value=mock_response):
        result = ask_claude("system prompt", "user prompt")
    assert isinstance(result, str)
    assert result == "test response"
```

- [ ] Run test — expect FAIL
```bash
pytest tests/test_claude_client.py -v
```

- [ ] Write `claude_client.py`
```python
import anthropic
from config import ANTHROPIC_API_KEY, FORGE_MODEL

anthropic_client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

def ask_claude(system_prompt: str, user_prompt: str, max_tokens: int = 2000) -> str:
    response = anthropic_client.messages.create(
        model=FORGE_MODEL,
        max_tokens=max_tokens,
        system=system_prompt,
        messages=[{"role": "user", "content": user_prompt}]
    )
    return response.content[0].text
```

- [ ] Run test — expect PASS
```bash
pytest tests/test_claude_client.py -v
```

- [ ] Commit
```bash
git add pavilion/forge/claude_client.py pavilion/forge/tests/test_claude_client.py
git commit -m "feat(forge): claude client wrapper"
```

---

## Chunk 2: Ingestion Layer

### Task 4: Transcript loader

**Files:**
- Create: `pavilion/forge/ingestion/transcript.py`
- Create: `pavilion/forge/tests/fixtures/sample_transcript.txt`
- Create test in `tests/test_scout.py` (ingestion section)

- [ ] Add a sample transcript fixture
Copy a real P&L Fluency transcript text into `tests/fixtures/sample_transcript.txt`. Plain text is fine — VTT format or raw text both work. This is the test data for all Scout testing.

- [ ] Write failing test
```python
# tests/test_scout.py
import pytest
from ingestion.transcript import load_transcript

def test_load_transcript_from_file(tmp_path):
    f = tmp_path / "transcript.txt"
    f.write_text("00:01 Sam: Hello everyone. 00:05 Jan: Hi Sam.")
    result = load_transcript(str(f))
    assert "Sam" in result
    assert len(result) > 10

def test_load_transcript_missing_file():
    with pytest.raises(FileNotFoundError):
        load_transcript("/nonexistent/path.txt")
```

- [ ] Run — expect FAIL
```bash
pytest tests/test_scout.py::test_load_transcript_from_file -v
```

- [ ] Write `ingestion/transcript.py`
```python
import os

def load_transcript(path: str) -> str:
    """Load transcript from a local file. Attention API integration added in Phase 2."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Transcript not found: {path}")
    with open(path, "r", encoding="utf-8") as f:
        return f.read()

def load_transcript_from_attention(session_id: str, api_key: str) -> str:
    """Placeholder for Attention API integration — Phase 2."""
    raise NotImplementedError("Attention API integration not yet built")
```

- [ ] Run — expect PASS
```bash
pytest tests/test_scout.py -v
```

- [ ] Commit
```bash
git add pavilion/forge/ingestion/transcript.py pavilion/forge/tests/
git commit -m "feat(forge): transcript loader — file-based with Attention API stub"
```

---

### Task 5: HiveBright client (registration data)

**Files:**
- Create: `pavilion/forge/ingestion/hive_bright.py`

Note: HiveBright API details need to be confirmed. This task builds the client with a fallback to a local JSON file so Scout testing isn't blocked.

- [ ] Write `ingestion/hive_bright.py`
```python
import json
import requests
from config import HIVE_BRIGHT_API_KEY, HIVE_BRIGHT_BASE_URL

def get_member_by_email(email: str) -> dict:
    """Fetch member profile from HiveBright by email."""
    if not HIVE_BRIGHT_API_KEY:
        return {}  # Graceful degradation during testing
    headers = {"Authorization": f"Bearer {HIVE_BRIGHT_API_KEY}"}
    response = requests.get(
        f"{HIVE_BRIGHT_BASE_URL}/members",
        params={"email": email},
        headers=headers,
        timeout=10
    )
    if response.status_code == 200:
        data = response.json()
        members = data.get("members", [])
        return members[0] if members else {}
    return {}

def get_member_profile(hive_bright_id: str) -> dict:
    """Fetch full member profile by HiveBright ID."""
    if not HIVE_BRIGHT_API_KEY:
        return {}
    headers = {"Authorization": f"Bearer {HIVE_BRIGHT_API_KEY}"}
    response = requests.get(
        f"{HIVE_BRIGHT_BASE_URL}/members/{hive_bright_id}",
        headers=headers,
        timeout=10
    )
    return response.json() if response.status_code == 200 else {}

def load_registration_from_file(path: str) -> list[dict]:
    """Load registration data from local JSON — for testing without HiveBright access."""
    with open(path, "r") as f:
        return json.load(f)
```

- [ ] Add sample registration fixture
Create `tests/fixtures/sample_registration.json` with 5-10 fake participants in this format:
```json
[
  {
    "email": "jan.young@example.com",
    "name": "Jan Young",
    "title": "CMO",
    "company": "Acme Corp",
    "stage": "Series B",
    "function": "Marketing"
  }
]
```

- [ ] Commit
```bash
git add pavilion/forge/ingestion/hive_bright.py pavilion/forge/tests/fixtures/
git commit -m "feat(forge): hive bright client with local file fallback"
```

---

### Task 6: Google Drive reader (Kyler's outputs)

**Files:**
- Create: `pavilion/forge/ingestion/drive.py`

- [ ] Write `ingestion/drive.py`
```python
import json
import os
from config import GOOGLE_SERVICE_ACCOUNT_JSON, KYLER_DRIVE_FOLDER_ID

def get_drive_service():
    """Build Google Drive service from service account credentials."""
    from google.oauth2 import service_account
    from googleapiclient.discovery import build

    if not GOOGLE_SERVICE_ACCOUNT_JSON:
        return None

    creds_dict = json.loads(GOOGLE_SERVICE_ACCOUNT_JSON)
    creds = service_account.Credentials.from_service_account_info(
        creds_dict,
        scopes=["https://www.googleapis.com/auth/drive.readonly"]
    )
    return build("drive", "v3", credentials=creds)

def list_course_assets(course_id: str, session_number: int) -> list[dict]:
    """List Kyler's output files for a given course and session."""
    service = get_drive_service()
    if not service:
        return []  # Graceful degradation during testing

    query = f"'{KYLER_DRIVE_FOLDER_ID}' in parents and name contains '{course_id}' and name contains 'session{session_number}'"
    results = service.files().list(q=query, fields="files(id, name, mimeType)").execute()
    return results.get("files", [])

def read_file_content(file_id: str) -> str:
    """Read text content from a Drive file."""
    service = get_drive_service()
    if not service:
        return ""
    from googleapiclient.http import MediaIoBaseDownload
    import io
    request = service.files().get_media(fileId=file_id)
    fh = io.BytesIO()
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while not done:
        _, done = downloader.next_chunk()
    return fh.getvalue().decode("utf-8")
```

- [ ] Commit
```bash
git add pavilion/forge/ingestion/drive.py
git commit -m "feat(forge): google drive reader for kyler's course assets"
```

---

## Chunk 3: Scout Agent

### Task 7: Scout system prompt

**Files:**
- Create: `pavilion/forge/prompts/scout_analyze.txt`

- [ ] Write `prompts/scout_analyze.txt`
```
You are the Scout for Pavilion Forge. You analyze class session transcripts to build participant profiles and identify Forge Leaders.

Your job:
1. Read the transcript carefully
2. For each participant who speaks, extract:
   - Name (as it appears in transcript)
   - The quality and type of their contributions
   - Any questions they asked (mark the best one)
   - Any case studies, real examples, or data they shared
   - Whether they challenged the instructor constructively
   - Estimated engagement level: HIGH / MEDIUM / LOW

3. Identify Forge Leader candidates — participants who match one or more of these patterns:
   - "The Question Everyone Was Thinking" (MJ Patent pattern): asked the uncomfortable question others wanted to ask
   - "Made The Class Better" (Winnie Palmer pattern): challenged the instructor and was right, or added important nuance
   - "Real Results" (Jan Young pattern): shared a specific case study with real numbers or outcomes
   - "The Synthesizer": connected two things nobody else had connected

4. For each Forge Leader candidate, write one sentence explaining exactly why they qualify.

Return a JSON object with this exact structure:
{
  "session_summary": "2-3 sentence summary of the session's key themes",
  "key_moments": [
    {"participant": "name", "moment": "what happened", "type": "question|challenge|case_study|synthesis"}
  ],
  "participant_profiles": [
    {
      "name": "name as in transcript",
      "engagement_level": "HIGH|MEDIUM|LOW",
      "best_contribution": "one sentence",
      "notable_quote": "exact quote if available",
      "forge_leader_candidate": true|false,
      "forge_leader_reason": "one sentence or null"
    }
  ]
}

Be specific. Use exact quotes. Do not invent contributions that aren't in the transcript.
```

---

### Task 8: Scout core logic

**Files:**
- Create: `pavilion/forge/agents/scout.py`
- Modify: `pavilion/forge/tests/test_scout.py`

- [ ] Add failing tests
```python
# tests/test_scout.py (add to existing file)
import json
from unittest.mock import patch
from agents.scout import analyze_session, nominate_forge_leaders

SAMPLE_TRANSCRIPT = """
00:01 Sam Jacobs: Welcome everyone to P&L Fluency session 2.
00:05 Jan Young: I decreased CAC by 75% using an advocacy program. Customers became marketers.
00:10 MJ Patent: How do you tell a CFO that the math says you need 8M when they're offering 2M?
00:15 Winnie Palmer: I have to challenge this. The model is limited to which gate the customer comes in. That's not what convinced them to buy.
00:20 Sam Jacobs: Winnie, you're right. Attribution is the single biggest quagmire in business.
"""

MOCK_CLAUDE_RESPONSE = json.dumps({
    "session_summary": "Session 2 focused on unit economics and CAC.",
    "key_moments": [
        {"participant": "Jan Young", "moment": "Shared advocacy program reduced CAC 75%", "type": "case_study"},
        {"participant": "MJ Patent", "moment": "Asked the CFO budget question", "type": "question"},
        {"participant": "Winnie Palmer", "moment": "Challenged the attribution model", "type": "challenge"}
    ],
    "participant_profiles": [
        {"name": "Jan Young", "engagement_level": "HIGH", "best_contribution": "Advocacy program cut CAC 75%",
         "notable_quote": "Customers became marketers", "forge_leader_candidate": True,
         "forge_leader_reason": "Real case study with specific results"},
        {"name": "MJ Patent", "engagement_level": "HIGH", "best_contribution": "Asked the CFO question",
         "notable_quote": None, "forge_leader_candidate": True,
         "forge_leader_reason": "Asked the question everyone was thinking"},
        {"name": "Winnie Palmer", "engagement_level": "HIGH", "best_contribution": "Challenged attribution model",
         "notable_quote": "That's not what convinced them to buy", "forge_leader_candidate": True,
         "forge_leader_reason": "Challenged instructor and was right"}
    ]
})

def test_analyze_session_returns_profiles():
    with patch("agents.scout.ask_claude", return_value=MOCK_CLAUDE_RESPONSE):
        result = analyze_session(SAMPLE_TRANSCRIPT, session_number=2)
    assert "participant_profiles" in result
    assert len(result["participant_profiles"]) == 3

def test_forge_leader_identification():
    with patch("agents.scout.ask_claude", return_value=MOCK_CLAUDE_RESPONSE):
        result = analyze_session(SAMPLE_TRANSCRIPT, session_number=2)
    leaders = nominate_forge_leaders(result["participant_profiles"], cohort_size=20)
    assert len(leaders) > 0
    assert all(p["forge_leader_candidate"] for p in leaders)
```

- [ ] Run — expect FAIL
```bash
pytest tests/test_scout.py::test_analyze_session_returns_profiles -v
```

- [ ] Write `agents/scout.py`
```python
import json
from claude_client import ask_claude
from config import FORGE_LEADER_THRESHOLD

def load_prompt(name: str) -> str:
    with open(f"prompts/{name}.txt") as f:
        return f.read()

def analyze_session(transcript: str, session_number: int) -> dict:
    """Run Claude on a session transcript and return structured participant profiles."""
    system_prompt = load_prompt("scout_analyze")
    user_prompt = f"Session number: {session_number}\n\nTranscript:\n{transcript}"
    response = ask_claude(system_prompt, user_prompt, max_tokens=4000)

    # Strip markdown code blocks if Claude wraps JSON
    cleaned = response.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    return json.loads(cleaned.strip())

def nominate_forge_leaders(profiles: list[dict], cohort_size: int) -> list[dict]:
    """Return profiles flagged as forge_leader_candidate=True."""
    return [p for p in profiles if p.get("forge_leader_candidate")]

def run_scout(transcript_path: str, session_id: str, session_number: int,
              total_sessions: int, cohort_id: str, db_path: str = None):
    """Full Scout pipeline: load transcript → analyze → save to DB."""
    from ingestion.transcript import load_transcript
    from db import get_connection, init_db
    from config import DATABASE_PATH
    import datetime

    db_path = db_path or DATABASE_PATH
    init_db(db_path)

    transcript = load_transcript(transcript_path)
    analysis = analyze_session(transcript, session_number)

    conn = get_connection(db_path)
    now = datetime.datetime.utcnow().isoformat()

    # Save session
    conn.execute("""
        INSERT OR REPLACE INTO sessions (id, course_id, session_number, total_sessions, transcript_path, processed_at)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (session_id, cohort_id, session_number, total_sessions, transcript_path, now))

    # Save participants and their session contributions
    for profile in analysis.get("participant_profiles", []):
        participant_id = f"{cohort_id}_{profile['name'].lower().replace(' ', '_')}"
        conn.execute("""
            INSERT OR IGNORE INTO participants (id, cohort_id, name, function)
            VALUES (?, ?, ?, ?)
        """, (participant_id, cohort_id, profile["name"], "unknown"))

        conn.execute("""
            INSERT OR REPLACE INTO session_participants
            (session_id, participant_id, contribution_score, notable_moment)
            VALUES (?, ?, ?, ?)
        """, (
            session_id,
            participant_id,
            1.0 if profile["engagement_level"] == "HIGH" else 0.5 if profile["engagement_level"] == "MEDIUM" else 0.0,
            profile.get("best_contribution", "")
        ))

        # Nominate Forge Leaders
        if profile.get("forge_leader_candidate"):
            conn.execute("""
                INSERT OR REPLACE INTO forge_leaders (participant_id, cohort_id, nominated_at_session, reason)
                VALUES (?, ?, ?, ?)
            """, (participant_id, cohort_id, session_number, profile.get("forge_leader_reason", "")))

    conn.commit()
    conn.close()

    return analysis
```

- [ ] Run tests — expect PASS
```bash
pytest tests/test_scout.py -v
```

- [ ] Commit
```bash
git add pavilion/forge/agents/scout.py pavilion/forge/prompts/scout_analyze.txt pavilion/forge/tests/test_scout.py
git commit -m "feat(forge): scout agent — transcript analysis and forge leader nomination"
```

---

### Task 9: Scout entry point + manual test on real transcript

**Files:**
- Create: `pavilion/forge/run_scout.py`

- [ ] Write `run_scout.py`
```python
#!/usr/bin/env python3
"""
Usage: python run_scout.py <transcript_path> <session_number> <total_sessions> <cohort_id>
Example: python run_scout.py tests/fixtures/sample_transcript.txt 2 3 pl-fluency-2026-q1
"""
import sys
import json
from agents.scout import run_scout

if __name__ == "__main__":
    if len(sys.argv) < 5:
        print("Usage: python run_scout.py <transcript_path> <session_number> <total_sessions> <cohort_id>")
        sys.exit(1)

    transcript_path = sys.argv[1]
    session_number = int(sys.argv[2])
    total_sessions = int(sys.argv[3])
    cohort_id = sys.argv[4]
    session_id = f"{cohort_id}_session{session_number}"

    print(f"Running Scout on: {transcript_path}")
    result = run_scout(transcript_path, session_id, session_number, total_sessions, cohort_id)

    print("\n=== SESSION SUMMARY ===")
    print(result.get("session_summary", ""))
    print(f"\n=== PARTICIPANTS ({len(result.get('participant_profiles', []))}) ===")
    for p in result.get("participant_profiles", []):
        leader = " ⭐ FORGE LEADER" if p.get("forge_leader_candidate") else ""
        print(f"  {p['name']} [{p['engagement_level']}]{leader}")
        if p.get("forge_leader_reason"):
            print(f"    → {p['forge_leader_reason']}")

    print("\n=== KEY MOMENTS ===")
    for m in result.get("key_moments", []):
        print(f"  [{m['type'].upper()}] {m['participant']}: {m['moment']}")
```

- [ ] Run Scout manually on the P&L Fluency sample transcript
```bash
cd pavilion/forge
python run_scout.py tests/fixtures/sample_transcript.txt 2 3 pl-fluency-test-001
```
Expected: session summary printed, participants listed, Forge Leaders identified with ⭐

- [ ] Verify database was written
```bash
python3 -c "
import sqlite3
conn = sqlite3.connect('forge.db')
print('Participants:', conn.execute('SELECT count(*) FROM participants').fetchone()[0])
print('Forge Leaders:', conn.execute('SELECT count(*) FROM forge_leaders').fetchone()[0])
conn.close()
"
```

- [ ] Commit
```bash
git add pavilion/forge/run_scout.py
git commit -m "feat(forge): scout entry point — manual trigger via CLI"
```

---

## Chunk 4: Forge Master Agent

### Task 10: Forge Master prompts

**Files:**
- Create: `pavilion/forge/prompts/forge_reflection.txt`
- Create: `pavilion/forge/prompts/forge_connection.txt`
- Create: `pavilion/forge/prompts/forge_pod_prompt.txt`
- Create: `pavilion/forge/prompts/forge_nudge.txt`

- [ ] Write `prompts/forge_reflection.txt`
```
You are the Forge Master for Pavilion University. You write personalized post-session reflections that go out to individual members within 6 hours of a session ending.

These messages land as Slack DMs. They must feel like they noticed something specific about THIS person — not like a summary sent to 250 people.

Rules:
- 3 sentences maximum
- Reference something this specific person said or asked in the session (use their notable_moment or notable_quote)
- Connect it to their specific role and company context
- End with one thing to sit with — not a call to action
- Never use: "Great question!", "I noticed that...", "As a reminder..."
- Tone: direct, warm, peer-level. Not a bot. Not a professor. A sharp colleague who was in the room.

Return only the message text. No subject line. No greeting. No sign-off.
```

- [ ] Write `prompts/forge_connection.txt`
```
You are the Forge Master for Pavilion University. You write peer connection messages — Slack DMs that introduce two cohort members to each other based on something they shared in the session.

Rules:
- The message goes to Person A and introduces them to Person B
- The connection must be based on a real shared context from the session — not just "you're both CMOs"
- Include Person B's Slack handle
- 2-3 sentences maximum
- Explain exactly why this introduction matters right now, based on what both people said
- Never say: "I thought you two should connect", "You have a lot in common"
- Tone: peer-level, direct, specific

Return only the message text. No greeting. No sign-off.
```

- [ ] Write `prompts/forge_pod_prompt.txt`
```
You are the Forge Master for Pavilion University. You select the right discussion prompt for a specific pod based on their function and the session content.

You have access to two types of prompts from Kyler's content assets:
- CHILL TAKE: conversational, surface-level, safe
- SERIOUS SHIT TAKE: vulnerable, uncomfortable, real

For pods of senior operators (VP and above), default to SERIOUS SHIT TAKE unless the session topic is introductory.
For pods with mixed seniority, use CHILL TAKE for sessions 1-2, SERIOUS SHIT TAKE from session 3 onwards.

Adapt the selected prompt slightly to reference something specific from this session.

Return: the adapted prompt text only. No explanation.
```

- [ ] Write `prompts/forge_nudge.txt`
```
You are the Forge Master for Pavilion University. You write a pre-session nudge — a single sentence Slack DM sent the day before the next session.

Rules:
- One sentence only
- Reference something specific this person raised in the previous session
- Tease something in the upcoming session that's relevant to their situation
- Make them feel prepared, not reminded
- Never say: "Don't forget", "Just a reminder", "See you tomorrow"

Return only the sentence. Nothing else.
```

- [ ] Commit
```bash
git add pavilion/forge/prompts/
git commit -m "feat(forge): forge master prompt library"
```

---

### Task 11: Pod formation logic

**Files:**
- Create: `pavilion/forge/agents/forge_master.py` (pod formation section)
- Modify: `pavilion/forge/tests/test_forge_master.py`

- [ ] Write failing test
```python
# tests/test_forge_master.py
import pytest
from agents.forge_master import form_pods

SAMPLE_PARTICIPANTS = [
    {"id": "p1", "function": "Marketing", "stage": "Series B", "is_forge_leader": False},
    {"id": "p2", "function": "Marketing", "stage": "Series B", "is_forge_leader": True},
    {"id": "p3", "function": "Marketing", "stage": "Series B", "is_forge_leader": False},
    {"id": "p4", "function": "Marketing", "stage": "Series B", "is_forge_leader": False},
    {"id": "p5", "function": "Marketing", "stage": "Series C", "is_forge_leader": False},
    {"id": "p6", "function": "Marketing", "stage": "Series B", "is_forge_leader": False},
    {"id": "p7", "function": "Sales", "stage": "Series B", "is_forge_leader": False},
    {"id": "p8", "function": "Sales", "stage": "Series B", "is_forge_leader": False},
    {"id": "p9", "function": "Sales", "stage": "Series B", "is_forge_leader": False},
    {"id": "p10", "function": "Sales", "stage": "Series B", "is_forge_leader": False},
    {"id": "p11", "function": "Sales", "stage": "Series B", "is_forge_leader": False},
    {"id": "p12", "function": "Sales", "stage": "Series B", "is_forge_leader": False},
]

def test_pods_max_size_six():
    pods = form_pods(SAMPLE_PARTICIPANTS)
    for pod in pods:
        assert len(pod["members"]) <= 6

def test_pods_same_function():
    pods = form_pods(SAMPLE_PARTICIPANTS)
    for pod in pods:
        functions = {m["function"] for m in pod["members"]}
        assert len(functions) == 1  # All same function

def test_forge_leader_in_pod():
    pods = form_pods(SAMPLE_PARTICIPANTS)
    marketing_pods = [p for p in pods if p["function"] == "Marketing"]
    # At least one pod should have a forge leader as wildcard
    leader_pods = [p for p in marketing_pods if any(m["is_forge_leader"] for m in p["members"])]
    assert len(leader_pods) >= 1
```

- [ ] Run — expect FAIL
```bash
pytest tests/test_forge_master.py -v
```

- [ ] Write pod formation in `agents/forge_master.py`
```python
import uuid
from typing import List, Dict

def form_pods(participants: List[Dict], pod_size: int = 6) -> List[Dict]:
    """
    Form pods of pod_size. Rules:
    - Same function (mandatory)
    - Similar stage (mandatory)
    - One Forge Leader per pod as wildcard (where available)
    """
    # Group by function
    by_function = {}
    for p in participants:
        fn = p.get("function", "Unknown")
        by_function.setdefault(fn, []).append(p)

    pods = []
    for function, members in by_function.items():
        # Separate forge leaders and regular members
        leaders = [m for m in members if m.get("is_forge_leader")]
        regulars = [m for m in members if not m.get("is_forge_leader")]

        # Sort regulars by stage for better matching
        regulars.sort(key=lambda x: x.get("stage", ""))

        # Form pods
        pod_members = []
        leader_idx = 0

        for i, member in enumerate(regulars):
            pod_members.append(member)
            # Add a forge leader as wildcard when pod is nearly full
            if len(pod_members) == pod_size - 1 and leader_idx < len(leaders):
                pod_members.append(leaders[leader_idx])
                leader_idx += 1

            if len(pod_members) >= pod_size or i == len(regulars) - 1:
                if pod_members:
                    pods.append({
                        "id": str(uuid.uuid4()),
                        "function": function,
                        "members": pod_members.copy()
                    })
                    pod_members = []

    return pods
```

- [ ] Run tests — expect PASS
```bash
pytest tests/test_forge_master.py -v
```

- [ ] Commit
```bash
git add pavilion/forge/agents/forge_master.py pavilion/forge/tests/test_forge_master.py
git commit -m "feat(forge): pod formation — function-matched, size-6, forge leaders as wildcards"
```

---

### Task 12: Forge Master touchpoint generation

**Files:**
- Modify: `pavilion/forge/agents/forge_master.py`

- [ ] Add touchpoint generation functions to `agents/forge_master.py`
```python
from claude_client import ask_claude
import json, datetime, uuid

def load_prompt(name: str) -> str:
    with open(f"prompts/{name}.txt") as f:
        return f.read()

def generate_reflection(participant: dict, session_analysis: dict) -> str:
    """Generate Day-1 personalized reflection for one participant."""
    system = load_prompt("forge_reflection")
    user = f"""
Participant: {participant['name']}
Title: {participant.get('title', 'unknown')}
Company: {participant.get('company', 'unknown')}
Stage: {participant.get('stage', 'unknown')}
Their notable moment: {participant.get('notable_moment', 'participated in discussion')}
Their notable quote: {participant.get('notable_quote', '')}

Session summary: {session_analysis.get('session_summary', '')}
"""
    return ask_claude(system, user, max_tokens=300)

def generate_connection(participant_a: dict, participant_b: dict,
                        shared_context: str) -> str:
    """Generate Day-2 peer intro message (sent to participant_a, introduces participant_b)."""
    system = load_prompt("forge_connection")
    user = f"""
Introducing TO: {participant_a['name']} ({participant_a.get('title', '')})
Introducing: {participant_b['name']} ({participant_b.get('title', '')})
Participant B's Slack handle: @{participant_b.get('slack_handle', participant_b['name'].lower().replace(' ', '.'))}
Shared context from session: {shared_context}
"""
    return ask_claude(system, user, max_tokens=200)

def generate_pod_prompt(pod: dict, session_content: str, kyler_prompts: dict) -> str:
    """Select and adapt a Kyler prompt for a specific pod."""
    system = load_prompt("forge_pod_prompt")
    user = f"""
Pod function: {pod['function']}
Members seniority: {', '.join(m.get('title', 'unknown') for m in pod['members'])}
Session content summary: {session_content}

CHILL TAKE prompts available:
{json.dumps(kyler_prompts.get('chill', []), indent=2)}

SERIOUS SHIT TAKE prompts available:
{json.dumps(kyler_prompts.get('serious', []), indent=2)}
"""
    return ask_claude(system, user, max_tokens=400)

def generate_nudge(participant: dict, next_session_topic: str,
                   their_previous_question: str) -> str:
    """Generate Day-6 pre-session nudge."""
    system = load_prompt("forge_nudge")
    user = f"""
Participant: {participant['name']}
Their previous session question/contribution: {their_previous_question}
Next session topic: {next_session_topic}
"""
    return ask_claude(system, user, max_tokens=100)
```

- [ ] Commit
```bash
git add pavilion/forge/agents/forge_master.py
git commit -m "feat(forge): forge master touchpoint generation — reflection, connection, pod prompt, nudge"
```

---

### Task 13: Forge Master entry point + manual test

**Files:**
- Create: `pavilion/forge/run_forge_master.py`

- [ ] Write `run_forge_master.py`
```python
#!/usr/bin/env python3
"""
Usage: python run_forge_master.py <cohort_id> <session_number>
Example: python run_forge_master.py pl-fluency-test-001 2
"""
import sys
import json
from db import get_connection
from agents.forge_master import generate_reflection, form_pods

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: python run_forge_master.py <cohort_id> <session_number>")
        sys.exit(1)

    cohort_id = sys.argv[1]
    session_number = int(sys.argv[2])

    conn = get_connection()
    session = conn.execute(
        "SELECT * FROM sessions WHERE course_id=? AND session_number=?",
        (cohort_id, session_number)
    ).fetchone()

    if not session:
        print(f"No session found for cohort {cohort_id} session {session_number}")
        print("Run the Scout first: python run_scout.py ...")
        sys.exit(1)

    participants = conn.execute(
        """SELECT p.*, sp.notable_moment, sp.contribution_score
           FROM participants p
           JOIN session_participants sp ON p.id = sp.participant_id
           WHERE p.cohort_id=? AND sp.session_id=?""",
        (cohort_id, session["id"])
    ).fetchall()
    conn.close()

    participants = [dict(p) for p in participants]
    print(f"Generating touchpoints for {len(participants)} participants...")

    for participant in participants[:3]:  # Preview first 3
        print(f"\n=== REFLECTION: {participant['name']} ===")
        reflection = generate_reflection(
            participant,
            {"session_summary": f"Session {session_number} of the Forge program"}
        )
        print(reflection)

    print(f"\n=== POD FORMATION ===")
    pods = form_pods(participants)
    for pod in pods:
        print(f"Pod [{pod['function']}]: {', '.join(m['name'] for m in pod['members'])}")
```

- [ ] Run manual test
```bash
cd pavilion/forge
python run_forge_master.py pl-fluency-test-001 2
```
Expected: 3 reflection previews printed, pods listed

- [ ] Commit
```bash
git add pavilion/forge/run_forge_master.py
git commit -m "feat(forge): forge master entry point and preview mode"
```

---

## Chunk 5: Slack Delivery + Bridge + Railway Deploy

### Task 14: Slack client

**Files:**
- Create: `pavilion/forge/slack_client.py`
- Create: `pavilion/forge/tests/test_slack_client.py`

- [ ] Write failing test
```python
# tests/test_slack_client.py
from unittest.mock import patch, MagicMock
from slack_client import send_dm, create_pod_channel

def test_send_dm_calls_slack():
    with patch("slack_client.client.conversations_open") as mock_open, \
         patch("slack_client.client.chat_postMessage") as mock_post:
        mock_open.return_value = {"channel": {"id": "D123"}}
        mock_post.return_value = {"ok": True}
        result = send_dm("U123456", "Hello Forge member")
    mock_post.assert_called_once()
    assert result is True

def test_create_pod_channel():
    with patch("slack_client.client.conversations_create") as mock_create, \
         patch("slack_client.client.conversations_invite") as mock_invite:
        mock_create.return_value = {"channel": {"id": "C789", "name": "forge-pod-abc"}}
        mock_invite.return_value = {"ok": True}
        result = create_pod_channel("forge-pod-abc", ["U1", "U2", "U3"])
    assert result == "C789"
```

- [ ] Run — expect FAIL
```bash
pytest tests/test_slack_client.py -v
```

- [ ] Write `slack_client.py`
```python
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from config import SLACK_BOT_TOKEN

client = WebClient(token=SLACK_BOT_TOKEN)

def send_dm(slack_user_id: str, message: str) -> bool:
    """Send a direct message to a Slack user by ID."""
    try:
        response = client.conversations_open(users=slack_user_id)
        channel_id = response["channel"]["id"]
        client.chat_postMessage(channel=channel_id, text=message)
        return True
    except SlackApiError as e:
        print(f"Slack DM failed for {slack_user_id}: {e.response['error']}")
        return False

def post_to_channel(channel_id: str, message: str) -> bool:
    """Post a message to a Slack channel."""
    try:
        client.chat_postMessage(channel=channel_id, text=message)
        return True
    except SlackApiError as e:
        print(f"Channel post failed: {e.response['error']}")
        return False

def create_pod_channel(channel_name: str, member_ids: list[str]) -> str | None:
    """Create a private Slack channel for a pod and add members."""
    try:
        response = client.conversations_create(name=channel_name, is_private=True)
        channel_id = response["channel"]["id"]
        if member_ids:
            client.conversations_invite(channel=channel_id, users=",".join(member_ids))
        return channel_id
    except SlackApiError as e:
        print(f"Pod channel creation failed: {e.response['error']}")
        return None

def lookup_user_by_email(email: str) -> str | None:
    """Look up a Slack user ID by email address."""
    try:
        response = client.users_lookupByEmail(email=email)
        return response["user"]["id"]
    except SlackApiError:
        return None
```

- [ ] Run tests — expect PASS
```bash
pytest tests/test_slack_client.py -v
```

- [ ] Commit
```bash
git add pavilion/forge/slack_client.py pavilion/forge/tests/test_slack_client.py
git commit -m "feat(forge): slack client — DM, channel creation, pod channels"
```

---

### Task 15: Bridge agent

**Files:**
- Create: `pavilion/forge/prompts/bridge_handoff.txt`
- Create: `pavilion/forge/agents/bridge.py`
- Create: `pavilion/forge/run_bridge.py`

- [ ] Write `prompts/bridge_handoff.txt`
```
You are the Bridge for Pavilion Forge. After the final session, you write a personalized "your next 30 days in Pavilion" message for each member.

This message is delivered via Slack DM 3 days after the final session.

Rules:
- Acknowledge what they specifically contributed or learned in the Forge
- Suggest 2-3 specific next steps inside Pavilion (Slack channels, upcoming events, next program)
- Make the suggestions feel earned — based on what they actually engaged with
- Never say: "We hope you enjoyed the program", "Don't forget to check out..."
- 4-5 sentences maximum
- End with a direct question that invites them to respond

Return only the message text.
```

- [ ] Write `agents/bridge.py`
```python
from claude_client import ask_claude
from db import get_connection

def load_prompt(name: str) -> str:
    with open(f"prompts/{name}.txt") as f:
        return f.read()

PAVILION_NEXT_STEPS = {
    "Marketing": {
        "slack_channels": ["#marketing", "#demand-gen", "#brand"],
        "next_program": "CMO School",
        "chapter": "local Marketing chapter dinner"
    },
    "Sales": {
        "slack_channels": ["#sales", "#enterprise-sales", "#rev-ops"],
        "next_program": "CRO School",
        "chapter": "local Sales chapter dinner"
    },
    "RevOps": {
        "slack_channels": ["#rev-ops", "#ops", "#data"],
        "next_program": "RevOps School",
        "chapter": "local RevOps chapter dinner"
    },
}

def generate_bridge_message(participant: dict, cohort_summary: str) -> str:
    """Generate personalized 30-day Pavilion onboarding message."""
    function = participant.get("function", "GTM")
    next_steps = PAVILION_NEXT_STEPS.get(function, {
        "slack_channels": ["#general", "#gtm-leaders"],
        "next_program": "GTM Leadership Accelerator",
        "chapter": "your local chapter dinner"
    })

    system = load_prompt("bridge_handoff")
    user = f"""
Participant: {participant['name']}
Title: {participant.get('title', 'unknown')}
Function: {function}
Their key contribution across the Forge: {participant.get('top_contribution', 'active participation')}
Forge Leader: {participant.get('is_forge_leader', False)}

Recommended Slack channels: {', '.join(next_steps['slack_channels'])}
Recommended next program: {next_steps['next_program']}
Recommended local event: {next_steps['chapter']}

Cohort summary: {cohort_summary}
"""
    return ask_claude(system, user, max_tokens=400)

def run_bridge(cohort_id: str, db_path: str = None):
    """Run Bridge for all participants in a completed cohort."""
    from config import DATABASE_PATH
    db_path = db_path or DATABASE_PATH
    conn = get_connection(db_path)

    participants = conn.execute(
        "SELECT * FROM participants WHERE cohort_id=?", (cohort_id,)
    ).fetchall()

    forge_leaders = {
        row["participant_id"] for row in
        conn.execute("SELECT participant_id FROM forge_leaders WHERE cohort_id=?", (cohort_id,)).fetchall()
    }
    conn.close()

    print(f"Running Bridge for {len(participants)} participants in {cohort_id}")
    messages = []
    for p in participants:
        participant = dict(p)
        participant["is_forge_leader"] = participant["id"] in forge_leaders
        message = generate_bridge_message(participant, f"Completed {cohort_id} Forge")
        messages.append({"participant": participant["name"], "message": message})
        print(f"  ✓ {participant['name']}")

    return messages
```

- [ ] Write `run_bridge.py`
```python
#!/usr/bin/env python3
"""
Usage: python run_bridge.py <cohort_id>
Example: python run_bridge.py pl-fluency-test-001
"""
import sys
from agents.bridge import run_bridge

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python run_bridge.py <cohort_id>")
        sys.exit(1)

    cohort_id = sys.argv[1]
    messages = run_bridge(cohort_id)

    print(f"\n=== BRIDGE PREVIEW: {len(messages)} messages ===")
    for item in messages[:3]:
        print(f"\n--- {item['participant']} ---")
        print(item["message"])
```

- [ ] Run manual test
```bash
python run_bridge.py pl-fluency-test-001
```
Expected: 3 bridge message previews

- [ ] Commit
```bash
git add pavilion/forge/agents/bridge.py pavilion/forge/prompts/bridge_handoff.txt pavilion/forge/run_bridge.py
git commit -m "feat(forge): bridge agent — community handoff messages and 30-day onboarding"
```

---

### Task 16: Railway deployment

**Files:**
- Create: `pavilion/forge/Procfile`
- Create: `pavilion/forge/railway.json`

Note: Three separate Railway services — one per agent, triggered manually for now. Scheduling automated triggers (Attention webhook → Scout) is Phase 2.

- [ ] Write `Procfile`
```
scout: python run_scout.py
forge_master: python run_forge_master.py
bridge: python run_bridge.py
```

- [ ] Write `railway.json`
```json
{
  "build": {
    "builder": "NIXPACKS"
  },
  "deploy": {
    "startCommand": "python run_scout.py",
    "healthcheckPath": null,
    "restartPolicyType": "ON_FAILURE"
  }
}
```

- [ ] Set Railway env vars (confirm each is set before deploying):
```
ANTHROPIC_API_KEY
SLACK_BOT_TOKEN
SLACK_SIGNING_SECRET
DATABASE_PATH=/data/forge.db
HIVE_BRIGHT_API_KEY
GOOGLE_SERVICE_ACCOUNT_JSON
KYLER_DRIVE_FOLDER_ID
```

- [ ] Deploy to Railway and run Scout manually on a test transcript
- Trigger: `python run_scout.py <transcript_path> 1 8 ai-gtm-school-2026-q2`
- Verify: output visible in Railway logs
- Verify: participants written to DB

- [ ] Commit
```bash
git add pavilion/forge/Procfile pavilion/forge/railway.json
git commit -m "feat(forge): railway deployment config"
```

---

## Phase 1 Validation Checklist (Before April 29)

Run the full pipeline on at least one historical transcript end-to-end:

- [ ] Scout reads transcript → correct participants identified
- [ ] Forge Leaders correctly nominated (manually verify against who actually stood out)
- [ ] Reflection messages feel personal, not generic (read 5 samples)
- [ ] Pod formation: 6 people max, same function, Forge Leader as wildcard
- [ ] Bridge messages feel earned and specific (read 5 samples)
- [ ] All outputs saved to DB correctly
- [ ] Get AI GTM School historical transcripts and run second validation

---

## Open Before April 29

1. **Attention API access** — get credentials to auto-pull transcripts post-session instead of manual download
2. **HiveBright API** — confirm endpoint for member lookup by email; test with real members
3. **Slack bot install** — confirm bot is installed in Pavilion workspace and has DM + channel permissions
4. **Kyler's Drive folder ID** — get the folder ID for his course output assets
5. **Participant Slack handle matching** — HiveBright email → Slack user ID lookup (slack_client.lookup_user_by_email)

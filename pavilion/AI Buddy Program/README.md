# Pavilion AI Buddy Program

Peer matching system for Pavilion members (and non-members) who want to share AI knowledge and get a thinking partner in their function.

**Google Sheet (source of truth):**
https://docs.google.com/spreadsheets/d/1nXqkzcW2HMA04jS4zjfB2Y7DT0RTjUdtVZY4XM1WFoY

**Code lives in:**
`/Users/joshmait/Desktop/Claude/outreach-agent/`

---

## How It Works

1. Someone fills out the intake form → their info goes into the **Requests** tab of the Sheet
2. You run the matching script → it proposes pairs in the **Matches** tab (status: Pending Approval)
3. You review matches in the Sheet → type `Approved` in the Approval column for the ones you want to send
4. You run the send script → Claude writes a personalized intro for each approved pair and sends it from your Gmail, cc'ing both people

---

## Workflow Commands

All commands are run from the project directory:

```bash
cd /Users/joshmait/Desktop/Claude/outreach-agent
```

### One-time setup (only needed once)
Creates the Google Sheet with Requests + Matches tabs and verifies Gmail auth:

```bash
venv/bin/python scripts/run_buddy_matching.py setup
```

### Step 1 — Propose matches
Reads the Requests tab, runs the matching algorithm, writes proposed pairs to the Matches tab.
Use `--dry-run` to preview without writing:

```bash
# Preview only (no changes)
venv/bin/python scripts/run_buddy_matching.py propose --dry-run

# Write matches to the Sheet
venv/bin/python scripts/run_buddy_matching.py propose
```

### Step 2 — Review in the Sheet
Open the Matches tab:
https://docs.google.com/spreadsheets/d/1nXqkzcW2HMA04jS4zjfB2Y7DT0RTjUdtVZY4XM1WFoY

For each match you want to send, type `Approved` in the **Approval** column.
Leave blank or type anything else to skip.

### Step 3 — Send intro emails
Reads approved matches, has Claude write a warm intro, sends from josh.mait@joinpavilion.com (cc's both people):

```bash
# Preview only (no emails sent)
venv/bin/python scripts/run_buddy_matching.py send --dry-run

# Send for real
venv/bin/python scripts/run_buddy_matching.py send
```

---

## Matching Logic

Matches are scored on four criteria:

| Criterion | Points |
|---|---|
| Same function (required) | 40 |
| Same chapter / city | 30 |
| Same AI experience level | 20 |
| Member + non-member mix | 10 |

- **Function match is required** — no cross-function matches
- **AI level gap max: 1** — "Just starting out" can match with "Using it regularly" but not "Building with it"
- **Member / non-member mix preferred** — non-members get a taste of Pavilion quality

---

## Google Sheet Structure

**Requests tab** (intake form responses):

| Column | Description |
|---|---|
| Name | Full name |
| Email | Work email |
| Function | Sales / Marketing / CS / RevOps / Finance / HR & People / Operations / Product / Founder / Other |
| Chapter / Location | City chapter or "Remote / No chapter" |
| AI Experience Level | Just starting out / Using it regularly / Building with it |
| Pavilion Member? | Yes / No |
| Anything specific you want help with? | Optional notes |
| Status | Unmatched → Matched (updated automatically after send) |

**Matches tab** (proposed and sent pairs):

| Column | Description |
|---|---|
| Match ID | Short unique ID (e.g., A3F92B1C) |
| Person A Name | |
| Person A Email | |
| Person B Name | |
| Person B Email | |
| Match Basis | e.g., "Function (Marketing) · Chapter (New York) · Same AI level" |
| Match Score | Numeric score (higher = better match) |
| Approval | Type `Approved` here to send |
| Status | Pending Approval → Intro Sent |
| Intro Sent At | Timestamp |

---

## Campaign Config

`/Users/joshmait/Desktop/Claude/outreach-agent/campaigns/ai_buddy_program.yaml`

Key settings:
- `prefer_member_nonmember_mix: true` — prefers mixed pairs
- `max_level_gap: 1` — allows adjacent AI experience levels
- Sender: Josh Mait, Head of Marketing, Pavilion
- Model: claude-opus-4-6 (for writing intros)

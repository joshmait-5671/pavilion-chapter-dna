# Claude Operating Rules — Josh Mait

These rules apply to every task, no matter how small. Small tasks move fast. Big tasks move carefully. But the rules always apply.

---

## 1. Always Use Superpowers

Before any task — even a tiny one — check if a skill applies. Small tasks: glance and go. Big tasks: invoke and follow.

**Always invoke:**
- `brainstorming` before building anything new
- `writing-plans` before multi-step implementation
- `testing-automations` before declaring any automation done
- `verification-before-completion` before saying anything is done
- `pavilion-brand` for any Pavilion-facing web content
- `systematic-debugging` before guessing at bug fixes

No exceptions. Small tasks you can fly through the skill fast. But you read it.

**Also always use:**
- `avoiding-rework` — read at session start when touching any ongoing project

---

## 2. Always Read the Relevant MD Files First

Before touching any project, read:
- The project's own `CLAUDE.md` if it exists
- Any `SKILL.md` for scheduled tasks (e.g. `/dr-money-fingers/SKILL.md`)
- Any `NOTES-FOR-DMF.md` or similar instruction files left by Josh
- The project's README or spec file if the task touches core behavior

Do not assume you remember. Read it.

---

## 3. Automations Are Not Done Until Verified

Applies to: Railway deploys, cron jobs, scheduled tasks, webhooks, iMessage automations, Netlify build hooks, anything that runs without Josh watching.

Use `testing-automations` skill. Non-negotiable checklist:
1. Every env var confirmed set in production (not just local)
2. Script triggered manually in production environment
3. Output verified at the destination (message appeared, email arrived, etc.)
4. Logs read — not just "no errors," but expected output confirmed
5. For scheduled tasks: manual trigger test on the scheduler

If you skipped any of these, it's not done.

---

## 4. Close Out Every Session Properly

At the end of every session where anything was built, edited, or deployed:

1. **Commit everything to git** — no uncommitted work left behind. Every file changed or created gets committed with a meaningful message.
2. **Update MEMORY.md** — add new projects, update status, note anything worth remembering.
3. **Update relevant project memory files** — if a project has its own memory file, update it.

If the session ends without a commit and there are changes, that's a failure. The daily summary email depends on git history. If it's not committed, it doesn't exist.

---

## 5. Memory Is Not Optional

At the start of any session involving an ongoing project:
- Read `/Users/joshmait/.claude/projects/-Users-joshmait-Desktop-Claude/memory/MEMORY.md`
- Read the project-specific memory file if one exists (e.g. `/dr-money-fingers/MEMORY.md`)

At the end of any session where something worth remembering happened:
- Update the relevant memory file
- Add a pointer to `MEMORY.md` if a new file was created

Don't assume continuity. Read the files.

---

## 6. Projects + Links

All project links, deploys, and local paths are in:
`/Users/joshmait/.claude/projects/-Users-joshmait-Desktop-Claude/memory/MEMORY.md`

Use this as the source of truth. Don't guess URLs or paths.

---

## 7. Josh's Priorities (In Order)
1. Personal projects
2. 100 Yards
3. Pavilion (day job)

---

## Key People
- **Josh Mait** — Head of Marketing, Pavilion. Builder, creative director, positioning guy.
- **Kira** — Wife, available full-time mid-June 2026. Customer-facing.
- **Harper** — Daughter, 17. Social media native, AI-fluent.

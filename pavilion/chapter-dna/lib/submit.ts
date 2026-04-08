import { Answers } from '@/types'

interface SubmitParams {
  chapter: string
  chapterId: string
  archetype: string
  answers: Answers
}

/**
 * Submits survey results to a Google Sheet via Apps Script web app.
 * Silent fail — never breaks the UI.
 *
 * Setup:
 * 1. Create a Google Sheet with columns:
 *    Timestamp | Chapter | Archetype | Q1 | Q2 | Q3 | Q4 | Q5 | Q6 | Q7 | Q8 | Q9 | Q10
 *
 * 2. In the sheet: Extensions → Apps Script → paste the script from /docs/sheets-script.js
 *
 * 3. Deploy as Web App: Execute as Me, Anyone can access
 *
 * 4. Add to .env.local:
 *    NEXT_PUBLIC_SHEETS_URL=https://script.google.com/macros/s/YOUR_ID/exec
 */
export async function submitToSheets(params: SubmitParams): Promise<void> {
  const url = process.env.NEXT_PUBLIC_SHEETS_URL
  if (!url) return // Not configured — skip silently

  try {
    await fetch(url, {
      method: 'POST',
      mode: 'no-cors', // Apps Script doesn't send CORS headers
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chapter: params.chapter,
        chapterId: params.chapterId,
        archetype: params.archetype,
        q1: params.answers.q1 ?? '',
        q2: params.answers.q2 ?? '',
        q3: params.answers.q3 ?? '',
        q4: params.answers.q4 ?? '',
        q5: params.answers.q5 ?? '',
        q6: params.answers.q6 ?? '',
        q7: params.answers.q7 ?? '',
        q8: params.answers.q8 ?? '',
        q9: params.answers.q9 ?? '',
        q10: params.answers.q10 ?? '',
        timestamp: new Date().toISOString(),
      }),
    })
  } catch {
    // Never break the UX — submission is best-effort
  }
}

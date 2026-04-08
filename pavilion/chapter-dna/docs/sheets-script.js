/**
 * Chapter DNA — Google Apps Script
 * Paste this into Extensions → Apps Script in your Google Sheet.
 * Then: Deploy → New deployment → Web app → Execute as Me → Anyone
 */

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents)
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet()

    sheet.appendRow([
      data.timestamp,
      data.chapter,
      data.chapterId,
      data.archetype,
      data.q1,
      data.q2,
      data.q3,
      data.q4,
      data.q5,
      data.q6,
      data.q7,
      data.q8,
      data.q9,
      data.q10,
    ])

    return ContentService
      .createTextOutput(JSON.stringify({ success: true }))
      .setMimeType(ContentService.MimeType.JSON)

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ success: false, error: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON)
  }
}

// ── Read all responses (for leaderboard) ────────────────────────────────────

function doGet(e) {
  try {
    const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet()
    const rows = sheet.getDataRange().getValues()

    // Skip header row (index 0)
    const data = []
    for (let i = 1; i < rows.length; i++) {
      const [timestamp, chapter, chapterId, archetype] = rows[i]
      if (chapter && archetype) {
        data.push({ timestamp, chapter, chapterId, archetype })
      }
    }

    return ContentService
      .createTextOutput(JSON.stringify({ success: true, data }))
      .setMimeType(ContentService.MimeType.JSON)

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ success: false, error: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON)
  }
}

// ── Set up column headers on first run ───────────────────────────────────────

function setupHeaders() {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet()
  sheet.getRange(1, 1, 1, 14).setValues([[
    'Timestamp', 'Chapter', 'Chapter ID', 'Archetype',
    'Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6', 'Q7', 'Q8', 'Q9', 'Q10'
  ]])
  sheet.getRange(1, 1, 1, 14).setFontWeight('bold')
}

// Google Apps Script — Pavilion Onboarding Backend
// Deploy as: Web App → Execute as Me → Who has access: Anyone
// Container: create this script from within a Google Sheet (Extensions → Apps Script)
// The active spreadsheet becomes the target for the "Pavilion Onboarding Responses" tab.

const SHEET_NAME = 'Pavilion Onboarding Responses';

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);
    const ss    = SpreadsheetApp.getActiveSpreadsheet();
    let sheet   = ss.getSheetByName(SHEET_NAME);

    // Create sheet + headers on first use
    if (!sheet) {
      sheet = ss.insertSheet(SHEET_NAME);
      sheet.appendRow([
        'timestamp', 'session_id', 'member_name', 'member_email', 'member_city',
        'step_key', 'step_value', 'completed',
      ]);
      sheet.setFrozenRows(1);
    }

    const sessionId = data.session_id || '';
    const stepKey   = data.key        || '';

    // Deduplication: overwrite existing row for same session_id + step_key.
    // Handles back-navigation where the user re-submits a step.
    if (sessionId && stepKey) {
      const values = sheet.getDataRange().getValues();
      for (let i = 1; i < values.length; i++) {
        if (values[i][1] === sessionId && values[i][5] === stepKey) {
          const rowNumber = i + 1; // Sheets rows are 1-indexed
          sheet.getRange(rowNumber, 1, 1, 8).setValues([[
            new Date().toISOString(),
            sessionId,
            data.member_name  || '',
            data.member_email || '',
            data.member_city  || '',
            stepKey,
            JSON.stringify(data.value),
            data.completed ? 'TRUE' : '',
          ]]);
          return ContentService
            .createTextOutput(JSON.stringify({ ok: true, action: 'updated' }))
            .setMimeType(ContentService.MimeType.JSON);
        }
      }
    }

    // No existing row for this session+step — append new
    sheet.appendRow([
      new Date().toISOString(),
      sessionId,
      data.member_name  || '',
      data.member_email || '',
      data.member_city  || '',
      stepKey,
      JSON.stringify(data.value),
      data.completed ? 'TRUE' : '',
    ]);

    return ContentService
      .createTextOutput(JSON.stringify({ ok: true, action: 'appended' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ ok: false, error: err.message }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService.createTextOutput('Pavilion Onboarding Backend — POST only.');
}

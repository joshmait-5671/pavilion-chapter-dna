/**
 * Google Apps Script — AI Buddy Program
 *
 * Handles: waitlist form submissions, live counter, dashboard data
 *
 * IMPORTANT: After updating this code, you must redeploy:
 * Deploy → Manage deployments → Edit (pencil icon) → Version: New version → Deploy
 */

function doPost(e) {
  try {
    var data = JSON.parse(e.postData.contents);
    var sheet = SpreadsheetApp.getActiveSpreadsheet();
    var ws = sheet.getSheetByName('Waitlist');

    if (!ws) {
      ws = sheet.insertSheet('Waitlist');
      ws.appendRow([
        'Timestamp', 'First Name', 'Last Name', 'Email', 'Company',
        'Function', 'Company Revenue', 'City', 'Timezone',
        'AI Experience Level', 'Engagement Style', 'Pavilion Member?',
        'Slack Name', 'Notes', 'Status'
      ]);
    }

    // Check for duplicate email
    var email = (data.email || '').toLowerCase().trim();
    var status = 'Waitlisted';
    if (email) {
      var allData = ws.getDataRange().getValues();
      for (var i = 1; i < allData.length; i++) {
        if (allData[i][3] && allData[i][3].toString().toLowerCase().trim() === email) {
          status = 'DUPLICATE — review';
          break;
        }
      }
    }

    ws.appendRow([
      new Date().toISOString(),
      data.first_name || '',
      data.last_name || '',
      data.email || '',
      data.company || '',
      data.function || '',
      data.revenue || '',
      data.city || '',
      data.timezone || '',
      data.ai_level || '',
      (data.engagement || []).join(', '),
      data.is_member || '',
      data.slack_name || '',
      data.notes || '',
      status
    ]);

    var count = countValid(ws);

    return ContentService
      .createTextOutput(JSON.stringify({ success: true, count: count, duplicate: status !== 'Waitlisted' }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ success: false, error: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  try {
    var sheet = SpreadsheetApp.getActiveSpreadsheet();
    var params = e ? (e.parameter || {}) : {};

    // Dashboard request — return full stats
    if (params.dashboard === 'true') {
      return ContentService
        .createTextOutput(JSON.stringify(getDashboardData(sheet)))
        .setMimeType(ContentService.MimeType.JSON);
    }

    // Simple counter request
    var ws = sheet.getSheetByName('Waitlist');
    var count = ws ? countValid(ws) : 0;

    return ContentService
      .createTextOutput(JSON.stringify({ count: count }))
      .setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService
      .createTextOutput(JSON.stringify({ count: 0, error: err.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function countValid(ws) {
  var allRows = ws.getDataRange().getValues();
  var count = 0;
  var statusCol = allRows[0].indexOf('Status');
  if (statusCol === -1) statusCol = 14; // fallback
  for (var i = 1; i < allRows.length; i++) {
    if (allRows[i][statusCol] !== 'DUPLICATE — review') count++;
  }
  return count;
}

function getDashboardData(sheet) {
  var result = {
    count: 0,
    pool: 0,
    matched: 0,
    total_matches: 0,
    pending_approval: 0,
    by_function: {},
    recent_matches: [],
    alerts: []
  };

  // Waitlist data
  var waitlistWs = sheet.getSheetByName('Waitlist');
  if (waitlistWs) {
    var wRows = waitlistWs.getDataRange().getValues();
    var wHeaders = wRows[0];
    var fnCol = wHeaders.indexOf('Function');
    var statusCol = wHeaders.indexOf('Status');
    if (fnCol === -1) fnCol = 5;
    if (statusCol === -1) statusCol = 14;

    for (var i = 1; i < wRows.length; i++) {
      if (wRows[i][statusCol] === 'DUPLICATE — review') continue;
      result.count++;
      var fn = wRows[i][fnCol] || 'Unknown';
      if (!result.by_function[fn]) result.by_function[fn] = { waitlisted: 0, pool: 0, matched: 0 };
      if (wRows[i][statusCol] !== 'Promoted') {
        result.by_function[fn].waitlisted++;
      }
    }
  }

  // Requests data (active pool)
  var requestsWs = sheet.getSheetByName('Requests');
  if (requestsWs && requestsWs.getLastRow() > 1) {
    var rRows = requestsWs.getDataRange().getValues();
    var rHeaders = rRows[0];
    var rFnCol = rHeaders.indexOf('Function');
    var rStatusCol = rHeaders.indexOf('Status');
    if (rFnCol === -1) rFnCol = 4;
    if (rStatusCol === -1) rStatusCol = 12;

    for (var j = 1; j < rRows.length; j++) {
      var status = (rRows[j][rStatusCol] || '').toString().toLowerCase();
      var fn = rRows[j][rFnCol] || 'Unknown';
      if (!result.by_function[fn]) result.by_function[fn] = { waitlisted: 0, pool: 0, matched: 0 };

      if (status === 'unmatched' || status.indexOf('seeking') > -1) {
        result.pool++;
        result.by_function[fn].pool++;
      } else if (status === 'matched') {
        result.matched++;
        result.by_function[fn].matched++;
      }
    }
  }

  // Matches data
  var matchesWs = sheet.getSheetByName('Matches');
  if (matchesWs && matchesWs.getLastRow() > 1) {
    var mRows = matchesWs.getDataRange().getValues();
    var mHeaders = mRows[0];

    for (var k = mRows.length - 1; k >= 1; k--) {
      var introSent = (mRows[k][mHeaders.indexOf('Intro Sent')] || '').toString().toLowerCase();
      var approval = (mRows[k][mHeaders.indexOf('Approval')] || '').toString().toLowerCase();

      if (introSent === 'yes') result.total_matches++;
      if (approval === 'pending approval') result.pending_approval++;

      // Recent matches (last 10)
      if (result.recent_matches.length < 10) {
        result.recent_matches.push({
          match_id: mRows[k][mHeaders.indexOf('Match ID')] || '',
          person_a: mRows[k][mHeaders.indexOf('Person A Name')] || '',
          person_b: mRows[k][mHeaders.indexOf('Person B Name')] || '',
          tier: mRows[k][mHeaders.indexOf('Match Tier')] || '',
          score: mRows[k][mHeaders.indexOf('Match Score')] || '',
          status: introSent === 'yes' ? 'Intro Sent' : (approval === 'pending approval' ? 'Pending Approval' : approval)
        });
      }
    }
  }

  // Lifecycle data — ghost alerts
  var lifecycleWs = sheet.getSheetByName('Lifecycle');
  if (lifecycleWs && lifecycleWs.getLastRow() > 1) {
    var lRows = lifecycleWs.getDataRange().getValues();
    var lHeaders = lRows[0];
    var sentDateCol = lHeaders.indexOf('Sent Date');
    var responseCol = lHeaders.indexOf('Response');
    var checkTypeCol = lHeaders.indexOf('Check Type');
    var personNameCol = lHeaders.indexOf('Person Name');
    var personEmailCol = lHeaders.indexOf('Person Email');
    var buddyNameCol = lHeaders.indexOf('Buddy Name');
    var matchIdCol = lHeaders.indexOf('Match ID');

    var now = new Date();
    var ghostThreshold = 14; // days

    for (var g = 1; g < lRows.length; g++) {
      var response = (lRows[g][responseCol] || '').toString().trim();
      var sentDate = lRows[g][sentDateCol];
      var checkType = (lRows[g][checkTypeCol] || '').toString().trim();

      // Skip non-actionable types and rows with responses
      if (response || !sentDate) continue;
      if (checkType === 'no_match_yet' || checkType === 'nonmember_nurture') continue;

      var sentMs = new Date(sentDate).getTime();
      var daysSince = Math.floor((now.getTime() - sentMs) / (1000 * 60 * 60 * 24));

      if (daysSince >= ghostThreshold) {
        result.alerts.push({
          match_id: (lRows[g][matchIdCol] || '').toString(),
          person_name: (lRows[g][personNameCol] || '').toString(),
          person_email: (lRows[g][personEmailCol] || '').toString(),
          buddy_name: (lRows[g][buddyNameCol] || '').toString(),
          check_type: checkType,
          days_since: daysSince
        });
      }
    }
  }

  return result;
}

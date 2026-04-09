// submit.js — Fire-and-forget progressive step submission to Apps Script.
// Fails silently — never blocks the wizard.

(function () {
  // Replace with actual Apps Script web app URL after deploy
  const ENDPOINT = '';

  // Stable session ID for this wizard run
  const SESSION_ID = (() => {
    const key = 'pav-session-id';
    let id = sessionStorage.getItem(key);
    if (!id) {
      id = 'sess-' + Date.now() + '-' + Math.random().toString(36).slice(2, 8);
      sessionStorage.setItem(key, id);
    }
    return id;
  })();

  window.submitStep = function (key, value) {
    if (!ENDPOINT) return; // No-op until endpoint is configured

    const payload = {
      session_id:   SESSION_ID,
      member_name:  window.member?.name  || '',
      member_email: window.member?.email || '',
      member_city:  window.member?.city  || '',
      key,
      value,
      completed: false,
    };

    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }).catch(() => {}); // Silently swallow all errors
  };

  window.submitComplete = function () {
    if (!ENDPOINT) return;
    const payload = {
      session_id:   SESSION_ID,
      member_name:  window.member?.name  || '',
      member_email: window.member?.email || '',
      member_city:  window.member?.city  || '',
      key: '__completed__',
      value: true,
      completed: true,
    };
    fetch(ENDPOINT, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload),
    }).catch(() => {});
  };
})();

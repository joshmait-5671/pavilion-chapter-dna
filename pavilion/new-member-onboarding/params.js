// params.js — Parse URL params; export `member` with safe fallbacks.
// URL format: ?name=Sarah+Chen&email=sarah@co.com&city=San+Francisco
// Fallbacks: hasName=false → welcome shows generic; hasCity=false → city steps degrade gracefully.

(function () {
  const p = new URLSearchParams(window.location.search);

  const raw = {
    name:  p.get('name')  || '',
    email: p.get('email') || '',
    city:  p.get('city')  || '',
  };

  // Sanitize — strip any HTML to prevent XSS
  function clean(str) {
    const div = document.createElement('div');
    div.textContent = str;
    return div.innerHTML.slice(0, 120);
  }

  const name  = clean(raw.name);
  const email = clean(raw.email);
  const city  = clean(raw.city);

  window.member = {
    name,
    firstName: name.split(' ')[0], // '' if name is empty — engine checks hasName before using
    email,
    city,
    hasName: name.trim().length > 0,
    hasCity: city.trim().length > 0,
  };
})();

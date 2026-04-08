/* ============================================================
   PAVILION TEAMS — MAIN JS
   ============================================================ */

/* ─── SMOOTH SCROLL (fallback for older browsers) ──────────── */
document.querySelectorAll('a[href^="#"]').forEach(anchor => {
  anchor.addEventListener('click', function (e) {
    const target = document.querySelector(this.getAttribute('href'));
    if (target) {
      e.preventDefault();
      target.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
  });
});

/* ─── STICKY HEADER SHADOW ON SCROLL ───────────────────────── */
const header = document.querySelector('.site-header');
if (header) {
  window.addEventListener('scroll', () => {
    header.classList.toggle('scrolled', window.scrollY > 10);
  }, { passive: true });
}

/* ─── FADE-IN ON SCROLL (Intersection Observer) ────────────── */
const fadeEls = document.querySelectorAll(
  '.hero, .pain-card, .benefit-item, .testimonial-card, .stat'
);

const observer = new IntersectionObserver((entries) => {
  entries.forEach(entry => {
    if (entry.isIntersecting) {
      entry.target.classList.add('visible');
      observer.unobserve(entry.target);
    }
  });
}, { threshold: 0.12 });

fadeEls.forEach(el => {
  el.classList.add('fade-in');
  observer.observe(el);
});

/* ─── HUBSPOT FORM INIT ─────────────────────────────────────── */
// Uncomment and configure once HubSpot portal/form IDs are ready
// window.addEventListener('load', () => {
//   if (typeof hbspt !== 'undefined') {
//     hbspt.forms.create({
//       region: "na1",
//       portalId: "YOUR_PORTAL_ID",
//       formId: "YOUR_FORM_ID",
//       target: "#hubspot-form",
//     });
//   }
// });

/* ─── UTILITY: Add .scrolled styles in CSS as needed ────────── */
// .site-header.scrolled { box-shadow: 0 2px 12px rgba(0,0,0,0.08); }

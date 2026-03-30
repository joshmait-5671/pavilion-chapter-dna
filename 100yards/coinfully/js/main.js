// main.js — Scroll behavior, nav active state, mobile menu

document.addEventListener('DOMContentLoaded', () => {

  // Nav scroll shadow
  const nav = document.querySelector('.nav');
  if (nav) {
    window.addEventListener('scroll', () => {
      nav.style.boxShadow = window.scrollY > 20
        ? '0 2px 20px rgba(0,0,0,0.1)'
        : 'none';
    });
  }

  // Mobile burger menu
  const burger = document.querySelector('.nav__burger');
  const navLinks = document.querySelector('.nav__links');
  if (burger && navLinks) {
    burger.addEventListener('click', () => {
      const isOpen = navLinks.classList.contains('nav__links--open');
      if (isOpen) {
        navLinks.classList.remove('nav__links--open');
        navLinks.removeAttribute('style');
      } else {
        navLinks.classList.add('nav__links--open');
        navLinks.style.cssText = 'display:flex;flex-direction:column;position:absolute;top:68px;left:0;right:0;background:white;padding:24px;gap:16px;border-bottom:1px solid rgba(0,0,0,0.08);z-index:99;';
      }
    });

    // Close mobile menu when a link is clicked
    navLinks.querySelectorAll('a').forEach(a => {
      a.addEventListener('click', () => {
        navLinks.classList.remove('nav__links--open');
        navLinks.removeAttribute('style');
      });
    });
  }

  // Smooth scroll for anchor links
  document.querySelectorAll('a[href^="#"]').forEach(a => {
    a.addEventListener('click', e => {
      const href = a.getAttribute('href');
      if (href === '#') return;
      const target = document.querySelector(href);
      if (target) {
        e.preventDefault();
        const offset = 80; // nav height + breathing room
        const top = target.getBoundingClientRect().top + window.scrollY - offset;
        window.scrollTo({ top, behavior: 'smooth' });
      }
    });
  });

});

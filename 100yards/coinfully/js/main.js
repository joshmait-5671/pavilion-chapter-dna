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

  // ── Coin Scanner ────────────────────────────────────────────
  const coinDrop      = document.getElementById('coinDrop');
  const coinFile      = document.getElementById('coinFile');
  const coinDropFace  = document.getElementById('coinDropFace');
  const coinSelected  = document.getElementById('coinSelected');
  const coinFileName  = document.getElementById('coinFileName');
  const coinRemove    = document.getElementById('coinRemove');
  const coinForm      = document.getElementById('coinForm');
  const coinEmail     = document.getElementById('coinEmail');
  const coinSubmit    = document.getElementById('coinSubmit');
  const coinSuccess   = document.getElementById('coinSuccess');
  const coinError     = document.getElementById('coinError');

  let selectedFile = null;

  // Show simple confirmation state — no image rendering, works on all devices
  function showSelected(file) {
    selectedFile = file;
    coinDropFace.style.display = 'none';
    coinSelected.style.display = 'flex';
    // Trim long filenames for display
    const name = file.name.length > 32 ? file.name.slice(0, 29) + '…' : file.name;
    coinFileName.textContent = name;
  }

  function clearSelected() {
    selectedFile = null;
    coinDropFace.style.display = '';
    coinSelected.style.display = 'none';
    coinFileName.textContent = '';
    coinFile.value = '';
  }

  if (coinFile) {
    coinFile.addEventListener('change', () => {
      if (coinFile.files[0]) showSelected(coinFile.files[0]);
    });
  }

  if (coinRemove) {
    coinRemove.addEventListener('click', e => {
      e.stopPropagation();
      e.preventDefault();
      clearSelected();
    });
  }

  // Drag & drop (desktop only — iOS doesn't support this, that's fine)
  if (coinDrop) {
    ['dragenter','dragover'].forEach(evt => {
      coinDrop.addEventListener(evt, e => {
        e.preventDefault();
        coinDrop.classList.add('is-dragover');
      });
    });
    ['dragleave','drop'].forEach(evt => {
      coinDrop.addEventListener(evt, e => {
        e.preventDefault();
        coinDrop.classList.remove('is-dragover');
      });
    });
    coinDrop.addEventListener('drop', e => {
      const file = e.dataTransfer.files[0];
      if (file && file.type.startsWith('image/')) showSelected(file);
    });
  }

  // Form submit — wires to serverless function once backend is ready
  if (coinForm) {
    coinForm.addEventListener('submit', async e => {
      e.preventDefault();
      coinError.style.display = 'none';

      if (!selectedFile) {
        coinError.textContent = 'Please add a photo of your coin first.';
        coinError.style.display = 'block';
        return;
      }

      const email = coinEmail.value.trim();
      if (!email || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
        coinError.textContent = 'Please enter a valid email address.';
        coinError.style.display = 'block';
        return;
      }

      // Show loading
      coinSubmit.querySelector('.coin-form__submit-text').style.display = 'none';
      coinSubmit.querySelector('.coin-form__submit-loading').style.display = 'inline';
      coinSubmit.disabled = true;

      try {
        // Resize image to max 1200px and convert to base64 before sending
        const { base64, type } = await resizeImage(selectedFile, 1200);

        const res = await fetch('/.netlify/functions/coin-scan', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ email, imageBase64: base64, imageType: type })
        });

        if (!res.ok) throw new Error('Server error');

        // Success
        coinForm.style.display = 'none';
        coinDrop.style.display = 'none';
        coinSuccess.style.display = 'block';

      } catch (err) {
        coinSubmit.querySelector('.coin-form__submit-text').style.display = 'inline';
        coinSubmit.querySelector('.coin-form__submit-loading').style.display = 'none';
        coinSubmit.disabled = false;
        coinError.textContent = 'Something went wrong. Please try again or call us directly.';
        coinError.style.display = 'block';
      }
    });
  }
  // Resize image using canvas before upload
  function resizeImage(file, maxPx) {
    return new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = e => {
        const img = new Image();
        img.onload = () => {
          const scale = Math.min(1, maxPx / Math.max(img.width, img.height));
          const w = Math.round(img.width * scale);
          const h = Math.round(img.height * scale);
          const canvas = document.createElement('canvas');
          canvas.width = w;
          canvas.height = h;
          canvas.getContext('2d').drawImage(img, 0, 0, w, h);
          const dataUrl = canvas.toDataURL('image/jpeg', 0.88);
          resolve({
            base64: dataUrl.split(',')[1],
            type: 'image/jpeg'
          });
        };
        img.onerror = reject;
        img.src = e.target.result;
      };
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });
  }
  // ── End Coin Scanner ─────────────────────────────────────────

  // Office tour hotspots
  document.querySelectorAll('.hotspot').forEach(btn => {
    // Build the tooltip element once
    const tip = document.createElement('span');
    tip.className = 'hotspot__tip';
    tip.textContent = btn.dataset.tip || '';

    // Position above or below based on vertical placement in photo
    const topPct = parseFloat(btn.style.top);
    if (topPct < 35) tip.classList.add('hotspot__tip--below');

    btn.appendChild(tip);

    btn.addEventListener('click', e => {
      e.stopPropagation();
      const isOpen = btn.classList.contains('is-open');

      // Close all others
      document.querySelectorAll('.hotspot.is-open').forEach(h => h.classList.remove('is-open'));

      if (!isOpen) btn.classList.add('is-open');
    });
  });

  // Click outside closes all hotspots
  document.addEventListener('click', () => {
    document.querySelectorAll('.hotspot.is-open').forEach(h => h.classList.remove('is-open'));
  });

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

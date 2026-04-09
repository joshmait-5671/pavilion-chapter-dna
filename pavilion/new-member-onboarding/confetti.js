// confetti.js — Minimal canvas confetti. Call window.launchConfetti() to fire.

window.launchConfetti = function () {
  const canvas = document.createElement('canvas');
  canvas.style.cssText = 'position:fixed;inset:0;pointer-events:none;z-index:999;width:100%;height:100%;';
  document.body.appendChild(canvas);
  canvas.width  = window.innerWidth;
  canvas.height = window.innerHeight;

  const ctx = canvas.getContext('2d');
  const colors = ['#DF285B', '#2B1887', '#EDEAFF', '#F14972', '#180A5C', '#ffffff', '#EDEAFF'];
  const pieces = Array.from({ length: 100 }, () => ({
    x:    Math.random() * canvas.width,
    y:    Math.random() * canvas.height * -0.5,
    r:    Math.random() * 6 + 3,
    d:    Math.random() * 2.5 + 1,
    c:    colors[Math.floor(Math.random() * colors.length)],
    tilt: Math.random() * 10 - 10,
    ts:   Math.random() * 0.2 - 0.1,
  }));

  let frame;
  let start = null;
  const duration = 2000;

  function draw(ts) {
    if (!start) start = ts;
    const elapsed = ts - start;
    const alpha = Math.max(0, 1 - elapsed / duration);

    ctx.clearRect(0, 0, canvas.width, canvas.height);
    pieces.forEach(p => {
      p.y    += p.d + 0.4;
      p.tilt += p.ts;
      ctx.globalAlpha = alpha;
      ctx.beginPath();
      ctx.ellipse(p.x, p.y, p.r, p.r * 0.45, p.tilt, 0, Math.PI * 2);
      ctx.fillStyle = p.c;
      ctx.fill();
    });

    if (elapsed < duration) {
      frame = requestAnimationFrame(draw);
    } else {
      cancelAnimationFrame(frame);
      canvas.remove();
    }
  }

  frame = requestAnimationFrame(draw);
};

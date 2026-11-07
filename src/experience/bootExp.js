// Experience Section Lifecycle & WebGL Controller
import { createGL } from '../gl/renderer.js';
import { ExpStage } from './expStage.js';

export async function initExperience() {
  const section = document.getElementById('experience');
  const canvas = document.getElementById('expCanvas');
  const fullTrack = document.getElementById('expFullTrack');
  const nextBtn = document.getElementById('expSideNext');
  const prevBtn = document.getElementById('expSidePrev');
  const slide1 = document.getElementById('expSlide1');
  const slide2 = document.getElementById('expSlide2');
  const infoDisplay = document.getElementById('expInfoDisplay');
  const expandBtn = document.getElementById('expExpandBtn');
  const expandLabel = document.getElementById('expExpandLabel');
  const collapseBtn = document.getElementById('expCollapseBtn');
  const detailsDrawer = document.getElementById('expDetailsDrawer');
  const bldZone = document.getElementById('expBldZone');

  if (!section || !fullTrack) return null;

  let stage = null;
  if (canvas) {
    const gl = createGL(canvas);
    if (gl) {
      stage = new ExpStage(canvas, gl);
    }
  }

  if (infoDisplay) {
    infoDisplay.addEventListener('pointerenter', () => {
      if (stage) stage.hover = 1.0;
    });
    infoDisplay.addEventListener('pointerleave', () => {
      if (stage) stage.hover = 0.0;
    });
  }

  function toggleExpanded(force) {
    if (!infoDisplay) return;
    const isExp = typeof force === 'boolean' ? force : !infoDisplay.classList.contains('is-expanded');
    infoDisplay.classList.toggle('is-expanded', isExp);
    if (expandBtn) expandBtn.setAttribute('aria-expanded', String(isExp));
    if (expandLabel) expandLabel.textContent = isExp ? 'Close' : 'Details';
    if (detailsDrawer) detailsDrawer.setAttribute('aria-hidden', String(!isExp));
  }

  expandBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleExpanded();
  });
  collapseBtn?.addEventListener('click', (e) => {
    e.stopPropagation();
    toggleExpanded(false);
  });

  // Pointer tracking for 3D WebGL stage camera (panel & building remain anchored)
  const coarseMQ = matchMedia('(pointer: coarse)');

  function onPointerMove(e) {
    if (coarseMQ.matches || !stage) return;
    const w = window.innerWidth || 1;
    const h = window.innerHeight || 1;
    stage.pointer.tx = (e.clientX / w) * 2 - 1;
    stage.pointer.ty = (e.clientY / h) * 2 - 1;
  }

  function onPointerLeave() {
    if (stage) {
      stage.pointer.tx = 0;
      stage.pointer.ty = 0;
    }
  }

  section.addEventListener('pointermove', onPointerMove, { passive: true });
  section.addEventListener('pointerleave', onPointerLeave);

  // Horizontal slide controller
  let currentSlide = 0;

  function goToSlide(index) {
    if (!slide2) return;
    currentSlide = Math.max(0, Math.min(1, index));
    fullTrack.style.transform = currentSlide === 1 ? 'translateX(-50%)' : 'translateX(0%)';

    if (slide1 && slide2) {
      slide1.classList.toggle('is-active', currentSlide === 0);
      slide1.setAttribute('aria-hidden', String(currentSlide !== 0));
      slide2.classList.toggle('is-active', currentSlide === 1);
      slide2.setAttribute('aria-hidden', String(currentSlide !== 1));
    }
  }

  nextBtn?.addEventListener('click', () => goToSlide(1));
  prevBtn?.addEventListener('click', () => goToSlide(0));

  // Keyboard navigation
  window.addEventListener('keydown', (e) => {
    const rect = section.getBoundingClientRect();
    const inView = rect.top < window.innerHeight * 0.7 && rect.bottom > window.innerHeight * 0.3;
    if (!inView) return;

    if (e.key === 'ArrowRight' && currentSlide === 0) goToSlide(1);
    else if (e.key === 'ArrowLeft' && currentSlide === 1) goToSlide(0);
  });

  // Touch gesture support on full-screen track (preserves vertical scroll)
  let touchStartX = 0;
  let touchStartY = 0;
  let isHorizontal = false;

  section.addEventListener('touchstart', (e) => {
    if (e.touches.length !== 1) return;
    touchStartX = e.touches[0].clientX;
    touchStartY = e.touches[0].clientY;
    isHorizontal = false;
  }, { passive: true });

  section.addEventListener('touchmove', (e) => {
    if (e.touches.length !== 1) return;
    const dx = Math.abs(e.touches[0].clientX - touchStartX);
    const dy = Math.abs(e.touches[0].clientY - touchStartY);
    if (dx > 25 && dx > dy * 1.5) isHorizontal = true;
  }, { passive: true });

  section.addEventListener('touchend', (e) => {
    if (!isHorizontal) return;
    const diff = touchStartX - e.changedTouches[0].clientX;
    if (diff > 50 && currentSlide === 0) goToSlide(1);
    else if (diff < -50 && currentSlide === 1) goToSlide(0);
  }, { passive: true });

  // WebGL Render Loop & Resize
  let running = false;
  let rafId = 0;
  let t0 = performance.now();

  function resize() {
    if (!stage || !canvas) return;
    const w = section.clientWidth || window.innerWidth;
    const h = section.clientHeight || window.innerHeight;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    stage.resize(w, h, dpr);
  }

  window.addEventListener('resize', resize);
  resize();

  function loop(now) {
    if (!running) return;
    const t = (now - t0) / 1000;
    if (stage) stage.render(t);
    rafId = requestAnimationFrame(loop);
  }

  // IntersectionObserver: trigger visibility and start 3D loop
  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        section.classList.add('is-visible');
        if (stage) stage.active = 1.0;
        running = true;
        cancelAnimationFrame(rafId);
        rafId = requestAnimationFrame(loop);
      } else {
        running = false;
        cancelAnimationFrame(rafId);
        if (stage) stage.active = 0.0;
      }
    }, { threshold: 0.15 });
    obs.observe(section);
  } else {
    section.classList.add('is-visible');
    running = true;
    rafId = requestAnimationFrame(loop);
  }

  return { section, stage };
}

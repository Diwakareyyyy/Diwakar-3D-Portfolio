// Scene two lifecycle: procedural WebGL creative universe with video fallback.
//
// Renders the eleven skill cards in 3D around the central figure, with
// warm rim-lighting, light ribbon trails, subtle float dynamics, and mouse parallax.
// If WebGL2 is unavailable, gracefully plays the reference film.

import { createGL } from '../gl/renderer.js';
import { Universe } from './universe.js';

const SEAM = 0.45;

export async function initUniverse() {
  const section = document.getElementById('universe');
  const canvas = document.getElementById('uniStage');
  const film = document.getElementById('uniFilm');
  const veil = document.getElementById('uniVeil');
  if (!section) return null;

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;
  const coarseMQ = matchMedia('(pointer: coarse)');

  // --------------------------------------------------------------------------
  // Video fallback player (used if WebGL2 is unavailable)
  // --------------------------------------------------------------------------
  const runFallbackVideo = () => {
    if (!film || !veil) return;
    section.classList.add('is-fallback');
    const state = { visible: false, raf: 0, entered: false };

    const play = () => {
      film.play().catch(() => {
        const retry = () => { film.play().catch(() => {}); };
        window.addEventListener('pointerdown', retry, { once: true });
        window.addEventListener('scroll', retry, { once: true });
      });
    };

    const watchSeam = () => {
      const tick = () => {
        if (!state.visible) return;
        const d = film.duration || 10;
        const t = film.currentTime;
        const toEnd = d - t;
        const dip = Math.min(1, Math.min(t, Math.max(toEnd, 0)) / SEAM);
        veil.style.opacity = state.entered ? String((1 - dip) * 0.92) : '1';
        state.raf = film.requestVideoFrameCallback
          ? film.requestVideoFrameCallback(tick)
          : requestAnimationFrame(tick);
      };
      state.raf = film.requestVideoFrameCallback
        ? film.requestVideoFrameCallback(tick)
        : requestAnimationFrame(tick);
    };

    new IntersectionObserver((entries) => {
      for (const e of entries) {
        state.visible = e.isIntersecting;
        if (e.isIntersecting) {
          if (!state.entered) {
            state.entered = true;
            section.classList.add('is-on');
            veil.style.opacity = '0';
          }
          if (reduced) {
            film.currentTime = Math.min(6.5, (film.duration || 10) * 0.6);
            film.pause();
            veil.style.opacity = '0';
          } else {
            play();
            watchSeam();
          }
        } else {
          film.pause();
        }
      }
    }, { threshold: 0.30 }).observe(section);

    document.addEventListener('visibilitychange', () => {
      if (document.visibilityState === 'hidden') film.pause();
      else if (state.visible && !reduced) play();
    });
  };

  // --------------------------------------------------------------------------
  // Procedural WebGL Engine
  // --------------------------------------------------------------------------
  let gl = null;
  if (canvas) {
    try {
      gl = createGL(canvas, { alpha: false, antialias: true, depth: false });
    } catch {
      gl = null;
    }
  }

  if (!gl) {
    runFallbackVideo();
    return { section, fallback: true };
  }

  let universe;
  try {
    universe = new Universe(canvas, gl);
    await universe.load();
  } catch (err) {
    console.warn('[universe] WebGL scene load failed, falling back to film:', err);
    runFallbackVideo();
    return { section, fallback: true };
  }

  const resize = () => {
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    universe.resize(section.clientWidth, section.clientHeight, dpr);
  };
  resize();

  let resizeTimer;
  window.addEventListener('resize', () => {
    clearTimeout(resizeTimer);
    resizeTimer = setTimeout(resize, 140);
  });
  window.addEventListener('orientationchange', () => setTimeout(resize, 220));

  // Pointer parallax & card pick
  section.addEventListener('pointermove', (e) => {
    if (coarseMQ.matches) return;
    const r = canvas.getBoundingClientRect();
    const px = e.clientX - r.left;
    const py = e.clientY - r.top;
    universe.pointer.tx = (px / r.width) * 2 - 1;
    universe.pointer.ty = (py / r.height) * 2 - 1;
    universe.pointer.inside = true;
    universe.hovered = universe.pick(px, py);
    section.classList.toggle('is-picking', universe.hovered >= 0);
  }, { passive: true });

  section.addEventListener('pointerleave', () => {
    universe.pointer.inside = false;
    universe.hovered = -1;
    section.classList.remove('is-picking');
  });

  // Click / Tap: a 3D pulse + energy ripple on the block. Never navigates/scrolls.
  let hoverResetTimer = 0;
  section.addEventListener('click', (e) => {
    const r = canvas.getBoundingClientRect();
    const i = universe.pick(e.clientX - r.left, e.clientY - r.top);
    if (i >= 0) {
      e.preventDefault();
      universe.click(i);
      if (coarseMQ.matches) {
        universe.hovered = i;
        clearTimeout(hoverResetTimer);
        hoverResetTimer = setTimeout(() => { universe.hovered = -1; }, 1100);
      }
    }
  });

  // Subtle scroll parallax tracking (cached metrics to avoid synchronous reflow)
  let scrollProgress = 0;
  let cachedUniTop = 0;
  let cachedUniTravel = 0;
  const updateUniMetrics = () => {
    cachedUniTop = section.offsetTop;
    cachedUniTravel = section.offsetHeight + window.innerHeight;
  };
  updateUniMetrics();
  window.addEventListener('resize', updateUniMetrics);

  const onScroll = () => {
    if (cachedUniTravel > 0) {
      const scrollY = window.scrollY || window.pageYOffset || 0;
      scrollProgress = Math.max(0, Math.min(1, (scrollY + window.innerHeight - cachedUniTop) / cachedUniTravel));
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });

  // Animation frame loop
  let rafId = 0;
  let lastTime = 0;
  let startedAt = 0;
  let running = false;
  let entered = false;

  const frame = (now) => {
    if (!running) return;
    const dt = Math.min(0.05, (now - lastTime) / 1000 || 0.016);
    lastTime = now;
    const t = (now - startedAt) / 1000;

    universe.render(t, dt, scrollProgress);
    rafId = requestAnimationFrame(frame);
  };

  new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        if (!entered) {
          entered = true;
          startedAt = performance.now();
          section.classList.add('is-on');
          if (veil) veil.style.opacity = '0';
        }
        running = true;
        lastTime = performance.now();
        cancelAnimationFrame(rafId);
        rafId = requestAnimationFrame(frame);
      } else {
        running = false;
        cancelAnimationFrame(rafId);
      }
    }
  }, { threshold: 0.15 }).observe(section);

  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') {
      running = false;
      cancelAnimationFrame(rafId);
    } else if (entered) {
      running = true;
      lastTime = performance.now();
      cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(frame);
    }
  });

  return { universe, section, fallback: false };
}

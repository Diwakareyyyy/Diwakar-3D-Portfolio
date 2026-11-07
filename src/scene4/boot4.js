// Scene four lifecycle: Two-row continuous project scrolling gallery with
// central seated developer workstation and interactive project details lightbox.
// ==============================================================================

import { createGL } from '../gl/renderer.js';
import { Gallery } from './gallery.js';
import { PERSON, fitCover } from './layout4.js';
import { PROJECTS } from '../data/projects.js';
import { sample4, T4 } from './timeline4.js';

const damp = (v, to, k, dt) => v + (to - v) * (1 - Math.exp(-k * dt));

export async function initGallery() {
  const section = document.getElementById('gallery');
  const canvas = document.getElementById('galleryStage');
  const streamTop = document.getElementById('projStreamTop');
  const streamBottom = document.getElementById('projStreamBottom');
  const trackTop = document.getElementById('projTrackTop');
  const trackBottom = document.getElementById('projTrackBottom');
  const person = document.getElementById('galleryPerson');
  const personWrap = document.getElementById('galleryPersonWrap');
  if (!section || !canvas || !trackTop || !trackBottom || !person) return null;

  // Modal elements
  const modal = document.getElementById('projectModal');
  const projModalPanel = document.getElementById('projModalPanel');
  const projModalImg = document.getElementById('projModalImg');
  const projModalTitle = document.getElementById('projModalTitle');
  const projModalShort = document.getElementById('projModalShort');
  const projModalDesc = document.getElementById('projModalDesc');
  const projModalProblem = document.getElementById('projModalProblem');
  const projModalSolution = document.getElementById('projModalSolution');
  const projModalFeatures = document.getElementById('projModalFeatures');
  const projModalTags = document.getElementById('projModalTags');
  const projModalCategory = document.getElementById('projModalCategory');
  const projModalCount = document.getElementById('projModalCount');
  const projModalGithub = document.getElementById('projModalGithub');
  const projModalClose = document.getElementById('projModalClose');
  const projModalBackdrop = document.getElementById('projModalBackdrop');
  const projModalBackBtn = document.getElementById('projModalBackBtn');
  const projModalPrev = document.getElementById('projModalPrev');
  const projModalNext = document.getElementById('projModalNext');

  const gl = createGL(canvas);
  if (!gl) {
    section.classList.add('is-fallback', 'is-set');
    return null;
  }
  const gallery = new Gallery(canvas, gl);
  await gallery.load();

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Split projects into Row 1 (0..5) and Row 2 (6..11)
  const row1Projects = PROJECTS.slice(0, 6);
  const row2Projects = PROJECTS.slice(6, 12);

  function createCardElement(project, originalIndex) {
    const btn = document.createElement('button');
    btn.type = 'button';
    btn.className = 'proj-panel';
    btn.dataset.index = String(originalIndex);
    btn.setAttribute('aria-label', `Project: ${project.name}`);

    btn.innerHTML = `
      <img class="proj-panel__img" src="${project.image}" alt="${project.name}" draggable="false" loading="lazy">
      <div class="proj-panel__glow" aria-hidden="true"></div>
      <div class="proj-panel__sheen" aria-hidden="true"></div>
    `;

    btn.addEventListener('click', () => openModal(originalIndex));
    return btn;
  }

  // Populate Row 1 (duplicated once for seamless infinite right-to-left loop)
  const row1Cards = [];
  [...row1Projects, ...row1Projects].forEach((p, i) => {
    const originalIndex = i % row1Projects.length;
    const cardEl = createCardElement(p, originalIndex);
    trackTop.appendChild(cardEl);
    row1Cards.push(cardEl);
  });

  // Populate Row 2 (duplicated once for seamless infinite left-to-right loop)

const row2Cards = [];
  [...row2Projects, ...row2Projects].forEach((p, i) => {
    const originalIndex = 6 + (i % row2Projects.length);
    const cardEl = createCardElement(p, originalIndex);
    trackBottom.appendChild(cardEl);
    row2Cards.push(cardEl);
  });

  // ---- Modal Controller (Interactive Project Details View) -----------------
  let activeModalIdx = 0;
  function updateModal(idx) {
    activeModalIdx = (idx + PROJECTS.length) % PROJECTS.length;
    const p = PROJECTS[activeModalIdx];

    if (projModalImg) {
      projModalImg.src = p.image;
      projModalImg.alt = p.name;
    }
    if (projModalTitle) projModalTitle.textContent = p.name;
    if (projModalDesc) projModalDesc.textContent = p.desc || p.shortDesc;
    if (projModalCategory) projModalCategory.textContent = p.category || 'Software Engineering';
    if (projModalCount) {
      projModalCount.textContent = `${String(activeModalIdx + 1).padStart(2, '0')} / ${String(PROJECTS.length).padStart(2, '0')}`;
    }
  }

  function openModal(idx) {
    if (!modal) return;
    updateModal(idx);
    modal.hidden = false;
    modal.classList.add('is-open');
    document.body.style.overflow = 'hidden';
  }

  function closeModal() {
    if (!modal) return;
    modal.classList.remove('is-open');
    setTimeout(() => {
      if (!modal.classList.contains('is-open')) {
        modal.hidden = true;
        document.body.style.overflow = '';
      }
    }, 280);
  }

  projModalClose?.addEventListener('click', closeModal);
  projModalBackBtn?.addEventListener('click', closeModal);
  projModalBackdrop?.addEventListener('click', closeModal);
  projModalPrev?.addEventListener('click', () => updateModal(activeModalIdx - 1));
  projModalNext?.addEventListener('click', () => updateModal(activeModalIdx + 1));

  window.addEventListener('keydown', (e) => {
    if (modal && !modal.hidden) {
      if (e.key === 'Escape') closeModal();
      else if (e.key === 'ArrowLeft') updateModal(activeModalIdx - 1);
      else if (e.key === 'ArrowRight') updateModal(activeModalIdx + 1);
    }
  });

  // Continuous scrolling: Movement NEVER pauses on hover, touch, or click

  // ---- Placement & Dimensions ----------------------------------------------
  let singleSet1Width = 1800;
  let singleSet2Width = 1800;

  function measureTracks() {
    const w = window.innerWidth;
    const h = window.innerHeight;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    gallery.resize(w, h, dpr);

    // Measure single-set width for seamless infinite loop calculation
    if (trackTop.children.length >= 6) {
      let sum1 = 0;
      const gap1 = parseFloat(window.getComputedStyle(trackTop).gap) || 24;
      for (let i = 0; i < 6; i++) {
        sum1 += trackTop.children[i].getBoundingClientRect().width + gap1;
      }
      if (sum1 > 0) singleSet1Width = sum1;
    }
    if (trackBottom.children.length >= 6) {
      let sum2 = 0;
      const gap2 = parseFloat(window.getComputedStyle(trackBottom).gap) || 24;
      for (let i = 0; i < 6; i++) {
        sum2 += trackBottom.children[i].getBoundingClientRect().width + gap2;
      }
      if (sum2 > 0) singleSet2Width = sum2;
    }

    // Set seated developer baseline dimensions
    const f = fitCover(w, h);
    person.style.width = `${Math.round(PERSON.w * f.s)}px`;
    person.style.height = `${Math.round(PERSON.h * f.s)}px`;
    person.style.left = `${Math.round(PERSON.x * f.s + f.ox)}px`;
    person.style.top = `${Math.round(PERSON.y * f.s + f.oy)}px`;
  }

  measureTracks();
  let resizeId;
  window.addEventListener('resize', () => {
    clearTimeout(resizeId);
    resizeId = setTimeout(measureTracks, 140);
  });
  window.addEventListener('orientationchange', () => setTimeout(measureTracks, 200));

  // ---- Pointer Parallax ----------------------------------------------------
  const ptr = { tx: 0, ty: 0, x: 0, y: 0, inside: false };
  section.addEventListener('pointermove', (e) => {
    const r = section.getBoundingClientRect();
    ptr.tx = ((e.clientX - r.left) / r.width) * 2 - 1;
    ptr.ty = ((e.clientY - r.top) / r.height) * 2 - 1;
    ptr.inside = true;
  }, { passive: true });
  section.addEventListener('pointerleave', () => { ptr.inside = false; });

  // ---- Continuous Animation Clock & Scroll-Linked Zoom --------------------
  const state = { started: 0, running: false, visible: false, raf: 0, last: 0, set: false, dolly: 0 };
  let offsetRow1 = 0;
  let offsetRow2 = 0;
  const speedRow1 = 36; // px per second right to left
  const speedRow2 = 34; // px per second left to right

  let cachedTop = 0;
  let cachedRoom = 0;
  function updatePinMetrics() {
    cachedTop = section.offsetTop;
    cachedRoom = section.offsetHeight - window.innerHeight;
  }
  updatePinMetrics();
  window.addEventListener('resize', updatePinMetrics);

  const frame = (now) => {
    if (!state.running) return;
    const dt = Math.min(0.05, (now - state.last) / 1000 || 0.016);
    state.last = now;
    const t = reduced ? T4.live + 2 : (now - state.started) / 1000;
    const s = sample4(t);

    // Continuous smooth looping: Never stops on hover, cursor move, or click
    // Top Row: Moves Right to Left
    if (!reduced) {
      offsetRow1 += speedRow1 * dt;
      if (offsetRow1 >= singleSet1Width) {
        offsetRow1 %= singleSet1Width;
      }
    }
    trackTop.style.transform = `translate3d(${-offsetRow1.toFixed(2)}px, 0px, 0px)`;

    // Bottom Row: Moves Left to Right
    if (!reduced) {
      offsetRow2 += speedRow2 * dt;
      if (offsetRow2 >= singleSet2Width) {
        offsetRow2 %= singleSet2Width;
      }
    }
    trackBottom.style.transform = `translate3d(${(offsetRow2 - singleSet2Width).toFixed(2)}px, 0px, 0px)`;

    // Scroll-linked camera zoom: progress of pin through extra scroll room
    const scrollY = window.scrollY || window.pageYOffset || 0;
    const rawSp = cachedRoom > 4 ? Math.min(1, Math.max(0, (scrollY - cachedTop) / cachedRoom)) : 0;
    state.dolly = damp(state.dolly, rawSp, 5.5, dt);
    const sp = state.dolly;
    const sCurve = sp * sp * (3.0 - 2.0 * sp);

    // WebGL Canvas Rendering (Warm red/black ambient lighting and floor rings)
    ptr.x = damp(ptr.x, ptr.inside ? ptr.tx : 0, 2.8, dt);
    ptr.y = damp(ptr.y, ptr.inside ? ptr.ty : 0, 2.8, dt);
    gallery.par.x = ptr.x;
    gallery.par.y = ptr.y;
    gallery.dolly = sCurve;
    gallery.render(t, s);

    // Seated Developer Character & Workstation: Zoom camera towards him on scroll
    // The human character becomes larger and more prominent while project tracks continue independent movement.
    const pe = s.person;
    const zoom = (1.0 + sCurve * 0.11).toFixed(4);
    const tx = (ptr.x * -6).toFixed(2);
    const ty = (ptr.y * -3 + (1 - pe) * 28 + sCurve * 6).toFixed(2);

    person.style.transform = `translate3d(${tx}px, ${ty}px, 0px) scale(${zoom})`;
    person.style.opacity = pe.toFixed(3);

    if (s.live && !state.set) {
      state.set = true;
      section.classList.add('is-live', 'is-set');
    }

    state.raf = requestAnimationFrame(frame);
  };

  const start = () => {
    if (state.running) return;
    state.running = true;
    state.last = performance.now();
    if (!state.started) state.started = performance.now();
    state.raf = requestAnimationFrame(frame);
  };
  const stop = () => { state.running = false; cancelAnimationFrame(state.raf); };

  new IntersectionObserver((entries) => {
    for (const e of entries) {
      state.visible = e.isIntersecting;
      if (e.isIntersecting) start(); else stop();
    }
  }, { threshold: 0.18 }).observe(section);

  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') stop();
    else if (state.visible) start();
  });

  window.__gallery = { gallery, state, section, openModal, closeModal };
  return { gallery, section };
}

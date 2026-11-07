// Scene five lifecycle: holographic 3D certifications in cinematic slate-cyan atmosphere.

import { createGL } from '../gl/renderer.js';
import { CertsStage } from './certs.js';
import { CERT_CARDS, PORTRAIT_CERTS } from './layout5.js';
import { CERTIFICATES } from '../data/certificates.js';
import { sample5, cardIn5 } from './timeline5.js';

const damp = (v, to, k, dt) => v + (to - v) * (1 - Math.exp(-k * dt));

export async function initCertificates() {
  const section = document.getElementById('certs');
  const canvas = document.getElementById('certsStage');
  const deck = document.getElementById('certsDeck');
  const modal = document.getElementById('certsModal');
  const modalImg = document.getElementById('certsModalImg');
  const modalTitle = document.getElementById('certsModalTitle');
  const modalIssuer = document.getElementById('certsModalIssuer');
  const modalDate = document.getElementById('certsModalDate');
  const modalId = document.getElementById('certsModalId');
  const modalClose = document.getElementById('certsModalClose');
  const personWrap = document.getElementById('certPersonWrap');

  if (!section || !canvas || !deck) return null;

  const gl = createGL(canvas);
  if (!gl) {
    section.classList.add('is-fallback');
    return null;
  }

  const stage = new CertsStage(canvas, gl);
  await stage.load();

  const reduced = matchMedia('(prefers-reduced-motion: reduce)').matches;

  // Build the 5 floating glass cards
  const cardElements = CERT_CARDS.map((geom, i) => {
    const data = CERTIFICATES[i] || {};
    const el = document.createElement('button');
    el.type = 'button';
    el.className = 'cert-card';
    el.dataset.index = String(i);
    el.setAttribute('aria-label', `Certificate: ${data.title || 'Credential'}`);
    el.style.setProperty('--depth', String(geom.depth));
    el.style.setProperty('--tint-r', String(geom.tint[0]));
    el.style.setProperty('--tint-g', String(geom.tint[1]));
    el.style.setProperty('--tint-b', String(geom.tint[2]));

    el.innerHTML = `
      <div class="cert-card__glass">
        <div class="cert-card__sheen" aria-hidden="true"></div>
        <div class="cert-card__header">
          <div class="cert-card__badge">
            <span class="cert-card__pip"></span>
            <span class="cert-card__issuer">${data.issuer || 'Issuing Authority'}</span>
          </div>
          <span class="cert-card__year">${data.date || '2024'}</span>
        </div>
        <div class="cert-card__body">
          <h3 class="cert-card__title">${data.title || 'Certificate Title'}</h3>
          <p class="cert-card__cat">${data.category || 'Specialization'}</p>
        </div>
        <div class="cert-card__footer">
          <div class="cert-card__status">
            <i class="cert-card__dot"></i>
            <span>${data.status || 'CERTIFIED'}</span>
          </div>
          <span class="cert-card__view">View Credential &rarr;</span>
        </div>
      </div>
    `;

    // Click handler to open certificate modal
    el.addEventListener('click', () => {
      openModal(data);
    });

    deck.appendChild(el);
    return el;
  });

  // Modal open / close handlers
  function openModal(data) {
    if (!modal) return;
    if (modalImg) {
      modalImg.src = data.image || 'public/certs/placeholder_01.png';
      modalImg.alt = data.title || 'Certificate Preview';
    }
    if (modalTitle) modalTitle.textContent = data.title || 'Certificate Title';
    if (modalIssuer) modalIssuer.textContent = `Awarded by: ${data.issuer || 'Issuing Organization'}`;
    if (modalDate) modalDate.textContent = `Issued: ${data.date || '2024'}`;
    if (modalId) modalId.textContent = `ID: ${data.credentialId || 'CRED-VERIFIED'}`;

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
    }, 300);
  }

  modalClose?.addEventListener('click', closeModal);
  modal?.addEventListener('click', (e) => {
    if (e.target === modal || e.target.classList.contains('certs-modal__backdrop')) {
      closeModal();
    }
  });
  window.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal && !modal.hidden) closeModal();
  });

  // Placement function
  let portrait = false;
  function place() {
    const w = window.innerWidth;
    const h = window.innerHeight;
    const dpr = Math.min(window.devicePixelRatio || 1, 2);
    const f = stage.resize(w, h, dpr);
    portrait = w / h < 0.85;
    section.classList.toggle('is-portrait', portrait);

    for (let i = 0; i < cardElements.length; i++) {
      const geom = CERT_CARDS[i];
      const el = cardElements[i];
      if (portrait) {
        const p = PORTRAIT_CERTS.get(i);
        if (!p) { el.style.display = 'none'; continue; }
        el.style.display = '';
        const cw = p.w * w;
        const ch = Math.max(114, Math.min(156, cw * (geom.box[3] / geom.box[2])));
        el.style.width = `${cw}px`;
        el.style.height = `${ch}px`;
        el.style.left = `${p.cx * w - cw / 2}px`;
        el.style.top = `${p.cy * h - ch / 2}px`;
      } else {
        el.style.display = '';
        const cardW = Math.min(geom.box[2] * f.s, w * 0.28);
        const cardH = cardW * (geom.box[3] / geom.box[2]);
        el.style.width = `${cardW}px`;
        el.style.height = `${cardH}px`;

        let left = geom.box[0] * f.s + f.ox;
        let top = geom.box[1] * f.s + f.oy;

        // Safe padding clamp to NEVER clip outside the section boundaries,
        // and keep left cards safely BELOW the Certifications title wrap:
        const padX = Math.max(16, w * 0.025);
        const padTopLeft = Math.max(185, h * 0.26); // Guaranteed clear zone below title
        const padTopRight = Math.max(68, h * 0.08);
        const padBottom = Math.max(24, h * 0.035);

        if (i < 2) {
          left = Math.max(padX, Math.min(left, w * 0.5 - cardW - 50));
          top = Math.max(padTopLeft, Math.min(top, h - cardH - padBottom));
        } else {
          left = Math.max(w * 0.5 + 50, Math.min(left, w - cardW - padX));
          top = Math.max(padTopRight, Math.min(top, h - cardH - padBottom));
        }

        el.style.left = `${left}px`;
        el.style.top = `${top}px`;
      }
    }
  }

  place();
  window.addEventListener('resize', place);
  window.addEventListener('orientationchange', () => setTimeout(place, 200));

  // Pointer tracking
  const pointer = { x: 0, y: 0, tx: 0, ty: 0 };
  const coarse = matchMedia('(pointer: coarse)').matches;

  if (!coarse) {
    section.addEventListener('pointermove', (e) => {
      pointer.tx = (e.clientX / window.innerWidth) * 2 - 1;
      pointer.ty = (e.clientY / window.innerHeight) * 2 - 1;
    }, { passive: true });

    section.addEventListener('pointerleave', () => {
      pointer.tx = 0;
      pointer.ty = 0;
    });
  }

  // Animation frame loop
  let startedAt = 0;
  let entered = false;
  let running = false;
  let last = 0;
  let rafId = 0;
  let scrollProgress = 0;

  let cachedCertsTop = 0;
  let cachedCertsTravel = 0;
  const updateCertsMetrics = () => {
    cachedCertsTop = section.offsetTop;
    cachedCertsTravel = section.offsetHeight + window.innerHeight;
  };
  updateCertsMetrics();
  window.addEventListener('resize', updateCertsMetrics);

  window.addEventListener('scroll', () => {
    if (cachedCertsTravel > 0) {
      const scrollY = window.scrollY || window.pageYOffset || 0;
      scrollProgress = Math.max(0, Math.min(1, (scrollY + window.innerHeight - cachedCertsTop) / cachedCertsTravel));
    }
  }, { passive: true });

  function frame(now) {
    if (!running) return;
    const dt = Math.min(0.05, (now - last) / 1000 || 0.016);
    last = now;
    const t = (now - startedAt) / 1000;

    pointer.x = damp(pointer.x, pointer.tx, 2.8, dt);
    pointer.y = damp(pointer.y, pointer.ty, 2.8, dt);
    stage.par.x = pointer.x;
    stage.par.y = pointer.y;
    stage.dolly = scrollProgress;

    const s = sample5(t);
    stage.render(t, s);

    if (personWrap) {
      personWrap.style.transform = `translateX(-50%) translate3d(${-pointer.x * 10}px, ${-pointer.y * 5}px, 0)`;
    }

    // Dynamic 3D transform updates on each card with zero-clipping limits
    for (let i = 0; i < cardElements.length; i++) {
      const geom = CERT_CARDS[i];
      const el = cardElements[i];
      const intro = cardIn5(t, i, cardElements.length);

      const bobPhase = t * 0.85 + i * 1.2;
      const bobY = Math.sin(bobPhase) * 3.5;
      const bobX = Math.cos(bobPhase * 0.7) * 2;
      const bobRot = Math.sin(bobPhase * 0.5) * 1.0;

      const parMul = (1 - geom.depth) * 8;
      const px = pointer.x * parMul;
      const py = pointer.y * parMul * 0.5;

      const rx = geom.rotX - pointer.y * 3.5;
      const ry = geom.rotY + pointer.x * 4.5;
      const rz = geom.rotZ + bobRot;

      const scale = (0.95 + 0.05 * intro);
      const ty = (1 - intro) * 35 + bobY + py;
      const tx = bobX + px;

      el.style.transform = `perspective(1000px) translate3d(${tx}px, ${ty}px, 0) `
        + `rotateX(${rx}deg) rotateY(${ry}deg) rotateZ(${rz}deg) scale(${scale})`;
      el.style.opacity = String(intro);
    }

    rafId = requestAnimationFrame(frame);
  }

  new IntersectionObserver(([entry]) => {
    if (entry.isIntersecting) {
      if (!entered) {
        entered = true;
        startedAt = performance.now();
        section.classList.add('is-visible');
      }
      running = true;
      last = performance.now();
      cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(frame);
    } else {
      running = false;
      cancelAnimationFrame(rafId);
    }
  }, { threshold: 0.12 }).observe(section);

  document.addEventListener('visibilitychange', () => {
    if (document.visibilityState === 'hidden') {
      running = false;
      cancelAnimationFrame(rafId);
    } else if (entered) {
      running = true;
      last = performance.now();
      cancelAnimationFrame(rafId);
      rafId = requestAnimationFrame(frame);
    }
  });

  return { section, stage };
}

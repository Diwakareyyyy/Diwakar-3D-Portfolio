/**
 * Experience Section Horizontal Slider & Walking Sequence Controller
 * ---------------------------------------------------------------------------
 * Manages:
 *  1. Full-screen horizontal slide transitions between Slide 1 (Infology)
 *     and Slide 2 ("UPDATING SOON").
 *  2. Casual developer walking-into-building sequence (single play, no continuous loop).
 *  3. Interactive Previous and Next button controls, keyboard arrows, and swipe.
 *  4. Fluid downward vertical scrolling without locking document scroll.
 */

export function initExperienceSlider() {
  const section = document.getElementById('experience');
  const fullTrack = document.getElementById('expFullTrack');
  const nextBtn = document.getElementById('expSideNext');
  const prevBtn = document.getElementById('expSidePrev');
  const slide1 = document.getElementById('expSlide1');
  const slide2 = document.getElementById('expSlide2');

  if (!section || !fullTrack) return;

  let currentSlide = 0;

  function goToSlide(index) {
    currentSlide = Math.max(0, Math.min(1, index));
    // Translate fulltrack: 0% for slide 1, -50% for slide 2
    fullTrack.style.transform = currentSlide === 1 ? 'translateX(-50%)' : 'translateX(0%)';

    if (slide1 && slide2) {
      slide1.classList.toggle('is-active', currentSlide === 0);
      slide1.setAttribute('aria-hidden', String(currentSlide !== 0));
      slide2.classList.toggle('is-active', currentSlide === 1);
      slide2.setAttribute('aria-hidden', String(currentSlide !== 1));
    }

    // When returning to slide 1 from slide 2, re-trigger character walking sequence
    if (currentSlide === 0 && section.classList.contains('is-visible')) {
      section.classList.remove('is-walking');
      void section.offsetWidth; // Force CSS reflow
      section.classList.add('is-walking');
    }
  }

  nextBtn?.addEventListener('click', () => goToSlide(1));
  prevBtn?.addEventListener('click', () => goToSlide(0));

  // Keyboard navigation when experience section is in viewport
  window.addEventListener('keydown', (e) => {
    const rect = section.getBoundingClientRect();
    const inView = rect.top < window.innerHeight * 0.7 && rect.bottom > window.innerHeight * 0.3;
    if (!inView) return;

    if (e.key === 'ArrowRight' && currentSlide === 0) {
      goToSlide(1);
    } else if (e.key === 'ArrowLeft' && currentSlide === 1) {
      goToSlide(0);
    }
  });

  // Touch gesture support on full-screen track (horizontal swipe only, preserves vertical scroll)
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
    if (dx > 25 && dx > dy * 1.5) {
      isHorizontal = true;
    }
  }, { passive: true });

  section.addEventListener('touchend', (e) => {
    if (!isHorizontal) return;
    const diff = touchStartX - e.changedTouches[0].clientX;
    if (diff > 50 && currentSlide === 0) {
      goToSlide(1);
    } else if (diff < -50 && currentSlide === 1) {
      goToSlide(0);
    }
  }, { passive: true });

  // IntersectionObserver: trigger visibility and single natural walk animation
  if ('IntersectionObserver' in window) {
    const obs = new IntersectionObserver(([entry]) => {
      if (entry.isIntersecting) {
        section.classList.add('is-visible');
        setTimeout(() => {
          section.classList.add('is-walking');
        }, 1200);
      }
    }, { threshold: 0.18 });
    obs.observe(section);
  } else {
    section.classList.add('is-visible', 'is-walking');
  }
}

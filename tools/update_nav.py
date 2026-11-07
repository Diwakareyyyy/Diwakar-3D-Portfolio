with open('src/styles/app.css', 'r', encoding='utf-8') as f:
    app_css = f.read()

# 1. Update .hdr in src/styles/app.css to position: absolute (Homepage only) with is-hidden support
old_hdr = """.hdr {
  position: fixed; top: 0; left: 0; right: 0;
  height: var(--hdr-h);
  display: flex;
  align-items: center;
  gap: clamp(12px, 1.6vw, 26px);
  padding: 0 var(--edge);
  z-index: 50;
  pointer-events: none;
  background: linear-gradient(180deg, rgba(0, 0, 0, 0.72) 0%, rgba(0, 0, 0, 0.35) 60%, transparent 100%);
  backdrop-filter: blur(8px);
  -webkit-backdrop-filter: blur(8px);
  transition: background 0.3s ease;
}
.hdr > * { pointer-events: auto; }"""

new_hdr = """.hdr {
  position: absolute; top: 0; left: 0; right: 0;
  height: var(--hdr-h);
  display: flex;
  align-items: center;
  gap: clamp(12px, 1.6vw, 26px);
  padding: 0 var(--edge);
  z-index: 20;
  pointer-events: none;
  transition: opacity 0.35s ease, transform 0.35s ease;
}
.hdr > * { pointer-events: auto; }

.hdr.is-hidden {
  opacity: 0 !important;
  pointer-events: none !important;
  visibility: hidden !important;
  transform: translateY(-8px);
}"""

assert old_hdr in app_css, "old_hdr not found in app.css"
app_css = app_css.replace(old_hdr, new_hdr, 1)

# 2. Update .mobile-nav-fab in src/styles/app.css to position: absolute with is-hidden support
old_fab = """.mobile-nav-fab {
  position: fixed;
  top: calc((var(--hdr-h) - 32px) * 0.5);
  right: var(--edge);
  z-index: 96;"""

new_fab = """.mobile-nav-fab {
  position: absolute;
  top: calc((var(--hdr-h) - 32px) * 0.5);
  right: var(--edge);
  z-index: 25;"""

assert old_fab in app_css, "old_fab not found in app.css"
app_css = app_css.replace(old_fab, new_fab, 1)

old_fab_end = """.is-header .mobile-nav-fab {
  opacity: 1;
  transform: none;
}"""

new_fab_end = """.is-header .mobile-nav-fab {
  opacity: 1;
  transform: none;
}
.mobile-nav-fab.is-hidden {
  opacity: 0 !important;
  pointer-events: none !important;
  visibility: hidden !important;
}"""

assert old_fab_end in app_css, "old_fab_end not found in app.css"
app_css = app_css.replace(old_fab_end, new_fab_end, 1)

with open('src/styles/app.css', 'w', encoding='utf-8') as f:
    f.write(app_css)

print("[OK] src/styles/app.css updated successfully!")

# 3. Update src/main.js
with open('src/main.js', 'r', encoding='utf-8') as f:
    main_js = f.read()

old_nav_js = """// High-performance direct smooth scrolling & section navigation
let isNavigating = false;
let navTimeout = null;

const navLinks = document.querySelectorAll('a[data-nav]');
navLinks.forEach((a) => {
  a.addEventListener('click', (e) => {
    const target = a.getAttribute('href');
    if (!target || !target.startsWith('#')) return;
    e.preventDefault();

    // Lock observer updates during scripted navigation to prevent clashing
    isNavigating = true;
    clearTimeout(navTimeout);
    navTimeout = setTimeout(() => { isNavigating = false; }, 900);

    // Immediate active highlight update
    navLinks.forEach((l) => {
      l.classList.toggle('is-active', l.getAttribute('href') === target);
    });

    if (root.classList.contains('is-menu')) setMenu(false);

    // Direct scroll handling:
    // HOME (#stage or #home or #): Smoothly scroll to the very top from anywhere
    if (target === '#stage' || target === '#home' || target === '#') {
      window.scrollTo({ top: 0, behavior: 'smooth' });
      app.audio?.onSectionChange('home');
      return;
    }

    // CONTACT (#fin) and other sections: calculate exact absolute offset
    const el = document.querySelector(target);
    if (el) {
      const targetTop = el.getBoundingClientRect().top + window.scrollY;
      window.scrollTo({ top: targetTop, behavior: 'smooth' });
      const secName = target.replace('#', '');
      app.audio?.onSectionChange(secName);
    }
  });
});"""

new_nav_js = """// High-performance direct smooth scrolling & section navigation (Homepage exclusive navbar)
let isNavigating = false;
let navTimeout = null;

const hdr = document.getElementById('hdr');
const mobileNavFab = document.getElementById('mobileNavFab');

function setNavVisibility(visible) {
  if (hdr) hdr.classList.toggle('is-hidden', !visible);
  if (mobileNavFab) mobileNavFab.classList.toggle('is-hidden', !visible);
  if (!visible && root.classList.contains('is-menu')) {
    setMenu(false);
  }
}

// Monitor scroll to ensure the navbar is exclusively visible on the Homepage / Hero
window.addEventListener('scroll', () => {
  const onHome = (window.scrollY || window.pageYOffset || 0) < 60;
  if (!isNavigating) {
    setNavVisibility(onHome);
  }
}, { passive: true });

const navLinks = document.querySelectorAll('a[data-nav]');
navLinks.forEach((a) => {
  a.addEventListener('click', (e) => {
    const target = a.getAttribute('href');
    if (!target || !target.startsWith('#')) return;
    e.preventDefault();

    // Lock observer updates during scripted navigation to prevent clashing
    isNavigating = true;
    clearTimeout(navTimeout);
    navTimeout = setTimeout(() => { isNavigating = false; }, 900);

    // Immediate active highlight update
    navLinks.forEach((l) => {
      l.classList.toggle('is-active', l.getAttribute('href') === target);
    });

    if (root.classList.contains('is-menu')) setMenu(false);

    // Direct scroll handling:
    // HOME (#stage or #home or #): Smoothly scroll to the very top and restore navbar
    if (target === '#stage' || target === '#home' || target === '#') {
      setNavVisibility(true);
      window.scrollTo({ top: 0, behavior: 'smooth' });
      app.audio?.onSectionChange('home');
      return;
    }

    // Navigating away from Homepage: navbar must disappear completely
    setNavVisibility(false);

    // CONTACT (#fin) and other sections: calculate exact absolute offset
    const el = document.querySelector(target);
    if (el) {
      const targetTop = el.getBoundingClientRect().top + window.scrollY;
      window.scrollTo({ top: targetTop, behavior: 'smooth' });
      const secName = target.replace('#', '');
      app.audio?.onSectionChange(secName);
    }
  });
});"""

assert old_nav_js in main_js, "old_nav_js not found in main.js"
main_js = main_js.replace(old_nav_js, new_nav_js, 1)

# Also update the hero spacer observer in main.js to sync nav visibility when returning to home
old_hero_obs = """      app.heroOnScreen = e.isIntersecting;
      if (e.isIntersecting) { c.play(); heroWrap.style.visibility = ''; }
      else { c.pause(); heroWrap.style.visibility = 'hidden'; }"""

new_hero_obs = """      app.heroOnScreen = e.isIntersecting;
      const onHome = e.isIntersecting && (window.scrollY || 0) < 100;
      setNavVisibility(onHome);
      if (e.isIntersecting) { c.play(); heroWrap.style.visibility = ''; }
      else { c.pause(); heroWrap.style.visibility = 'hidden'; }"""

assert old_hero_obs in main_js, "old_hero_obs not found in main.js"
main_js = main_js.replace(old_hero_obs, new_hero_obs, 1)

with open('src/main.js', 'w', encoding='utf-8') as f:
    f.write(main_js)

print("[OK] src/main.js updated successfully!")

with open('src/main.js', 'r', encoding='utf-8') as f:
    code = f.read()

# 1. Update frame loop to pause hero rendering when off-screen
old_render = "  app.stage.render(state, t, app.clips);\n  app.audio?.syncIntroWalk(t, app.clips.hero, app.heroOnScreen, T.settled);"
new_render = """  if (app.heroOnScreen !== false) {
    app.stage.render(state, t, app.clips);
  }
  app.audio?.syncIntroWalk(t, app.clips.hero, app.heroOnScreen, T.settled);"""

assert old_render in code, "old_render not found in src/main.js"
code = code.replace(old_render, new_render, 1)

# 2. Update navigation click and tracking logic
old_nav = """// smooth scrolling for internal navigation links
const navLinks = document.querySelectorAll('a[data-nav]');
navLinks.forEach((a) => {
  a.addEventListener('click', (e) => {
    const target = a.getAttribute('href');
    if (target && target.startsWith('#') && target.length > 1) {
      e.preventDefault();
      const el = document.querySelector(target);
      if (el) {
        el.scrollIntoView({ behavior: 'smooth' });
        if (root.classList.contains('is-menu')) setMenu(false);
      }
    }
  });
});

// Active navigation item tracking across all sections
const trackedSections = ['stage', 'universe', 'chrono', 'experience', 'gallery', 'certs', 'fin']
  .map(id => document.getElementById(id))
  .filter(Boolean);

if (trackedSections.length && 'IntersectionObserver' in window) {
  const navObs = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        const id = '#' + entry.target.id;
        app.audio?.onSectionChange(entry.target.id);
        navLinks.forEach((a) => {
          a.classList.toggle('is-active', a.getAttribute('href') === id);
        });
      }
    }
  }, { threshold: 0.25 });
  trackedSections.forEach(s => navObs.observe(s));
}"""

new_nav = """// High-performance direct smooth scrolling & section navigation
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
});

// Accurate active section tracking across all sections (using in-flow anchors)
const sectionMap = [
  { id: '#stage', name: 'home', el: document.getElementById('home') || document.querySelector('.hero-spacer') },
  { id: '#universe', name: 'universe', el: document.getElementById('universe') },
  { id: '#chrono', name: 'chrono', el: document.getElementById('chrono') },
  { id: '#experience', name: 'experience', el: document.getElementById('experience') },
  { id: '#gallery', name: 'gallery', el: document.getElementById('gallery') },
  { id: '#certs', name: 'certs', el: document.getElementById('certs') },
  { id: '#fin', name: 'fin', el: document.getElementById('fin') },
].filter(s => s.el);

if (sectionMap.length && 'IntersectionObserver' in window) {
  const navObs = new IntersectionObserver((entries) => {
    if (isNavigating) return;
    for (const entry of entries) {
      if (entry.isIntersecting) {
        const item = sectionMap.find(s => s.el === entry.target);
        if (item) {
          app.audio?.onSectionChange(item.name);
          navLinks.forEach((a) => {
            a.classList.toggle('is-active', a.getAttribute('href') === item.id);
          });
        }
      }
    }
  }, { threshold: 0.25 });
  sectionMap.forEach(s => navObs.observe(s.el));
}"""

assert old_nav in code, "old_nav not found in src/main.js"
code = code.replace(old_nav, new_nav, 1)

with open('src/main.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("[OK] src/main.js updated successfully!")

# Performance script to eliminate layout thrashing across scene boot files

# 1. Optimize scene4/boot4.js
with open('src/scene4/boot4.js', 'r', encoding='utf-8') as f:
    b4 = f.read()

old_b4 = """    // scroll dolly: progress of the pin through its extra scroll room, smoothly damped
    const r = section.getBoundingClientRect();
    const room = section.offsetHeight - window.innerHeight;
    const rawSp = room > 4 ? Math.min(1, Math.max(0, -r.top / room)) : 0;"""

new_b4 = """    // scroll dolly: progress of the pin through its extra scroll room (cached to avoid layout thrashing)
    const scrollY = window.scrollY || window.pageYOffset || 0;
    const rawSp = cachedRoom > 4 ? Math.min(1, Math.max(0, (scrollY - cachedTop) / cachedRoom)) : 0;"""

if old_b4 in b4:
    # Add cached variables before frame function
    insert_marker = "  const frame = (now) => {"
    cached_vars = """  let cachedTop = 0;
  let cachedRoom = 0;
  function updatePinMetrics() {
    cachedTop = section.offsetTop;
    cachedRoom = section.offsetHeight - window.innerHeight;
  }
  updatePinMetrics();
  window.addEventListener('resize', updatePinMetrics);
  window.addEventListener('orientationchange', () => setTimeout(updatePinMetrics, 200));

  const frame = (now) => {"""
    b4 = b4.replace(insert_marker, cached_vars, 1)
    b4 = b4.replace(old_b4, new_b4, 1)
    with open('src/scene4/boot4.js', 'w', encoding='utf-8') as f:
        f.write(b4)
    print("[OK] scene4/boot4.js optimized!")

# 2. Optimize scene6/boot6.js
with open('src/scene6/boot6.js', 'r', encoding='utf-8') as f:
    b6 = f.read()

old_b6 = """    if (frame2Ready) {
      const r = section.getBoundingClientRect();
      const room = section.offsetHeight - window.innerHeight;
      const raw = room > 4 ? Math.min(1, Math.max(0, -r.top / room)) : 0;"""

new_b6 = """    if (frame2Ready) {
      const scrollY = window.scrollY || window.pageYOffset || 0;
      const raw = cachedFinRoom > 4 ? Math.min(1, Math.max(0, (scrollY - cachedFinTop) / cachedFinRoom)) : 0;"""

if old_b6 in b6:
    insert_marker_6 = "  const frame = (now) => {"
    cached_vars_6 = """  let cachedFinTop = 0;
  let cachedFinRoom = 0;
  function updateFinMetrics() {
    cachedFinTop = section.offsetTop;
    cachedFinRoom = section.offsetHeight - window.innerHeight;
  }
  updateFinMetrics();
  window.addEventListener('resize', updateFinMetrics);
  window.addEventListener('orientationchange', () => setTimeout(updateFinMetrics, 200));

  const frame = (now) => {"""
    b6 = b6.replace(insert_marker_6, cached_vars_6, 1)
    b6 = b6.replace(old_b6, new_b6, 1)
    with open('src/scene6/boot6.js', 'w', encoding='utf-8') as f:
        f.write(b6)
    print("[OK] scene6/boot6.js optimized!")

# 3. Optimize scene2/boot2.js
with open('src/scene2/boot2.js', 'r', encoding='utf-8') as f:
    b2 = f.read()

old_b2 = """  // Subtle scroll parallax tracking
  let scrollProgress = 0;
  const onScroll = () => {
    const r = section.getBoundingClientRect();
    const travel = r.height + window.innerHeight;
    if (travel > 0) {
      scrollProgress = Math.max(0, Math.min(1, (window.innerHeight - r.top) / travel));
    }
  };
  window.addEventListener('scroll', onScroll, { passive: true });"""

new_b2 = """  // Subtle scroll parallax tracking (cached metrics to avoid synchronous reflow)
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
  window.addEventListener('scroll', onScroll, { passive: true });"""

if old_b2 in b2:
    b2 = b2.replace(old_b2, new_b2, 1)
    with open('src/scene2/boot2.js', 'w', encoding='utf-8') as f:
        f.write(b2)
    print("[OK] scene2/boot2.js optimized!")

# 4. Optimize scene5/boot5.js
with open('src/scene5/boot5.js', 'r', encoding='utf-8') as f:
    b5 = f.read()

old_b5 = """  window.addEventListener('scroll', () => {
    const r = section.getBoundingClientRect();
    const travel = r.height + window.innerHeight;
    if (travel > 0) {
      scrollProgress = Math.max(0, Math.min(1, (window.innerHeight - r.top) / travel));
    }
  }, { passive: true });"""

new_b5 = """  let cachedCertsTop = 0;
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
  }, { passive: true });"""

if old_b5 in b5:
    b5 = b5.replace(old_b5, new_b5, 1)
    with open('src/scene5/boot5.js', 'w', encoding='utf-8') as f:
        f.write(b5)
    print("[OK] scene5/boot5.js optimized!")

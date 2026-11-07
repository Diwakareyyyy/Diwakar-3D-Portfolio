import os

with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

target = """      <h2 class="g-label g-label--projects" id="galleryTitle">Projects</h2>
      <p class="g-label g-label--ideas" aria-hidden="true">
        Ideas<br>Interfaces<br>Experiences<br><b>Real Impact</b>
      </p>
      <p class="g-label g-label--scroll" aria-hidden="true">
        Scroll<br>Explore<br>Interact
      </p>
      <p class="g-label g-label--real" aria-hidden="true">
        Real<br>Projects<br>Real<br>Stories
      </p>
      <p class="g-label g-label--tomorrow" aria-hidden="true">
        Designing<br>A Brighter<br>Tomorrow
      </p>
      <span class="g-label g-label--num" id="galleryNum" aria-hidden="true">01</span>
    </div>
  </section>"""

replacement = """      <h2 class="g-label g-label--projects" id="galleryTitle">Projects</h2>
      <p class="g-label g-label--ideas" aria-hidden="true">
        <b>EVCDRP &amp; 15 PROJECTS</b><br>
        Engineering Systems For Impact
      </p>
      <p class="g-label g-label--scroll" aria-hidden="true">
        Scroll · Orbit · Explore<br>Click any card to inspect
      </p>
      <p class="g-label g-label--real" aria-hidden="true">
        AI · Mobile · Web · Logistics
      </p>
      <p class="g-label g-label--tomorrow" aria-hidden="true">
        Designing<br>A Brighter<br>Tomorrow
      </p>
      <span class="g-label g-label--num" id="galleryNum" aria-hidden="true">01</span>

      <!-- Interactive Showcase Filter Dock (All 15 / Featured 5 / Remaining 10) -->
      <nav class="gallery__filter-dock" id="galleryFilterDock" aria-label="Project Showcase Filter">
        <button class="g-filter-btn is-active" data-filter="all" type="button">ALL 15 PROJECTS</button>
        <button class="g-filter-btn" data-filter="featured" type="button">★ TOP 5 FEATURED</button>
        <button class="g-filter-btn" data-filter="orbit" type="button">REMAINING 10</button>
      </nav>
    </div>
  </section>

  <!-- Interactive Project Lightbox Modal -->
  <div class="project-modal" id="projectModal" role="dialog" aria-modal="true" aria-labelledby="projModalTitle" hidden>
    <div class="project-modal__backdrop" id="projModalBackdrop" aria-hidden="true"></div>
    <div class="project-modal__panel">
      <div class="project-modal__top">
        <div class="project-modal__badge">
          <span class="project-modal__pip"></span>
          <span id="projModalCategory">EV Logistics &amp; Route Optimization</span>
        </div>
        <div class="project-modal__actions">
          <button class="project-modal__nav" id="projModalPrev" type="button" aria-label="Previous project">&larr;</button>
          <span class="project-modal__counter" id="projModalCount">01 / 15</span>
          <button class="project-modal__nav" id="projModalNext" type="button" aria-label="Next project">&rarr;</button>
          <button class="project-modal__close" id="projModalClose" type="button" aria-label="Close project preview">&times;</button>
        </div>
      </div>
      <div class="project-modal__frame">
        <img id="projModalImg" src="public/projects/p01_evcdrp.png" alt="Project Preview" draggable="false">
      </div>
      <div class="project-modal__info">
        <div class="project-modal__head">
          <h3 class="project-modal__title" id="projModalTitle">Electric Vehicle Constraint-Aware Delivery Routing Problem</h3>
          <span class="project-modal__short" id="projModalShort">EVCDRP</span>
        </div>
        <p class="project-modal__desc" id="projModalDesc">
          An intelligent EV delivery route optimization system that considers battery constraints, vehicle load, driving range, traffic conditions, and charging requirements to generate efficient delivery routes.
        </p>
      </div>
    </div>
  </div>"""

if target in content:
    content = content.replace(target, replacement, 1)
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS: index.html patched!")
else:
    print("ERROR: Target block not found in index.html")

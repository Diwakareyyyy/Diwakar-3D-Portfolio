with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the entire experience section with the new clean composition
exp_start = content.find('<section class="experience"')
exp_end = content.find('</section>', exp_start) + len('</section>')

new_exp_section = '''<section class="experience" id="experience" aria-labelledby="expTitle">
    <!-- Atmospheric Scene Background & Perspective Floor -->
    <div class="exp__env" aria-hidden="true">
      <div class="exp__env-glow"></div>
      <div class="exp__env-floor">
        <div class="exp__floor-grid"></div>
        <div class="exp__floor-horizon"></div>
      </div>
    </div>

    <!-- Full-Screen Sliding Viewport & Track -->
    <div class="exp__viewport" id="expViewport">
      <div class="exp__fulltrack" id="expFullTrack">

        <!-- ============================================================== -->
        <!-- SLIDE 01: Infology Technologies — Exact Two-Halves Composition   -->
        <!-- ============================================================== -->
        <div class="exp__slide exp__slide--primary is-active" id="expSlide1" data-slide="0">
          <div class="exp__wrap">
            <!-- Section Header -->
            <header class="exp__header">
              <p class="exp__over">Scene 03.5 &bull; Career &amp; Industry</p>
              <h2 class="exp__title" id="expTitle">Work Experience</h2>
              <p class="exp__sub">Observing corporate horizons &bull; Engineering scalable applications &bull; Production impact</p>
            </header>

            <!-- Main Stage: Strict Two Halves -->
            <div class="exp__stage">

              <!-- LEFT SIDE: Experience Image Box & Grounded Developer Character -->
              <div class="exp__left-col">

                <!-- Content Box ABOVE the Developer containing Experience Image -->
                <div class="exp__card-box" id="expCardBox">
                  <div class="exp__card-img-wrap">
                    <img class="exp__card-img"
                         src="public/experience/expense_app_preview.png"
                         alt="Infology Technologies — Cross-platform Expense Tracking App"
                         draggable="false">
                  </div>
                  <div class="exp__card-body">
                    <div class="exp__card-meta">
                      <span class="exp__card-tag">Internship</span>
                      <span class="exp__card-date">July 2026 – August 2026</span>
                    </div>
                    <h3 class="exp__card-role">Software Developer Intern</h3>
                    <h4 class="exp__card-company">Infology Technologies</h4>
                    <p class="exp__card-desc">
                      Worked on a cross-platform expense tracking application using Flutter and Dart.
                      Contributed to responsive and reusable UI components, expense-management features, and application testing.
                    </p>
                    <div class="exp__card-skills" aria-label="Core technologies">
                      <span class="exp__skill-pill">Flutter</span>
                      <span class="exp__skill-pill">Dart</span>
                      <span class="exp__skill-pill">Cross-Platform UI</span>
                      <span class="exp__skill-pill">State Management</span>
                      <span class="exp__skill-pill">Testing &amp; QA</span>
                    </div>
                  </div>
                </div>

                <!-- Grounded Developer Character at Bottom-Left facing Right -->
                <div class="exp__char-col" id="expCharCol" aria-hidden="true">
                  <div class="exp__char-shadow" id="expCharShadow"></div>
                  <img class="exp__char-fig" id="expCharFig"
                       src="public/experience/developer_facing_building.png"
                       alt="Software Developer facing Infology Technologies building"
                       draggable="false">
                  <div class="exp__char-badge" id="expCharBadge">
                    <span class="exp__badge-dot"></span>
                    <span class="exp__badge-text">S Diwakar &bull; Developer</span>
                  </div>
                </div>

              </div>

              <!-- RIGHT SIDE: Full-Size Company Building Sketch (From Top to Bottom) -->
              <div class="exp__bld-zone" id="expBldZone" aria-hidden="true">
                <div class="exp__bld-frame">
                  <div class="exp__bld-grid-lines"></div>
                  <img class="exp__bld-sketch" id="expBldSketch"
                       src="public/experience/office_sketch_startup.png"
                       alt="Infology Technologies architectural headquarters sketch"
                       draggable="false">
                  <div class="exp__pencil-tracer" id="expPencilTracer" aria-hidden="true"></div>

                  <!-- Facade Signboard with exact legal name: Infology Technologies -->
                  <div class="exp__signboard" id="expSignboard">
                    <span class="exp__signboard-pip"></span>
                    <span class="exp__signboard-text">Infology Technologies</span>
                  </div>

                  <!-- Entrance Portal Target -->
                  <div class="exp__bld-door-target" id="expDoorTarget" aria-hidden="true"></div>
                </div>
              </div>

            </div>
          </div>

          <!-- Professional Arrow Control: Next Slide (Away from building details) -->
          <button class="exp__nav-btn exp__nav-btn--next" id="expSideNext"
                  aria-label="Next experience slide: Upcoming career milestone"
                  title="Next Experience">
            <span class="exp__nav-label">Next</span>
            <svg class="exp__nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="5" y1="12" x2="19" y2="12"></line>
              <polyline points="12 5 19 12 12 19"></polyline>
            </svg>
          </button>
        </div>

        <!-- ============================================================== -->
        <!-- SLIDE 02: Full-Screen "UPDATING SOON" Continuation Screen       -->
        <!-- ============================================================== -->
        <div class="exp__slide exp__slide--future" id="expSlide2" data-slide="1" aria-hidden="true">
          <!-- Professional Arrow Control: Previous Slide -->
          <button class="exp__nav-btn exp__nav-btn--prev" id="expSidePrev"
                  aria-label="Previous experience slide: Infology Technologies"
                  title="Previous: Infology Technologies">
            <svg class="exp__nav-icon" width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
              <line x1="19" y1="12" x2="5" y2="12"></line>
              <polyline points="12 19 5 12 12 5"></polyline>
            </svg>
            <span class="exp__nav-label">Previous</span>
          </button>

          <div class="exp__future-container">
            <div class="exp__future-content">
              <!-- Pulsing Red Beacon -->
              <div class="exp__future-pulse">
                <span class="exp__pulse-pip"></span>
                <span class="exp__pulse-text">Upcoming Career Milestone</span>
              </div>

              <!-- Main Full-Screen Typography: UPDATING SOON -->
              <h2 class="exp__future-title">UPDATING SOON</h2>

              <!-- Required Subtitle Text -->
              <p class="exp__future-lead">More professional experiences are on the way.</p>

              <p class="exp__future-desc">
                Actively preparing for high-impact software engineering roles, scalable full-stack applications, and interactive 3D digital platforms.
              </p>

              <!-- Target Technical Focus Badges -->
              <div class="exp__future-tags" aria-label="Technical focus areas">
                <span class="exp__future-tag">Full-Stack Engineering</span>
                <span class="exp__future-tag">Interactive 3D / WebGL</span>
                <span class="exp__future-tag">Flutter &amp; Dart</span>
                <span class="exp__future-tag">React Ecosystem</span>
                <span class="exp__future-tag">Scalable Backend Architecture</span>
              </div>

              <div class="exp__future-meta">
                <span class="exp__future-badge">Open to High-Impact Opportunities</span>
                <span class="exp__future-batch">2026 – 2027</span>
              </div>
            </div>
          </div>
        </div>

      </div>
    </div>
  </section>'''

updated_content = content[:exp_start] + new_exp_section + content[exp_end:]

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(updated_content)

print("Updated index.html experience section successfully!")

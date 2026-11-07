with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

target = """            <!-- Side Slide Next Navigation Button -->
            <button class="exp__nav-btn exp__nav-btn--next" id="expSideNext" type="button" aria-label="Next experience slide">
              <span class="exp__nav-text">Next</span>
              <svg class="exp__nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M5 12h14M12 5l7 7-7 7"/></svg>
            </button>
          </div>
        </div>

        <!-- ============================================================== -->
        <!-- SLIDE 02: Full-Screen Future Continuation Screen              -->
        <!-- ============================================================== -->
        <div class="exp__slide exp__slide--future" id="expSlide2" data-slide="1" aria-hidden="true">
          <div class="exp__future-container">
            <div class="exp__future-content">
              <div class="exp__future-pulse" aria-hidden="true">
                <span class="exp__pulse-pip"></span>
                <span class="exp__pulse-text">Pipeline Status &bull; Active</span>
              </div>
              <h3 class="exp__future-title">UPDATING SOON</h3>
              <p class="exp__future-lead">More professional experiences are on the way</p>
              <p class="exp__future-desc">
                Actively engineering full-stack and mobile solutions. Upcoming roles, open-source software contributions, and industry engagements will be spotlighted here.
              </p>
              <div class="exp__future-tags">
                <span class="exp__future-tag">Flutter &amp; Dart</span>
                <span class="exp__future-tag">Full-Stack Web</span>
                <span class="exp__future-tag">Python &amp; AI Systems</span>
                <span class="exp__future-tag">Interactive 3D</span>
              </div>
              <div class="exp__future-meta">
                <span class="exp__future-badge">2026–2027 Pipeline</span>
                <span class="exp__future-batch">Chennai, Tamil Nadu</span>
              </div>
            </div>
            <!-- Side Slide Previous Navigation Button -->
            <button class="exp__nav-btn exp__nav-btn--prev" id="expSidePrev" type="button" aria-label="Previous experience slide">
              <svg class="exp__nav-icon" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M19 12H5M12 19l-7-7 7-7"/></svg>
              <span class="exp__nav-text">Back</span>
            </button>
          </div>
        </div>"""

replacement = """          </div>
        </div>"""

assert target in html, "Target Slide 2 block not found in index.html"
html = html.replace(target, replacement, 1)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("[OK] Updating Soon placeholder and slide 2 successfully removed from index.html!")

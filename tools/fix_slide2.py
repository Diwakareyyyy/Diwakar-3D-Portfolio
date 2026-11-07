with open('index.html', 'r', encoding='utf-8') as f:
    content = f.read()

old_prev = '''          <!-- Return Side Navigation Button (Left Edge) -->
          <button class="exp__nav-side exp__nav-side--prev" id="expSidePrev"
                  aria-label="Previous experience slide: Infology Technologies"
                  title="Return to Infology Technologies">
            <span class="exp__nav-side-arrow">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round">
                <polyline points="15 18 9 12 15 6"></polyline>
              </svg>
            </span>
            <span class="exp__nav-side-text">Back to Infology</span>
          </button>'''

new_prev = '''          <!-- Return Triangular Navigation Button (Left Edge) -->
          <button class="exp__triangle-nav exp__triangle-nav--prev" id="expSidePrev"
                  aria-label="Previous experience slide: Infology Technologies"
                  title="Return to Infology Technologies">
            <span class="exp__triangle-arrow" aria-hidden="true">&#9664;</span>
            <span class="exp__triangle-label">BACK</span>
          </button>'''

content = content.replace(old_prev, new_prev)
content = content.replace('<h2 class="exp__future-title">UPDATING SOON</h2>', '<h2 class="exp__future-title">EXPERIENCE LOADING...</h2>')
content = content.replace('<!-- SLIDE 02: Full-Screen "UPDATING SOON" Continuation Screen       -->', '<!-- SLIDE 02: Full-Screen "EXPERIENCE LOADING..." Continuation Screen -->')

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("Slide 2 return button and EXPERIENCE LOADING... replaced successfully!")

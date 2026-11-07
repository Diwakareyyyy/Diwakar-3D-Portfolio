with open('index.html', 'r', encoding='utf-8') as f:
    code = f.read()

target = '''    <!-- Atmospheric Scene Background & Perspective Floor -->
    <div class="exp__env" aria-hidden="true">
      <div class="exp__env-glow"></div>
      <div class="exp__env-floor">
        <div class="exp__floor-grid"></div>
        <div class="exp__floor-horizon"></div>
      </div>
    </div>'''

replacement = '''    <!-- Atmospheric Scene Background & WebGL 3D Canvas Stage -->
    <div class="exp__env" aria-hidden="true">
      <canvas id="expCanvas" class="exp__canvas"></canvas>
      <div class="exp__env-glow"></div>
      <div class="exp__env-floor">
        <div class="exp__floor-grid"></div>
        <div class="exp__floor-horizon"></div>
      </div>
    </div>'''

assert target in code, "Target not found in index.html"
code = code.replace(target, replacement)

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(code)

print("Added expCanvas to index.html successfully!")

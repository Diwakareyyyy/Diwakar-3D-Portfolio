with open('src/styles/experience.css', 'r', encoding='utf-8') as f:
    css = f.read()

target = '''.exp__env {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
}'''

replacement = '''.exp__env {
  position: absolute;
  inset: 0;
  pointer-events: none;
  z-index: 1;
}

.exp__canvas {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  display: block;
  z-index: 1;
  pointer-events: none;
}'''

css = css.replace(target, replacement)

target_box = '''.exp__card-box {
  position: relative;
  width: 100%;
  background: rgba(14, 8, 12, 0.90);
  border: 1px solid rgba(222, 27, 28, 0.42);
  border-left: 3px solid #ff4532;
  border-radius: 10px;
  overflow: hidden;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.88), 0 0 20px rgba(222, 27, 28, 0.12);
  opacity: 0;
  transform: translateY(-12px);
  transition: opacity 1.2s cubic-bezier(0.16, 1, 0.3, 1) 0.1s,
              transform 1.2s cubic-bezier(0.16, 1, 0.3, 1) 0.1s;
  box-sizing: border-box;
}'''

replacement_box = '''.exp__card-box {
  position: relative;
  width: 100%;
  background: rgba(14, 8, 12, 0.90);
  border: 1px solid rgba(222, 27, 28, 0.42);
  border-left: 3px solid #ff4532;
  border-radius: 10px;
  overflow: hidden;
  backdrop-filter: blur(14px);
  -webkit-backdrop-filter: blur(14px);
  box-shadow: 0 16px 36px rgba(0, 0, 0, 0.88), 0 0 20px rgba(222, 27, 28, 0.12);
  opacity: 0;
  transform: translateY(-12px);
  transform-style: preserve-3d;
  will-change: transform;
  transition: opacity 1.2s cubic-bezier(0.16, 1, 0.3, 1) 0.1s,
              transform 0.25s cubic-bezier(0.2, 0.8, 0.2, 1),
              box-shadow 0.3s ease, border-color 0.3s ease;
  box-sizing: border-box;
}

.exp__card-box:hover {
  border-color: rgba(255, 69, 50, 0.75);
  box-shadow: 0 22px 52px rgba(0, 0, 0, 0.95), 0 0 32px rgba(222, 27, 28, 0.30);
}'''

css = css.replace(target_box, replacement_box)

with open('src/styles/experience.css', 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated experience.css with canvas and 3D card tilt styles!")

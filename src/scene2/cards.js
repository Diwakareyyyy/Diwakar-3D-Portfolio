// The eleven 3D skill blocks for the creative universe.
//
// Balanced wide-stage 3D composition around the central human silhouette:
// Left Wing (6 blocks, spread across left side & lowered into balanced vertical space):
//   - Upper-left hero block: Python
//   - Far-left mid hero block: Figma
//   - Upper-mid inner left: React
//   - Lower-mid inner left: Antigravity
//   - Lower-left outer midground: SQL
//   - Lower-left inner floor: Flutter
// Right Wing (5 blocks, spread across right side & lowered into balanced vertical space):
//   - Upper-right hero block: Claude
//   - Far-right mid block: GitHub
//   - Center-right inner block: C++
//   - Lower-right outer block: HTML
//   - Lower-right inner block: Vercel
//
// Order of skills strictly follows the required 11 skills:
// 1. Python, 2. SQL, 3. React, 4. Antigravity, 5. Flutter, 6. Vercel,
// 7. C++, 8. GitHub, 9. HTML, 10. Figma, 11. Claude.

// [name, rx, ry, rw, aspect, depthRatio, inwardYaw, pitchOffset, roll]
const REF = [
  // 1. Python: Upper-left hero panel (lowered from top edge & expanded left)
  ['python',      0.235, 0.265, 0.136, 0.94, 0.28,  0.42, -0.34, -0.12],
  // 2. SQL: Lower-left outer panel (expanded left and positioned into lower scene space)
  ['sql',         0.175, 0.765, 0.102, 0.93, 0.26,  0.46,  0.16,  0.04],
  // 3. React: Upper-mid inner left (lowered and widened clear of central character)
  ['react',       0.325, 0.445, 0.088, 0.94, 0.26,  0.44, -0.10,  0.03],
  // 4. Antigravity: Lower-mid inner left (balanced spacing between Figma, React, and SQL)
  ['antigravity', 0.258, 0.615, 0.085, 0.94, 0.26,  0.44,  0.12,  0.04],
  // 5. Flutter: Lower-left inner panel (uses lower space while keeping clear of character)
  ['flutter',     0.355, 0.775, 0.078, 0.94, 0.25,  0.42,  0.10,  0.02],
  // 6. Vercel: Lower-right inner panel (uses lower space while keeping clear of character)
  ['vercel',      0.665, 0.775, 0.096, 0.94, 0.26, -0.42, -0.14,  0.05],
  // 7. C++: Center-right inner panel (lowered and shifted right for wider balance)
  ['cpp',         0.682, 0.525, 0.098, 0.94, 0.28, -0.46, -0.18,  0.07],
  // 8. GitHub: Far-right mid panel (expanded into right-side space & lowered)
  ['github',      0.882, 0.475, 0.116, 0.92, 0.28, -0.48, -0.16,  0.05],
  // 9. HTML: Lower-right outer panel (expanded right & lowered into bottom-right space)
  ['html',        0.822, 0.695, 0.104, 1.04, 0.25, -0.44, -0.12,  0.04],
  // 10. Figma: Foreground hero panel on far-left (expanded left & centered vertically)
  ['figma',       0.115, 0.495, 0.144, 0.86, 0.28,  0.44, -0.16,  0.03],
  // 11. Claude: Foreground hero panel on upper-right (lowered from top & expanded right)
  ['claude',      0.755, 0.275, 0.156, 0.90, 0.30, -0.48, -0.30,  0.08],
];

const NEAREST = 0.185;

let seedState = 1;
function rnd() {
  seedState = (seedState * 1664525 + 1013904223) % 4294967296;
  return seedState / 4294967296;
}

export function buildCards() {
  seedState = 7;
  return REF.map(([name, rx, ry, rw, aspect, depthRatio, inwardYaw, pitchOffset, roll], i) => ({
    name,
    i,
    ref: { rx, ry, rw, aspect, depthRatio, inwardYaw, pitchOffset, roll },
    home: [0, 0, 0],
    size: [1, 1, 0.48],
    rest: [0, 0, roll || 0],
    phase: rnd() * Math.PI * 2,
    speed: 0.40 + rnd() * 0.42,
    // Controlled vertical float so panels never drift too high, paired with wider horizontal drift
    bobY: 0.026 + rnd() * 0.020,
    bobX: 0.032 + rnd() * 0.026,
    swing: 0.042 + rnd() * 0.036,
    launch: 0.85 + rnd() * 0.50,
    spin: (rnd() - 0.5) * 0.35,
    hover: 0,
    pulse: 0,
    pulseK: 1,
    clickT: -99,
    screen: null,
  }));
}

export function layoutCards(cards, aspect, fovY, camZ, opts = {}) {
  const tanH = Math.tan(fovY / 2);
  const spread = opts.spread ?? 1;
  const lift = opts.lift ?? 1;
  const sizeMul = opts.sizeMul ?? 1;

  for (const c of cards) {
    const { rx, ry, rw, depthRatio, inwardYaw, pitchOffset, roll } = c.ref;
    const f = rw / NEAREST;
    const dist = camZ / f;
    const z = camZ - dist;

    const ndcX = (rx - 0.5) * 2 * spread;
    const ndcY = -(ry - 0.5) * 2 * lift;

    const hx = ndcX * tanH * aspect * dist;
    const hy = ndcY * tanH * dist;
    c.home = [hx, hy, z];

    const halfW = rw * sizeMul * tanH * aspect * dist;
    const w = halfW * 2;
    const h = w / c.ref.aspect;
    const d = w * (depthRatio || 0.48);
    c.size = [w, h, d];
    c.dist = dist;

    // Compute camera view ray angles so every block's 3D rotation reliably exposes
    // its outer side wall and top/bottom thickness face regardless of viewport aspect.
    const rayYaw = Math.atan2(hx, dist);
    const rayPitch = Math.atan2(hy, dist);
    c.rest = [
      rayPitch + pitchOffset,
      -rayYaw + inwardYaw,
      roll,
    ];
  }
  return cards;
}

export function layoutFigure(aspect, fovY, camZ, refH = 0.60, refY = 0.60, apparent = 0.62) {
  const tanH = Math.tan(fovY / 2);
  const dist = camZ / apparent;
  return {
    z: camZ - dist,
    y: -(refY - 0.5) * 2 * tanH * dist,
    halfH: refH * tanH * dist,
    dist,
  };
}

export function poseCard(c, t, s, pointer) {
  const [hx, hy, hz] = c.home;

  const lag = 1 - s.rise;
  const drop = c.dist * 0.28 * c.launch;
  const y = hy - drop * lag * lag;
  const over = s.settle * c.dist * 0.015 * c.launch;

  const p = t * c.speed + c.phase;
  const scale = c.dist * 0.22;
  let fy = Math.sin(p) * c.bobY * scale * s.float;
  let fx = Math.cos(p * 0.78 + 1.1) * c.bobX * scale * s.float;
  const fz = Math.sin(p * 0.51 + 2.2) * 0.48 * s.float;

  // Soft boundary damping so upper cards never float too close to the top edge
  // and lower cards maintain comfortable breathing room above the bottom edge.
  if (c.ref.ry < 0.35 && fy > 0) fy *= 0.48;
  if (c.ref.ry > 0.72 && fy < 0) fy *= 0.58;
  if (c.ref.rx < 0.15 && fx < 0) fx *= 0.55;
  if (c.ref.rx > 0.85 && fx > 0) fx *= 0.55;

  const near = camNear(c.dist);
  const px = pointer.x * 0.46 * near * s.float;
  const py = -pointer.y * 0.24 * near * s.float;

  // click pulse: a quick bump toward the camera that settles back
  const pulse = c.pulse || 0;
  const bump = Math.sin(Math.min(1, c.pulseK ?? 1) * Math.PI) * pulse;

  const pos = [
    hx + fx + px,
    y + fy + over + py + c.hover * c.dist * 0.006,
    hz + fz + c.hover * c.dist * 0.075 + bump * c.dist * 0.05,
  ];

  // Independent multi-axis 3D oscillation + hover presentation turn
  const sideSign = c.ref.rx < 0.5 ? 1 : -1;
  const rot = [
    c.rest[0] + Math.sin(p * 0.63) * c.swing * s.float
      - pointer.y * 0.08 * near - c.hover * 0.07,
    c.rest[1] + Math.cos(p * 0.55 + 0.7) * c.swing * 1.25 * s.float
      + pointer.x * 0.10 * near - sideSign * c.hover * 0.14,
    c.rest[2] + c.spin * lag + Math.sin(p * 0.42 + 1.6) * 0.035 * s.float,
  ];

  const grow = (0.88 + 0.12 * s.mat) * (1 + c.hover * 0.06 + bump * 0.07);
  return {
    pos,
    rot,
    scale: [c.size[0] * grow, c.size[1] * grow, c.size[2] * grow],
  };
}

function camNear(dist) {
  return Math.min(1.6, 8.2 / Math.max(dist, 1));
}

export { REF };

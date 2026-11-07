// Scene five layout & geometry — calibrated for zero-clipping alignment and unobstructed central portrait.
// ==============================================================================

export const FRAME = [1600, 900];

export const CERT_CARDS = [
  // Left Wing: Positioned safely below the header title (X: 300, safe distance from center)
  {
    index: 0,
    box: [290, 250, 310, 195],
    depth: 0.50,
    rotY: 14,
    rotX: -4,
    rotZ: 2,
    tint: [1.0, 0.2, 0.2],
  },
  {
    index: 1,
    box: [290, 490, 310, 195],
    depth: 0.35,
    rotY: 16,
    rotX: -3,
    rotZ: 2,
    tint: [1.0, 0.2, 0.2],
  },
  // Right Wing: Consistently aligned at x = 1000, safe distance from center portrait
  {
    index: 2,
    box: [1000, 130, 310, 195],
    depth: 0.55,
    rotY: -14,
    rotX: -4,
    rotZ: -2,
    tint: [1.0, 0.2, 0.2],
  },
  {
    index: 3,
    box: [1000, 360, 310, 195],
    depth: 0.45,
    rotY: -15,
    rotX: -3,
    rotZ: -2,
    tint: [1.0, 0.2, 0.2],
  },
  {
    index: 4,
    box: [1000, 590, 310, 195],
    depth: 0.35,
    rotY: -16,
    rotX: -2,
    rotZ: -2,
    tint: [1.0, 0.2, 0.2],
  },
];

/** Cover-fit the reference frame onto any viewport. */
export function fitCover(w, h) {
  const s = Math.max(w / FRAME[0], h / FRAME[1]);
  return { s, ox: (w - FRAME[0] * s) / 2, oy: (h - FRAME[1] * s) / 2 };
}

/**
 * Recomposition for mobile & tablet screens:
 * Preserves the central personal portrait by positioning all 5 cards in the left & right wings.
 * The central column (38% to 62%) is strictly kept clear so Card 4 NEVER overlaps the portrait.
 */
export const PORTRAIT_CERTS = new Map([
  [0, { cx: 0.24, cy: 0.26, w: 0.40 }],
  [1, { cx: 0.24, cy: 0.50, w: 0.40 }],
  [2, { cx: 0.76, cy: 0.24, w: 0.40 }],
  [3, { cx: 0.76, cy: 0.46, w: 0.40 }],
  [4, { cx: 0.76, cy: 0.68, w: 0.40 }],
]);

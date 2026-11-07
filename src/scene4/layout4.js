// Scene four geometry and layout helpers
// ==============================================================================
// 12 Projects divided into two horizontal streams:
//   Row 1: Projects 01 - 06 (Moving Right to Left)
//   Row 2: Projects 07 - 12 (Moving Left to Right)
// ==============================================================================

import { PROJECTS } from '../data/projects.js';

export const FRAME = [1600, 900];

// The central figure: seated developer working at workstation desk with computer
// positioned cleanly at bottom-center (x=660, y=586, w=280, h=232)
export const PERSON = { x: 620, y: 478, w: 360, h: 342 };

// The floor's lit ellipses and overhead ring for shader ambient lighting
export const FLOOR_OUT = [798, 735, 372, 80];
export const FLOOR_IN = [798, 741, 240, 57];
export const RING = [802, 34, 392, 148];

/** Cover-fit the reference frame onto any viewport. */
export function fitCover(w, h) {
  const s = Math.max(w / FRAME[0], h / FRAME[1]);
  return { s, ox: (w - FRAME[0] * s) / 2, oy: (h - FRAME[1] * s) / 2 };
}

// Renders S DIWAKAR into a single coverage texture and reports the ink rectangle
// of every individual letter.
//
// Why a texture and not DOM text: sharing one atlas means the clip
// mask and the visible letters are the same pixels, so they can never drift apart
// by even a subpixel, at any size or device pixel ratio.
//
// The typeface is set in Anton (compressed heavy grotesque). A calibrated
// horizontal scale factor is solved dynamically at runtime to hit the measured
// word-width : cap-height ratio while preserving letterform proportions.

export const TEXT = 'DIWAKAR';

/**
 * Calculates the exact ink aspect ratio (ink width / cap height) for the text
 * in the active Anton typeface with natural tracking and subtle grotesque condensation.
 */
export function measureTargetRatio(text = TEXT, condense = 0.89) {
  const probe = 400;
  const c = ctx2d(8, 8);
  c.font = `${probe}px Anton, "Arial Narrow", Impact, sans-serif`;
  c.textBaseline = 'alphabetic';
  const capAt = metricsFor(c, 'H').ascent || probe * 0.72;
  const tracking = -0.012 * capAt;
  const per = [...text].map((ch) => metricsFor(c, ch));

  let pen = 0;
  let natL = Infinity;
  let natR = -Infinity;
  per.forEach((m, i) => {
    const at = pen;
    if (text[i] !== ' ') {
      natL = Math.min(natL, at - m.left);
      natR = Math.max(natR, at + m.right);
    }
    pen += m.advance + tracking;
  });
  if (!Number.isFinite(natL)) natL = 0;
  if (!Number.isFinite(natR)) natR = pen;
  const naturalInk = Math.max(1, natR - natL);
  return (naturalInk / capAt) * condense;
}

// Calibrated initial ratio for 'DIWAKAR' (~3.25). Re-computed dynamically once fonts load.
export let TARGET_RATIO = 3.25;

export function updateTargetRatio() {
  TARGET_RATIO = measureTargetRatio(TEXT, 0.89);
  return TARGET_RATIO;
}

function ctx2d(w, h) {
  const c = document.createElement('canvas');
  c.width = Math.max(1, Math.ceil(w));
  c.height = Math.max(1, Math.ceil(h));
  return c.getContext('2d', { willReadFrequently: false });
}

function metricsFor(ctx, ch) {
  const m = ctx.measureText(ch);
  return {
    advance: m.width,
    left: m.actualBoundingBoxLeft || 0,
    right: m.actualBoundingBoxRight || (ch === ' ' ? 0 : m.width),
    ascent: m.actualBoundingBoxAscent || 0,
    descent: m.actualBoundingBoxDescent || 0,
  };
}

/**
 * @param {number} capHeightPx desired cap height in device pixels
 * @param {number} maxTexture  gl.MAX_TEXTURE_SIZE
 */
export function buildWord(capHeightPx, maxTexture = 4096) {
  const probe = 400;
  let c = ctx2d(8, 8);
  c.font = `${probe}px Anton, "Arial Narrow", Impact, sans-serif`;
  c.textBaseline = 'alphabetic';

  // solve font size so the cap height lands exactly where we want it
  const capAt = metricsFor(c, 'H').ascent || probe * 0.72;
  let size = (capHeightPx / capAt) * probe;

  // Natural ink extent at that size, with negative tracking for tightly packed setting.
  c.font = `${size}px Anton, "Arial Narrow", Impact, sans-serif`;
  const tracking = -0.012 * capHeightPx;
  const per = [...TEXT].map((ch) => metricsFor(c, ch));

  let pen = 0;
  let natL = Infinity;
  let natR = -Infinity;
  const walk = per.map((m, i) => {
    const at = pen;
    const ch = TEXT[i];
    if (ch !== ' ') {
      natL = Math.min(natL, at - m.left);
      natR = Math.max(natR, at + m.right);
    }
    pen += m.advance + tracking;
    return { char: ch, pen: at, m };
  });
  if (!Number.isFinite(natL)) natL = 0;
  if (!Number.isFinite(natR)) natR = pen;
  const naturalInk = Math.max(1, natR - natL);

  // Calibrate scaleX with subtle aesthetic condensation (~0.89 factor)
  const naturalRatio = naturalInk / capHeightPx;
  const condense = 0.89;
  TARGET_RATIO = naturalRatio * condense;
  const scaleX = condense;

  // lay the letters out in scaled space
  const pad = Math.ceil(capHeightPx * 0.06);
  const raw = walk.map((r) => ({
    char: r.char,
    penX: r.pen * scaleX,
    x0: (r.char === ' ' ? r.pen : r.pen - r.m.left) * scaleX,
    x1: (r.char === ' ' ? r.pen : r.pen + r.m.right) * scaleX,
    m: r.m,
  }));
  const inkL = natL * scaleX;
  const inkR = natR * scaleX;
  const descent = Math.max(0, ...per.map((m) => m.descent));

  let W = Math.ceil(inkR - inkL) + pad * 2;
  let H = Math.ceil(capHeightPx + descent) + pad * 2;

  // stay inside the GPU limit; the whole composition scales down together
  let fit = 1;
  if (W > maxTexture) fit = maxTexture / W;
  if (H * fit > maxTexture) fit = maxTexture / H;
  if (fit < 1) {
    size *= fit;
    W = Math.floor(W * fit);
    H = Math.floor(H * fit);
  }

  const g = ctx2d(W, H);
  g.font = `${size}px Anton, "Arial Narrow", Impact, sans-serif`;
  g.textBaseline = 'alphabetic';
  g.fillStyle = '#fff';
  g.setTransform(scaleX * fit, 0, 0, fit, (-inkL * fit) + pad, capHeightPx * fit + pad);

  const letters = raw.map((r) => {
    if (r.char !== ' ') {
      g.fillText(r.char, r.penX / scaleX, 0);
    }
    const x = (r.x0 - inkL) * fit + pad;
    const w = (r.x1 - r.x0) * fit;
    return {
      char: r.char,
      x,
      y: pad + (capHeightPx - r.m.ascent) * fit,
      w,
      h: r.m.ascent * fit,
    };
  });
  g.setTransform(1, 0, 0, 1, 0, 0);

  return {
    canvas: g.canvas,
    width: W,
    height: H,
    pad,
    fit,
    // ink box of the whole word inside the canvas
    ink: { x: pad, y: pad, w: (inkR - inkL) * fit, h: capHeightPx * fit },
    letters: letters.map((l) => ({
      ...l,
      u0: l.x / W,
      v0: l.y / H,
      u1: (l.x + l.w) / W,
      v1: (l.y + l.h) / H,
    })),
  };
}

export async function fontsReady() {
  if (!document.fonts) return;
  try {
    await Promise.all([
      document.fonts.load('400 200px Anton'),
      document.fonts.load('700 40px Oswald'),
      document.fonts.load('400 40px Oswald'),
    ]);
    await document.fonts.ready;
    updateTargetRatio();
  } catch { /* fall back to the stack in the font shorthand */ }
}

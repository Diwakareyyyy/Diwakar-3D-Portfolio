// Scene two: the creative universe.
//
// Draw order, back to front:
//   1  environment   dark room, red bloom behind the core, reflective floor
//   2  core ring     concentric arcs, rotating and pulsing
//   3  ribbon (far)  the segments that pass BEHIND the figure
//   4  figure        silhouette from the artwork, lit by this scene
//   5  ribbon (near) the segments in front of him
//   6  debris + cards, depth sorted back to front
//   7  embers        additive, with depth-of-field
//   8  post          grain and vignette
//
// Cards are drawn painter-style with the depth buffer off, because everything
// here is translucent and additive; sorting by w each frame is cheap for a
// dozen quads and avoids the sorting artefacts blending would otherwise give.

import { program, unitQuad, unitCube, texture, upload, bind, loadImage } from '../gl/renderer.js';
import {
  V2_FULL, F2_ENV, F2_RING, V2_CARD, F2_CARD, V2_RIBBON, F2_RIBBON,
  V2_SPARK, F2_SPARK, V2_QUAD3D, F2_FIGURE, F2_CUBE, F2_POST,
} from '../gl/shaders2.js';
import { perspective, multiply, compose, projectPoint } from '../lib/mat4.js';
import { buildCards, layoutCards, layoutFigure, poseCard } from './cards.js';
import { Ribbon } from './ribbon.js';
import { Sparks, buildDebris } from './particles.js';
import { sample2 } from './timeline2.js';
import { damp, clamp } from '../lib/ease.js';

const TOOLS = [
  'python', 'sql', 'react', 'antigravity', 'flutter', 'vercel',
  'cpp', 'github', 'html', 'figma', 'claude',
];

const CORNERS = [[-1, -1], [1, -1], [-1, 1], [1, 1]];
// the nearest card sits at z=0; anything closer than this passes over the shell
const NEAR_CARD_Z = 0.55;
const FIGURE_Z = 1.6;      // he stands behind the card shell
const CAM_Z = 8.2;
const FOV = 0.85;

export class Universe {
  constructor(canvas, gl) {
    this.canvas = canvas;
    this.gl = gl;
    this.cards = buildCards();
    this.debris = buildDebris(16);
    this.pointer = { x: 0, y: 0, tx: 0, ty: 0, inside: false };
    this.hovered = -1;
    this.quality = 1;
    this.time = 0;
    this.dolly = 0;

    this.progs = {
      env: program(gl, V2_FULL, F2_ENV, 'env'),
      ring: program(gl, V2_FULL, F2_RING, 'ring'),
      card: program(gl, V2_CARD, F2_CARD, 'card'),
      cube: program(gl, V2_CARD, F2_CUBE, 'cube'),
      figure: program(gl, V2_QUAD3D, F2_FIGURE, 'figure'),
      ribbon: program(gl, V2_RIBBON, F2_RIBBON, 'ribbon'),
      spark: program(gl, V2_SPARK, F2_SPARK, 'spark'),
      post: program(gl, V2_FULL, F2_POST, 'post'),
    };
    this.quad = unitQuad(gl);
    // every skill block and debris fragment is a real 3D volume: a bounding
    // cube that the fragment shaders ray-cast a rounded box inside
    this.cube = unitCube(gl);
    this.ribbon = new Ribbon(gl, FIGURE_Z);
    this.sparks = new Sparks(gl, 900);

    this.tex = { grain: texture(gl, { wrap: 'repeat' }), figure: texture(gl) };
    this.logos = {};
    this.proj = new Float32Array(16);
    this.mvp = new Float32Array(16);
    this.model = new Float32Array(16);
    this.mvpTmp = new Float32Array(16);
    this.figMvp = new Float32Array(16);
    this.res = [1, 1];
    this.core = [0.5, 0.47];
  }

  async load() {
    const gl = this.gl;
    const [grain, fig] = await Promise.all([
      loadImage('public/tex/grain.png'),
      loadImage('public/tools/figure.png'),
    ]);
    upload(gl, this.tex.grain, grain);
    upload(gl, this.tex.figure, fig);
    this.figureAspect = fig.width / fig.height;

    const imgs = await Promise.all(
      TOOLS.map((n) => loadImage(`public/tools/${n}.png`).catch(() => null)));
    TOOLS.forEach((n, i) => {
      if (!imgs[i]) return;
      const t = texture(gl);
      upload(gl, t, imgs[i], false, true);
      this.logos[n] = { tex: t, aspect: imgs[i].width / imgs[i].height };
    });
  }

  resize(w, h, dpr) {
    const W = Math.round(w * dpr);
    const H = Math.round(h * dpr);
    if (this.canvas.width !== W || this.canvas.height !== H) {
      this.canvas.width = W;
      this.canvas.height = H;
    }
    this.res = [W, H];
    this.cssW = w;
    this.cssH = h;
    this.dpr = dpr;
    this.portrait = h / w > 1.05;
    const aspect = W / H;
    perspective(FOV, aspect, 0.1, 100, this.proj);

    // The composition is re-solved for the actual viewport rather than scaled:
    // on a narrow screen the shell is pulled in and flattened so the cards stay
    // on stage instead of drifting off the sides.
    // Portrait is a genuine recomposition, not the desktop frame scaled down.
    // The reference is a landscape poster: mapped straight onto a tall screen
    // its cards collapse toward the vertical middle, which is exactly where the
    // figure stands. So on a phone the shell is spread wider and taller, the
    // cards shrink, and the figure steps back to leave the centre clear.
    const narrow = w < 760;
    const tall = aspect < 1.0;
    this.quality = w < 600 ? 0.52 : (w < 1024 ? 0.76 : 1.0);
    layoutCards(this.cards, aspect, FOV, CAM_Z, {
      spread: tall ? 0.86 : 1.0,
      lift: tall ? 0.94 : 1.0,
      sizeMul: tall ? 1.24 : (narrow ? 0.92 : 1.0),
    });
    this.fig = layoutFigure(aspect, FOV, CAM_Z, tall ? 0.65 : 1.08, tall ? 0.61 : 0.60, tall ? 0.68 : 0.86);
    // the ring is measured against the SHORTER edge, or it overflows a phone
    this.ringScale = tall ? 0.58 : 1.0;
    // the energy ribbon orbits the figure where he actually stands
    this.ribbon.figureZ = this.fig.z + 0.6;
    this.ribbon.centerY = this.fig.y;
    this.ribbon.scale = tall ? 0.75 : 1.0;
  }

  /** A click on a block: a 3D pulse, a flash, and an energy ripple. */
  click(i) {
    const c = this.cards[i];
    if (!c) return;
    c.clickT = this.time;
  }

  /** Screen-space hit test, using each card's projected quad. */
  pick(cx, cy) {
    const nx = (cx / this.cssW) * 2 - 1;
    const ny = 1 - (cy / this.cssH) * 2;
    let best = -1;
    let bestW = 1e9;
    for (const c of this.cards) {
      const s = c.screen;
      if (!s) continue;
      if (nx >= s.x0 && nx <= s.x1 && ny >= s.y0 && ny <= s.y1 && s.w < bestW) {
        best = c.i;
        bestW = s.w;
      }
    }
    return best;
  }

  render(t, dt, scroll = 0) {
    const gl = this.gl;
    const [W, H] = this.res;
    const s = sample2(t);
    this.time = t;
    const aspect = W / H;

    const p = this.pointer;
    p.x = damp(p.x, p.inside ? p.tx : 0, 3.0, dt);
    p.y = damp(p.y, p.inside ? p.ty : 0, 3.0, dt);
    const gate = s.float;
    const ptr = { x: p.x * gate, y: p.y * gate };

    // scrolling dollies the camera through the room; the sequence itself is
    // time-based so its choreography cannot be scrubbed out of shape
    this.dolly = damp(this.dolly, scroll * 1.5, 4.0, dt);

    const view = new Float32Array([
      1, 0, 0, 0, 0, 1, 0, 0, 0, 0, 1, 0,
      -ptr.x * 0.25, -ptr.y * 0.15, -(CAM_Z + this.dolly), 1,
    ]);
    multiply(this.proj, view, this.mvp);

    gl.viewport(0, 0, W, H);
    gl.disable(gl.DEPTH_TEST);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
    gl.clearColor(0, 0, 0, 1);
    gl.clear(gl.COLOR_BUFFER_BIT);
    gl.bindVertexArray(this.quad);

    // where is the stroke's head on screen? the environment blushes around it
    this.ribbon.update(t, 0.15 + 0.02 * Math.sin(t * 0.9),
      Math.max(s.ribbonDraw, 0.001),
      Math.min(1, s.ribbonDraw * 2.2));
    const hp3 = this.ribbon.headPos;
    const hndc = projectPoint(this.mvp, hp3[0], hp3[1], hp3[2]);
    const headScr = [(hndc[0] + 1) * 0.5, (1 - hndc[1]) * 0.5,
      s.ribbonLife * 0.9];

    // ---- 1 environment ----------------------------------------------------
    {
      const pr = this.progs.env;
      gl.useProgram(pr.p);
      gl.uniform1i(pr.u.uGrain, bind(gl, this.tex.grain, 0));
      gl.uniform2f(pr.u.uRes, W, H);
      gl.uniform1f(pr.u.uTime, t);
      gl.uniform1f(pr.u.uAspect, aspect);
      gl.uniform1f(pr.u.uWake, s.wake);
      gl.uniform1f(pr.u.uBurst, s.burst);
      gl.uniform2f(pr.u.uCore, this.core[0], this.core[1]);
      gl.uniform3f(pr.u.uStroke, headScr[0], headScr[1], headScr[2]);
      const fHalfW = this.fig.halfH * (this.figureAspect || 0.357);
      const fC = projectPoint(this.mvp, 0, this.fig.y - this.fig.halfH * 0.965, this.fig.z);
      const fR = projectPoint(this.mvp, fHalfW * 0.695, this.fig.y - this.fig.halfH * 0.965, this.fig.z);
      gl.uniform3f(pr.u.uFigFeet, (fC[0] + 1) * 0.5, (1 - fC[1]) * 0.5, Math.abs(fR[0] - fC[0]) * 0.5 * aspect);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }

    // ---- 2 core ring (additive) -------------------------------------------
    gl.blendFunc(gl.ONE, gl.ONE);
    {
      const pr = this.progs.ring;
      gl.useProgram(pr.p);
      gl.uniform2f(pr.u.uRes, W, H);
      gl.uniform1f(pr.u.uTime, t);
      gl.uniform1f(pr.u.uAspect, aspect);
      gl.uniform1f(pr.u.uLife, s.ring);
      gl.uniform1f(pr.u.uBurst, s.burst);
      gl.uniform1f(pr.u.uScale, this.ringScale);
      gl.uniform2f(pr.u.uCore, this.core[0], this.core[1]);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }
    gl.bindVertexArray(null);

    // ---- 3 / 5 ribbon ------------------------------------------------------
    // One strip (already rebuilt above), drawn in depth bands: the trail
    // weaves through the room, so its behind-the-figure and in-front-of-the-
    // cards stretches interleave.
    const drawRibbon = (zMin, zMax) => {
      const pr = this.progs.ribbon;
      gl.useProgram(pr.p);
      gl.uniformMatrix4fv(pr.u.uMVP, false, this.mvp);
      gl.uniform1f(pr.u.uIntensity, 0.5 + 0.7 * s.ribbonLife);
      gl.uniform1f(pr.u.uTime, t);
      gl.uniform2f(pr.u.uZBand, zMin, zMax);
      this.ribbon.draw();
    };
    // far half: everything beyond the figure
    drawRibbon(-99, this.fig.z);

    // ---- 4 figure ----------------------------------------------------------
    gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
    {
      const pr = this.progs.figure;
      gl.useProgram(pr.p);
      const halfH = this.fig.halfH;
      const halfW = halfH * this.figureAspect;
      const breathe = 1 + Math.sin(t * 0.55) * 0.004;
      compose([0, this.fig.y, this.fig.z], [0, 0, 0],
        [halfW, halfH * breathe], this.model);
      multiply(this.mvp, this.model, this.figMvp);
      gl.uniformMatrix4fv(pr.u.uMVP, false, this.figMvp);
      gl.uniform2f(pr.u.uHalf, 1, 1);
      gl.uniform1i(pr.u.uFig, bind(gl, this.tex.figure, 0));
      gl.uniform1i(pr.u.uGrain, bind(gl, this.tex.grain, 1));
      gl.uniform1f(pr.u.uOpacity, s.wake);
      gl.uniform1f(pr.u.uRim, 0.55 + 0.75 * s.ring);
      gl.uniform2f(pr.u.uLightDir, 0.35, 0.55);
      gl.uniform1f(pr.u.uTime, t);
      gl.bindVertexArray(this.quad);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
      gl.bindVertexArray(null);
    }

    // the rest of the stroke, in front of the figure. It is painted BEFORE the
    // skill blocks so it weaves behind them and never crosses a logo or name;
    // the blocks receive its warm light instead (uRibbonLocal below).
    gl.blendFunc(gl.ONE, gl.ONE);
    drawRibbon(this.fig.z, 99);
    gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);

    // ---- 6 debris + cards, sorted far to near ------------------------------
    const camPos = [ptr.x * 0.25, ptr.y * 0.15, CAM_Z + this.dolly];
    const corePos = [0, this.fig.y + this.fig.halfH * 0.18, this.fig.z - 0.2];
    const hp = this.ribbon.headPos;
    const ribLife = Math.min(1, s.ribbonDraw * 1.4) * (0.45 + 0.55 * s.ribbonLife);

    const items = [];
    for (const d of this.debris) {
      const ph = t * d.speed + d.phase;
      const pos = [
        d.home[0] + Math.sin(ph) * 0.16 * s.float,
        d.home[1] + Math.cos(ph * 0.8) * 0.12 * s.float,
        d.home[2] + Math.sin(ph * 0.6 + 1.3) * 0.18 * s.float,
      ];
      const rot = [
        d.rot[0] + t * 0.16 * d.speed,
        d.rot[1] + t * 0.22 * d.speed,
        d.rot[2] + Math.sin(ph * 0.5) * 0.25,
      ];
      items.push({ kind: 'cube', d, pos, rot, w: CAM_Z + this.dolly - pos[2] });
    }
    for (const c of this.cards) {
      c.hover = damp(c.hover, this.hovered === c.i ? 1 : 0, 7, dt);
      const k = (t - c.clickT) / 0.9;
      c.pulseK = Math.max(0, Math.min(1, k));
      c.pulse = k >= 0 && k < 1 ? 1 : 0;
      const pose = poseCard(c, t, s, ptr);
      items.push({
        kind: 'card', c, pose, k, w: CAM_Z + this.dolly - pose.pos[2],
      });
    }
    items.sort((a, b) => b.w - a.w);

    // block-local copies of the world points the shaders light against
    const m = this.model;
    const toLocal = (p, pos) => {
      const vx = p[0] - pos[0];
      const vy = p[1] - pos[1];
      const vz = p[2] - pos[2];
      return [
        m[0] * vx + m[1] * vy + m[2] * vz,
        m[4] * vx + m[5] * vy + m[6] * vz,
        m[8] * vx + m[9] * vy + m[10] * vz,
      ];
    };

    gl.bindVertexArray(this.cube);
    gl.enable(gl.CULL_FACE);
    gl.cullFace(gl.BACK);

    for (const it of items) {
      if (it.kind === 'cube') {
        const pr = this.progs.cube;
        gl.useProgram(pr.p);
        compose(it.pos, it.rot, [1, 1, 1], m);
        multiply(this.mvp, m, this.mvpTmp);
        const sz = it.d.size;
        gl.uniformMatrix4fv(pr.u.uMVP, false, this.mvpTmp);
        gl.uniform3f(pr.u.uBoxHalf, sz, sz, sz);
        gl.uniform1f(pr.u.uGlowPad, 0);
        gl.uniform1f(pr.u.uBevel, sz * 0.065);
        gl.uniform3fv(pr.u.uCamLocal, toLocal(camPos, it.pos));
        gl.uniform3fv(pr.u.uLightLocal, toLocal(corePos, it.pos));
        gl.uniform3f(pr.u.uUpLocal, m[1], m[5], m[9]);
        gl.uniform1f(pr.u.uOpacity, s.mat * 0.95);
        gl.drawArrays(gl.TRIANGLES, 0, 36);
        continue;
      }

      const { c, pose } = it;
      const lg = this.logos[c.name];
      const pr = this.progs.card;
      gl.useProgram(pr.p);
      compose(pose.pos, pose.rot, [1, 1, 1], m);
      multiply(this.mvp, m, this.mvpTmp);

      const [bw, bh, bd] = pose.scale;
      const halfW = bw * 0.5;
      const halfH = bh * 0.5;
      const halfD = bd * 0.5;
      const glowPad = Math.max(halfW, halfH) * 0.55;

      gl.uniformMatrix4fv(pr.u.uMVP, false, this.mvpTmp);
      gl.uniform3f(pr.u.uBoxHalf, halfW, halfH, halfD);
      gl.uniform1f(pr.u.uBevel, Math.min(halfW, halfH) * 0.042);
      gl.uniform1f(pr.u.uGlowPad, glowPad);
      gl.uniform3fv(pr.u.uCamLocal, toLocal(camPos, pose.pos));
      gl.uniform3fv(pr.u.uLightLocal, toLocal(corePos, pose.pos));
      gl.uniform3f(pr.u.uUpLocal, m[1], m[5], m[9]);
      gl.uniform1i(pr.u.uLogo, bind(gl, lg ? lg.tex : this.tex.grain, 0));
      gl.uniform1i(pr.u.uGrain, bind(gl, this.tex.grain, 1));

      // the logo texture already carries its own padding + the skill name, so
      // it is fitted to the face preserving its aspect
      const faceAspect = halfW / halfH;
      const pad = 0.90;
      const la = lg ? lg.aspect : 1;
      let lw = pad;
      let lh = (pad * faceAspect) / la;
      if (lh > pad) { lh = pad; lw = (pad * la) / faceAspect; }
      gl.uniform2f(pr.u.uLogoScale, lw, lh);

      // the ribbon's head lights the blocks it passes
      const dx = hp[0] - pose.pos[0];
      const dy = hp[1] - pose.pos[1];
      const dz = hp[2] - pose.pos[2];
      const near = Math.exp(-(dx * dx + dy * dy + dz * dz) / (4.5 * Math.max(halfW, 0.5)));
      gl.uniform3fv(pr.u.uRibbonLocal, toLocal(hp, pose.pos));
      gl.uniform1f(pr.u.uRibbonAmt, near * ribLife);

      const k = it.k;
      const active = k >= 0 && k < 1;
      gl.uniform1f(pr.u.uPulse, active ? (1 - k) * (1 - k) : 0);
      gl.uniform1f(pr.u.uRipple, active ? k : 1);
      gl.uniform1f(pr.u.uOpacity, s.mat);
      gl.uniform1f(pr.u.uMat, s.mat);
      gl.uniform1f(pr.u.uHover, c.hover);
      gl.uniform1f(pr.u.uTime, t);
      gl.drawArrays(gl.TRIANGLES, 0, 36);

      // Cache the projected block for hit testing (all eight corners).
      let x0 = 9, x1 = -9, y0 = 9, y1 = -9;
      for (const [sx, sy] of CORNERS) {
        for (const sz of [-1, 1]) {
          const [px, py] = projectPoint(this.mvpTmp, sx * halfW, sy * halfH, sz * halfD);
          x0 = Math.min(x0, px); x1 = Math.max(x1, px);
          y0 = Math.min(y0, py); y1 = Math.max(y1, py);
        }
      }
      c.screen = { x0, x1, y0, y1, w: it.w };
    }
    gl.disable(gl.CULL_FACE);
    gl.bindVertexArray(null);

    // ---- 7 embers ----------------------------------------------------------
    gl.blendFunc(gl.ONE, gl.ONE);
    {
      const pr = this.progs.spark;
      gl.useProgram(pr.p);
      gl.uniformMatrix4fv(pr.u.uMVP, false, this.mvp);
      gl.uniform1f(pr.u.uTime, t);
      gl.uniform1f(pr.u.uConverge, s.converge * 0.55);
      gl.uniform1f(pr.u.uLife, 0.25 + 0.75 * s.wake);
      gl.uniform2f(pr.u.uPointer, ptr.x, ptr.y);
      gl.uniform1f(pr.u.uRes, H);
      const hp = this.ribbon.headPos;
      gl.uniform3f(pr.u.uHead, hp[0], hp[1], hp[2]);
      this.sparks.draw(Math.round(this.sparks.count * this.quality));
    }

    // ---- 8 post ------------------------------------------------------------
    gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
    gl.bindVertexArray(this.quad);
    {
      const pr = this.progs.post;
      gl.useProgram(pr.p);
      gl.uniform1i(pr.u.uGrain, bind(gl, this.tex.grain, 0));
      gl.uniform2f(pr.u.uRes, W, H);
      gl.uniform1f(pr.u.uTime, t);
      gl.uniform1f(pr.u.uAmount, s.grain);
      gl.uniform1f(pr.u.uAspect, aspect);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }
    gl.bindVertexArray(null);

    return s;
  }
}

export { TOOLS };

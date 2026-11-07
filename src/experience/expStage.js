// WebGL2 Stage for the 3D Experience Section
import { program, unitQuad } from '../gl/renderer.js';
import { perspective, multiply, compose } from '../lib/mat4.js';
import {
  V_EXP_ENV, F_EXP_ENV,
  F_EXP_CORE,
  V_EXP_PARTICLES, F_EXP_PARTICLES,
} from './expShaders.js';

export class ExpStage {
  constructor(canvas, gl) {
    this.canvas = canvas;
    this.gl = gl;
    this.quad = unitQuad(gl);

    this.progs = {
      env: program(gl, V_EXP_ENV, F_EXP_ENV, 'expEnv'),
      core: program(gl, V_EXP_ENV, F_EXP_CORE, 'expCore'),
      particles: program(gl, V_EXP_PARTICLES, F_EXP_PARTICLES, 'expParticles'),
    };

    this._initParticles(54);

    this.pointer = { x: 0, y: 0, tx: 0, ty: 0 };
    this.hover = 0;
    this.active = 0;
    this.res = [1, 1];
    this.aspect = 1.6;
    this.mvp = new Float32Array(16);
    this.proj = new Float32Array(16);
    this.view = new Float32Array(16);
  }

  _initParticles(count) {
    const gl = this.gl;
    const pos = [];
    const data = [];

    let seed = 42;
    const rnd = () => {
      seed = (seed * 1664525 + 1013904223) % 4294967296;
      return seed / 4294967296;
    };

    for (let i = 0; i < count; i++) {
      // 3D coordinates spread across the cyber office space
      const x = (rnd() - 0.4) * 6.0;
      const y = (rnd() - 0.45) * 3.6;
      const z = (rnd() - 0.5) * 4.0;
      pos.push(x, y, z);

      const phase = rnd() * Math.PI * 2;
      const scale = 0.3 + rnd() * 0.7;
      data.push(phase, scale);
    }

    this.particleCount = count;
    this.particleVAO = gl.createVertexArray();
    gl.bindVertexArray(this.particleVAO);

    const posBuf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, posBuf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(pos), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0);
    gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0);

    const dataBuf = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, dataBuf);
    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(data), gl.STATIC_DRAW);
    gl.enableVertexAttribArray(1);
    gl.vertexAttribPointer(1, 2, gl.FLOAT, false, 0, 0);

    gl.bindVertexArray(null);
  }

  resize(w, h, dpr) {
    const W = Math.round(w * dpr);
    const H = Math.round(h * dpr);
    if (this.canvas.width !== W || this.canvas.height !== H) {
      this.canvas.width = W;
      this.canvas.height = H;
    }
    this.res = [W, H];
    this.aspect = w / h;
    this.gl.viewport(0, 0, W, H);
  }

  render(time) {
    const gl = this.gl;
    const [W, H] = this.res;

    // Dampen pointer
    this.pointer.x += (this.pointer.tx - this.pointer.x) * 0.08;
    this.pointer.y += (this.pointer.ty - this.pointer.y) * 0.08;

    gl.disable(gl.DEPTH_TEST);
    gl.enable(gl.BLEND);
    gl.blendFunc(gl.SRC_ALPHA, gl.ONE_MINUS_SRC_ALPHA);
    gl.clearColor(0, 0, 0, 1);
    gl.clear(gl.COLOR_BUFFER_BIT);

    // 1. Render Atmospheric 3D Environment with Perspective Floor
    gl.bindVertexArray(this.quad);
    {
      const p = this.progs.env;
      gl.useProgram(p.p);
      gl.uniform2f(p.u.uRes, W, H);
      gl.uniform1f(p.u.uTime, time);
      gl.uniform1f(p.u.uAspect, this.aspect);
      gl.uniform2f(p.u.uPointer, this.pointer.x, this.pointer.y);
      gl.uniform1f(p.u.uActive, this.active);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }

    // 2. Render Holographic Cyber-Architectural Core Rings (Additive)
    gl.blendFunc(gl.ONE, gl.ONE);
    {
      const p = this.progs.core;
      gl.useProgram(p.p);
      gl.uniform2f(p.u.uRes, W, H);
      gl.uniform1f(p.u.uTime, time);
      gl.uniform1f(p.u.uAspect, this.aspect);
      gl.uniform2f(p.u.uPointer, this.pointer.x, this.pointer.y);
      gl.uniform1f(p.u.uHover, this.hover);
      gl.drawArrays(gl.TRIANGLE_STRIP, 0, 4);
    }

    // 3. Render 3D Floating Particles & Embers
    perspective(0.85, this.aspect, 0.1, 50.0, this.proj);
    const camPos = [this.pointer.x * 0.6, -this.pointer.y * 0.4, 4.8];
    const camRot = [-this.pointer.y * 0.15, this.pointer.x * 0.22, 0];
    compose(camPos, camRot, [1, 1], this.view);
    multiply(this.proj, this.view, this.mvp);

    gl.bindVertexArray(this.particleVAO);
    {
      const p = this.progs.particles;
      gl.useProgram(p.p);
      gl.uniformMatrix4fv(p.u.uMVP, false, this.mvp);
      gl.uniform1f(p.u.uTime, time);
      gl.uniform2f(p.u.uPointer, this.pointer.x, this.pointer.y);
      gl.drawArrays(gl.POINTS, 0, this.particleCount);
    }

    gl.bindVertexArray(null);
  }
}

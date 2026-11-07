// Embers & 3D Floating Geometric Fragments (Debris Cubes).
//
// All spark motion happens in the vertex shader from a per-point seed, so the CPU
// never touches these after upload - 900 sparks cost one draw call and no
// per-frame work.
// The 18 small dark 3D cubes sit in the scenic spaces around the figure and
// skill blocks, matching IMAGE 2's floating 3D fragments with red rim-lit edges.

export class Sparks {
  constructor(gl, count = 900) {
    this.gl = gl;
    this.count = count;

    const pos = new Float32Array(count * 3);
    const seed = new Float32Array(count * 3);
    let s = 12345;
    const rnd = () => {
      s = (s * 1664525 + 1013904223) % 4294967296;
      return s / 4294967296;
    };

    for (let i = 0; i < count; i++) {
      const r = 2.2 + Math.pow(rnd(), 0.6) * 11.5;
      const a = rnd() * Math.PI * 2;
      const yb = (rnd() - 0.38) * 8.5;
      pos[i * 3] = Math.cos(a) * r * 1.05;
      pos[i * 3 + 1] = yb;
      pos[i * 3 + 2] = Math.sin(a) * r * 0.75 - 3.6;

      seed[i * 3] = rnd();
      seed[i * 3 + 1] = Math.pow(rnd(), 2.5);   // mostly fine particles, a few soft bokeh
      seed[i * 3 + 2] = 0.45 + rnd() * 0.9;
    }

    this.vao = gl.createVertexArray();
    gl.bindVertexArray(this.vao);
    const pb = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, pb);
    gl.bufferData(gl.ARRAY_BUFFER, pos, gl.STATIC_DRAW);
    gl.enableVertexAttribArray(0);
    gl.vertexAttribPointer(0, 3, gl.FLOAT, false, 0, 0);

    const sb = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, sb);
    gl.bufferData(gl.ARRAY_BUFFER, seed, gl.STATIC_DRAW);
    gl.enableVertexAttribArray(1);
    gl.vertexAttribPointer(1, 3, gl.FLOAT, false, 0, 0);
    gl.bindVertexArray(null);
  }

  draw(n = this.count) {
    const gl = this.gl;
    gl.bindVertexArray(this.vao);
    gl.drawArrays(gl.POINTS, 0, Math.min(n, this.count));
    gl.bindVertexArray(null);
  }
}

// Unnecessary empty decorative cubes removed to keep all 11 skill logos completely unobstructed, bright and clear.
const DEBRIS_LAYOUT = [];

export function buildDebris() {
  return [];
}

// WebGL shaders for the 3D cinematic Experience environment.
// Red & Black palette, volumetric atmospheric lighting, 3D perspective grid,
// floating technological energy core, and floating 3D embers.

export const V_EXP_ENV = `#version 300 es
precision highp float;
layout(location=0) in vec2 aPos;
out vec2 vUV;
void main(){
  vUV = vec2(aPos.x, 1.0 - aPos.y);
  gl_Position = vec4(aPos * 2.0 - 1.0, 0.0, 1.0);
}`;

export const F_EXP_ENV = `#version 300 es
precision highp float;
in vec2 vUV;
uniform vec2  uRes;
uniform float uTime;
uniform float uAspect;
uniform vec2  uPointer;
uniform float uActive;
out vec4 frag;

void main(){
  vec2 p = vUV;
  vec2 center = vec2(0.5, 0.48) + uPointer * 0.04;
  vec2 d = (p - center) * vec2(uAspect, 1.0);
  float r = length(d);

  // Atmospheric deep dark void
  vec3 col = vec3(0.016, 0.008, 0.012);

  // Volumetric crimson & ember-red core glow
  float coreBloom = exp(-r * r * 4.5);
  col += vec3(0.32, 0.045, 0.035) * coreBloom * (0.4 + 0.6 * uActive);

  // Secondary pulsating cyber bloom
  float pulse = 0.5 + 0.5 * sin(uTime * 1.4);
  col += vec3(0.45, 0.08, 0.05) * exp(-r * r * 14.0) * (0.3 + 0.3 * pulse);

  // Subtle digital horizon line
  float horizon = 0.62 + uPointer.y * 0.03;
  if(p.y > horizon){
    float f = (p.y - horizon) / max(1.0 - horizon, 0.001);
    // Perspective floor lines
    float z = 1.0 / max(f, 0.02);
    float gridX = abs(fract((p.x - 0.5 - uPointer.x * 0.05) * z * 8.0) - 0.5);
    float gridZ = abs(fract(z * 1.5 - uTime * 0.4) - 0.5);
    float gridLine = smoothstep(0.46, 0.50, max(gridX, gridZ));

    // Wet reflective sheen
    float sheen = exp(-abs(p.x - center.x) * uAspect * 3.2) * (1.0 - f * 0.6);
    col += vec3(0.18, 0.024, 0.022) * sheen * (0.35 + 0.65 * uActive);
    col += vec3(0.35, 0.05, 0.04) * gridLine * (1.0 - f * 0.8) * 0.28;
  }

  // Vignette
  vec2 v = (p - 0.5) * vec2(uAspect, 1.0);
  col *= 1.0 - smoothstep(0.40, 1.15, length(v)) * 0.85;

  frag = vec4(col, 1.0);
}`;

export const F_EXP_CORE = `#version 300 es
precision highp float;
in vec2 vUV;
uniform vec2  uRes;
uniform float uTime;
uniform float uAspect;
uniform vec2  uPointer;
uniform float uHover;
out vec4 frag;

// Concentric rotating architectural cyber-energy arcs
float cyberArc(vec2 d, float R, float w, float speed, float coverage){
  float r = length(d);
  float band = smoothstep(w, 0.0, abs(r - R));
  float angle = atan(d.y, d.x) + uTime * speed;
  float s = 0.5 + 0.5 * sin(angle * 3.0);
  float gate = smoothstep(1.0 - coverage - 0.1, 1.0 - coverage + 0.1, s);
  return band * mix(0.15, 1.0, gate);
}

void main(){
  vec2 center = vec2(0.68, 0.46) + uPointer * 0.06;
  vec2 d = (vUV - center) * vec2(uAspect, 1.0);
  float r = length(d);

  float energy = 0.0;
  // Multiple concentric rotating holographic rings representing corporate technology core
  energy += cyberArc(d, 0.14, 0.0035, 0.32, 0.65) * 0.95;
  energy += cyberArc(d, 0.20, 0.0028, -0.24, 0.55) * 0.75;
  energy += cyberArc(d, 0.27, 0.0022, 0.18, 0.45) * 0.55;
  energy += cyberArc(d, 0.34, 0.0016, -0.12, 0.35) * 0.40;

  // Central glowing nexus
  energy += exp(-r * r * 38.0) * 0.35;
  energy += exp(-r * r * 12.0) * 0.18;

  // Interactive hover flare
  energy *= (1.0 + uHover * 0.45);

  vec3 col = vec3(1.0, 0.18, 0.14) * energy;
  col += vec3(1.0, 0.82, 0.75) * pow(max(energy - 0.65, 0.0), 2.0) * 1.8;

  float alpha = clamp(energy * 1.4, 0.0, 1.0);
  frag = vec4(col, alpha);
}`;

export const V_EXP_PARTICLES = `#version 300 es
precision highp float;
layout(location=0) in vec3 aPos;
layout(location=1) in vec2 aData; // x: phase, y: scale
uniform mat4  uMVP;
uniform float uTime;
uniform vec2  uPointer;
out float vAlpha;
out float vGlow;

void main(){
  vec3 p = aPos;
  // Dynamic floating movement in 3D space
  float t = uTime * 0.6 + aData.x;
  p.y += sin(t * 1.4) * 0.18 + cos(t * 0.8) * 0.08;
  p.x += cos(t * 0.9) * 0.14 + uPointer.x * 0.35;
  p.z += sin(t * 0.7) * 0.16 + uPointer.y * 0.25;

  gl_Position = uMVP * vec4(p, 1.0);
  float size = (aData.y * 3.8 + 2.0) * (3.5 / max(gl_Position.w, 0.6));
  gl_PointSize = clamp(size, 2.0, 32.0);

  vAlpha = smoothstep(0.1, 0.5, aData.y) * (0.4 + 0.6 * sin(t * 2.0));
  vGlow = aData.y;
}`;

export const F_EXP_PARTICLES = `#version 300 es
precision highp float;
in float vAlpha;
in float vGlow;
out vec4 frag;

void main(){
  vec2 d = gl_PointCoord - 0.5;
  float r2 = dot(d, d);
  if(r2 > 0.25) discard;

  float core = smoothstep(0.25, 0.0, r2);
  float halo = exp(-r2 * 9.0);

  vec3 col = mix(vec3(1.0, 0.22, 0.16), vec3(1.0, 0.88, 0.82), core * 0.8);
  float a = (core * 0.7 + halo * 0.3) * vAlpha;
  frag = vec4(col * a, a);
}`;

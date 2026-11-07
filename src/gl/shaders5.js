// Scene five — the certifications environment.
// Stages the cyan/ice-blue atmospheric room, floor sheen, and breathing fog.

export const V5 = `#version 300 es
layout(location=0) in vec2 aPos;
out vec2 vUV;
void main(){
  vUV = vec2(aPos.x, 1.0 - aPos.y);
  gl_Position = vec4(aPos * 2.0 - 1.0, 0.0, 1.0);
}`;

export const F5_ROOM = `#version 300 es
precision highp float;
in vec2 vUV;
uniform sampler2D uPlate;
uniform sampler2D uGrain;
uniform vec4  uCover;    // xy scale, zw offset: viewport uv -> plate uv
uniform float uTime;
uniform float uAspect;
uniform float uWake;     // global exposure 0..1
uniform float uGlow;     // cyan atmospheric mist pulse
uniform float uFloorL;   // wet floor reflection intensity
uniform vec2  uPar;      // pointer parallax, -1..1
uniform float uDolly;    // scroll push-in 0..1
out vec4 frag;

void main(){
  vec2 uv = vUV;
  uv = (uv - 0.5) * (1.0 - 0.032 * uDolly) + 0.5;
  uv += vec2(-uPar.x * 0.007, -uPar.y * 0.005);
  vec2 p = uv * uCover.xy + uCover.zw;
  p = clamp(p, 0.001, 0.999);

  vec3 base = texture(uPlate, p).rgb;

  // Wet floor reflection enhancement below horizon
  float horizon = 0.65;
  float floorSheen = smoothstep(horizon - 0.05, horizon + 0.25, p.y);
  float wetGlint = exp(-abs(p.x - 0.5) * 4.2) * floorSheen;

  // Volumetric crimson/amber atmospheric haze breathing
  float mistBreath = sin(uTime * 0.6 + p.x * 2.5) * 0.5 + 0.5;
  vec3 redMist = vec3(0.22, 0.024, 0.028) * exp(-length(p - vec2(0.5, 0.42)) * 2.4) * (0.8 + 0.2 * mistBreath) * uGlow;

  vec3 col = base * (0.15 + 0.85 * uWake);
  col += redMist * uWake;
  col += vec3(0.36, 0.05, 0.04) * wetGlint * 0.22 * uFloorL * uWake;

  // Post grain
  float g = texture(uGrain, p * (1280.0 / 512.0) + vec2(uTime * 0.008, 0.0)).r;
  col += (g - 0.5) * 0.024;

  // Vignette
  vec2 v = (vUV - 0.5) * vec2(uAspect, 1.0);
  float vig = smoothstep(0.48, 1.15, length(v));
  col *= 1.0 - vig * 0.45;

  frag = vec4(col, 1.0);
}`;

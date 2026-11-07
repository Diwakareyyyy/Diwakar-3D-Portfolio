// Scene four - the project universe. One environment pass over the extracted
// reference plate, plus the shared grain/vignette post from scene three.
//
// The plate IS the reference (cards, person and captions lifted out), so this
// shader's job is not to paint the room but to LIGHT it: stage the blackout,
// wake the overhead structure, ignite the floor circle, breathe life into the
// baked reflections, and drift everything a few pixels with the pointer so
// the photograph stops being a photograph.

export const V4 = `#version 300 es
layout(location=0) in vec2 aPos;
out vec2 vUV;
void main(){
  // y-DOWN to match CSS-normalised coordinates, same convention as scene 3
  vUV = vec2(aPos.x, 1.0 - aPos.y);
  gl_Position = vec4(aPos * 2.0 - 1.0, 0.0, 1.0);
}`;

export const F4_ROOM = `#version 300 es
precision highp float;
in vec2 vUV;
uniform sampler2D uPlate;
uniform sampler2D uGrain;
uniform vec4  uCover;    // xy scale, zw offset: viewport uv -> plate uv
uniform float uTime;
uniform float uAspect;
uniform float uWake;     // global exposure 0..1
uniform float uRing;     // overhead structure light
uniform float uFloorL;   // floor circle light
uniform float uSpark;    // ignition sweep 0..1 around the circle
uniform float uPerson;   // his arrival warms the centre glow
uniform vec2  uPar;      // pointer parallax, -1..1
uniform float uDolly;    // scroll push-in 0..1
uniform vec4  uEllA;     // outer floor ellipse, frame fractions (cx cy rx ry)
uniform vec4  uEllB;     // inner floor ellipse
uniform vec4  uRingE;    // overhead ring ellipse
out vec4 frag;

float ellDist(vec2 p, vec4 e){
  vec2 d = (p - e.xy) / e.zw;
  return length(d);
}

void main(){
  // parallax + dolly live in plate space: the room drifts against the cards
  // and eases toward the camera as the visitor scrolls
  vec2 uv = vUV;
  uv += vec2(-uPar.x * 0.004, -uPar.y * 0.003);
  vec2 p = uv * uCover.xy + uCover.zw;      // frame fractions 0..1
  p = clamp(p, 0.001, 0.999);

  vec3 base = texture(uPlate, p).rgb;

  // ---- staged lighting ----------------------------------------------------
  // the room is never fully dark - an ember floor - and reaches full only
  // when the deck has assembled
  float zone = 1.0;
  // overhead structure: everything above the horizon band answers to uRing
  float top = smoothstep(0.42, 0.12, p.y);
  zone = mix(zone, uRing, top);
  // floor: everything below answers to uFloorL
  float low = smoothstep(0.55, 0.78, p.y);
  zone = mix(zone, uFloorL, low);
  vec3 col = base * (0.05 + 0.95 * zone * uWake);

  // ---- the floor circle, live ---------------------------------------------
  // additive glints riding exactly on the baked ellipses; during ignition a
  // hot spark sweeps the ring and leaves it lit behind itself
  float aA = atan((p.y - uEllA.y) / uEllA.w, (p.x - uEllA.x) / uEllA.z);
  float sweep = uSpark * 6.9 - 3.45;        // -pi..pi as the spark travels
  float litA = smoothstep(0.06, -0.4, aA - sweep) + step(6.85, uSpark * 6.9);
  float dA = abs(ellDist(p, uEllA) - 1.0);
  float lineA = exp(-dA * dA * 2600.0);
  float dB = abs(ellDist(p, uEllB) - 1.0);
  float lineB = exp(-dB * dB * 2200.0);
  // whisper-level: the plate already carries the lit lines, these breathe in red & ember
  float breathe = 0.90 + 0.10 * sin(uTime * 0.8 + p.x * 4.0);
  // Red & crimson neon cyber-ring floor reflections
  col += vec3(1.0, 0.26, 0.16) * lineA * 0.22 * uFloorL * min(litA, 1.0) * breathe;
  col += vec3(1.0, 0.20, 0.12) * lineB * 0.14 * uFloorL * breathe;
  // the spark head itself - hot crimson pulse
  vec2 head = uEllA.xy + vec2(cos(sweep) * uEllA.z, sin(sweep) * uEllA.w);
  vec2 hd = (p - head) * vec2(uAspect, 1.0);
  col += vec3(1.0, 0.35, 0.22) * exp(-dot(hd, hd) * 2400.0)
       * uFloorL * (1.0 - step(0.999, uSpark)) * 1.05;

  // ---- the overhead ring, live: radiant crimson halo ---------------------
  float dR = abs(ellDist(p, uRingE) - 1.0);
  float rim = exp(-dR * dR * 900.0) * smoothstep(0.02, 0.10, p.y);
  col += vec3(1.0, 0.28, 0.20) * rim * 0.15 * uRing
       * (0.75 + 0.25 * sin(uTime * 0.6 + p.x * 9.0));

  // ---- centre glow: ambient red stage light around the workstation --------
  vec2 g = (p - vec2(0.499, 0.70)) * vec2(uAspect * 0.62, 4.4);
  float pool = exp(-dot(g, g) * 5.5);
  col += vec3(1.0, 0.24, 0.15) * pool * 0.09 * (0.35 + 0.65 * uPerson) * uFloorL;

  // Subtle radial ambient crimson depth centered along the horizon
  float ambGlow = exp(-length((p - vec2(0.5, 0.54)) * vec2(uAspect * 0.7, 2.2)) * 3.4);
  col += vec3(0.70, 0.08, 0.06) * ambGlow * 0.14 * uWake;

  // ---- wet-floor shimmer --------------------------------------------------
  // the baked reflections already streak the tiles; a slow-scrolling grain
  // multiplied over the bright parts makes the water feel live
  float wet = smoothstep(0.62, 0.9, p.y) * smoothstep(0.35, 0.12, abs(p.x - 0.5) - 0.18);
  float g1 = texture(uGrain, p * vec2(3.0, 1.2) + vec2(0.0, uTime * 0.015)).r;
  float lum = dot(base, vec3(0.35, 0.45, 0.2));
  col += base * (g1 - 0.5) * wet * smoothstep(0.05, 0.35, lum) * 0.38 * uFloorL;

  frag = vec4(col, 1.0);
}`;

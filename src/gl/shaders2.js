// GLSL for the creative-universe scene (True 3D Volumetric Rounded Box Edition).

// --------------------------------------------------------------------------
// Environment: deep black room, atmospheric crimson backlight behind the core,
// architectural dark floor with wet red & blue reflections and dual-leg shadows.
// --------------------------------------------------------------------------
export const V2_FULL = `#version 300 es
precision highp float;
layout(location=0) in vec2 aPos;
out vec2 vUV;
void main(){
  vUV = vec2(aPos.x, 1.0 - aPos.y);
  gl_Position = vec4(aPos * 2.0 - 1.0, 0.0, 1.0);
}`;

export const F2_ENV = `#version 300 es
precision highp float;
in vec2 vUV;
uniform sampler2D uGrain;
uniform vec2  uRes;
uniform float uTime;
uniform float uAspect;
uniform float uWake;
uniform float uBurst;
uniform vec2  uCore;      // where the ring sits, normalised
uniform vec3  uStroke;    // xy: the light-painting head on screen, z: strength
uniform vec3  uFigFeet;   // xy: projected character feet center in vUV, z: half foot span in dx units
out vec4 frag;

void main(){
  vec2 p = vUV;
  vec2 d = (p - uCore) * vec2(uAspect, 1.0);
  float r = length(d);

  // Deep cinema black base
  vec3 col = vec3(0.007, 0.006, 0.009);

  // Tight crimson-red atmospheric backlight behind the central character
  float bloom = exp(-r * r * 6.5);
  float wideHalo = exp(-r * r * 2.2);
  col += vec3(0.115, 0.012, 0.014) * bloom * (0.25 + 0.75 * uWake);
  col += vec3(0.038, 0.004, 0.006) * wideHalo * uWake;
  col += vec3(0.22, 0.030, 0.035) * exp(-r * r * 16.0) * uBurst * 0.22;

  // Warm wall blush around the moving amber energy ribbon head
  vec2 hd = (p - uStroke.xy) * vec2(uAspect, 1.0);
  col += vec3(0.20, 0.075, 0.018) * exp(-dot(hd, hd) * 18.0) * uStroke.z;

  // Floor: wet reflective dark architectural tiles aligned with the character's stance
  float feetY = uFigFeet.y > 0.1 ? uFigFeet.y : 0.888;
  float feetX = uFigFeet.y > 0.1 ? uFigFeet.x : uCore.x;
  float footSpan = uFigFeet.z > 0.005 ? uFigFeet.z : 0.074;
  float horizon = feetY - 0.075;

  if(p.y > horizon){
    float f = clamp((p.y - horizon) / max(1.0 - horizon, 1e-3), 0.0, 1.0);
    float dx = (p.x - feetX) * uAspect;

    // Perspective tile / plank grid on the floor
    float perspX = dx / (0.22 + f * 0.82);
    float tileX = smoothstep(0.96, 1.0, abs(sin(perspX * 22.0)));
    float tileY = smoothstep(0.94, 1.0, abs(sin(pow(f, 0.55) * 28.0)));
    float texG = texture(uGrain, vec2(perspX * 1.4, f * 3.5)).r;
    float roughness = 0.75 + 0.25 * texG;

    // Smooth horizon blend so the floor never starts on a harsh horizontal line
    float floorFadeIn = smoothstep(0.0, 0.18, f);

    // Central crimson-red wet reflection from the core & backlight
    float centerSheen = exp(-dx * dx * 7.5) * (1.0 - f * 0.35);
    float wideRedSheen = exp(-dx * dx * 2.0) * (1.0 - f * 0.52);
    vec3 floorLight = (vec3(0.29, 0.030, 0.026) * centerSheen
                     + vec3(0.11, 0.013, 0.014) * wideRedSheen) * roughness * floorFadeIn;

    // Subtle secondary floor reflections under left and right block wings
    float leftWing = exp(-pow(dx + 0.42, 2.0) * 12.0) * smoothstep(0.05, 0.38, f) * (1.0 - f * 0.48);
    float rightBlue = exp(-pow(dx - 0.36, 2.0) * 16.0) * smoothstep(0.08, 0.45, f) * (1.0 - f * 0.42);
    float rightRed  = exp(-pow(dx - 0.56, 2.0) * 12.0) * smoothstep(0.05, 0.38, f) * (1.0 - f * 0.48);
    floorLight += vec3(0.20, 0.025, 0.020) * leftWing * roughness;
    floorLight += vec3(0.016, 0.044, 0.13) * rightBlue * roughness;
    floorLight += vec3(0.15, 0.018, 0.016) * rightRed * roughness;

    // ---- Realistic Ground Contact & Perspective Cast Shadow ----
    // Exact shoe contact coordinates in (dx, dy) around the character's two feet
    float dyFeet = p.y - feetY;
    float dxL = dx + footSpan;
    float dxR = dx - footSpan * 0.96;

    // 1. Tight soft elliptical contact occlusion directly under left & right soles
    float soleL = exp(-(dxL * dxL) / 0.00052 - (dyFeet * dyFeet) / 0.000055);
    float soleR = exp(-(dxR * dxR) / 0.00052 - (dyFeet * dyFeet) / 0.000055);

    // 2. Soft grounding ambient-occlusion ellipse bridging the stance between both feet
    float stanceW = footSpan * 1.48;
    float stanceAO = exp(-(dx * dx) / (stanceW * stanceW) - ((dyFeet - 0.003) * (dyFeet - 0.003)) / 0.00032);

    // 3. Forward perspective cast shadows from the rear core light past both legs
    float fwd = max(dyFeet, 0.0);
    float fwdGate = smoothstep(-0.004, 0.010, dyFeet) * exp(-fwd * 14.5);
    // Perspective ray divergence outward as shadow travels toward camera
    float rayL = dxL + fwd * 0.24;
    float rayR = dxR - fwd * 0.23;
    float penumbra = 0.00045 + fwd * 0.012;
    float castL = exp(-(rayL * rayL) / penumbra) * fwdGate;
    float castR = exp(-(rayR * rayR) / penumbra) * fwdGate;

    float totalShadow = clamp(
      max(soleL, soleR) * 0.88 + stanceAO * 0.56 + (castL + castR) * 0.62,
      0.0, 0.94
    );
    float shadowMask = 1.0 - totalShadow;

    // Subtle crimson environmental light grazing the outer penumbra of the grounded feet
    float rimPenumbra = clamp((stanceAO * 0.8 + (castL + castR) * 0.6) * (1.0 - totalShadow * 0.85), 0.0, 1.0);
    floorLight += vec3(0.18, 0.018, 0.016) * rimPenumbra * roughness * floorFadeIn;

    col += floorLight * shadowMask * (0.3 + 0.7 * uWake);

    // Subtle dark tile seam lines catching the red reflection outside the deep contact shadow
    col += vec3(0.08, 0.012, 0.012) * (tileX * 0.6 + tileY * 0.4) * (1.0 - f * 0.7) * shadowMask * floorFadeIn * 0.32 * uWake;
    col *= mix(1.0, 0.50, totalShadow * 0.85);
    col *= mix(1.0, 0.48, f * 0.62);
  }

  float g = texture(uGrain, p * (uRes / 512.0) * 0.55 + vec2(uTime * 0.003, 0.0)).r;
  col += (g - 0.5) * 0.022;

  vec2 v = (p - 0.5) * vec2(uAspect, 1.0);
  col *= 1.0 - smoothstep(0.45, 1.22, length(v)) * 0.90;

  frag = vec4(col, 1.0);
}`;

// --------------------------------------------------------------------------
// The core ring: concentric crimson-red energy arcs behind the character.
// --------------------------------------------------------------------------
export const F2_RING = `#version 300 es
precision highp float;
in vec2 vUV;
uniform vec2  uRes;
uniform float uTime;
uniform float uAspect;
uniform float uLife;
uniform float uBurst;
uniform vec2  uCore;
uniform float uScale;
out vec4 frag;

float arc(vec2 d, float R, float w, float spin, float coverage){
  float r = length(d);
  float band = smoothstep(w, 0.0, abs(r - R));
  float a = atan(d.y, d.x) + spin;
  float s = 0.5 + 0.5 * sin(a);
  float gate = smoothstep(1.0 - coverage - 0.12, 1.0 - coverage + 0.12, s);
  return band * mix(0.22, 1.0, gate);
}

void main(){
  vec2 d = (vUV - uCore) * vec2(uAspect, 1.0) / max(uScale, 1e-3);
  float t = uTime;
  float pulse = 0.86 + 0.14 * sin(t * 0.85);
  float r = length(d);

  float e = 0.0;
  // Crisp concentric crimson rings matching IMAGE 2's portal behind the character
  e += arc(d, 0.148, 0.0026,  t * 0.24, 0.68) * 0.72;
  e += arc(d, 0.162, 0.0016, -t * 0.18, 0.55) * 0.45;
  e += arc(d, 0.205, 0.0020, -t * 0.15, 0.52) * 0.42;
  e += arc(d, 0.258, 0.0015,  t * 0.11, 0.38) * 0.26;
  e += arc(d, 0.315, 0.0012, -t * 0.08, 0.28) * 0.16;

  // Soft ring bloom along the main 0.155 radius band
  e += exp(-pow((r - 0.155) / 0.032, 2.0)) * 0.18;
  // Subtle inner crimson glow
  e += exp(-r * r * 38.0) * 0.14;

  e *= pulse * uLife;
  e += uBurst * exp(-r * r * 26.0) * 0.22;

  vec3 col = vec3(1.0, 0.12, 0.10) * e;
  col += vec3(1.0, 0.65, 0.55) * pow(max(e - 0.65, 0.0), 2.0) * 1.35;
  frag = vec4(col, 1.0);
}`;

// --------------------------------------------------------------------------
// True 3D Volumetric Rounded Box Vertex Shader (used by both Skill Blocks and Debris Cubes)
// --------------------------------------------------------------------------
export const V2_CARD = `#version 300 es
precision highp float;
layout(location=0) in vec3 aPos;
uniform mat4 uMVP;
uniform vec3 uBoxHalf;
uniform float uGlowPad;     // extra proxy room for the hover glow / click ripple
out vec3 vLocalPos;
out float vDepth;
void main(){
  // Slightly pad bounding box so analytical silhouette AA is never clipped
  vLocalPos = aPos * (uBoxHalf * 1.04 + vec3(uGlowPad));
  vec4 clip = uMVP * vec4(vLocalPos, 1.0);
  vDepth = clip.w;
  gl_Position = clip;
}`;

// --------------------------------------------------------------------------
// True 3D Volumetric Skill Block Fragment Shader (F2_CARD)
// Casts a 3D perspective ray from the camera through the oriented 3D bounding box
// to intersect an exact 3D rounded/beveled block (sdRoundBox).
// Renders:
//   - Front face with crisp official logo + skill name
//   - Thick 3D side wall & top/bottom wall in true perspective
//   - Gleaming front bevel highlight separating front face from side/bottom walls
//   - Fiery crimson-red neon back/outer bevel edge & soft red side-wall spill (IMAGE 2)
//   - Realistic underside ambient occlusion & hover illumination
// --------------------------------------------------------------------------
export const F2_CARD = `#version 300 es
precision highp float;
in vec3 vLocalPos;
in float vDepth;

uniform sampler2D uLogo;
uniform sampler2D uGrain;
uniform vec3  uBoxHalf;     // (halfW, halfH, halfD) in isometric world units
uniform float uBevel;       // 3D bevel radius in world units
uniform vec3  uCamLocal;    // camera position in block's local space
uniform vec3  uLightLocal;  // central red core light position in block's local space
uniform vec3  uUpLocal;     // world up (0,1,0) in block's local space
uniform vec2  uLogoScale;   // logo scale on front face
uniform float uOpacity;
uniform float uMat;         // materialisation 0..1
uniform float uHover;
uniform float uTime;
uniform float uPulse;       // click flash 1 -> 0
uniform float uRipple;      // click ripple phase 0 -> 1 (1 = idle)
uniform float uGlowPad;
uniform vec3  uRibbonLocal; // the energy ribbon's hot head, in block space
uniform float uRibbonAmt;   // how close that head is (0..1)
out vec4 frag;

float sdBox(vec3 p, vec3 bi, float r){
  vec3 q = abs(p) - bi;
  return length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0) - r;
}

// Hover aura + click energy ripple around the block, emitted additively
// (alpha 0 under premultiplied blending), so it lights the room behind.
vec3 aura(vec3 ro, vec3 rd, vec3 bInner){
  float amt = uHover * 0.55 + uPulse * 1.1;
  float rip = (1.0 - uRipple);
  if(amt + rip < 0.002) return vec3(0.0);
  float tc = max(dot(-ro, rd), 0.0);
  float d = max(sdBox(ro + rd * tc, bInner, uBevel), 0.0);
  float w = max(uGlowPad, 1e-3);
  float glow = exp(-d / (w * 0.28)) * amt;
  float R = uRipple * w * 0.95;
  float ring = exp(-pow((d - R) / (w * 0.07), 2.0)) * rip * rip * 1.4;
  vec3 warm = vec3(1.0, 0.30, 0.10);
  return warm * glow * 0.55 + vec3(1.0, 0.62, 0.30) * ring;
}

void main(){
  vec3 ro = uCamLocal;
  vec3 rd = normalize(vLocalPos - uCamLocal);
  vec3 bInner = max(uBoxHalf - uBevel, vec3(0.001));

  // 1. Exact ray-AABB intersection with [-uBoxHalf, uBoxHalf]
  vec3 invR = 1.0 / (rd + sign(rd + 1e-6) * 1e-6);
  vec3 tbot = invR * (-uBoxHalf - ro);
  vec3 ttop = invR * ( uBoxHalf - ro);
  vec3 tmin = min(ttop, tbot);
  vec3 tmax = max(ttop, tbot);
  float t0 = max(max(tmin.x, tmin.y), max(tmin.z, 0.0));
  float t1 = min(min(tmax.x, tmax.y), tmax.z);
  if(t0 > t1){
    vec3 g = aura(ro, rd, bInner) * uOpacity;
    if(dot(g, vec3(1.0)) < 0.002) discard;
    frag = vec4(g, 0.0);
    return;
  }

  // 2. High-precision 3D beveled panel intersection inside AABB
  float t = t0;
  float minD = 1e5;
  float bestT = t0;
  for(int i = 0; i < 30; i++){
    vec3 p = ro + rd * t;
    vec3 q = abs(p) - bInner;
    float d = length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0) - uBevel;
    if(d < minD){
      minD = d;
      bestT = t;
    }
    if(d < 0.00015 || t > t1) break;
    t += max(d * 0.85, 0.0004);
  }

  // Crisp analytical anti-aliased 3D silhouette edge
  float aa = max(fwidth(minD) * 0.85, uBevel * 0.04);
  float edgeSoft = mix(uBevel * 0.35, aa, uMat);
  float faceAlpha = 1.0 - smoothstep(-edgeSoft * 0.4, edgeSoft * 0.8, minD);
  vec3 halo = aura(ro, rd, bInner) * uOpacity;
  if(faceAlpha <= 0.003){
    if(dot(halo, vec3(1.0)) < 0.002) discard;
    frag = vec4(halo, 0.0);
    return;
  }

  // 3. Exact 3D hit point & analytical chamfered-panel normal
  vec3 pos = ro + rd * min(bestT, t1);
  vec3 q = pos - clamp(pos, -bInner, bInner);
  vec3 N = normalize(q + 1e-6);
  vec3 V = -rd;

  vec3 L_core = normalize(uLightLocal - pos);
  vec3 Up = normalize(uUpLocal);
  vec3 L_key = normalize(Up * 0.72 + V * 0.52 + L_core * 0.22);

  // Face weights
  float isFront  = smoothstep(0.65, 0.95, N.z);
  float isSideX  = smoothstep(0.40, 0.88, abs(N.x));
  float isBottom = clamp(dot(N, -Up), 0.0, 1.0);
  float isTop    = clamp(dot(N,  Up), 0.0, 1.0);

  // Normalized coordinates within panel [-1, 1]^3
  vec3 nPos = pos / max(uBoxHalf, vec3(1e-4));
  vec3 bEx = max(abs(pos) - bInner, 0.0) / max(uBevel, 1e-4);

  // --- A. Premium Dark Black Glass & Anodized Metallic Material (Reference Image 2) ---
  // Front face: deep black glass-like obsidian (#07070a .. #111117) with controlled diagonal studio reflection
  vec3 frontCol = vec3(0.030, 0.030, 0.038);
  frontCol *= 1.0 - 0.28 * (0.5 - nPos.y * 0.5);
  // Subtle diagonal dark-glass specular sheen across the upper-left / top half
  float glassDiag = clamp(0.52 - nPos.x * 0.30 + nPos.y * 0.36, 0.0, 1.0);
  frontCol += vec3(0.026, 0.025, 0.034) * pow(glassDiag, 1.6);
  // Crisp, soft glass reflection band across the top edge of the front face
  float topGlassSheen = exp(-pow((nPos.y - 0.72) * 3.2, 2.0)) * (0.6 + 0.4 * (1.0 - abs(nPos.x)));
  frontCol += vec3(0.022, 0.023, 0.030) * topGlassSheen;

  // Precision thin dark-metallic inner bezel line framing the front panel face
  vec2 edgeDist2D = abs(nPos.xy);
  float innerBezel = smoothstep(0.915, 0.945, max(edgeDist2D.x, edgeDist2D.y))
                   * (1.0 - smoothstep(0.955, 0.985, max(edgeDist2D.x, edgeDist2D.y)));
  frontCol += vec3(0.032, 0.034, 0.044) * innerBezel * (0.5 + 0.5 * glassDiag);

  // Side wall: slim 3D anodized black-metallic extruded side face with depth gradient from front (+z) to back (-z)
  float depthShade = 0.48 + 0.52 * (nPos.z * 0.5 + 0.5);
  vec3 sideCol = vec3(0.014, 0.013, 0.018) * depthShade;
  // Top wall catches controlled overhead studio highlight; Bottom underside wall has deep shadow + AO
  vec3 topCol  = vec3(0.028, 0.027, 0.036) * depthShade;
  vec3 botCol  = vec3(0.005, 0.004, 0.007) * (0.60 + 0.40 * depthShade);

  vec3 col = mix(sideCol, topCol, isTop * 0.78);
  col = mix(col, botCol, isBottom * 0.88);
  col = mix(col, frontCol, isFront);

  // --- B. Sharp Angular Chamfer Highlight (Separating Front Glass Face from 3D Extruded Walls) ---
  float frontBevel = smoothstep(0.06, 0.65, bEx.z)
                   * smoothstep(0.06, 0.65, max(bEx.x, bEx.y))
                   * step(0.0, pos.z);
  vec3 H_key  = normalize(L_key + V);
  vec3 H_core = normalize(L_core + V);
  float specKey  = pow(max(dot(N, H_key), 0.0), 28.0);
  float specCore = pow(max(dot(N, H_core), 0.0), 18.0);
  float fresnel  = pow(1.0 - clamp(dot(N, V), 0.0, 1.0), 3.0);

  // Crisp metallic/glass specular rim along the sharp front chamfer
  col += vec3(0.42, 0.45, 0.56) * frontBevel * (0.20 + 0.80 * specKey);
  col += vec3(0.98, 0.22, 0.14) * frontBevel * specCore * (0.50 + uHover * 0.70);

  // --- C. Subtle Red Rim Lighting Along the 3D Panel Edges & Controlled Side Reflection (Reference Image 2) ---
  float coreFacing = clamp(dot(N, L_core), 0.0, 1.0);
  float rimBoost = 0.92 + uHover * 1.15 + uPulse * 1.6;

  // Back/outer bevel edge on the 3D extruded side/top/bottom walls (z near -uBoxHalf.z)
  float backEdge = smoothstep(-bInner.z + uBevel * 0.90, -uBoxHalf.z + uBevel * 0.08, pos.z)
                 * smoothstep(0.92, 0.28, abs(N.z));
  float backLaser = smoothstep(-bInner.z + uBevel * 0.45, -uBoxHalf.z + uBevel * 0.02, pos.z)
                  * smoothstep(0.05, 0.55, max(bEx.x, bEx.y))
                  * step(pos.z, 0.0);
  // Controlled red reflection spilling across the visible 3D side wall from the rim-lit edge
  float sideSpill = smoothstep(bInner.z * 0.45, -uBoxHalf.z, pos.z)
                  * (1.0 - smoothstep(0.22, 0.80, abs(N.z)));

  vec3 crimson = vec3(1.0, 0.12, 0.07);
  vec3 hotRed  = vec3(1.0, 0.62, 0.46);

  // Controlled side-wall red metallic reflection
  col += crimson * sideSpill * (0.10 + 0.16 * coreFacing + 0.07 * isSideX) * rimBoost;
  // Crisp glowing crimson rim along the outer/back angular edge of the 3D panel
  col += crimson * backEdge * (0.82 + 0.38 * coreFacing) * rimBoost;
  col += hotRed  * pow(backLaser, 1.25) * 1.65 * rimBoost;

  // Sharp angular corner & side-chamfer red rim on core-facing edges
  float sideCorner = smoothstep(0.10, 0.70, bEx.x) * smoothstep(0.10, 0.70, bEx.y);
  col += crimson * sideCorner * (0.38 + 0.62 * coreFacing) * (1.0 - isFront) * 0.75 * rimBoost;
  col += crimson * fresnel * (0.16 + 0.58 * coreFacing) * (1.0 - isFront * 0.75) * rimBoost;

  // Subtle warm red bounce light on the dark bottom underside face
  col += vec3(0.12, 0.016, 0.012) * isBottom * (0.35 + 0.65 * coreFacing) * (1.0 - isFront);

  // Hover interior sheen on the front face
  float sheen = exp(-length(nPos.xy - L_core.xy * 0.45) * 1.45);
  col += vec3(0.08, 0.022, 0.018) * sheen * isFront * (0.35 + uHover * 0.85);

  // Warm amber light cast by the passing energy ribbon
  vec3 L_rib = normalize(uRibbonLocal - pos);
  float ribFacing = clamp(dot(N, L_rib), 0.0, 1.0);
  col += vec3(1.0, 0.55, 0.16) * uRibbonAmt * (0.10 * ribFacing + 0.55 * fresnel * ribFacing
       + 0.45 * frontBevel * pow(max(dot(N, normalize(L_rib + V)), 0.0), 10.0));

  // Click flash: a quick bright wash across the bevels and face
  col += vec3(1.0, 0.36, 0.14) * uPulse * (0.10 * isFront + 0.60 * frontBevel + 0.35 * fresnel);

  // --- D. Official Skill Logo & Label on the Front Face ---
  if(pos.z > 0.0 && N.z > 0.55){
    float frontMask = smoothstep(0.55, 0.88, N.z);
    vec2 luv = (nPos.xy / uLogoScale) * 0.5 + 0.5;
    if(luv.x > 0.0 && luv.x < 1.0 && luv.y > 0.0 && luv.y < 1.0){
      // Contact drop-shadow under the logo & typography on the block face
      vec2 shUV = luv - vec2(0.008, -0.012);
      if(shUV.x > 0.0 && shUV.x < 1.0 && shUV.y > 0.0 && shUV.y < 1.0){
        float shA = texture(uLogo, vec2(shUV.x, 1.0 - shUV.y)).a;
        col *= 1.0 - shA * 0.45 * frontMask * uMat;
      }
      vec4 lg = texture(uLogo, vec2(luv.x, 1.0 - luv.y));
      // Crisp illumination & soft white highlight on logo/text
      vec3 lc = lg.rgb * (1.04 + uHover * 0.38 + uPulse * 0.30);
      col = mix(col, lc, lg.a * frontMask * mix(0.65, 1.0, uMat));
    }
  }

  // Micro surface grain
  float g = texture(uGrain, gl_FragCoord.xy / 512.0 + vec2(uTime * 0.01, 0.0)).r;
  col += (g - 0.5) * 0.020;

  // Subtle atmospheric depth haze for distant blocks
  float haze = clamp((vDepth - 4.2) / 11.0, 0.0, 0.42);
  col = mix(col, vec3(0.018, 0.006, 0.008), haze * (1.0 - uHover * 0.8));

  float a = faceAlpha * uOpacity;
  frag = vec4(col * a + halo * (1.0 - a), a);
}`;

// --------------------------------------------------------------------------
// The red energy ribbon: sleek, refined crimson laser filament (matching IMAGE 2).
// --------------------------------------------------------------------------
export const V2_RIBBON = `#version 300 es
precision highp float;
layout(location=0) in vec3 aPos;
layout(location=1) in vec2 aSide;   // x: -1..1 across, y: AGE along the trail
uniform mat4 uMVP;
out float vAcross;
out float vAge;
out float vZ;
out float vDepth;
void main(){
  vAcross = aSide.x;
  vAge = aSide.y;
  vZ = aPos.z;
  vec4 clip = uMVP * vec4(aPos, 1.0);
  vDepth = clip.w;
  gl_Position = clip;
}`;

export const F2_RIBBON = `#version 300 es
precision highp float;
in float vAcross;
in float vAge;
in float vZ;
in float vDepth;
uniform float uIntensity;
uniform float uTime;
uniform vec2  uZBand;
out vec4 frag;

void main(){
  if(vZ < uZBand.x || vZ >= uZBand.y) discard;

  float x = abs(vAcross);
  // Medium-thick light-painting stroke: white-hot core, yellow inner body,
  // soft orange outer illumination
  float core = exp(-x * x * 26.0);
  float innerGlow = exp(-x * x * 7.0);
  float outerGlow = exp(-x * x * 1.9);

  float heat = 1.0 - vAge;
  float fade = pow(heat, 1.15) * smoothstep(1.0, 0.90, vAge);

  // the stroke cools as it ages: yellow-white at the head, deep orange in the tail
  vec3 outerOrange = mix(vec3(1.00, 0.42, 0.06), vec3(0.95, 0.22, 0.04), vAge);
  vec3 innerYellow = mix(vec3(1.00, 0.80, 0.26), vec3(1.00, 0.52, 0.10), vAge);
  vec3 hotCore     = mix(vec3(1.00, 0.97, 0.82), vec3(1.00, 0.80, 0.45), vAge);

  // energy pulses travelling along the trail
  float flow = 0.80 + 0.20 * sin(vAge * 46.0 - uTime * 7.5)
             + 0.25 * pow(0.5 + 0.5 * sin(vAge * 9.0 - uTime * 3.2), 8.0);

  vec3 col = outerOrange * outerGlow * 0.80
           + innerYellow * innerGlow * 1.25
           + hotCore     * core * 1.70;

  float a = (outerGlow * 0.34 + innerGlow * 0.80 + core * 1.25)
          * fade * uIntensity * flow * 0.80;

  float headness = smoothstep(0.05, 0.0, vAge);
  a += (core * 1.2 + innerGlow * 0.4) * headness * uIntensity;
  a *= clamp(1.45 - vDepth * 0.028, 0.35, 1.0);
  frag = vec4(col * a, a);
}`;

// --------------------------------------------------------------------------
// Embers: glowing red & warm particles with depth-of-field bokeh.
// --------------------------------------------------------------------------
export const V2_SPARK = `#version 300 es
precision highp float;
layout(location=0) in vec3 aPos;
layout(location=1) in vec3 aSeed;
uniform mat4 uMVP;
uniform float uTime;
uniform float uConverge;
uniform float uLife;
uniform vec2 uPointer;
uniform vec3 uHead;
uniform float uRes;
out float vGlow;
out float vBlur;
void main(){
  vec3 p = aPos;
  float ph = aSeed.x * 6.283;
  p.x += sin(uTime * aSeed.z * 0.52 + ph) * 0.32 + uPointer.x * 0.25;
  p.y += cos(uTime * aSeed.z * 0.40 + ph * 1.7) * 0.26 - uPointer.y * 0.16;
  p.z += sin(uTime * aSeed.z * 0.30 + ph * 2.3) * 0.28;
  p *= mix(1.0, 0.42, uConverge);

  vec4 clip = uMVP * vec4(p, 1.0);
  gl_Position = clip;
  float near = clamp(3.0 / max(clip.w, 0.4), 0.15, 3.0);
  gl_PointSize = (2.2 + aSeed.y * 26.0) * near * (uRes / 900.0);
  vBlur = clamp(near * 0.42, 0.12, 1.0);

  float wave = 0.5 + 0.5 * sin(p.x * 0.42 + p.z * 0.30 - uTime * 0.42 + ph * 0.3);
  float boost = 0.25 + 1.40 * wave * wave * wave;

  float d = length(p - uHead);
  boost += 1.4 * exp(-d * d * 0.55);

  vGlow = uLife * (0.20 + aSeed.y * 0.80) * clamp(near, 0.2, 1.5) * boost;
}`;

export const F2_SPARK = `#version 300 es
precision highp float;
in float vGlow;
in float vBlur;
out vec4 frag;
void main(){
  vec2 c = gl_PointCoord - 0.5;
  float r = length(c) * 2.0;
  float core = exp(-r * r / max(vBlur * 0.52, 0.05));
  float halo = exp(-r * r * 2.2);
  float a = (core * 0.85 + halo * 0.32) * vGlow;
  if(a <= 0.003) discard;
  vec3 col = mix(vec3(1.0, 0.22, 0.14), vec3(1.0, 0.78, 0.64), core);
  frag = vec4(col * a, a);
}`;

// --------------------------------------------------------------------------
// Central Human Silhouette (F2_FIGURE):
// Deep silhouette with natural crimson-red rim light wrapping both shoulders,
// head/hair contour, sleeves, and inner leg edges from the central core behind him.
// --------------------------------------------------------------------------
export const V2_QUAD3D = `#version 300 es
precision highp float;
layout(location=0) in vec2 aPos;
uniform mat4 uMVP;
uniform vec2 uHalf;
out vec2 vP;
out float vDepth;
void main(){
  vP = aPos * 2.0 - 1.0;
  vec4 clip = uMVP * vec4(vP * uHalf, 0.0, 1.0);
  vDepth = clip.w;
  gl_Position = clip;
}`;

export const F2_FIGURE = `#version 300 es
precision highp float;
in vec2 vP;
in float vDepth;
uniform sampler2D uFig;
uniform sampler2D uGrain;
uniform float uOpacity;
uniform float uRim;
uniform vec2  uLightDir;
uniform float uTime;
out vec4 frag;

void main(){
  vec2 uv = vP * 0.5 + 0.5;
  vec4 s = texture(uFig, vec2(uv.x, 1.0 - uv.y));
  float a = s.a;
  if(a <= 0.015) discard;

  // Deep silhouette with subtle suit fabric tone
  vec3 col = s.rgb;

  // Radial direction from the central ring core behind his upper torso (0.0, 0.22)
  vec2 fromCore = vP - vec2(0.0, 0.18);
  vec2 radDir = normalize(fromCore + vec2(0.0, 1e-4));

  // Sample alpha gradient at two radii for both crisp edge wire and soft shoulder wrap
  vec2 texel = vec2(1.35) / vec2(textureSize(uFig, 0));
  float ax = texture(uFig, vec2(uv.x + texel.x, 1.0 - uv.y)).a
           - texture(uFig, vec2(uv.x - texel.x, 1.0 - uv.y)).a;
  float ay = texture(uFig, vec2(uv.x, 1.0 - uv.y - texel.y)).a
           - texture(uFig, vec2(uv.x, 1.0 - uv.y + texel.y)).a;
  vec2 n = vec2(-ax, -ay);
  float edge = length(n);

  if(edge > 0.001){
    vec2 nDir = normalize(n);
    // Rim light from core behind shoulders & head, plus subtle floor red rim on lower legs
    float upperZone = smoothstep(-0.35, 0.55, vP.y);
    float lowerZone = 1.0 - smoothstep(-0.85, -0.15, vP.y);
    float outward = clamp(dot(nDir, radDir), 0.0, 1.0);
    float topBias = clamp(dot(nDir, vec2(0.0, 1.0)), 0.0, 1.0);

    float rimStrength = (0.45 + 0.55 * outward + 0.45 * topBias) * upperZone
                      + 0.45 * lowerZone;
    col += vec3(1.0, 0.18, 0.12) * edge * rimStrength * 1.0 * uRim;
    col += vec3(1.0, 0.55, 0.42) * pow(edge, 1.6) * topBias * upperZone * 1.4 * uRim;
  }

  // Soft ground contact occlusion at the very bottom of the shoes so feet sit naturally on the floor
  float soleContact = smoothstep(-0.985, -0.86, vP.y);
  col *= mix(0.28, 1.0, soleContact);

  float g = texture(uGrain, gl_FragCoord.xy / 512.0).r;
  col += (g - 0.5) * 0.016;

  float o = a * uOpacity;
  frag = vec4(col * o, o);
}`;

// --------------------------------------------------------------------------
// True 3D Floating Debris Cubes (F2_CUBE):
// Uses V2_CARD (3D cube VAO) and ray-casts a 3D beveled cube in perspective,
// shading 3 distinct 3D faces + a glowing crimson-red neon edge facing the core.
// --------------------------------------------------------------------------
export const F2_CUBE = `#version 300 es
precision highp float;
in vec3 vLocalPos;
in float vDepth;
uniform vec3  uBoxHalf;
uniform float uBevel;
uniform vec3  uCamLocal;
uniform vec3  uLightLocal;
uniform vec3  uUpLocal;
uniform float uOpacity;
out vec4 frag;

void main(){
  vec3 ro = uCamLocal;
  vec3 rd = normalize(vLocalPos - uCamLocal);

  vec3 invR = 1.0 / (rd + sign(rd + 1e-6) * 1e-6);
  vec3 tbot = invR * (-uBoxHalf - ro);
  vec3 ttop = invR * ( uBoxHalf - ro);
  vec3 tmin = min(ttop, tbot);
  vec3 tmax = max(ttop, tbot);
  float t0 = max(max(tmin.x, tmin.y), max(tmin.z, 0.0));
  float t1 = min(min(tmax.x, tmax.y), tmax.z);
  if(t0 > t1) discard;

  vec3 bInner = max(uBoxHalf - uBevel, vec3(0.001));
  float t = t0;
  float minD = 1e5;
  float bestT = t0;
  for(int i = 0; i < 22; i++){
    vec3 p = ro + rd * t;
    vec3 q = abs(p) - bInner;
    float d = length(max(q, 0.0)) + min(max(q.x, max(q.y, q.z)), 0.0) - uBevel;
    if(d < minD){
      minD = d;
      bestT = t;
    }
    if(d < 0.0002 || t > t1) break;
    t += max(d * 0.85, 0.0005);
  }

  float edgeSoft = max(fwidth(minD) * 0.85, uBevel * 0.05);
  float faceAlpha = 1.0 - smoothstep(-edgeSoft * 0.4, edgeSoft * 0.8, minD);
  if(faceAlpha <= 0.004) discard;

  vec3 pos = ro + rd * min(bestT, t1);
  vec3 q = pos - clamp(pos, -bInner, bInner);
  vec3 N = normalize(q + 1e-6);
  vec3 V = -rd;
  vec3 L_core = normalize(uLightLocal - pos);
  vec3 Up = normalize(uUpLocal);

  // 3 distinct face tones so the small cube clearly reads as 3D solid geometry
  float coreFace = clamp(dot(N, L_core), 0.0, 1.0);
  float upFace   = clamp(dot(N, Up), 0.0, 1.0);
  float downFace = clamp(dot(N, -Up), 0.0, 1.0);

  vec3 col = vec3(0.018, 0.017, 0.022);
  col += vec3(0.024, 0.022, 0.028) * upFace;
  col *= 1.0 - 0.55 * downFace;
  // Soft red reflection on the face turned toward the core
  col += vec3(0.11, 0.015, 0.012) * pow(coreFace, 1.5);

  // Bevel detection: where at least 2 axes exceed bInner
  vec3 bEx = max(abs(pos) - bInner, 0.0) / max(uBevel, 1e-4);
  float edgeBevel = smoothstep(0.05, 0.65, (bEx.x * bEx.y + bEx.y * bEx.z + bEx.z * bEx.x));

  // Razor-sharp glowing crimson-red edge on the bevel facing the core
  float redRim = edgeBevel * pow(clamp(dot(N, L_core) * 0.75 + 0.35, 0.0, 1.0), 1.6);
  col += vec3(1.0, 0.15, 0.09) * redRim * 1.35;
  col += vec3(1.0, 0.62, 0.48) * pow(redRim, 2.2) * 0.95;

  // Subtle specular highlight on top bevel
  col += vec3(0.28, 0.30, 0.38) * edgeBevel * upFace * 0.45;

  float a = faceAlpha * uOpacity;
  frag = vec4(col * a, a);
}`;

// --------------------------------------------------------------------------
export const F2_POST = `#version 300 es
precision highp float;
in vec2 vUV;
uniform sampler2D uGrain;
uniform vec2 uRes;
uniform float uTime;
uniform float uAmount;
uniform float uAspect;
out vec4 frag;
void main(){
  vec2 j = vec2(fract(sin(uTime * 12.9898) * 43758.5453),
                fract(sin(uTime * 78.233) * 12345.6789));
  float g = texture(uGrain, vUV * (uRes / 512.0) + j).r - 0.5;
  vec2 v = (vUV - 0.5) * vec2(uAspect, 1.0);
  float vig = smoothstep(0.46, 1.18, length(v));
  frag = vec4(vec3(g * uAmount), vig * 0.5);
}`;

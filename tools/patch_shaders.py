with open('src/gl/shaders.js', 'r', encoding='utf-8') as f:
    code = f.read()

target = '''  if(uPacked > 0.5){
    // colour occupies the left half, matte the right
    vec2 c = vec2(clamp(uv.x * 0.5, uTexel.x, 0.5 - uTexel.x), uv.y);
    vec3 col = texture(uClip, c).rgb;
    float a = texture(uClip, c + vec2(0.5, 0.0)).r;
    return vec4(col, a);
  } else {
    vec3 col = texture(uClip, uv).rgb;
    float maxC = max(col.r, max(col.g, col.b));
    float borderFade = smoothstep(0.0, 0.08, uv.x) * smoothstep(1.0, 0.92, uv.x);
    float a = smoothstep(0.038, 0.14, maxC) * borderFade;
    float centerDist = abs(uv.x - 0.5);
    if(centerDist < 0.28 && uv.y > 0.08 && uv.y < 0.94){
      a = max(a, smoothstep(0.022, 0.07, maxC) * borderFade);
    }
    return vec4(col, a);
  }'''

replacement = '''  if(uPacked > 0.5){
    // colour occupies the left half, matte the right
    vec2 c = vec2(clamp(uv.x * 0.5, uTexel.x, 0.5 - uTexel.x), uv.y);
    vec3 col = texture(uClip, c).rgb;
    float a = texture(uClip, c + vec2(0.5, 0.0)).r;
    return vec4(col, a);
  } else {
    vec4 samp = texture(uClip, uv);
    float edgeFade = smoothstep(0.0, 0.015, uv.x) * smoothstep(1.0, 0.985, uv.x)
                   * smoothstep(0.0, 0.015, uv.y) * smoothstep(1.0, 0.985, uv.y);
    float a = samp.a;
    // When VP9 transparent video is decoded, samp.a holds the true transparent matte
    if(a < 0.98) {
      return vec4(samp.rgb, a * edgeFade);
    }
    // High-precision luma/chroma key fallback if browser strips alpha stream
    float maxC = max(samp.r, max(samp.g, samp.b));
    float fallbackA = smoothstep(0.025, 0.085, maxC);
    return vec4(samp.rgb, fallbackA * edgeFade);
  }'''

assert target in code, "Target not found in shaders.js"
code = code.replace(target, replacement)

with open('src/gl/shaders.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated shaders.js sampleClip successfully!")

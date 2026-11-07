with open('src/gl/shaders.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('vec4 sampleClip(vec2 uv){')
print(text[idx:idx+1200])

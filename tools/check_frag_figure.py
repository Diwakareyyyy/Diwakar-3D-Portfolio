with open('src/gl/shaders.js', 'r', encoding='utf-8') as f:
    text = f.read()

idx = text.find('FRAG_FIGURE =')
print(text[idx:idx+1600])

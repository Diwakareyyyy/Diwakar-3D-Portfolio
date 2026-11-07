with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

idx1 = text.find('id="experience"')
idx2 = text.find('id="gallery"')
print(text[idx1:idx2])

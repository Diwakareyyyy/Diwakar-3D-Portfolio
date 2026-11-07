with open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

for i, l in enumerate(lines):
    if 'id="experience"' in l or 'id="certificates"' in l or 'id="finale"' in l or 'id="contact"' in l:
        print(f'{i+1}: {l.strip()[:100]}')

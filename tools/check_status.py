with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

print('experience present:', 'id="experience"' in text)
print('Infology present in index:', 'Infology' in text)
print('InfoLogia present in index:', 'InfoLogia' in text)
print('EXPERIENCE LOADING present:', 'EXPERIENCE LOADING' in text)
print('cert-hud--title-wrap present:', 'cert-hud--title-wrap' in text)

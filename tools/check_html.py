with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

checks = [
    'id="projectModal"',
    'id="galleryFilterDock"',
    'id="certsModal"',
    'id="uniStage"',
    'id="chronoStage"',
    'id="experience"',
    'id="fin"'
]
for c in checks:
    assert c in html, f'Missing {c}'
    print(f'[OK] Found {c}')

print('HTML structural integrity check PASSED!')

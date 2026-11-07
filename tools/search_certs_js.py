with open('src/scene5/certs.js', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for i, line in enumerate(lines):
    if 'page' in line.lower() or 'text' in line.lower() or 'font' in line.lower():
        print(f"{i+1}: {line}")

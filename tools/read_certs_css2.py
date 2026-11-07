with open('src/styles/certs.css', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for i in range(120, min(240, len(lines))):
    print(f"{i+1}: {lines[i]}")

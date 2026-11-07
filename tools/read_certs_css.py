with open('src/styles/certs.css', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for i in range(min(120, len(lines))):
    print(f"{i+1}: {lines[i]}")

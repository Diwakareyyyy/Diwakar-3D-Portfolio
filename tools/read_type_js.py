with open('src/scene/type.js', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for i in range(min(100, len(lines))):
    print(f"{i+1}: {lines[i]}")

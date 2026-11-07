with open('src/gl/stage.js', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for i in range(120, min(220, len(lines))):
    print(f"{i+1}: {lines[i]}")

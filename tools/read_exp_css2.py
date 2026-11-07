with open('src/styles/experience.css', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for i in range(140, min(300, len(lines))):
    print(f"{i+1}: {lines[i]}")

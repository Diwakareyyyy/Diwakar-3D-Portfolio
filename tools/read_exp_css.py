with open('src/styles/experience.css', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
print(f"Total lines: {len(lines)}")
for i in range(min(140, len(lines))):
    print(f"{i+1}: {lines[i]}")

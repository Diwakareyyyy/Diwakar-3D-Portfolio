with open('src/scene2/cards.js', 'r', encoding='utf-8') as f:
    text = f.read()

lines = text.splitlines()
for i in range(min(80, len(lines))):
    print(f"{i+1}: {lines[i]}")

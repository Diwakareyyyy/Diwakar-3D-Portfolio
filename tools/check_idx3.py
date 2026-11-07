with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

exp_idx = text.find('<!-- RIGHT WING')
print(text[exp_idx:exp_idx+3500])

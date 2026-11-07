with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

exp_idx = text.find('<section class="experience"')
print(text[exp_idx+1500:exp_idx+4000])

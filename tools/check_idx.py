with open('index.html', 'r', encoding='utf-8') as f:
    text = f.read()

# Let's inspect from <section class="experience" to </html>
exp_idx = text.find('<section class="experience"')
print('exp_idx:', exp_idx)
print(text[exp_idx:exp_idx+1500])

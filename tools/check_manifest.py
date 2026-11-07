import json
with open('public/media/manifest.json', 'r') as f:
    m = json.load(f)
print(m['clips']['hero'])

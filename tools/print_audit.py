import json

with open("tools/assets_audit.json", "r", encoding="utf-8") as f:
    data = json.load(f)

keeps = [x for x in data if x["status"] == "KEEP"]
removes = [x for x in data if x["status"] == "REMOVE"]
reviews = [x for x in data if x["status"] == "REVIEW"]

print(f"Total: {len(data)}")
print(f"KEEP: {len(keeps)}")
print(f"REMOVE: {len(removes)}")
print(f"REVIEW: {len(reviews)}")

print(f"\n--- KEEP ASSETS ({len(keeps)}) ---")
for x in keeps:
    print(f"- {x['path']} ({x['format']}, {x['size_kb']} KB, {x['dimensions']}) -> {x['section']}")

print(f"\n--- REMOVE CANDIDATES ({len(removes)}) ---")
for x in removes:
    print(f"- {x['path']} ({x['format']}, {x['size_kb']} KB, {x['dimensions']}) -> {x['section']}")

print(f"\n--- REVIEW CANDIDATES ({len(reviews)}) ---")
for x in reviews:
    print(f"- {x['path']} ({x['format']}, {x['size_kb']} KB, {x['dimensions']}) -> {x['section']}")

import os
import shutil
import json
import re
from PIL import Image

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BACKUP_DIR = os.path.join(ROOT, "_backup_assets")

asset_exts = {'.png', '.jpg', '.jpeg', '.webp', '.svg', '.gif', '.mp4', '.webm', '.mov', '.ttf', '.otf', '.woff', '.woff2', '.wav', '.mp3', '.ogg', '.pdf'}

# 1. Read all code files into memory for fast comprehensive text search
code_texts = {}
for root, dirs, files in os.walk(ROOT):
    if any(p in root for p in ['.git', 'node_modules', '.gemini', '_backup_assets', 'tools']):
        continue
    for f in files:
        if f.endswith(('.html', '.css', '.js', '.json')):
            p = os.path.join(root, f)
            try:
                with open(p, 'r', encoding='utf-8', errors='ignore') as fp:
                    code_texts[os.path.relpath(p, ROOT)] = fp.read()
            except:
                pass

print(f"Loaded {len(code_texts)} source/config files for reference checking.")

# 2. Gather all assets
all_assets = []
root_tools = os.path.join(ROOT, "tools")
for root, dirs, files in os.walk(ROOT):
    if any(p in root for p in ['.git', 'node_modules', '.gemini', '_backup_assets']):
        continue
    if root == root_tools or root.startswith(root_tools + os.sep):
        continue
    for f in files:
        ext = os.path.splitext(f)[1].lower()
        if ext in asset_exts:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, ROOT)
            size = os.path.getsize(full)
            all_assets.append((rel, f, ext, size, full))

print(f"Found {len(all_assets)} asset files in project.")

# 3. Create full backup of asset folders to _backup_assets
os.makedirs(BACKUP_DIR, exist_ok=True)
backup_count = 0
for rel, f, ext, size, full in all_assets:
    dest = os.path.join(BACKUP_DIR, rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    if not os.path.exists(dest) or os.path.getsize(dest) != size:
        shutil.copy2(full, dest)
        backup_count += 1

print(f"Backed up all {len(all_assets)} assets to {os.path.relpath(BACKUP_DIR, ROOT)} ({backup_count} files written/verified).")

# 4. Analyze each asset
inventory = []
for rel, f, ext, size, full in all_assets:
    # Dimensions
    dim = "N/A"
    if ext in ['.png', '.jpg', '.jpeg', '.webp']:
        try:
            with Image.open(full) as im:
                dim = f"{im.size[0]}x{im.size[1]}"
        except:
            dim = "Corrupt/Unreadable"
    elif ext in ['.mp4', '.webm', '.mov']:
        # Rough check or known size
        dim = "Video"
    elif ext in ['.ttf', '.woff', '.woff2', '.otf']:
        dim = "Font"

    # Reference check across all code
    # Match by exact rel path (with / or \), or by filename
    norm_rel_fwd = rel.replace('\\', '/')
    pattern_f = re.escape(f)
    pattern_rel = re.escape(norm_rel_fwd)

    ref_files = []
    for code_file, content in code_texts.items():
        if f in content or norm_rel_fwd in content or norm_rel_fwd.replace('public/', '') in content:
            ref_files.append(code_file)

    # Classification logic based on user instructions
    # User's explicit keepers:
    # - Diwakar video 1.mp4 (Home video user uses)
    # - section 2 refrence video.mp4, section 2 image.jpg
    # - section 5 main refrence.jpg
    # - tools logos (11 skills)
    # - public/media/hero.*, public/media/manifest.json
    # - public/certs/ (person_walking.png, plate.jpg, placeholders)
    # - public/experience/ (developer_facing_building.png, office_sketch_startup.png)
    # - public/tex/
    # - public/projects/ (all active project cards, plate, figure)
    # - public/chrono/ (all active timeline slides, thumb, dial)
    # - public/fin/ (plate.jpg, man.png, fin.json)
    # - active fonts
    
    category = "REVIEW"
    section = "Unknown"

    if 'public/tools' in norm_rel_fwd:
        section = "Scene 2 - Skills"
        category = "KEEP" if f in ['figure.png', 'python.png', 'sql.png', 'react.png', 'antigravity.png', 'flutter.png', 'vercel.png', 'cpp.png', 'github.png', 'html.png', 'figma.png', 'claude.png'] else "REMOVE"
    elif 'public/certs' in norm_rel_fwd:
        section = "Scene 5 - Certificates"
        category = "KEEP" if f in ['person_walking.png', 'plate.jpg', 'placeholder_01.png', 'placeholder_02.png', 'placeholder_03.png', 'placeholder_04.png', 'placeholder_05.png'] else "REMOVE"
    elif 'public/experience' in norm_rel_fwd:
        section = "Scene 3.5 - Experience"
        category = "KEEP" if f in ['developer_facing_building.png', 'office_sketch_startup.png', 'expense_app_preview.png'] else "REMOVE"
    elif 'public/audio' in norm_rel_fwd:
        section = "Global - Audio"
        category = "KEEP"
    elif 'public/tex' in norm_rel_fwd:
        section = "Global - Textures"
        category = "KEEP"
    elif 'public/projects' in norm_rel_fwd:
        section = "Scene 4 - Projects"
        category = "REVIEW" if f == 'person_seated.png' else "KEEP"
    elif 'public/years' in norm_rel_fwd:
        section = "Scene 3 - Journey & Bio"
        category = "KEEP" if f in ['figure.png', '2023.jpg', '2024.jpg', '2025.jpg', '2026.jpg', '2027.jpg'] else "REMOVE"
    elif 'public/fin' in norm_rel_fwd:
        section = "Scene 6 - Finale"
        category = "KEEP" if f in ['plate.jpg', 'man.png', 'fin.json', 'frame2.jpg'] else "REMOVE"
    elif 'public/media' in norm_rel_fwd:
        section = "Scene 1 & 2 - Media"
        if f in ['hero.mp4', 'hero.webm', 'hero.jpg', 'hero_new.png', 'universe.mp4', 'universe.jpg']:
            category = "KEEP"
        elif f == 'hero_v1_backup.mp4':
            category = "REVIEW"
        else:
            category = "REMOVE"
    elif norm_rel_fwd.startswith('public/fonts') or norm_rel_fwd.endswith(('.woff', '.woff2', '.ttf')):
        section = "Global - Typography"
        category = "KEEP"
    elif norm_rel_fwd == 'public/resume.pdf':
        section = "Global - Resume / CV"
        category = "KEEP"
    elif rel in ['footer 2nd image.jpg', 'Footer image.jpg', 'section 2 image.jpg', 'section 2 refrence video.mp4', 'section 3 image.jpg', 'section 4 image.jpg', 'section 5 main refrence.jpg', 'Diwakar video 1.mp4']:
        section = "Root - Design & Video References"
        category = "KEEP" if rel == 'footer 2nd image.jpg' else "REVIEW"
    elif rel in ['Diwakar  video 2.mp4', 'Diwakar video 3.mov', 'Diwakar typo.jpg', 'Man_walking_and_smoking_cigarette_202609051235.mp4', 'test_iio.mp4', 'Blank Screen.jpg', 'all the dots.jpg', 'welcome to my world.jpg', 'Header.jpg', 'main refrence.jpg']:
        section = "Root - Original Owner Assets"
        category = "REMOVE"
    elif 'assets_src' in norm_rel_fwd:
        section = "Original Owner Source Archives"
        category = "REMOVE"
    else:
        category = "KEEP" if len(ref_files) > 0 else "REMOVE"

    inventory.append({
        "path": norm_rel_fwd,
        "filename": f,
        "format": ext.upper().lstrip('.'),
        "dimensions": dim,
        "size_kb": round(size / 1024, 1),
        "referenced_in": ref_files,
        "section": section,
        "status": category
    })

# Save inventory to JSON for reporting
with open("tools/assets_audit.json", "w", encoding="utf-8") as fp:
    json.dump(inventory, fp, indent=2)

keeps = [x for x in inventory if x['status'] == 'KEEP']
removes = [x for x in inventory if x['status'] == 'REMOVE']
reviews = [x for x in inventory if x['status'] == 'REVIEW']

print(f"\nAUDIT SUMMARY:")
print(f"Total Assets Found: {len(inventory)}")
print(f"  KEEP:   {len(keeps)}")
print(f"  REMOVE: {len(removes)}")
print(f"  REVIEW: {len(reviews)}")

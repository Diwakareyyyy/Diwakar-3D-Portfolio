import shutil
import json
import os

src_video = '1000306733-Picsart-BackgroundRemover.webm'
dest_video = 'public/media/hero.webm'
shutil.copyfile(src_video, dest_video)
print('Copied', src_video, 'to', dest_video, f'({os.path.getsize(dest_video)} bytes)')

# Also copy with original name for explicit reference
dest_video2 = 'public/media/1000306733-Picsart-BackgroundRemover.webm'
shutil.copyfile(src_video, dest_video2)

# Load computed track
with open('public/media/hero_track.json', 'r') as f:
    track_data = json.load(f)

# Update manifest
manifest = {
    "clips": {
        "hero": {
            "name": "hero",
            "frames": track_data['count'],
            "w": track_data['w'],
            "h": track_data['h'],
            "webm": "hero.webm",
            "mp4": "hero.webm",
            "poster": "hero_new.jpg",
            "packed": False,
            "track": track_data['frames']
        }
    }
}

with open('public/media/manifest.json', 'w') as f:
    json.dump(manifest, f, indent=2)

print('Updated public/media/manifest.json successfully!')

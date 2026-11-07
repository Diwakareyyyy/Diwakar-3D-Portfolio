import os
import cv2
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = r"C:\Users\sdiwa\.gemini\antigravity\brain\a09d3c4d-404e-4a35-bb42-f992e3e8777e\developer_seated_workstation_cinematic_black_1793722874156.jpg"
PERSON_OUT = os.path.join(ROOT, "public", "projects", "person.png")
PLATE_OUT = os.path.join(ROOT, "public", "projects", "plate.jpg")

# 1. Clean the plate's floor ring so NO shadow/silhouette of the standing person exists
plate = cv2.imread(os.path.join(ROOT, "tools", "plate_clean_floor.jpg"))
# Blend vertical seam smoothly
seam_mask = np.zeros(plate.shape[:2], dtype=np.uint8)
seam_mask[480:830, 725:870] = 255
seam_blur = cv2.GaussianBlur(seam_mask.astype(np.float32) / 255.0, (21, 21), 0)[..., None]
smooth_plate = cv2.GaussianBlur(plate, (5, 5), 0)
clean_plate = (plate.astype(np.float32) * (1.0 - seam_blur * 0.4) + smooth_plate.astype(np.float32) * (seam_blur * 0.4)).astype(np.uint8)
cv2.imwrite(PLATE_OUT, clean_plate, [cv2.IMWRITE_JPEG_QUALITY, 93])
print(f"Updated {PLATE_OUT} with seamless concentric floor ring!")

# 2. Grade the seated developer into the portfolio's cinematic dark silhouette aesthetic
raw = cv2.imread(SRC)
H, W = raw.shape[:2]

# Crop bounds of the workstation
gray = cv2.cvtColor(raw, cv2.COLOR_BGR2GRAY)
ys, xs = np.where(gray > 6)
ymin, ymax = ys.min(), ys.max()
xmin, xmax = xs.min(), xs.max()
crop = raw[ymin:ymax+1, xmin:xmax+1].copy()
ch, cw = crop.shape[:2]
c_gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

# Alpha mask
alpha = np.clip((c_gray.astype(np.float32) - 3.0) / 8.0 * 255.0, 0, 255).astype(np.uint8)
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19))
closed = cv2.morphologyEx((c_gray > 4).astype(np.uint8) * 255, cv2.MORPH_CLOSE, kernel)
contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
hull_mask = np.zeros((ch, cw), dtype=np.uint8)
cv2.drawContours(hull_mask, contours, -1, 255, -1)
interior = (hull_mask > 0) & (c_gray > 1)
alpha[interior] = np.maximum(alpha[interior], 255)

# Clean lower floor diffuse haze
bot_start = int(ch * 0.88)
for y in range(bot_start, ch):
    factor = (y - bot_start) / float(ch - bot_start)
    fade_thresh = 15 + factor * 25
    low_haze = (c_gray[y, :] < fade_thresh)
    alpha[y, low_haze] = 0

alpha = cv2.GaussianBlur(alpha, (3, 3), 0)

# Style as cinematic dark silhouette with rim lighting & glowing code monitor:
# Convert to float
rgb = crop.astype(np.float32)

# Identify monitor screen (bright cyan/green/white code syntax lines):
# In crop, monitor is around y in [120, 360], x in [480, 720]
is_screen = np.zeros((ch, cw), dtype=bool)
is_screen[120:380, 480:730] = (c_gray[120:380, 480:730] > 35)

# Identify warm amber rim lighting: pixels with high red & green (amber/gold)
is_rim = (rgb[:, :, 2] > 70) & (rgb[:, :, 1] > 40) & (rgb[:, :, 0] < 50) & (~is_screen)

# Deep silhouette body:
# Darken the core body of the developer and chair to match the dark silhouette aesthetic
body_mask = (alpha > 50) & (~is_screen) & (~is_rim)
# Tone body down to rich obsidian silhouette
rgb[body_mask] = rgb[body_mask] * 0.45

# Boost warm amber rim highlights
rgb[is_rim] = np.clip(rgb[is_rim] * 1.35, 0, 255)

# Enhance monitor screen code glow
rgb[is_screen] = np.clip(rgb[is_screen] * 1.15, 0, 255)

final_crop = np.clip(rgb, 0, 255).astype(np.uint8)
person_rgba = np.dstack([final_crop, alpha])

cv2.imwrite(PERSON_OUT, person_rgba)
print(f"Saved {PERSON_OUT} as cinematic dark silhouette developer!")

# 3. Composite preview over plate
target_w = 280
scale = target_w / float(cw)
target_h = int(ch * scale)
resized = cv2.resize(person_rgba, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

y_pos = 818 - target_h
x_pos = 798 - target_w // 2

preview = clean_plate.copy()
roi = preview[y_pos:y_pos+target_h, x_pos:x_pos+target_w]
a = (resized[:, :, 3].astype(np.float32) / 255.0)[..., None]
c = resized[:, :, :3]
preview[y_pos:y_pos+target_h, x_pos:x_pos+target_w] = np.clip(roi * (1.0 - a) + c * a, 0, 255).astype(np.uint8)

cv2.imwrite(os.path.join(ROOT, "tools", "preview_seated_silhouette.jpg"), preview, [cv2.IMWRITE_JPEG_QUALITY, 93])
print(f"Preview saved to tools/preview_seated_silhouette.jpg (x={x_pos}, y={y_pos}, w={target_w}, h={target_h})")

import os
import cv2
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = r"C:\Users\sdiwa\.gemini\antigravity\brain\a09d3c4d-404e-4a35-bb42-f992e3e8777e\developer_seated_workstation_cinematic_black_1793722874156.jpg"
OUT = os.path.join(ROOT, "public", "projects", "person.png")

img = cv2.imread(SRC)
H, W = img.shape[:2]

# Workstation bounding box in the source image
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
ys, xs = np.where(gray > 6)
ymin, ymax = ys.min(), ys.max()
xmin, xmax = xs.min(), xs.max()

# Crop tightly
crop = img[ymin:ymax+1, xmin:xmax+1].copy()
ch, cw = crop.shape[:2]
c_gray = cv2.cvtColor(crop, cv2.COLOR_BGR2GRAY)

# Segment the workstation cleanly
# 1. Base alpha from luminance with threshold at pure black
alpha = np.clip((c_gray.astype(np.float32) - 3.0) / 8.0 * 255.0, 0, 255).astype(np.uint8)

# 2. Solid interior fill for dark regions of the jacket / chair / desk
# Find contours of foreground elements
kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (19, 19))
closed = cv2.morphologyEx((c_gray > 4).astype(np.uint8) * 255, cv2.MORPH_CLOSE, kernel)
contours, _ = cv2.findContours(closed, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
hull_mask = np.zeros((ch, cw), dtype=np.uint8)
cv2.drawContours(hull_mask, contours, -1, 255, -1)

# Solid interior where contour exists and luminance > 1
interior = (hull_mask > 0) & (c_gray > 1)
alpha[interior] = np.maximum(alpha[interior], 255)

# 3. Clean floor shadow artifacts:
# In the bottom 10% of the crop (around wheels and desk feet), remove low-intensity diffuse haze
# Keep only crisp wheel casters and desk foot metal
bot_start = int(ch * 0.88)
for y in range(bot_start, ch):
    factor = (y - bot_start) / float(ch - bot_start) # 0 at bot_start, 1 at bottom
    # If pixel luminance is low, it's diffuse floor glow / bounding box edge, not metal
    fade_thresh = 15 + factor * 25
    low_haze = (c_gray[y, :] < fade_thresh)
    alpha[y, low_haze] = 0

# Soft antialiased boundary
alpha_clean = cv2.GaussianBlur(alpha, (3, 3), 0)

# Build RGBA
person_rgba = np.dstack([crop, alpha_clean])

# Save to public/projects/person.png
cv2.imwrite(OUT, person_rgba)
print(f"Successfully generated clean {OUT} ({cw}x{ch})")

# Verify composite on plate.jpg
plate = cv2.imread(os.path.join(ROOT, "public", "projects", "plate.jpg"))
target_w = 270
scale = target_w / float(cw)
target_h = int(ch * scale)
resized = cv2.resize(person_rgba, (target_w, target_h), interpolation=cv2.INTER_LANCZOS4)

y_pos = 818 - target_h
x_pos = 798 - target_w // 2

roi = plate[y_pos:y_pos+target_h, x_pos:x_pos+target_w]
a = (resized[:, :, 3].astype(np.float32) / 255.0)[..., None]
rgb = resized[:, :, :3]
plate[y_pos:y_pos+target_h, x_pos:x_pos+target_w] = np.clip(roi * (1.0 - a) + rgb * a, 0, 255).astype(np.uint8)
cv2.imwrite(os.path.join(ROOT, "tools", "verified_plate_seated.jpg"), plate, [cv2.IMWRITE_JPEG_QUALITY, 93])
print(f"Verified composite saved to tools/verified_plate_seated.jpg (w={target_w}, h={target_h}, x={x_pos}, y={y_pos})")

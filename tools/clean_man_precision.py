import os
import cv2
import numpy as np

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "Footer image.jpg")
MAN_OUT = os.path.join(ROOT, "public", "fin", "man.png")
PLATE_OUT = os.path.join(ROOT, "public", "fin", "plate.jpg")

# 1. Re-extract man cleanly from Footer image.jpg
img = cv2.imread(SRC)
H, W = img.shape[:2]
BOX = (580, 170, 1030, 900)
x0, y0, x1, y1 = BOX
man_rgb = img[y0:y1, x0:x1].copy()
mh, mw = man_rgb.shape[:2]

# Let's inspect the original man.png alpha:
# Load original man.png to keep the pristine suit mask
orig_man = cv2.imread(MAN_OUT, cv2.IMREAD_UNCHANGED)
orig_alpha = orig_man[:, :, 3].copy()

# The letter artifacts in orig_alpha are:
# A. Above the hair top (y < 62): 100% letter
orig_alpha[:62, :] = 0

# B. Chimney prongs sticking up between y=62 and y=110:
# Hair curve:
# at x=190: y=95
# at x=210: y=75
# at x=230: y=68
# at x=260: y=72
# at x=280: y=80
# at x=310: y=110
# For any pixel above this hair curve, if it is bright (letter), clear alpha!
for x in range(mw):
    for y in range(0, 120):
        # Sample color in man_rgb
        b, g, r = int(man_rgb[y, x, 0]), int(man_rgb[y, x, 1]), int(man_rgb[y, x, 2])
        # Background letter pixels are either bright white/cream (r>130, g>100, b>90)
        # or red pillar (r>90, g<50, b<50)
        if (r > 120 and g > 90) or (r > 80 and g < 50):
            orig_alpha[y, x] = 0

# C. Left vertical pillar:
# In man_box, to the left of x=155, above the shoulder (y < 230)
for y in range(60, 240):
    for x in range(0, 160):
        b, g, r = int(man_rgb[y, x, 0]), int(man_rgb[y, x, 1]), int(man_rgb[y, x, 2])
        if (r > 120 and g > 90) or (r > 70 and g < 50):
            orig_alpha[y, x] = 0

# D. Left outer background block: x < 55, y < 380
orig_alpha[:380, :55] = 0

# E. Pillar on right side behind smoke: x > 380, y < 350
for y in range(80, 350):
    for x in range(375, mw):
        b, g, r = int(man_rgb[y, x, 0]), int(man_rgb[y, x, 1]), int(man_rgb[y, x, 2])
        if r > 80 and g < 55:
            orig_alpha[y, x] = 0

# F. Red letter patch between hand and neck: x in [320, 380], y in [130, 200]
for y in range(130, 205):
    for x in range(320, 385):
        b, g, r = int(man_rgb[y, x, 0]), int(man_rgb[y, x, 1]), int(man_rgb[y, x, 2])
        # Hair/smoke is not pure saturated red (r>110, g<45)
        if r > 105 and g < 45 and b < 45:
            orig_alpha[y, x] = 0

# Soft antialiased blend on alpha
alpha_clean = cv2.GaussianBlur(orig_alpha, (3, 3), 0)
man_final = np.dstack([man_rgb, alpha_clean])

cv2.imwrite(MAN_OUT, man_final)
print("Updated public/fin/man.png with clean cutout!")

# Composite with plate
plate = cv2.imread(PLATE_OUT)
roi = plate[y0:y1, x0:x1]
m_a = (alpha_clean.astype(np.float32) / 255.0)[..., None]
m_c = man_rgb.astype(np.float32)
comp = roi * (1.0 - m_a) + m_c * m_a
plate[y0:y1, x0:x1] = np.clip(comp, 0, 255).astype(np.uint8)

cv2.imwrite(os.path.join(ROOT, "tools", "final_clean_composite.jpg"), plate, [cv2.IMWRITE_JPEG_QUALITY, 93])
print("Updated tools/final_clean_composite.jpg")

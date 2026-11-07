import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "fin", "plate.jpg")
MAN_PATH = os.path.join(ROOT, "public", "fin", "man.png")
GRUNGE_PATH = os.path.join(ROOT, "public", "tex", "grunge.png")

H, W = 900, 1600

# -----------------------------------------------------------------------------
# 1. Seamless cinematic furnace environment with red smoke & atmospheric haze
# -----------------------------------------------------------------------------
bg = np.zeros((H, W, 3), dtype=np.float32)

cx, cy = W // 2, int(H * 0.44)
yy, xx = np.mgrid[:H, :W]

# Main backlight glow
r1 = np.sqrt(((xx - cx) / (W * 0.44)) ** 2 + ((yy - cy) / (H * 0.40)) ** 2)
glow1 = np.exp(-r1 * 2.2)

# Upper hot beam
r2 = np.sqrt(((xx - cx) / (W * 0.32)) ** 2 + ((yy - 40) / (H * 0.48)) ** 2)
glow2 = np.exp(-r2 * 2.8)

# Lower floor reflection
r3 = np.sqrt(((xx - cx) / (W * 0.52)) ** 2 + ((yy - H) / (H * 0.38)) ** 2)
glow3 = np.exp(-r3 * 3.2)

crimson = np.array([16, 12, 138], dtype=np.float32)
bright_red = np.array([24, 20, 188], dtype=np.float32)
deep_red = np.array([8, 6, 68], dtype=np.float32)
dark_base = np.array([3, 2, 15], dtype=np.float32)

bg += dark_base
bg += (crimson - dark_base) * glow1[..., None] * 1.15
bg += (bright_red - crimson) * glow2[..., None] * 0.65
bg += (deep_red - dark_base) * glow3[..., None] * 0.45

# Smoke turbulence
rng = np.random.default_rng(101)
noise = rng.normal(0, 1.0, (H // 4, W // 4, 3)).astype(np.float32)
smoke = cv2.resize(cv2.GaussianBlur(noise, (15, 15), 0), (W, H)) * 13.0
bg = np.clip(bg + smoke, 0, 255)

# -----------------------------------------------------------------------------
# 2. Render DIWAKAR with precise ink bounds: NO top empty space, NO clipping
# -----------------------------------------------------------------------------
text = "DIWAKAR"
font_size = 320
font = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", font_size)

# Render raw unconstrained text on oversized canvas to find exact ink bounds
raw_canvas = Image.new("RGBA", (1800, 800), (0, 0, 0, 0))
raw_d = ImageDraw.Draw(raw_canvas)
raw_d.text((50, 50), text, font=font, fill=(255, 255, 255, 255))
raw_arr = np.array(raw_canvas)[:, :, 3]

# Extract exact ink boundaries
ys, xs = np.where(raw_arr > 0)
ink_min_y, ink_max_y = ys.min(), ys.max()
ink_min_x, ink_max_x = xs.min(), xs.max()
ink_crop = raw_canvas.crop((ink_min_x, ink_min_y, ink_max_x + 1, ink_max_y + 1))

# Target placement:
# In the original, the colossal text starts right near the top at y = 42 and reaches down to y = 820.
# Height = 820 - 42 = 778px!
# Width = 960px centered at W // 2 = 800 -> x = 320 to 1280.
# This leaves 320px margins on left and right, ensuring letter 'D' and 'R' never clip on any screen!
target_top = 42
target_bottom = 822
target_height = target_bottom - target_top
target_width = 960
target_left = (W - target_width) // 2

# Scale exact ink tightly to target dimensions
scaled_ink = ink_crop.resize((target_width, target_height), Image.Resampling.LANCZOS)

# Paste onto full frame at exact top coordinate
text_frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
text_frame.paste(scaled_ink, (target_left, target_top), scaled_ink)

letter_alpha = (np.array(text_frame)[:, :, 3].astype(np.float32) / 255.0)

# Distress letter face with grunge texture
if os.path.exists(GRUNGE_PATH):
    grunge = cv2.imread(GRUNGE_PATH, cv2.IMREAD_GRAYSCALE)
    if grunge is not None:
        grunge = cv2.resize(grunge, (W, H)).astype(np.float32) / 255.0
        letter_alpha = letter_alpha * (0.78 + 0.22 * grunge)

letter_mask = cv2.GaussianBlur(letter_alpha, (3, 3), 0)[..., None]

# -----------------------------------------------------------------------------
# 3. Dual-Tone Typography: Light Cream-White Upper + Saturated Crimson Lower
# -----------------------------------------------------------------------------
# BGR colors matching the original KRISH reference exactly:
# Top: warm cream-white
cream_top = np.array([236, 242, 248], dtype=np.float32)
# Warm ivory transition
ivory_mid = np.array([195, 215, 245], dtype=np.float32)
# Vivid crimson
crimson_mid = np.array([28, 38, 225], dtype=np.float32)
# Deep blood red
blood_bot = np.array([8, 10, 115], dtype=np.float32)
# Dark shadow floor fade
dark_floor = np.array([2, 2, 45], dtype=np.float32)

y_coords = np.arange(H, dtype=np.float32)[:, None, None]
# Progress along the letter height (0.0 at top line 42, 1.0 at bottom line 822)
p = np.clip((y_coords - target_top) / target_height, 0.0, 1.0)

# 4-stage smooth gradient:
# p in 0.00..0.35: Cream-white top
# p in 0.35..0.52: Smooth transition from cream-white through warm ivory into vivid crimson
# p in 0.52..0.80: Saturated rich red / crimson
# p in 0.80..1.00: Deep shadow red fading toward base
letter_color = np.zeros((H, W, 3), dtype=np.float32)

mask1 = (p <= 0.35).astype(np.float32)
mask2 = ((p > 0.35) & (p <= 0.52)).astype(np.float32)
mask3 = ((p > 0.52) & (p <= 0.80)).astype(np.float32)
mask4 = (p > 0.80).astype(np.float32)

# p2 normalized inside 0.35..0.52
t2 = np.clip((p - 0.35) / 0.17, 0.0, 1.0)
smooth_t2 = t2 * t2 * (3.0 - 2.0 * t2)

# p3 normalized inside 0.52..0.80
t3 = np.clip((p - 0.52) / 0.28, 0.0, 1.0)

# p4 normalized inside 0.80..1.00
t4 = np.clip((p - 0.80) / 0.20, 0.0, 1.0)

letter_color += cream_top * mask1
letter_color += (cream_top * (1.0 - smooth_t2) + crimson_mid * smooth_t2) * mask2
letter_color += (crimson_mid * (1.0 - t3) + blood_bot * t3) * mask3
letter_color += (blood_bot * (1.0 - t4) + dark_floor * t4) * mask4

# -----------------------------------------------------------------------------
# 4. Atmospheric outer glow and final plate composition
# -----------------------------------------------------------------------------
glow_mask = cv2.GaussianBlur(letter_alpha, (45, 45), 0)[..., None]
glow_color = np.array([20, 24, 185], dtype=np.float32)

final_plate = bg.copy()
final_plate += glow_color * glow_mask * 0.65
final_plate = final_plate * (1.0 - letter_mask * 0.96) + letter_color * (letter_mask * 0.96)
final_plate = np.clip(final_plate, 0, 255).astype(np.uint8)

cv2.imwrite(OUT, final_plate, [cv2.IMWRITE_JPEG_QUALITY, 93])
print("Saved public/fin/plate.jpg with dual-tone DIWAKAR!")

# Composite with cleaned man.png for preview
if os.path.exists(MAN_PATH):
    man = cv2.imread(MAN_PATH, cv2.IMREAD_UNCHANGED)
    if man is not None and man.shape[2] == 4:
        mh, mw = man.shape[:2]
        x0, y0 = 580, 170
        preview = final_plate.copy()
        m_rgb = man[:, :, :3]
        m_a = (man[:, :, 3].astype(np.float32) / 255.0)[..., None]
        roi = preview[y0:y0+mh, x0:x0+mw]
        preview[y0:y0+mh, x0:x0+mw] = (roi * (1.0 - m_a) + m_rgb * m_a).astype(np.uint8)
        cv2.imwrite(os.path.join(ROOT, "tools", "preview_dualtone_plate.jpg"), preview, [cv2.IMWRITE_JPEG_QUALITY, 92])
        print("Saved tools/preview_dualtone_plate.jpg")

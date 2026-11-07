import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, "Footer image.jpg")
OUT = os.path.join(ROOT, "public", "fin", "plate.jpg")
GRUNGE_PATH = os.path.join(ROOT, "public", "tex", "grunge.png")

H, W = 900, 1600

# 1. Build a rich, seamless cinematic red-fog furnace environment from scratch
# Base background: deep near-black with rich red ambient smoke gradients
bg = np.zeros((H, W, 3), dtype=np.float32)

# Multiple radial and directional Gaussian smoke layers
# Atmosphere center
cx, cy = W // 2, int(H * 0.44)
yy, xx = np.mgrid[:H, :W]

# Main furnace glow in the upper-center
r1 = np.sqrt(((xx - cx) / (W * 0.42)) ** 2 + ((yy - cy) / (H * 0.38)) ** 2)
glow1 = np.exp(-r1 * 2.2)

# Upper backlight beam
r2 = np.sqrt(((xx - cx) / (W * 0.30)) ** 2 + ((yy - 40) / (H * 0.45)) ** 2)
glow2 = np.exp(-r2 * 2.8)

# Lower ground reflection glow
r3 = np.sqrt(((xx - cx) / (W * 0.50)) ** 2 + ((yy - H) / (H * 0.40)) ** 2)
glow3 = np.exp(-r3 * 3.2)

# Fog colors (BGR)
crimson = np.array([18, 12, 135], dtype=np.float32)
bright_red = np.array([25, 20, 185], dtype=np.float32)
deep_red = np.array([8, 6, 65], dtype=np.float32)
dark_base = np.array([3, 2, 16], dtype=np.float32)

bg += dark_base
bg += (crimson - dark_base) * glow1[..., None] * 1.15
bg += (bright_red - crimson) * glow2[..., None] * 0.65
bg += (deep_red - dark_base) * glow3[..., None] * 0.45

# Add subtle organic noise and smoke clouds
noise = np.random.default_rng(42).normal(0, 1.0, (H // 4, W // 4, 3)).astype(np.float32)
smoke = cv2.resize(cv2.GaussianBlur(noise, (15, 15), 0), (W, H)) * 14.0
bg = np.clip(bg + smoke, 0, 255)

# 2. Render giant DIWAKAR title in exact original tall typography
text = "DIWAKAR"
font_size = 280
font = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", font_size)

# Measure standard text width
dummy = Image.new("RGBA", (100, 100))
d_dummy = ImageDraw.Draw(dummy)
bbox = d_dummy.textbbox((0, 0), text, font=font)
orig_w = bbox[2] - bbox[0]
orig_h = bbox[3] - bbox[1]

# Render to raw mask
raw_txt = Image.new("RGBA", (orig_w + 40, orig_h + 40), (0, 0, 0, 0))
raw_d = ImageDraw.Draw(raw_txt)
raw_d.text((20, 20), text, font=font, fill=(255, 255, 255, 255))

# Target dimensions matching original reference (height ~ 720px, width ~ 1000px)
target_w = 1010
target_h = 715
target_x = (W - target_w) // 2
target_y = 44

stretched_txt = raw_txt.resize((target_w, target_h), Image.Resampling.LANCZOS)
text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
text_layer.paste(stretched_txt, (target_x, target_y), stretched_txt)

letter_alpha = (np.array(text_layer)[:, :, 3].astype(np.float32) / 255.0)

# Distress letter face with grunge texture
if os.path.exists(GRUNGE_PATH):
    grunge = cv2.imread(GRUNGE_PATH, cv2.IMREAD_GRAYSCALE)
    if grunge is not None:
        grunge = cv2.resize(grunge, (W, H)).astype(np.float32) / 255.0
        letter_alpha = letter_alpha * (0.76 + 0.24 * grunge)

letter_mask = cv2.GaussianBlur(letter_alpha, (3, 3), 0)[..., None]

# 3. Two-tone dramatic lighting gradient:
# Top ~35%: brilliant white/cream with subtle warm tint
# Mid ~45%: vibrant saturated crimson
# Bottom ~20%: deep dark blood-red fading into black floor
top_color = np.array([242, 244, 250], dtype=np.float32)   # Brilliant white / cream
mid_color = np.array([22, 28, 220], dtype=np.float32)     # Vivid red/crimson
bot_color = np.array([8, 10, 110], dtype=np.float32)      # Deep shadow red

y_coords = np.arange(H, dtype=np.float32)
y_norm = np.clip((y_coords - target_y) / target_h, 0.0, 1.0)[:, None, None]

# Key points: y=0..0.36 is top, 0.36..0.72 is transition, 0.72..1.0 is bottom
w_top = np.clip(1.0 - (y_norm / 0.40), 0.0, 1.0)
w_mid = np.clip(1.0 - np.abs(y_norm - 0.52) / 0.35, 0.0, 1.0)
w_bot = np.clip((y_norm - 0.65) / 0.35, 0.0, 1.0)

letter_color = top_color * w_top + mid_color * (1.0 - w_top) * (1.0 - w_bot) + bot_color * w_bot

# 4. Atmospheric outer glow around the letters
glow_mask = cv2.GaussianBlur(letter_alpha, (45, 45), 0)[..., None]
glow_color = np.array([18, 22, 175], dtype=np.float32)

# Composite final plate
final_plate = bg.copy()
final_plate += glow_color * glow_mask * 0.68
final_plate = final_plate * (1.0 - letter_mask * 0.96) + letter_color * (letter_mask * 0.96)
final_plate = np.clip(final_plate, 0, 255).astype(np.uint8)

cv2.imwrite(OUT, final_plate, [cv2.IMWRITE_JPEG_QUALITY, 93])
print("Generated seamless cinematic plate with single giant DIWAKAR title!")

# Also generate a composite preview with man.png
man_path = os.path.join(ROOT, "public", "fin", "man.png")
if os.path.exists(man_path):
    man = cv2.imread(man_path, cv2.IMREAD_UNCHANGED)
    if man is not None and man.shape[2] == 4:
        mh, mw = man.shape[:2]
        x0, y0 = 580, 170
        preview = final_plate.copy()
        m_rgb = man[:, :, :3]
        m_a = (man[:, :, 3].astype(np.float32) / 255.0)[..., None]
        roi = preview[y0:y0+mh, x0:x0+mw]
        preview[y0:y0+mh, x0:x0+mw] = (roi * (1.0 - m_a) + m_rgb * m_a).astype(np.uint8)
        cv2.imwrite(os.path.join(ROOT, "tools", "final_composition_preview.jpg"), preview, [cv2.IMWRITE_JPEG_QUALITY, 92])
        print("Generated tools/final_composition_preview.jpg")

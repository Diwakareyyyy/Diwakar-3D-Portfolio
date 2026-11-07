import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "public", "fin", "plate.jpg")
MAN_PATH = os.path.join(ROOT, "public", "fin", "man.png")
GRUNGE_PATH = os.path.join(ROOT, "public", "tex", "grunge.png")

H, W = 900, 1600

# 1. Seamless red furnace fog background
bg = np.zeros((H, W, 3), dtype=np.float32)
cx, cy = W // 2, int(H * 0.44)
yy, xx = np.mgrid[:H, :W]

# Backlight atmospheric falloff
r1 = np.sqrt(((xx - cx) / (W * 0.46)) ** 2 + ((yy - cy) / (H * 0.42)) ** 2)
glow1 = np.exp(-r1 * 2.2)

r2 = np.sqrt(((xx - cx) / (W * 0.34)) ** 2 + ((yy - 40) / (H * 0.50)) ** 2)
glow2 = np.exp(-r2 * 2.8)

r3 = np.sqrt(((xx - cx) / (W * 0.54)) ** 2 + ((yy - H) / (H * 0.40)) ** 2)
glow3 = np.exp(-r3 * 3.2)

crimson = np.array([18, 12, 142], dtype=np.float32)
bright_red = np.array([26, 22, 192], dtype=np.float32)
deep_red = np.array([8, 6, 68], dtype=np.float32)
dark_base = np.array([3, 2, 15], dtype=np.float32)

bg += dark_base
bg += (crimson - dark_base) * glow1[..., None] * 1.15
bg += (bright_red - crimson) * glow2[..., None] * 0.65
bg += (deep_red - dark_base) * glow3[..., None] * 0.45

# Add organic smoke turbulence
rng = np.random.default_rng(202)
noise = rng.normal(0, 1.0, (H // 4, W // 4, 3)).astype(np.float32)
smoke = cv2.resize(cv2.GaussianBlur(noise, (15, 15), 0), (W, H)) * 13.0
bg = np.clip(bg + smoke, 0, 255)

# 2. Render spacious DIWAKAR title with elegant letter proportions & tracking
# We render each letter individually or with balanced tracking so they are never cramped
text = "DIWAKAR"
font_size = 280
font = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", font_size)

# Render text with natural tracking
raw_canvas = Image.new("RGBA", (2000, 800), (0, 0, 0, 0))
raw_d = ImageDraw.Draw(raw_canvas)

# Render individual letters with custom spacious tracking
pen_x = 40
letter_crops = []
for ch in text:
    bbox = raw_d.textbbox((0, 0), ch, font=font)
    lw = bbox[2] - bbox[0]
    lh = bbox[3] - bbox[1]
    ch_img = Image.new("RGBA", (lw + 20, lh + 20), (0, 0, 0, 0))
    ch_d = ImageDraw.Draw(ch_img)
    ch_d.text((10 - bbox[0], 10 - bbox[1]), ch, font=font, fill=(255, 255, 255, 255))
    letter_crops.append(ch_img)

# Combine into tracked word:
# Target dimensions: Width = 1140px, Height = 635px, Top = 70px
target_w = 1140
target_h = 635
target_top = 70
target_left = (W - target_w) // 2

# Scale each letter proportionally and place with elegant spacing
total_orig_w = sum(img.width for img in letter_crops)
# Distribute across target_w
tracked_word = Image.new("RGBA", (target_w, target_h), (0, 0, 0, 0))

# Width for each letter proportionally scaled
spacing = int(target_w * 0.022) # Subtle space between letters
avail_w = target_w - spacing * (len(text) - 1)
scale_w = avail_w / float(total_orig_w)

cur_x = 0
for img in letter_crops:
    ch_target_w = max(10, int(img.width * scale_w))
    ch_scaled = img.resize((ch_target_w, target_h), Image.Resampling.LANCZOS)
    tracked_word.paste(ch_scaled, (cur_x, 0), ch_scaled)
    cur_x += ch_target_w + spacing

# Paste onto full 1600x900 frame
text_frame = Image.new("RGBA", (W, H), (0, 0, 0, 0))
text_frame.paste(tracked_word, (target_left, target_top), tracked_word)

letter_alpha = (np.array(text_frame)[:, :, 3].astype(np.float32) / 255.0)

# Apply distressed grunge texture
if os.path.exists(GRUNGE_PATH):
    grunge = cv2.imread(GRUNGE_PATH, cv2.IMREAD_GRAYSCALE)
    if grunge is not None:
        grunge = cv2.resize(grunge, (W, H)).astype(np.float32) / 255.0
        letter_alpha = letter_alpha * (0.80 + 0.20 * grunge)

letter_mask = cv2.GaussianBlur(letter_alpha, (3, 3), 0)[..., None]

# 3. Dual-Tone Gradient: Cream-White Upper + Crimson Lower
cream_top   = np.array([238, 244, 250], dtype=np.float32) # Light cream-white
ivory_mid   = np.array([205, 222, 248], dtype=np.float32) # Warm transition
crimson_mid = np.array([26, 36, 228], dtype=np.float32)   # Vivid crimson
blood_bot   = np.array([8, 10, 120], dtype=np.float32)    # Rich blood red
dark_base_c = np.array([2, 2, 45], dtype=np.float32)      # Shadow base

y_coords = np.arange(H, dtype=np.float32)[:, None, None]
p = np.clip((y_coords - target_top) / target_h, 0.0, 1.0)

# Smooth transition curve
letter_color = np.zeros((H, W, 3), dtype=np.float32)
mask1 = (p <= 0.38).astype(np.float32)
mask2 = ((p > 0.38) & (p <= 0.55)).astype(np.float32)
mask3 = ((p > 0.55) & (p <= 0.82)).astype(np.float32)
mask4 = (p > 0.82).astype(np.float32)

t2 = np.clip((p - 0.38) / 0.17, 0.0, 1.0)
smooth_t2 = t2 * t2 * (3.0 - 2.0 * t2)
t3 = np.clip((p - 0.55) / 0.27, 0.0, 1.0)
t4 = np.clip((p - 0.82) / 0.18, 0.0, 1.0)

letter_color += cream_top * mask1
letter_color += (cream_top * (1.0 - smooth_t2) + crimson_mid * smooth_t2) * mask2
letter_color += (crimson_mid * (1.0 - t3) + blood_bot * t3) * mask3
letter_color += (blood_bot * (1.0 - t4) + dark_base_c * t4) * mask4

# 4. Outer glow and composite
glow_mask = cv2.GaussianBlur(letter_alpha, (45, 45), 0)[..., None]
glow_color = np.array([20, 24, 185], dtype=np.float32)

final_plate = bg.copy()
final_plate += glow_color * glow_mask * 0.65
final_plate = final_plate * (1.0 - letter_mask * 0.96) + letter_color * (letter_mask * 0.96)
final_plate = np.clip(final_plate, 0, 255).astype(np.uint8)

cv2.imwrite(OUT, final_plate, [cv2.IMWRITE_JPEG_QUALITY, 93])
print(f"Saved spacious dual-tone plate to {OUT}")

# Composite with man.png
if os.path.exists(MAN_PATH):
    man = cv2.imread(MAN_PATH, cv2.IMREAD_UNCHANGED)
    if man is not None:
        mh, mw = man.shape[:2]
        x0, y0 = 580, 170
        preview = final_plate.copy()
        m_rgb = man[:, :, :3]
        m_a = (man[:, :, 3].astype(np.float32) / 255.0)[..., None]
        roi = preview[y0:y0+mh, x0:x0+mw]
        preview[y0:y0+mh, x0:x0+mw] = np.clip(roi * (1.0 - m_a) + m_rgb * m_a, 0, 255).astype(np.uint8)
        cv2.imwrite(os.path.join(ROOT, "tools", "preview_spacious_plate.jpg"), preview, [cv2.IMWRITE_JPEG_QUALITY, 92])
        print("Saved tools/preview_spacious_plate.jpg")

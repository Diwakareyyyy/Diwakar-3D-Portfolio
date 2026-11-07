import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PLATE_PATH = os.path.join(ROOT, "public", "fin", "plate.jpg")
GRUNGE_PATH = os.path.join(ROOT, "public", "tex", "grunge.png")

plate = cv2.imread(PLATE_PATH)
H, W = plate.shape[:2]

# 1. Clean the old wordmark area in the center while preserving the red background fog
# Red fog background color is approx BGR: (15, 12, 60)
hsv = cv2.cvtColor(plate, cv2.COLOR_BGR2HSV)
red_mask = ((hsv[:, :, 1] > 70) & (hsv[:, :, 2] > 60) & (hsv[:, :, 0] < 20)).astype(np.uint8)

# Inpaint/diffuse the old red letters to create a smooth red-fog backdrop
smooth_fog = cv2.inpaint(plate, red_mask, 15, cv2.INPAINT_TELEA)
# Blend to keep ambient fog natural
backdrop = cv2.addWeighted(plate, 0.35, smooth_fog, 0.65, 0)

# 2. Render DIWAKAR onto a text mask
text_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d = ImageDraw.Draw(text_layer)

# Load heavy grotesque font (Impact or Segoe UI Black)
font = ImageFont.truetype("C:/Windows/Fonts/impact.ttf", 360)
text = "DIWAKAR"
bbox = d.textbbox((0, 0), text, font=font)
tw = bbox[2] - bbox[0]
th = bbox[3] - bbox[1]

# Position centered behind where the man stands
tx = int((W - tw) / 2)
ty = int(H * 0.44 - th / 2)

d.text((tx, ty), text, font=font, fill=(255, 255, 255, 255))

# Convert text mask to numpy
t_arr = np.array(text_layer)
alpha = (t_arr[:, :, 3].astype(np.float32) / 255.0)

# Apply grunge texture to distress the letters
if os.path.exists(GRUNGE_PATH):
    grunge = cv2.imread(GRUNGE_PATH, cv2.IMREAD_GRAYSCALE)
    if grunge is not None:
        grunge = cv2.resize(grunge, (W, H)).astype(np.float32) / 255.0
        alpha = alpha * (0.65 + 0.35 * grunge)

# Soft edge blur
alpha_blur = cv2.GaussianBlur(alpha, (5, 5), 0)

# 3. Create the vibrant distressed red/crimson letter color
# BGR: Red highlights around (40, 50, 220) and deep glow (20, 25, 160)
letter_color = np.zeros_like(plate, dtype=np.float32)
letter_color[:, :, 0] = 30   # Blue
letter_color[:, :, 1] = 45   # Green
letter_color[:, :, 2] = 225  # Red

# Add subtle vertical gradient (top lighter, bottom deeper)
y_grad = np.linspace(1.15, 0.75, H)[:, None, None]
letter_color = np.clip(letter_color * y_grad, 0, 255)

# Outer glow around DIWAKAR
glow_mask = cv2.GaussianBlur(alpha, (35, 35), 0)[..., None]
glow_color = np.zeros_like(plate, dtype=np.float32)
glow_color[:, :, 0] = 15
glow_color[:, :, 1] = 25
glow_color[:, :, 2] = 160

# Composite: backdrop + glow + text
result = backdrop.astype(np.float32)
result += glow_color * glow_mask * 0.75

a_mask = alpha_blur[..., None]
result = result * (1.0 - a_mask * 0.88) + letter_color * (a_mask * 0.88)
result = np.clip(result, 0, 255).astype(np.uint8)

# Save back to plate.jpg
cv2.imwrite(PLATE_PATH, result, [cv2.IMWRITE_JPEG_QUALITY, 92])
print("Updated finale plate.jpg with DIWAKAR successfully!")

from PIL import Image, ImageDraw, ImageFont
import math
import os

W, H = 720, 480
img = Image.new('RGBA', (W, H), (14, 10, 14, 255))
draw = ImageDraw.Draw(img)

# Background gradient: dark red-black atmosphere
for y in range(H):
    r = int(18 + 12 * (y / H))
    g = int(8 + 4 * (y / H))
    b = int(12 + 6 * (y / H))
    draw.line([(0, y), (W, y)], fill=(r, g, b, 255))

# Subtle grid pattern
for x in range(0, W, 32):
    draw.line([(x, 0), (x, H)], fill=(222, 27, 28, 15))
for y in range(0, H, 32):
    draw.line([(0, y), (W, y)], fill=(222, 27, 28, 15))

# Phone / Tablet UI Container (Centered mockup)
phone_w, phone_h = 320, 440
px0, py0 = (W - phone_w) // 2, (H - phone_h) // 2
px1, py1 = px0 + phone_w, py0 + phone_h

# Outer glow
for i in range(16, 0, -2):
    alpha = int(45 * (1 - i / 16))
    draw.rounded_rectangle([px0 - i, py0 - i, px1 + i, py1 + i], radius=24 + i, outline=(222, 27, 28, alpha), width=2)

# Phone chassis
draw.rounded_rectangle([px0, py0, px1, py1], radius=24, fill=(10, 8, 10, 255), outline=(222, 27, 28, 120), width=2)

# Phone status notch / bar
draw.rounded_rectangle([px0 + 90, py0 + 6, px1 - 90, py0 + 16], radius=5, fill=(24, 18, 20, 255))

# App Header
try:
    font_sm = ImageFont.truetype("arial.ttf", 11)
    font_md = ImageFont.truetype("arial.ttf", 13)
    font_bd = ImageFont.truetype("arialbd.ttf", 15)
    font_lg = ImageFont.truetype("arialbd.ttf", 22)
except:
    font_sm = ImageFont.load_default()
    font_md = ImageFont.load_default()
    font_bd = ImageFont.load_default()
    font_lg = ImageFont.load_default()

# App Bar
draw.text((px0 + 20, py0 + 28), "Infology Expense", fill=(255, 255, 255, 255), font=font_bd)
# Flutter badge
draw.rounded_rectangle([px1 - 85, py0 + 26, px1 - 20, py0 + 44], radius=4, fill=(2, 86, 155, 180), outline=(1, 117, 194, 255))
draw.text((px1 - 77, py0 + 29), "Flutter & Dart", fill=(255, 255, 255, 255), font=font_sm)

# Main Card: Monthly Spend & Balance
card_y0 = py0 + 56
card_y1 = card_y0 + 115
draw.rounded_rectangle([px0 + 16, card_y0, px1 - 16, card_y1], radius=14, fill=(24, 14, 18, 255), outline=(222, 27, 28, 80), width=1)

draw.text((px0 + 28, card_y0 + 12), "TOTAL MONTHLY EXPENSES", fill=(220, 160, 160, 255), font=font_sm)
draw.text((px0 + 28, card_y0 + 30), "$3,420.50", fill=(255, 255, 255, 255), font=font_lg)

# Mini bar chart in card
bars = [35, 58, 42, 80, 65, 92, 74, 50, 88, 62]
bx_start = px0 + 30
bw = 18
bgap = 8
for i, val in enumerate(bars):
    bh = int(val * 0.38)
    bx = bx_start + i * (bw + bgap)
    by = card_y1 - 12 - bh
    color = (255, 75, 60, 255) if i == 5 else (180, 50, 50, 200)
    draw.rounded_rectangle([bx, by, bx + bw, card_y1 - 12], radius=3, fill=color)

# Section: Analytics Categories
draw.text((px0 + 20, card_y1 + 14), "Expense Categories", fill=(240, 220, 220, 255), font=font_md)

# Category pills
cats = [
    ("Development & Cloud", "$1,450", (222, 27, 28)),
    ("UI Components", "$890", (255, 95, 60)),
    ("Testing & QA Tools", "$680", (255, 140, 60)),
    ("Team Subscriptions", "$400", (160, 60, 80)),
]

cat_y = card_y1 + 36
for name, amt, col in cats:
    draw.rounded_rectangle([px0 + 16, cat_y, px1 - 16, cat_y + 42], radius=10, fill=(20, 14, 18, 220), outline=(col[0], col[1], col[2], 60))
    # Icon circle
    draw.ellipse([px0 + 26, cat_y + 9, px0 + 50, cat_y + 33], fill=(col[0], col[1], col[2], 80), outline=col)
    draw.text((px0 + 60, cat_y + 8), name, fill=(245, 240, 240, 255), font=font_md)
    draw.text((px0 + 60, cat_y + 24), "Reusable component", fill=(180, 150, 150, 255), font=font_sm)
    draw.text((px1 - 75, cat_y + 14), amt, fill=(255, 255, 255, 255), font=font_bd)
    cat_y += 50

# Bottom Navigation Bar
nav_y = py1 - 42
draw.rounded_rectangle([px0 + 12, nav_y, px1 - 12, py1 - 8], radius=12, fill=(18, 12, 16, 255))
nav_items = ["Dashboard", "Expenses", "Reports", "Profile"]
for idx, item in enumerate(nav_items):
    nx = px0 + 25 + idx * 72
    col = (255, 75, 60, 255) if idx == 1 else (160, 140, 140, 255)
    draw.text((nx, nav_y + 10), item, fill=col, font=font_sm)

# Left info banner (beside phone)
draw.rounded_rectangle([18, 24, px0 - 24, 130], radius=10, fill=(16, 10, 14, 230), outline=(222, 27, 28, 90))
draw.text((32, 36), "CROSS-PLATFORM APP", fill=(255, 100, 80, 255), font=font_sm)
draw.text((32, 54), "Flutter & Dart Engine", fill=(255, 255, 255, 255), font=font_bd)
draw.text((32, 78), "Responsive UI Components\nReal-time State Management\nAutomated Testing & QA", fill=(210, 190, 190, 255), font=font_sm)

# Right tech spec banner (beside phone)
draw.rounded_rectangle([px1 + 24, 24, W - 18, 130], radius=10, fill=(16, 10, 14, 230), outline=(222, 27, 28, 90))
draw.text((px1 + 38, 36), "INFOLOGY TECHNOLOGIES", fill=(255, 100, 80, 255), font=font_sm)
draw.text((px1 + 38, 54), "Expense Tracking UI", fill=(255, 255, 255, 255), font=font_bd)
draw.text((px1 + 38, 78), "Internship Project 2026\nCross-Platform Mobile\nModular Architecture", fill=(210, 190, 190, 255), font=font_sm)

out_path = 'public/experience/expense_app_preview.png'
img.save(out_path, format='PNG')
print(f"Generated {out_path} successfully ({W}x{H})")

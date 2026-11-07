import os
import math
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = 'public/tools'
os.makedirs(OUT_DIR, exist_ok=True)

# 4x supersampling canvas
W, H = 800, 1000
FONT_PATH = 'C:/Windows/Fonts/segoeuib.ttf'
FONT_REG = 'C:/Windows/Fonts/segoeui.ttf'

def get_font(size, bold=True):
    try:
        return ImageFont.truetype(FONT_PATH if bold else FONT_REG, size)
    except:
        return ImageFont.load_default()

def create_base():
    return Image.new('RGBA', (W, H), (0, 0, 0, 0))

def draw_label(draw, text, y=720, font_size=72, color=(245, 245, 250, 255)):
    font = get_font(font_size, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    tx = (W - tw) / 2
    draw.text((tx, y), text, font=font, fill=color)

def finish_and_save(img, filename):
    out = img.resize((200, 250), Image.Resampling.LANCZOS)
    out.save(os.path.join(OUT_DIR, filename), 'PNG')
    print(f'Saved {filename}: {out.size}')

# 1. Python (Official blue & yellow snakes)
def make_python():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    blue = (55, 118, 171, 255)
    yellow = (255, 212, 59, 255)
    
    # Top-left blue snake
    d.rounded_rectangle([cx - 150, cy - 180, cx + 50, cy + 20], radius=60, fill=blue)
    d.rounded_rectangle([cx - 50, cy - 80, cx + 150, cy + 20], radius=40, fill=blue)
    d.rounded_rectangle([cx - 150, cy - 180, cx - 10, cy - 60], radius=50, fill=blue)
    d.ellipse([cx - 70, cy - 140, cx - 40, cy - 110], fill=(255, 255, 255, 255))
    
    # Bottom-right yellow snake
    d.rounded_rectangle([cx - 50, cy - 20, cx + 150, cy + 180], radius=60, fill=yellow)
    d.rounded_rectangle([cx - 150, cy - 20, cx + 50, cy + 80], radius=40, fill=yellow)
    d.rounded_rectangle([cx + 10, cy + 60, cx + 150, cy + 180], radius=50, fill=yellow)
    d.ellipse([cx + 40, cy + 110, cx + 70, cy + 140], fill=(255, 255, 255, 255))
    
    draw_label(d, 'Python')
    finish_and_save(im, 'python.png')

# 2. SQL (Clean database / relational cylinder symbol)
def make_sql():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    c_base = (0, 117, 180, 255)
    c_top = (40, 170, 235, 255)
    
    for i, dy in enumerate([-110, -20, 70]):
        # Base/side cylinder body
        d.chord([cx - 140, cy + dy, cx + 140, cy + dy + 100], start=0, end=180, fill=c_base)
        d.rectangle([cx - 140, cy + dy + 20, cx + 140, cy + dy + 50], fill=c_base)
        # Cap
        d.ellipse([cx - 140, cy + dy, cx + 140, cy + dy + 60], fill=c_top if i == 0 else (20, 140, 210, 255))
        
    draw_label(d, 'SQL')
    finish_and_save(im, 'sql.png')

# 3. React (Official cyan atom symbol)
def make_react():
    im = create_base()
    cx, cy = 400, 380
    cyan = (97, 218, 251, 255)
    
    # 3 elliptical orbiting rings at 0, 60, 120
    for angle in [0, 60, 120]:
        t_im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        t_d = ImageDraw.Draw(t_im)
        t_d.ellipse([cx - 200, cy - 75, cx + 200, cy + 75], outline=cyan, width=18)
        rot_im = t_im.rotate(angle, center=(cx, cy), resample=Image.Resampling.BICUBIC)
        im = Image.alpha_composite(im, rot_im)
        
    d = ImageDraw.Draw(im)
    # Center nucleus
    d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=cyan)
    
    draw_label(d, 'React')
    finish_and_save(im, 'react.png')

# 4. Antigravity (Official mountain-style logo: stylized geometric mountain peaks)
def make_antigravity():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    # Mountain-style geometric mark
    # Main bold mountain peak with sharp geometric facets
    c_peak_l = (255, 255, 255, 255)        # Crisp white left facet
    c_peak_r = (210, 215, 225, 255)        # Light shading right facet
    c_sub_l = (90, 150, 240, 255)          # Vibrant cyan-blue left ridge
    c_sub_r = (50, 100, 200, 255)          # Deep blue right ridge
    c_accent = (255, 100, 60, 255)         # Warm orange sunrise notch
    
    # Outer mountain silhouette (sub-peaks)
    # Left secondary peak
    d.polygon([(cx - 180, cy + 140), (cx - 90, cy - 20), (cx, cy + 140)], fill=c_sub_l)
    # Right secondary peak
    d.polygon([(cx, cy + 140), (cx + 90, cy - 20), (cx + 180, cy + 140)], fill=c_sub_r)
    
    # Primary central mountain peak (towering higher)
    # Left facet
    d.polygon([(cx - 150, cy + 140), (cx, cy - 180), (cx, cy + 140)], fill=c_peak_l)
    # Right facet
    d.polygon([(cx, cy - 180), (cx + 150, cy + 140), (cx, cy + 140)], fill=c_peak_r)
    
    # Sharp center divide
    d.line([(cx, cy - 180), (cx, cy + 140)], fill=(180, 185, 195, 255), width=4)
    
    # Modern floating horizon / base cut
    d.rectangle([cx - 200, cy + 132, cx + 200, cy + 150], fill=(0, 0, 0, 0))
    
    draw_label(d, 'Antigravity')
    finish_and_save(im, 'antigravity.png')

# 5. Flutter (Official sky-blue origami chevrons)
def make_flutter():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    c_deep = (2, 86, 155, 255)
    c_mid = (1, 117, 194, 255)
    c_light = (19, 185, 253, 255)
    
    # Top chevron
    d.polygon([
        (cx - 150, cy - 200),
        (cx + 80, cy + 30),
        (cx - 10, cy + 30),
        (cx - 240, cy - 200)
    ], fill=c_light)
    
    # Lower chevron
    d.polygon([
        (cx - 10, cy + 30),
        (cx + 150, cy + 190),
        (cx + 60, cy + 190),
        (cx - 100, cy + 30)
    ], fill=c_mid)
    
    # Joining shadow
    d.polygon([
        (cx - 10, cy + 30),
        (cx + 65, cy + 105),
        (cx + 35, cy + 135),
        (cx - 40, cy + 60)
    ], fill=c_deep)
    
    draw_label(d, 'Flutter')
    finish_and_save(im, 'flutter.png')

# 6. Vercel (Official crisp equilateral triangle)
def make_vercel():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    # Pure clean white triangle
    r = 170
    pts = [
        (cx, cy - r),
        (cx + r * 1.155, cy + r * 0.95),
        (cx - r * 1.155, cy + r * 0.95)
    ]
    d.polygon(pts, fill=(255, 255, 255, 255))
    
    draw_label(d, 'Vercel')
    finish_and_save(im, 'vercel.png')

# 7. C++ (Official dark blue hexagonal shield with white/cyan C++)
def make_cpp():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    # Deep blue hexagon
    r = 200
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(30, 390, 60)]
    d.polygon(pts, fill=(0, 68, 130, 255))
    
    # Inner border
    r_in = 185
    pts_in = [(cx + r_in * math.cos(math.radians(a)), cy + r_in * math.sin(math.radians(a))) for a in range(30, 390, 60)]
    d.polygon(pts_in, outline=(0, 140, 220, 255), width=8)
    
    font = get_font(180, bold=True)
    bbox = d.textbbox((0, 0), 'C++', font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((cx - tw / 2, cy - th / 2 - 25), 'C++', font=font, fill=(255, 255, 255, 255))
    
    draw_label(d, 'C++')
    finish_and_save(im, 'cpp.png')

# 8. GitHub (Official white Octocat silhouette)
def make_github():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    white = (250, 250, 255, 255)
    
    # Head & ears
    d.ellipse([cx - 130, cy - 120, cx + 130, cy + 120], fill=white)
    # Left ear
    d.polygon([(cx - 120, cy - 60), (cx - 130, cy - 160), (cx - 50, cy - 105)], fill=white)
    # Right ear
    d.polygon([(cx + 120, cy - 60), (cx + 130, cy - 160), (cx + 50, cy - 105)], fill=white)
    
    # Body base
    d.chord([cx - 100, cy + 20, cx + 100, cy + 155], start=0, end=180, fill=white)
    
    draw_label(d, 'GitHub')
    finish_and_save(im, 'github.png')

# 9. HTML (Official HTML5 orange shield with 5)
def make_html():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    # Orange shield
    pts = [
        (cx - 150, cy - 180),
        (cx + 150, cy - 180),
        (cx + 125, cy + 120),
        (cx, cy + 180),
        (cx - 125, cy + 120)
    ]
    d.polygon(pts, fill=(228, 77, 38, 255))
    
    # Right half lighter
    pts_r = [
        (cx, cy - 180),
        (cx + 150, cy - 180),
        (cx + 125, cy + 120),
        (cx, cy + 180)
    ]
    d.polygon(pts_r, fill=(241, 101, 41, 255))
    
    # White 5
    font = get_font(230, bold=True)
    bbox = d.textbbox((0, 0), '5', font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((cx - tw / 2, cy - th / 2 - 30), '5', font=font, fill=(255, 255, 255, 255))
    
    draw_label(d, 'HTML5')
    finish_and_save(im, 'html.png')

if __name__ == '__main__':
    make_python()
    make_sql()
    make_react()
    make_antigravity()
    make_flutter()
    make_vercel()
    make_cpp()
    make_github()
    make_html()
    print('All custom logos generated successfully!')

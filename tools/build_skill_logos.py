import os
import math
from PIL import Image, ImageDraw, ImageFont

OUT_DIR = 'public/tools'
os.makedirs(OUT_DIR, exist_ok=True)

# 4x supersampling size
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

def draw_label(draw, text, y=720, font_size=72, color=(240, 240, 245, 255)):
    font = get_font(font_size, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    tx = (W - tw) / 2
    draw.text((tx, y), text, font=font, fill=color)

def finish_and_save(img, filename):
    # Downsample with Lanczos to 200x250
    out = img.resize((200, 250), Image.Resampling.LANCZOS)
    out.save(os.path.join(OUT_DIR, filename), 'PNG')
    print(f'Saved {filename}: {out.size}')

# 1. Python
def make_python():
    im = create_base()
    d = ImageDraw.Draw(im)
    # Python logo: Blue top-left snake, Yellow bottom-right snake
    cx, cy = 400, 380
    
    # Blue upper snake
    blue = (55, 118, 171, 255)
    yellow = (255, 212, 59, 255)
    
    # Blue body
    d.rounded_rectangle([cx - 150, cy - 180, cx + 50, cy + 20], radius=60, fill=blue)
    d.rounded_rectangle([cx - 50, cy - 80, cx + 150, cy + 20], radius=40, fill=blue)
    d.rounded_rectangle([cx - 150, cy - 180, cx - 10, cy - 60], radius=50, fill=blue)
    # Blue eye
    d.ellipse([cx - 70, cy - 140, cx - 40, cy - 110], fill=(255, 255, 255, 255))
    
    # Yellow lower snake
    d.rounded_rectangle([cx - 50, cy - 20, cx + 150, cy + 180], radius=60, fill=yellow)
    d.rounded_rectangle([cx - 150, cy - 20, cx + 50, cy + 80], radius=40, fill=yellow)
    d.rounded_rectangle([cx + 10, cy + 60, cx + 150, cy + 180], radius=50, fill=yellow)
    # Yellow eye
    d.ellipse([cx + 40, cy + 110, cx + 70, cy + 140], fill=(255, 255, 255, 255))
    
    draw_label(d, 'Python')
    finish_and_save(im, 'python.png')

# 2. C
def make_c():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    # Stylized blue hexagon ring
    blue_outer = (101, 154, 210, 255)
    blue_inner = (0, 89, 156, 255)
    
    # Outer hexagon
    r = 200
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(30, 390, 60)]
    d.polygon(pts, fill=blue_inner)
    
    # Stylized C letter inside
    font = get_font(260, bold=True)
    bbox = d.textbbox((0, 0), 'C', font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((cx - tw / 2 - 10, cy - th / 2 - 30), 'C', font=font, fill=(255, 255, 255, 255))
    
    draw_label(d, 'C Language')
    finish_and_save(im, 'c.png')

# 3. C++
def make_cpp():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    # Dark blue hexagon
    r = 200
    pts = [(cx + r * math.cos(math.radians(a)), cy + r * math.sin(math.radians(a))) for a in range(30, 390, 60)]
    d.polygon(pts, fill=(0, 68, 130, 255))
    
    font = get_font(180, bold=True)
    bbox = d.textbbox((0, 0), 'C++', font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((cx - tw / 2, cy - th / 2 - 25), 'C++', font=font, fill=(255, 255, 255, 255))
    
    draw_label(d, 'C++')
    finish_and_save(im, 'cpp.png')

# 4. Java
def make_java():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    # Java coffee cup and steam
    # Red/orange steam swirls
    steam = (231, 111, 0, 255)
    d.arc([cx - 80, cy - 220, cx + 20, cy - 70], start=180, end=360, fill=steam, width=18)
    d.arc([cx - 20, cy - 200, cx + 80, cy - 50], start=180, end=360, fill=(245, 140, 30, 255), width=20)
    
    # Blue cup body
    blue = (83, 130, 161, 255)
    d.chord([cx - 130, cy - 40, cx + 130, cy + 130], start=0, end=180, fill=blue)
    d.rectangle([cx - 130, cy - 40, cx + 130, cy + 40], fill=blue)
    # Cup handle
    d.arc([cx + 90, cy - 30, cx + 180, cy + 70], start=270, end=90, fill=blue, width=22)
    # Saucer base
    d.ellipse([cx - 160, cy + 120, cx + 160, cy + 165], fill=blue)
    
    draw_label(d, 'Java')
    finish_and_save(im, 'java.png')

# 5. HTML
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
    
    # Number 5
    font = get_font(230, bold=True)
    bbox = d.textbbox((0, 0), '5', font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((cx - tw / 2, cy - th / 2 - 30), '5', font=font, fill=(255, 255, 255, 255))
    
    draw_label(d, 'HTML5')
    finish_and_save(im, 'html.png')

# 6. CSS
def make_css():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    # Blue shield
    pts = [
        (cx - 150, cy - 180),
        (cx + 150, cy - 180),
        (cx + 125, cy + 120),
        (cx, cy + 180),
        (cx - 125, cy + 120)
    ]
    d.polygon(pts, fill=(38, 77, 228, 255))
    
    # Right half lighter
    pts_r = [
        (cx, cy - 180),
        (cx + 150, cy - 180),
        (cx + 125, cy + 120),
        (cx, cy + 180)
    ]
    d.polygon(pts_r, fill=(41, 101, 241, 255))
    
    font = get_font(230, bold=True)
    bbox = d.textbbox((0, 0), '3', font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((cx - tw / 2, cy - th / 2 - 30), '3', font=font, fill=(255, 255, 255, 255))
    
    draw_label(d, 'CSS3')
    finish_and_save(im, 'css.png')

# 7. React
def make_react():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    cyan = (97, 218, 251, 255)
    # Center nucleus
    d.ellipse([cx - 36, cy - 36, cx + 36, cy + 36], fill=cyan)
    
    # 3 elliptical rings at angles 0, 60, 120
    # To draw rotated ellipses, we can draw on temporary layers and rotate
    for angle in [0, 60, 120]:
        t_im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        t_d = ImageDraw.Draw(t_im)
        t_d.ellipse([cx - 190, cy - 70, cx + 190, cy + 70], outline=cyan, width=16)
        rot_im = t_im.rotate(angle, center=(cx, cy), resample=Image.Resampling.BICUBIC)
        im = Image.alpha_composite(im, rot_im)
        
    d = ImageDraw.Draw(im)
    draw_label(d, 'React')
    finish_and_save(im, 'react.png')

# 8. SQL
def make_sql():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    # 3 database disks
    blue = (0, 122, 204, 255)
    cyan = (50, 180, 240, 255)
    
    for i, dy in enumerate([-100, -10, 80]):
        # Base/side
        d.chord([cx - 140, cy + dy, cx + 140, cy + dy + 100], start=0, end=180, fill=blue)
        d.rectangle([cx - 140, cy + dy + 20, cx + 140, cy + dy + 50], fill=blue)
        # Top cap
        d.ellipse([cx - 140, cy + dy, cx + 140, cy + dy + 60], fill=cyan if i == 0 else (30, 150, 220, 255))
        
    draw_label(d, 'SQL')
    finish_and_save(im, 'sql.png')

# 9. MySQL
def make_mysql():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    # Dolphin / wave emblem in cyan & orange
    teal = (0, 117, 143, 255)
    orange = (242, 145, 17, 255)
    
    # Swooping dolphin curve
    d.arc([cx - 160, cy - 180, cx + 160, cy + 140], start=190, end=350, fill=teal, width=48)
    d.chord([cx - 90, cy - 140, cx + 130, cy + 40], start=210, end=350, fill=teal)
    # Fin
    pts = [(cx + 20, cy - 130), (cx + 80, cy - 200), (cx + 60, cy - 100)]
    d.polygon(pts, fill=teal)
    # Dolphin eye
    d.ellipse([cx + 95, cy - 45, cx + 115, cy - 25], fill=(255, 255, 255, 255))
    # Orange wave below
    d.arc([cx - 140, cy + 30, cx + 140, cy + 180], start=0, end=180, fill=orange, width=28)
    
    draw_label(d, 'MySQL')
    finish_and_save(im, 'mysql.png')

# 10. MongoDB
def make_mongodb():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    # Green leaf emblem
    g1 = (71, 162, 72, 255)
    g2 = (61, 142, 62, 255)
    
    # Left half leaf
    pts_l = [
        (cx, cy - 180),
        (cx - 110, cy - 40),
        (cx - 90, cy + 90),
        (cx, cy + 170)
    ]
    d.polygon(pts_l, fill=g1)
    
    # Right half leaf
    pts_r = [
        (cx, cy - 180),
        (cx + 110, cy - 40),
        (cx + 90, cy + 90),
        (cx, cy + 170)
    ]
    d.polygon(pts_r, fill=g2)
    
    # Center vein
    d.line([(cx, cy - 170), (cx, cy + 165)], fill=(255, 255, 255, 180), width=6)
    
    draw_label(d, 'MongoDB')
    finish_and_save(im, 'mongodb.png')

# 11. VS Code
def make_vscode():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    # VS Code ribbon / bowtie origami
    blue1 = (0, 101, 181, 255)
    blue2 = (0, 122, 204, 255)
    blue3 = (31, 163, 239, 255)
    
    # Back wings
    d.polygon([(cx - 140, cy - 120), (cx - 30, cy - 20), (cx - 140, cy + 80), (cx - 180, cy + 50)], fill=blue1)
    d.polygon([(cx - 140, cy + 120), (cx - 30, cy + 20), (cx - 140, cy - 80), (cx - 180, cy - 50)], fill=blue1)
    # Right wing
    d.polygon([(cx - 30, cy - 160), (cx + 150, cy - 20), (cx + 150, cy + 20), (cx - 30, cy + 160)], fill=blue2)
    # Front fold
    d.polygon([(cx - 30, cy - 160), (cx + 110, cy - 20), (cx - 30, cy + 60)], fill=blue3)
    
    draw_label(d, 'VS Code')
    finish_and_save(im, 'vscode.png')

# 12. Google Antigravity
def make_antigravity():
    im = create_base()
    cx, cy = 400, 380
    
    # Sleek 4-color orbital gravity gyroscopic rings
    colors = [
        (66, 133, 244, 255),   # Blue
        (234, 67, 53, 255),    # Red
        (251, 188, 5, 255),    # Yellow
        (52, 168, 83, 255),    # Green
    ]
    
    for i, (col, angle) in enumerate(zip(colors, [0, 45, 90, 135])):
        t_im = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        t_d = ImageDraw.Draw(t_im)
        t_d.ellipse([cx - 180, cy - 80, cx + 180, cy + 80], outline=col, width=18)
        rot_im = t_im.rotate(angle, center=(cx, cy), resample=Image.Resampling.BICUBIC)
        im = Image.alpha_composite(im, rot_im)
        
    d = ImageDraw.Draw(im)
    # Central gravity core
    d.ellipse([cx - 40, cy - 40, cx + 40, cy + 40], fill=(255, 255, 255, 255))
    draw_label(d, 'Antigravity')
    finish_and_save(im, 'antigravity.png')

# 13. Cursor
def make_cursor():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    # Futuristic glowing isometric cube / prism
    v_top = (168, 85, 247, 255)
    v_left = (126, 34, 206, 255)
    v_right = (88, 28, 135, 255)
    
    r = 160
    # Top face
    d.polygon([(cx, cy - r), (cx + r * 0.866, cy - r * 0.5), (cx, cy), (cx - r * 0.866, cy - r * 0.5)], fill=v_top)
    # Left face
    d.polygon([(cx - r * 0.866, cy - r * 0.5), (cx, cy), (cx, cy + r), (cx - r * 0.866, cy + r * 0.5)], fill=v_left)
    # Right face
    d.polygon([(cx + r * 0.866, cy - r * 0.5), (cx, cy), (cx, cy + r), (cx + r * 0.866, cy + r * 0.5)], fill=v_right)
    
    # Center arrow mark / cursor pointer
    d.polygon([(cx - 30, cy - 60), (cx + 40, cy + 10), (cx, cy + 15), (cx - 10, cy + 50)], fill=(255, 255, 255, 255))
    
    draw_label(d, 'Cursor')
    finish_and_save(im, 'cursor.png')

# 14. Lovable
def make_lovable():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    # Stylized glowing magenta/pink heart emblem
    pink = (255, 46, 126, 255)
    # Left curve
    d.ellipse([cx - 140, cy - 140, cx, cy], fill=pink)
    # Right curve
    d.ellipse([cx, cy - 140, cx + 140, cy], fill=pink)
    # Bottom triangle
    pts = [(cx - 140, cy - 70), (cx + 140, cy - 70), (cx, cy + 140)]
    d.polygon(pts, fill=pink)
    
    draw_label(d, 'Lovable')
    finish_and_save(im, 'lovable.png')

# 15. GitHub
def make_github():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    # White Octocat silhouette
    white = (245, 245, 250, 255)
    
    # Head & ears
    d.ellipse([cx - 120, cy - 110, cx + 120, cy + 110], fill=white)
    # Left ear
    d.polygon([(cx - 110, cy - 50), (cx - 120, cy - 145), (cx - 45, cy - 95)], fill=white)
    # Right ear
    d.polygon([(cx + 110, cy - 50), (cx + 120, cy - 145), (cx + 45, cy - 95)], fill=white)
    
    # Body base
    d.chord([cx - 90, cy + 20, cx + 90, cy + 145], start=0, end=180, fill=white)
    
    draw_label(d, 'GitHub')
    finish_and_save(im, 'github.png')

# 16. Vercel
def make_vercel():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    # Pure clean equilateral triangle
    white = (255, 255, 255, 255)
    r = 160
    pts = [
        (cx, cy - r),
        (cx + r * 1.15, cy + r * 0.9),
        (cx - r * 1.15, cy + r * 0.9)
    ]
    d.polygon(pts, fill=white)
    
    draw_label(d, 'Vercel')
    finish_and_save(im, 'vercel.png')

# 17. Render
def make_render():
    im = create_base()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 380
    
    # Emerald green / cyan "R" emblem
    teal = (70, 227, 183, 255)
    # Stylized square / geometric R
    d.rectangle([cx - 120, cy - 140, cx - 40, cy + 140], fill=teal)
    d.arc([cx - 120, cy - 140, cx + 120, cy + 20], start=270, end=90, fill=teal, width=80)
    d.line([(cx, cy + 10), (cx + 110, cy + 140)], fill=teal, width=70)
    
    draw_label(d, 'Render')
    finish_and_save(im, 'render.png')

if __name__ == '__main__':
    make_python()
    make_c()
    make_cpp()
    make_java()
    make_html()
    make_css()
    make_react()
    make_sql()
    make_mysql()
    make_mongodb()
    make_vscode()
    make_antigravity()
    make_cursor()
    make_lovable()
    make_github()
    make_vercel()
    make_render()
    print('All logos built successfully!')

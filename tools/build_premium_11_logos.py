import math
from PIL import Image, ImageDraw, ImageFont

W, H = 800, 1000

def create_canvas():
    return Image.new('RGBA', (W, H), (0, 0, 0, 0))

def get_font(size, bold=True):
    names = ['arialbd.ttf' if bold else 'arial.ttf', 'SegoeUI-Bold.ttf', 'calibrib.ttf']
    for name in names:
        try:
            return ImageFont.truetype(name, size)
        except:
            continue
    return ImageFont.load_default()

def draw_label(draw, text, y=810, font_size=62, color=(240, 242, 248, 240)):
    font = get_font(font_size, bold=True)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    draw.text(((W - tw) / 2, y), text, font=font, fill=color)

# -----------------------------------------------------------------------------
# 1. PYTHON
# -----------------------------------------------------------------------------
def build_python():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 420
    s = 1.35
    
    # Official Python colors
    BLUE = (55, 118, 171, 255)
    YELLOW = (255, 212, 59, 255)
    WHITE = (255, 255, 255, 255)
    
    # Blue top/left snake
    d.rounded_rectangle([cx - 150*s, cy - 160*s, cx + 50*s, cy - 20*s], radius=int(60*s), fill=BLUE)
    d.rounded_rectangle([cx - 150*s, cy - 160*s, cx - 20*s, cy + 60*s], radius=int(50*s), fill=BLUE)
    d.rectangle([cx - 80*s, cy - 60*s, cx + 50*s, cy + 20*s], fill=BLUE)
    d.ellipse([cx - 65*s - 14*s, cy - 105*s - 14*s, cx - 65*s + 14*s, cy - 105*s + 14*s], fill=WHITE)
    
    # Yellow bottom/right snake
    d.rounded_rectangle([cx - 50*s, cy + 20*s, cx + 150*s, cy + 160*s], radius=int(60*s), fill=YELLOW)
    d.rounded_rectangle([cx + 20*s, cy - 60*s, cx + 150*s, cy + 160*s], radius=int(50*s), fill=YELLOW)
    d.rectangle([cx - 50*s, cy - 20*s, cx + 80*s, cy + 60*s], fill=YELLOW)
    d.ellipse([cx + 65*s - 14*s, cy + 105*s - 14*s, cx + 65*s + 14*s, cy + 105*s + 14*s], fill=WHITE)
    
    draw_label(d, 'Python')
    return im

# -----------------------------------------------------------------------------
# 2. SQL
# -----------------------------------------------------------------------------
def build_sql():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 420
    
    # Tiered database cylinder
    tiers = [cy - 140, cy, cy + 140]
    rw, rh = 210, 56
    
    # Bottom to top draw
    for i in reversed(range(3)):
        ty = tiers[i]
        # cylinder body
        if i < 2:
            next_y = tiers[i+1]
            # draw body rectangle connecting to next tier
            d.rectangle([cx - rw, ty, cx + rw, next_y], fill=(0, 110, 195, 255))
            # side shadow & center highlight
            d.rectangle([cx - rw, ty, cx - rw + 35, next_y], fill=(0, 75, 145, 255))
            d.rectangle([cx - 40, ty, cx + 40, next_y], fill=(0, 140, 235, 255))
            d.ellipse([cx - rw, next_y - rh, cx + rw, next_y + rh], fill=(0, 100, 185, 255))
        
        # Tier top disc
        d.ellipse([cx - rw, ty - rh, cx + rw, ty + rh], fill=(0, 155, 245, 255), outline=(130, 215, 255, 255), width=7)
        # Inner sheen
        d.ellipse([cx - rw + 28, ty - rh + 12, cx + rw - 28, ty + rh - 12], outline=(180, 235, 255, 160), width=4)
        
    draw_label(d, 'SQL')
    return im

# -----------------------------------------------------------------------------
# 3. REACT
# -----------------------------------------------------------------------------
def build_react():
    im = create_canvas()
    cx, cy = 400, 420
    
    CYAN = (97, 218, 251, 255)
    
    # Render 3 rotated ellipses
    for angle in [0, 60, 120]:
        e_img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
        ed = ImageDraw.Draw(e_img)
        rx, ry = 230, 85
        ed.ellipse([cx - rx, cy - ry, cx + rx, cy + ry], outline=CYAN, width=19)
        e_rot = e_img.rotate(angle, resample=Image.Resampling.BICUBIC, center=(cx, cy))
        im = Image.alpha_composite(im, e_rot)
        
    d = ImageDraw.Draw(im)
    # Nucleus
    cr = 38
    d.ellipse([cx - cr, cy - cr, cx + cr, cy + cr], fill=CYAN)
    
    draw_label(d, 'React')
    return im

# -----------------------------------------------------------------------------
# 4. ANTIGRAVITY (Official Geometric Mountain / Peak Logo)
# -----------------------------------------------------------------------------
def build_antigravity():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 420
    
    # Faceted mountain pyramid
    top = (cx, cy - 210)
    bl = (cx - 180, cy + 170)
    br = (cx + 180, cy + 170)
    center_ridge = (cx - 15, cy + 140)
    
    # Left main peak facet: luminous crisp silver-white
    d.polygon([top, bl, center_ridge], fill=(245, 248, 255, 255))
    
    # Right mountain facet: tech blue/slate
    d.polygon([top, center_ridge, br], fill=(68, 125, 215, 255))
    
    # Bottom reflective base facet: deep midnight indigo
    d.polygon([bl, center_ridge, (cx, cy + 170)], fill=(32, 58, 120, 255))
    d.polygon([center_ridge, br, (cx, cy + 170)], fill=(20, 38, 85, 255))
    
    # Subtle inner accent line for crisp geometric definition
    d.line([top, center_ridge], fill=(255, 255, 255, 230), width=5)
    d.line([top, bl], fill=(255, 255, 255, 200), width=4)
    d.line([top, br], fill=(130, 180, 255, 200), width=4)
    
    draw_label(d, 'Antigravity')
    return im

# -----------------------------------------------------------------------------
# 5. FLUTTER (Official Origami Wings Mark)
# -----------------------------------------------------------------------------
def build_flutter():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 410
    
    # Official Flutter colors
    SKY = (66, 165, 245, 255)
    CYAN_MID = (41, 182, 246, 255)
    NAVY = (1, 87, 155, 255)
    
    # Top primary diagonal slash
    # Top-right to center-left
    p1 = [(cx - 30, cy - 210), (cx + 170, cy - 210), (cx - 90, cy + 50), (cx - 190, cy + 50)]
    d.polygon(p1, fill=SKY)
    
    # Lower chevron top wing
    p2 = [(cx - 90, cy + 50), (cx + 10, cy + 50), (cx + 140, cy + 200), (cx + 40, cy + 200)]
    d.polygon(p2, fill=CYAN_MID)
    
    # Lower chevron fold corner (Navy overlap)
    p3 = [(cx - 15, cy + 125), (cx + 40, cy + 200), (cx - 65, cy + 200)]
    d.polygon(p3, fill=NAVY)
    
    draw_label(d, 'Flutter')
    return im

# -----------------------------------------------------------------------------
# 6. VERCEL (Official Equilateral Triangle)
# -----------------------------------------------------------------------------
def build_vercel():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 420
    
    h = 320
    side = h * 2 / math.sqrt(3)
    top = (cx, cy - h/2 - 20)
    bl = (cx - side/2, cy + h/2 - 20)
    br = (cx + side/2, cy + h/2 - 20)
    
    # Pure white with bevel
    d.polygon([top, bl, br], fill=(255, 255, 255, 255))
    # Subtle inner bevel line
    d.line([top, bl], fill=(255, 255, 255, 255), width=3)
    d.line([bl, br], fill=(230, 230, 235, 255), width=3)
    d.line([br, top], fill=(210, 210, 215, 255), width=3)
    
    draw_label(d, 'Vercel')
    return im

# -----------------------------------------------------------------------------
# 7. C++ (Official Blue Hexagon & Clean Lettering)
# -----------------------------------------------------------------------------
def build_cpp():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 415
    
    # Outer hexagon
    r = 195
    hex_pts = []
    for i in range(6):
        a = math.radians(i * 60 - 30)
        hex_pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        
    d.polygon(hex_pts, fill=(0, 89, 156, 255), outline=(101, 154, 210, 255), width=14)
    
    # Inner accent shield
    r_in = 168
    hex_in = []
    for i in range(6):
        a = math.radians(i * 60 - 30)
        hex_in.append((cx + r_in * math.cos(a), cy + r_in * math.sin(a)))
    d.polygon(hex_in, outline=(0, 115, 195, 180), width=6)
    
    # Bold white C++ text
    font = get_font(120, bold=True)
    bbox = d.textbbox((0, 0), 'C++', font=font)
    tw = bbox[2] - bbox[0]
    th = bbox[3] - bbox[1]
    d.text((cx - tw/2, cy - th/2 - 12), 'C++', font=font, fill=(255, 255, 255, 255))
    
    draw_label(d, 'C++')
    return im

# -----------------------------------------------------------------------------
# 8. GITHUB (Official Invertocat Silhouette)
# -----------------------------------------------------------------------------
def build_github():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 415
    
    WHITE = (255, 255, 255, 255)
    
    # Head circle
    hr = 155
    d.ellipse([cx - hr, cy - hr, cx + hr, cy + hr], fill=WHITE)
    
    # Left cat ear
    ear_l = [(cx - 150, cy - 40), (cx - 130, cy - 180), (cx - 40, cy - 135)]
    d.polygon(ear_l, fill=WHITE)
    
    # Right cat ear
    ear_r = [(cx + 150, cy - 40), (cx + 130, cy - 180), (cx + 40, cy - 135)]
    d.polygon(ear_r, fill=WHITE)
    
    # Whiskers / neck trim
    d.rounded_rectangle([cx - 120, cy + 90, cx + 120, cy + 175], radius=35, fill=WHITE)
    
    draw_label(d, 'GitHub')
    return im

# -----------------------------------------------------------------------------
# 9. HTML (Official HTML5 Shield & "HTML" Label)
# -----------------------------------------------------------------------------
def build_html():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 415
    
    # Shield points
    tl = (cx - 165, cy - 185)
    tr = (cx + 165, cy - 185)
    br = (cx + 138, cy + 125)
    bot = (cx, cy + 195)
    bl = (cx - 138, cy + 125)
    
    # Left half: orange
    d.polygon([tl, (cx, cy - 185), bot, bl], fill=(241, 101, 41, 255))
    # Right half: darker red-orange
    d.polygon([(cx, cy - 185), tr, br, bot], fill=(227, 76, 38, 255))
    
    # Stylized clean white "5" badge
    # Top bar
    d.polygon([(cx - 105, cy - 145), (cx + 105, cy - 145), (cx + 95, cy - 95), (cx - 100, cy - 95)], fill=(255, 255, 255, 255))
    # Middle bar & loop
    d.polygon([(cx - 95, cy - 95), (cx - 90, cy - 30), (cx + 90, cy - 30), (cx + 80, cy + 85), (cx, cy + 120), (cx - 80, cy + 70), (cx - 75, cy + 25), (cx - 30, cy + 25), (cx - 25, cy + 45), (cx, cy + 65), (cx + 40, cy + 45), (cx + 45, cy + 10), (cx - 92, cy + 10)], fill=(255, 255, 255, 255))
    
    draw_label(d, 'HTML')
    return im

# -----------------------------------------------------------------------------
# 10. FIGMA (Official 5-capsule logo + crisp upright typography)
# -----------------------------------------------------------------------------
def build_figma():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 400
    
    r = 54
    # Official Figma palette
    ORANGE = (242, 78, 30, 255)
    PURPLE = (162, 89, 255, 255)
    BLUE_V = (26, 188, 254, 255)
    GREEN  = (10, 207, 131, 255)
    PINK   = (255, 114, 98, 255)
    
    # Row 1
    d.rounded_rectangle([cx - 2*r, cy - 3*r, cx, cy - r], radius=r, fill=ORANGE)
    d.rounded_rectangle([cx, cy - 3*r, cx + 2*r, cy - r], radius=r, fill=PINK)
    
    # Row 2
    d.rounded_rectangle([cx - 2*r, cy - r, cx, cy + r], radius=r, fill=PURPLE)
    d.rounded_rectangle([cx, cy - r, cx + 2*r, cy + r], radius=r, fill=BLUE_V)
    
    # Row 3 (teardrop: rounded on left, square on right)
    d.rounded_rectangle([cx - 2*r, cy + r, cx, cy + 3*r], radius=r, fill=GREEN)
    d.rectangle([cx - r, cy + r, cx, cy + 2*r], fill=GREEN)
    
    draw_label(d, 'Figma')
    return im

# -----------------------------------------------------------------------------
# 11. CLAUDE (Official Anthropic Claude Terracotta Sunburst + upright text)
# -----------------------------------------------------------------------------
def build_claude():
    im = create_canvas()
    d = ImageDraw.Draw(im)
    cx, cy = 400, 400
    
    CLAUDE_ORANGE = (217, 119, 87, 255)
    
    # Multi-ray radiating starburst (14 organic rays)
    num_rays = 14
    for i in range(num_rays):
        angle = (i * 2 * math.pi / num_rays) + 0.15
        ray_len = 165 if (i % 2 == 0) else 140
        w = 26 if (i % 2 == 0) else 22
        
        # Ray points from center out
        dx = math.cos(angle)
        dy = math.sin(angle)
        px = -dy
        py = dx
        
        tip_x = cx + dx * ray_len
        tip_y = cy + dy * ray_len
        
        p = [
            (cx + px * w/2, cy + py * w/2),
            (tip_x + px * w/3, tip_y + py * w/3),
            (tip_x + dx * 12, tip_y + dy * 12),
            (tip_x - px * w/3, tip_y - py * w/3),
            (cx - px * w/2, cy - py * w/2),
        ]
        d.polygon(p, fill=CLAUDE_ORANGE)
        d.ellipse([tip_x - w/3, tip_y - w/3, tip_x + w/3, tip_y + w/3], fill=CLAUDE_ORANGE)
        
    d.ellipse([cx - 55, cy - 55, cx + 55, cy + 55], fill=CLAUDE_ORANGE)
    
    draw_label(d, 'Claude')
    return im

# -----------------------------------------------------------------------------
# Generate and downsample to 200x250 with Lanczos
# -----------------------------------------------------------------------------
generators = [
    ('python', build_python),
    ('sql', build_sql),
    ('react', build_react),
    ('antigravity', build_antigravity),
    ('flutter', build_flutter),
    ('vercel', build_vercel),
    ('cpp', build_cpp),
    ('github', build_github),
    ('html', build_html),
    ('figma', build_figma),
    ('claude', build_claude),
]

for name, gen in generators:
    high_res = gen()
    low_res = high_res.resize((200, 250), Image.Resampling.LANCZOS)
    low_res.save(f'public/tools/{name}.png')
    print(f'Successfully built public/tools/{name}.png')

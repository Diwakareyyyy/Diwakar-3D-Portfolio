"""
Build 15 cinematic, domain-specific project visuals for Scene 4 (Project Showcase).
Each project gets a tailored, high-detail dark UI / 3D diagram / HUD visual
consistent with the red-and-black cinematic theme.
"""

import os
import math
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "public", "projects")
os.makedirs(OUT_DIR, exist_ok=True)

# System fonts
def get_font(size, bold=False):
    try:
        path = "C:\\Windows\\Fonts\\segoeuib.ttf" if bold else "C:\\Windows\\Fonts\\segoeui.ttf"
        return ImageFont.truetype(path, size)
    except:
        try:
            path = "C:\\Windows\\Fonts\\arialbd.ttf" if bold else "C:\\Windows\\Fonts\\arial.ttf"
            return ImageFont.truetype(path, size)
        except:
            return ImageFont.load_default()

def get_mono_font(size):
    try:
        return ImageFont.truetype("C:\\Windows\\Fonts\\consola.ttf", size)
    except:
        return get_font(size)

def add_neon_frame(img, w, h, primary_col=(222, 27, 28), accent_col=(235, 95, 45)):
    """Creates a dark glass screen bezel with glowing red/amber rims and feathered alpha."""
    pad = 12
    # Create canvas with border pad
    card = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(card)
    
    # Outer rounded rect bounding
    r = 14
    box = [pad, pad, w - pad, h - pad]
    
    # Base dark glass background
    draw.rounded_rectangle(box, radius=r, fill=(12, 13, 18, 248), outline=(35, 38, 48, 255), width=2)
    
    # Paste content inside inner viewport
    inner_box = (pad + 4, pad + 4, w - pad - 4, h - pad - 4)
    inner_w = inner_box[2] - inner_box[0]
    inner_h = inner_box[3] - inner_box[1]
    
    # Rescale content image to fit inner area
    content_resized = img.resize((inner_w, inner_h), Image.Resampling.LANCZOS)
    
    # Mask for inner content rounded corners
    inner_mask = Image.new("L", (inner_w, inner_h), 0)
    ImageDraw.Draw(inner_mask).rounded_rectangle([0, 0, inner_w, inner_h], radius=r - 3, fill=255)
    
    card.paste(content_resized, (inner_box[0], inner_box[1]), inner_mask)
    
    # Draw glossy glass reflection sheen across upper half
    sheen = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(sheen)
    s_draw.polygon([
        (pad + 4, pad + 4),
        (w - pad - 4, pad + 4),
        (w - pad - 4, pad + int(inner_h * 0.35)),
        (pad + 4, pad + int(inner_h * 0.15))
    ], fill=(255, 255, 255, 14))
    card = Image.alpha_composite(card, sheen)
    
    # Glowing neon accent lines on top and bottom bevels
    c_draw = ImageDraw.Draw(card)
    c_draw.arc([pad, pad, pad + 2*r, pad + 2*r], 180, 270, fill=primary_col, width=2)
    c_draw.line([pad + r, pad, pad + int(inner_w * 0.65), pad], fill=primary_col, width=2)
    c_draw.line([pad, pad + r, pad, pad + int(inner_h * 0.45)], fill=primary_col, width=2)
    
    # Bottom corner accent
    c_draw.arc([w - pad - 2*r, h - pad - 2*r, w - pad, h - pad], 0, 90, fill=accent_col, width=2)
    c_draw.line([w - pad - int(inner_w * 0.4), h - pad, w - pad - r, h - pad], fill=accent_col, width=2)
    
    # Add subtle outer red glow drop shadow
    glow = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(glow)
    g_draw.rounded_rectangle([pad - 2, pad - 2, w - pad + 2, h - pad + 2], radius=r + 2, outline=(primary_col[0], primary_col[1], primary_col[2], 90), width=3)
    glow = glow.filter(ImageFilter.GaussianBlur(6))
    
    final_card = Image.alpha_composite(glow, card)
    return final_card

# --------------------------------------------------------------------------
# Content Renderers for all 15 Projects
# --------------------------------------------------------------------------

def draw_header(draw, title, short_name, cat, w, h, primary_color=(222, 27, 28)):
    """Draws top HUD bar with title, short badge, and category."""
    # Top bar
    draw.rectangle([0, 0, w, 38], fill=(16, 18, 25))
    draw.line([0, 38, w, 38], fill=(42, 46, 58), width=1)
    
    # Short name badge (Pill)
    badge_font = get_font(11, bold=True)
    draw.rounded_rectangle([12, 8, 12 + len(short_name)*7 + 22, 28], radius=4, fill=(primary_color[0], primary_color[1], primary_color[2], 50), outline=primary_color, width=1)
    draw.text((23, 11), short_name.upper(), font=badge_font, fill=(255, 220, 215))
    
    # Category / Title
    cat_font = get_font(10, bold=False)
    draw.text((12 + len(short_name)*7 + 34, 12), f"// {cat.upper()}", font=cat_font, fill=(160, 168, 185))
    
    # Status light
    draw.ellipse([w - 24, 14, w - 16, 22], fill=(46, 213, 115))
    draw.text((w - 74, 12), "LIVE", font=get_font(9, bold=True), fill=(46, 213, 115))

# 1. EVCDRP – Electric Vehicle Constraint-Aware Delivery Routing Problem
def render_evcdrp(w=960, h=576):
    img = Image.new("RGB", (w, h), (8, 9, 14))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "EV ROUTE OPTIMIZATION", "EVCDRP", "Intelligent EV Logistics Engine", w, h, (222, 27, 28))
    
    # High-tech GIS Map grid
    for x in range(30, w - 30, 48):
        draw.line([x, 50, x, h - 30], fill=(18, 22, 32), width=1)
    for y in range(50, h - 30, 48):
        draw.line([30, y, w - 30, y], fill=(18, 22, 32), width=1)
        
    # City roads & delivery route
    nodes = [
        (120, 420), (220, 360), (310, 220), (460, 180), (620, 240),
        (740, 160), (840, 280), (780, 440), (590, 460), (420, 390)
    ]
    # Draw neon route
    for i in range(len(nodes) - 1):
        draw.line([nodes[i], nodes[i+1]], fill=(222, 27, 28), width=4)
        draw.line([nodes[i], nodes[i+1]], fill=(255, 120, 100), width=1)
        
    # Station nodes
    for i, (nx, ny) in enumerate(nodes):
        is_depot = (i == 0)
        is_charge = (i in [3, 6])
        if is_depot:
            draw.ellipse([nx-10, ny-10, nx+10, ny+10], fill=(235, 95, 45), outline=(255, 255, 255), width=2)
            draw.text((nx+14, ny-8), "MAIN HUB", font=get_font(11, bold=True), fill=(255, 200, 180))
        elif is_charge:
            draw.ellipse([nx-9, ny-9, nx+9, ny+9], fill=(0, 210, 255), outline=(255, 255, 255), width=2)
            draw.text((nx+13, ny-8), f"FAST CHARGE #{i}", font=get_font(10, bold=True), fill=(100, 235, 255))
        else:
            draw.ellipse([nx-6, ny-6, nx+6, ny+6], fill=(222, 27, 28), outline=(255, 200, 200), width=1)
            draw.text((nx+10, ny-6), f"WP-{i:02d}", font=get_mono_font(9), fill=(180, 190, 210))
            
    # Floating Telemetry HUD Cards
    # Left HUD: Fleet SoC & Range
    draw.rounded_rectangle([44, 60, 310, 200], radius=8, fill=(14, 17, 25), outline=(45, 52, 70), width=1)
    draw.text((58, 72), "FLEET TELEMETRY [ACTIVE ROUTE]", font=get_font(11, bold=True), fill=(235, 95, 45))
    draw.text((58, 96), "Vehicle: Electric Van #EV-409", font=get_font(11), fill=(210, 215, 225))
    draw.text((58, 116), "Battery State of Charge: 86.4%", font=get_font(11, bold=True), fill=(46, 213, 115))
    # Battery progress bar
    draw.rounded_rectangle([58, 136, 290, 146], radius=4, fill=(24, 28, 40))
    draw.rounded_rectangle([58, 136, 58 + int(232 * 0.864), 146], radius=4, fill=(46, 213, 115))
    draw.text((58, 154), "Estimated Range: 312 km  |  Payload: 480 kg", font=get_font(10), fill=(160, 170, 190))
    draw.text((58, 172), "Dynamic Traffic Delay: -4.2 min (Compensated)", font=get_font(10), fill=(255, 180, 100))

    # Right HUD: Optimization Constraints
    draw.rounded_rectangle([w - 320, 60, w - 44, 200], radius=8, fill=(14, 17, 25), outline=(45, 52, 70), width=1)
    draw.text((w - 304, 72), "MULTI-OBJECTIVE CONSTRAINTS", font=get_font(11, bold=True), fill=(222, 27, 28))
    draw.text((w - 304, 96), "✓ Battery Degradation Factor: Minimized", font=get_font(10), fill=(200, 205, 220))
    draw.text((w - 304, 116), "✓ Time Windows Adherence: 99.8%", font=get_font(10), fill=(200, 205, 220))
    draw.text((w - 304, 136), "✓ Elevation & Grade Energy Recovery: ON", font=get_font(10), fill=(200, 205, 220))
    draw.text((w - 304, 156), "✓ Charging Station Queue Time: 0 min", font=get_font(10), fill=(200, 205, 220))
    draw.text((w - 304, 176), "Optimal Energy Saved: 34.6 kWh", font=get_font(11, bold=True), fill=(0, 210, 255))
    
    # Bottom Center Banner: Project Prominence
    draw.rounded_rectangle([w//2 - 280, h - 75, w//2 + 280, h - 20], radius=6, fill=(18, 20, 30), outline=(222, 27, 28), width=2)
    draw.text((w//2 - 260, h - 66), "EVCDRP — Electric Vehicle Constraint-Aware Delivery Routing Problem", font=get_font(12, bold=True), fill=(255, 240, 235))
    draw.text((w//2 - 260, h - 45), "AI Route Optimization considering Battery, Range, Load, Traffic & Charging", font=get_font(10), fill=(180, 185, 200))
    
    return img

# 2. AI-Powered Expense Tracker
def render_expense_tracker(w=768, h=546):
    img = Image.new("RGB", (w, h), (9, 10, 15))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "EXPENSE TRACKER", "AI Expense Tracker", "Flutter & OCR Intelligence", w, h, (235, 95, 45))
    
    # Mobile UI mockup on left
    mx, my, mw, mh = 50, 60, 260, 450
    draw.rounded_rectangle([mx, my, mx+mw, my+mh], radius=24, fill=(16, 18, 26), outline=(60, 66, 85), width=3)
    # Notch & speaker
    draw.rounded_rectangle([mx + mw//2 - 40, my + 8, mx + mw//2 + 40, my + 20], radius=6, fill=(8, 9, 12))
    # Mobile Screen Header
    draw.text((mx + 20, my + 34), "My Expenses", font=get_font(15, bold=True), fill=(255, 255, 255))
    draw.text((mx + 20, my + 56), "October 2026 Overview", font=get_font(9), fill=(160, 168, 185))
    # Big total balance card
    draw.rounded_rectangle([mx + 16, my + 80, mx + mw - 16, my + 155], radius=12, fill=(222, 27, 28))
    draw.text((mx + 28, my + 92), "Total Spent This Month", font=get_font(10), fill=(255, 220, 215))
    draw.text((mx + 28, my + 112), "$2,845.50", font=get_font(22, bold=True), fill=(255, 255, 255))
    
    # Donut chart preview in mobile
    draw.ellipse([mx + 30, my + 175, mx + 110, my + 255], outline=(235, 95, 45), width=10)
    draw.arc([mx + 30, my + 175, mx + 110, my + 255], 0, 140, fill=(222, 27, 28), width=10)
    draw.arc([mx + 30, my + 175, mx + 110, my + 255], 140, 260, fill=(0, 210, 255), width=10)
    
    draw.text((mx + 125, my + 180), "Food: 42%", font=get_font(9, bold=True), fill=(222, 27, 28))
    draw.text((mx + 125, my + 200), "Travel: 28%", font=get_font(9, bold=True), fill=(0, 210, 255))
    draw.text((mx + 125, my + 220), "Utilities: 18%", font=get_font(9, bold=True), fill=(235, 95, 45))
    
    # Recent Transactions in mobile
    tx_items = [("Uber Trip", "$24.50", "Travel"), ("Whole Foods", "$112.80", "Groceries"), ("Cloud Server", "$35.00", "Services")]
    for idx, (tname, tamt, tcat) in enumerate(tx_items):
        ty = my + 275 + idx * 48
        draw.rounded_rectangle([mx + 16, ty, mx + mw - 16, ty + 40], radius=8, fill=(22, 26, 36))
        draw.text((mx + 26, ty + 6), tname, font=get_font(10, bold=True), fill=(240, 245, 255))
        draw.text((mx + 26, ty + 22), tcat, font=get_font(8), fill=(140, 150, 170))
        draw.text((mx + mw - 65, ty + 12), tamt, font=get_font(10, bold=True), fill=(255, 120, 100))
        
    # Right panel: OCR Receipt Scanning Intelligence
    rx = 345
    draw.rounded_rectangle([rx, 60, w - 40, h - 40], radius=12, fill=(14, 16, 24), outline=(42, 48, 64), width=1)
    draw.text((rx + 20, 78), "OCR RECEIPT SCANNING PIPELINE", font=get_font(13, bold=True), fill=(235, 95, 45))
    
    # Receipt paper mockup
    draw.rectangle([rx + 20, 115, rx + 190, 370], fill=(245, 242, 235), outline=(180, 180, 180), width=1)
    draw.text((rx + 40, 130), "SUPERMARKET #402", font=get_mono_font(8), fill=(40, 40, 40))
    draw.text((rx + 40, 145), "Date: 2026-10-24 14:22", font=get_mono_font(7), fill=(80, 80, 80))
    draw.line([rx + 30, 160, rx + 180, 160], fill=(120, 120, 120), width=1)
    draw.text((rx + 35, 175), "Item 1 ......... $12.50", font=get_mono_font(8), fill=(50, 50, 50))
    draw.text((rx + 35, 195), "Item 2 ......... $45.00", font=get_mono_font(8), fill=(50, 50, 50))
    draw.text((rx + 35, 215), "Tax ............ $05.20", font=get_mono_font(8), fill=(50, 50, 50))
    draw.text((rx + 35, 245), "TOTAL .......... $62.70", font=get_mono_font(9), fill=(0, 0, 0))
    
    # Glowing Laser Scan Line
    draw.line([rx + 15, 205, rx + 195, 205], fill=(222, 27, 28), width=3)
    draw.line([rx + 15, 205, rx + 195, 205], fill=(255, 200, 180), width=1)
    
    # Bounding extraction boxes on receipt
    draw.rectangle([rx + 30, 170, rx + 180, 190], outline=(0, 210, 255), width=1)
    draw.rectangle([rx + 30, 240, rx + 180, 260], outline=(46, 213, 115), width=2)
    
    # Extracted JSON Schema on right
    jx = rx + 210
    draw.text((jx, 120), "Extracted Key-Value Entity:", font=get_font(11, bold=True), fill=(255, 255, 255))
    json_lines = [
        '{',
        '  "merchant": "Supermarket #402",',
        '  "date": "2026-10-24",',
        '  "category": "Groceries",',
        '  "total_amount": 62.70,',
        '  "currency": "USD",',
        '  "confidence": 0.994,',
        '  "payment_sync": "Google Pay"',
        '}'
    ]
    for idx, l in enumerate(json_lines):
        draw.text((jx + 8, 148 + idx * 20), l, font=get_mono_font(10), fill=(100, 235, 255) if ":" in l else (200, 205, 220))
        
    draw.rounded_rectangle([rx + 20, 400, w - 60, h - 55], radius=6, fill=(20, 24, 34))
    draw.text((rx + 32, 412), "✓ Instant OCR Parsing  ✓ Categorization  ✓ UPI/Wallet Integration", font=get_font(10, bold=True), fill=(46, 213, 115))
    draw.text((rx + 32, 432), "Built with Flutter & Dart for iOS & Android cross-platform performance.", font=get_font(9), fill=(160, 170, 190))
    
    return img

# 3. Personalized Cloud Storage Platform
def render_cloud_storage(w=880, h=700):
    img = Image.new("RGB", (w, h), (8, 9, 14))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "CLOUD STORAGE PLATFORM", "Personal Cloud", "Individual Allocation & Secure Access", w, h, (0, 180, 255))
    
    # 3D Cloud Topology & Node Cluster
    cx, cy = w // 2, 220
    # Central isometric cloud server cube
    draw.ellipse([cx - 240, cy - 80, cx + 240, cy + 80], outline=(30, 42, 65), width=1)
    draw.ellipse([cx - 160, cy - 50, cx + 160, cy + 50], outline=(0, 180, 255), width=2)
    
    # Central Server Icon / Hexagon
    pts = [(cx, cy - 70), (cx + 60, cy - 35), (cx + 60, cy + 35), (cx, cy + 70), (cx - 60, cy + 35), (cx - 60, cy - 35)]
    draw.polygon(pts, fill=(16, 24, 38), outline=(0, 210, 255))
    draw.text((cx - 42, cy - 14), "CLOUD CORE", font=get_font(11, bold=True), fill=(255, 255, 255))
    draw.text((cx - 36, cy + 6), "AES-256", font=get_mono_font(9), fill=(0, 210, 255))
    
    # 4 Satellites around core
    satellites = [
        (cx - 220, cy - 70, "User Space A", "256 GB"),
        (cx + 220, cy - 70, "User Space B", "512 GB"),
        (cx - 190, cy + 90, "Backup Vault", "1.0 TB"),
        (cx + 190, cy + 90, "Media Cluster", "750 GB")
    ]
    for sx, sy, sname, scap in satellites:
        draw.line([cx, cy, sx, sy], fill=(35, 75, 120), width=2)
        draw.rounded_rectangle([sx - 65, sy - 25, sx + 65, sy + 25], radius=8, fill=(14, 20, 32), outline=(0, 180, 255), width=1)
        draw.text((sx - 52, sy - 18), sname, font=get_font(10, bold=True), fill=(240, 245, 255))
        draw.text((sx - 52, sy + 2), f"Allocated: {scap}", font=get_mono_font(9), fill=(46, 213, 115))
        
    # Bottom Dashboard Panels
    # Panel 1: Storage Allocation Quota
    draw.rounded_rectangle([50, 350, 440, h - 50], radius=10, fill=(14, 17, 26), outline=(42, 48, 65), width=1)
    draw.text((70, 370), "USER STORAGE ALLOCATION", font=get_font(12, bold=True), fill=(0, 210, 255))
    draw.text((70, 400), "Active Plan: Personalized Dedicated Drive", font=get_font(10), fill=(200, 205, 220))
    # Big gauge bar
    draw.rounded_rectangle([70, 430, 420, 452], radius=6, fill=(24, 28, 40))
    draw.rounded_rectangle([70, 430, 70 + int(350 * 0.64), 452], radius=6, fill=(0, 180, 255))
    draw.text((70, 465), "Used: 1.28 TB / 2.00 TB (64%)", font=get_font(11, bold=True), fill=(255, 255, 255))
    
    file_types = [("Documents & Data", "420 GB", (0, 210, 255)), ("Media & Videos", "650 GB", (235, 95, 45)), ("Code Repos", "210 GB", (46, 213, 115))]
    for idx, (ftitle, fsize, fcol) in enumerate(file_types):
        fy = 500 + idx * 36
        draw.ellipse([70, fy + 4, 80, fy + 14], fill=fcol)
        draw.text((90, fy), ftitle, font=get_font(10), fill=(210, 215, 225))
        draw.text((360, fy), fsize, font=get_mono_font(10), fill=(255, 255, 255))
        
    # Panel 2: Secure File Access & Sync Activity
    draw.rounded_rectangle([470, 350, w - 50, h - 50], radius=10, fill=(14, 17, 26), outline=(42, 48, 65), width=1)
    draw.text((490, 370), "SECURE TRANSFER & SYNC METRICS", font=get_font(12, bold=True), fill=(46, 213, 115))
    
    sync_logs = [
        ("auth_token_refresh", "Success (OAuth2)", "2s ago"),
        ("project_assets.zip", "Uploaded (142 MB/s)", "42s ago"),
        ("dataset_backup.h5", "Encrypted & Synced", "3m ago"),
        ("client_contract.pdf", "Access Verified", "8m ago"),
        ("global_cdn_cache", "Synced (Frankfurt/Mumbai)", "12m ago")
    ]
    for idx, (fname, fstat, ftime) in enumerate(sync_logs):
        sy = 405 + idx * 46
        draw.rounded_rectangle([490, sy, w - 70, sy + 38], radius=6, fill=(20, 24, 34))
        draw.text((502, sy + 6), fname, font=get_mono_font(9), fill=(255, 255, 255))
        draw.text((502, sy + 20), fstat, font=get_font(8), fill=(0, 210, 255))
        draw.text((w - 145, sy + 12), ftime, font=get_mono_font(8), fill=(140, 150, 170))
        
    return img

# 4. SEVRA – GeoFace AI Assistant
def render_sevra(w=710, h=496):
    img = Image.new("RGB", (w, h), (9, 9, 14))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "GEOFACE AI ASSISTANT", "SEVRA", "Conversational Enterprise SaaS Assistant", w, h, (222, 27, 28))
    
    # Left: Glowing Neural AI Orb
    ox, oy = 160, h // 2 + 10
    for r in range(120, 20, -15):
        alpha = int(255 * (1 - r/120) * 0.4)
        draw.ellipse([ox - r, oy - r, ox + r, oy + r], outline=(222, 27, 28, alpha), width=1)
    draw.ellipse([ox - 45, oy - 45, ox + 45, oy + 45], fill=(222, 27, 28), outline=(255, 255, 255), width=2)
    draw.text((ox - 28, oy - 12), "SEVRA", font=get_font(12, bold=True), fill=(255, 255, 255))
    draw.text((ox - 24, oy + 8), "ONLINE", font=get_mono_font(8), fill=(255, 220, 210))
    
    # Audio spectrum below orb
    for i in range(24):
        bx = ox - 90 + i * 8
        bh = int(math.sin(i * 0.4) * 20 + 25)
        draw.line([bx, oy + 85 - bh//2, bx, oy + 85 + bh//2], fill=(235, 95, 45), width=3)
        
    # Right: Conversation Stream & Knowledge Engine
    rx = 320
    draw.rounded_rectangle([rx, 60, w - 30, h - 30], radius=10, fill=(14, 16, 24), outline=(45, 50, 68), width=1)
    draw.text((rx + 20, 78), "GEOFACE SAAS KNOWLEDGE ENGINE", font=get_font(12, bold=True), fill=(235, 95, 45))
    
    # Chat message 1 (User)
    draw.rounded_rectangle([rx + 20, 110, w - 50, 160], radius=8, fill=(22, 26, 38))
    draw.text((rx + 32, 120), "User:", font=get_font(9, bold=True), fill=(0, 210, 255))
    draw.text((rx + 32, 136), '"What are the upcoming releases for GeoFace enterprise attendance?"', font=get_font(10), fill=(240, 245, 255))
    
    # Chat message 2 (SEVRA AI)
    draw.rounded_rectangle([rx + 20, 175, w - 50, 285], radius=8, fill=(28, 20, 24), outline=(222, 27, 28), width=1)
    draw.text((rx + 32, 186), "SEVRA AI Assistant:", font=get_font(9, bold=True), fill=(222, 27, 28))
    ai_resp = [
        "GeoFace v3.2 launches Q4 2026 featuring:",
        "• Real-time anti-spoofing 3D depth liveness detection",
        "• Offline edge sync for industrial field locations",
        "• Automated payroll integration with SAP & Workday API"
    ]
    for idx, line in enumerate(ai_resp):
        draw.text((rx + 32, 208 + idx * 18), line, font=get_font(9), fill=(255, 230, 225) if "•" in line else (255, 255, 255))
        
    # Query Knowledge Graph metrics
    draw.rounded_rectangle([rx + 20, 305, w - 50, h - 50], radius=8, fill=(18, 20, 30))
    draw.text((rx + 32, 318), "Vector Search Latency: 18ms  |  Embedding: GeoFace-LLM-8B", font=get_mono_font(9), fill=(46, 213, 115))
    draw.text((rx + 32, 338), "Accuracy Confidence Score: 99.1% across company SaaS documentation", font=get_font(9), fill=(160, 170, 190))
    
    return img

# 5. VehicleGPT – Offline Vehicle Intelligence Assistant
def render_vehiclegpt(w=690, h=480):
    img = Image.new("RGB", (w, h), (8, 9, 14))
    draw = ImageDraw.Draw(img)
    draw_header(draw, "AUTOMOTIVE EDGE AI", "VehicleGPT", "On-Device Offline Vehicle Assistant", w, h, (222, 27, 28))
    
    # Modern Digital Cockpit Dashboard
    # Center Speedometer
    cx, cy = 180, 200
    draw.arc([cx - 100, cy - 100, cx + 100, cy + 100], 135, 405, fill=(40, 48, 65), width=12)
    draw.arc([cx - 100, cy - 100, cx + 100, cy + 100], 135, 310, fill=(222, 27, 28), width=12)
    draw.text((cx - 36, cy - 30), "108", font=get_font(36, bold=True), fill=(255, 255, 255))
    draw.text((cx - 18, cy + 16), "KM/H", font=get_font(10, bold=True), fill=(200, 210, 225))
    
    # Status badges
    draw.rounded_rectangle([cx - 70, 330, cx + 70, 360], radius=4, fill=(16, 24, 34), outline=(46, 213, 115), width=1)
    draw.text((cx - 55, 338), "● NO CLOUD REQ (EDGE)", font=get_mono_font(8), fill=(46, 213, 115))
    
    # Right Side: Vehicle Query Terminal
    rx = 330
    draw.rounded_rectangle([rx, 60, w - 30, h - 30], radius=10, fill=(14, 16, 24), outline=(45, 52, 70), width=1)
    draw.text((rx + 20, 78), "ON-DEVICE NATURAL LANGUAGE DIAGNOSTICS", font=get_font(11, bold=True), fill=(235, 95, 45))
    
    queries = [
        ("Query: \"Check tire pressure & brake pad wear\"", (0, 210, 255)),
        ("ECU Response: Front Left 33 PSI, Right 33 PSI (Normal)", (240, 245, 255)),
        ("Brake pads estimated remaining life: 18,400 km.", (46, 213, 115)),
        ("Query: \"When is next transmission fluid service due?\"", (0, 210, 255)),
        ("History Retrieved: Last changed at 42,000 km.", (240, 245, 255)),
        ("Next scheduled interval at 60,000 km (in 4,200 km).", (255, 180, 100)),
        ("CAN-Bus Status: All 18 microcontrollers synchronized.", (46, 213, 115))
    ]
    for idx, (qtext, qcol) in enumerate(queries):
        draw.text((rx + 20, 115 + idx * 28), qtext, font=get_mono_font(9), fill=qcol)
        
    # Bottom Vehicle Control Indicators
    draw.rounded_rectangle([rx + 20, 340, w - 50, h - 45], radius=6, fill=(20, 24, 34))
    draw.text((rx + 30, 355), "CAN Bus Read: OK  |  Battery: 12.8V  |  Engine Coolant: 90°C", font=get_mono_font(9), fill=(180, 190, 210))
    draw.text((rx + 30, 380), "Local Neural Model: 1.4B Param Quantized INT4 on NPU", font=get_font(9, bold=True), fill=(222, 27, 28))
    
    return img

# Remaining 10 Projects
def render_generic_project(title, short_name, cat, subtitle, details, color=(222, 27, 28), w=450, h=300):
    """Clean, high-density cinematic project card for the remaining 10 projects."""
    img = Image.new("RGB", (w, h), (10, 11, 16))
    draw = ImageDraw.Draw(img)
    draw_header(draw, title, short_name, cat, w, h, color)
    
    # Inner graphical representation
    draw.rounded_rectangle([20, 52, w - 20, h - 20], radius=8, fill=(15, 17, 25), outline=(38, 42, 56), width=1)
    
    # Main project title on card
    draw.text((36, 68), title, font=get_font(13, bold=True), fill=(255, 255, 255))
    draw.text((36, 90), subtitle, font=get_font(10), fill=(color[0], color[1], color[2]))
    
    # Grid lines / schematic
    for y in range(120, h - 50, 26):
        draw.line([36, y, w - 36, y], fill=(22, 26, 38), width=1)
        
    for idx, detail in enumerate(details):
        dy = 126 + idx * 26
        if dy < h - 40:
            draw.text((42, dy), f"• {detail}", font=get_font(9), fill=(205, 210, 225))
            
    # Bottom tag pill
    draw.rounded_rectangle([36, h - 42, w - 36, h - 26], radius=4, fill=(20, 24, 36))
    draw.text((46, h - 39), f"Verified Portfolio Project: {short_name}", font=get_mono_font(8), fill=(140, 150, 175))
    
    return img

# Generate all 15 images
def generate_all():
    print("Generating 15 Studio-Grade Project Assets...")
    
    # 1. EVCDRP (Main Featured)
    ev_img = render_evcdrp(960, 576)
    card_ev = add_neon_frame(ev_img, 492, 302, primary_col=(222, 27, 28), accent_col=(0, 210, 255))
    card_ev.save(os.path.join(OUT_DIR, "p01_evcdrp.png"))
    print("1/15 Created p01_evcdrp.png")
    
    # 2. AI Expense Tracker (Top Left)
    exp_img = render_expense_tracker(768, 546)
    card_exp = add_neon_frame(exp_img, 395, 280, primary_col=(235, 95, 45), accent_col=(222, 27, 28))
    card_exp.save(os.path.join(OUT_DIR, "p02_expense.png"))
    print("2/15 Created p02_expense.png")
    
    # 3. Personal Cloud (Top Right)
    cloud_img = render_cloud_storage(880, 700)
    card_cloud = add_neon_frame(cloud_img, 440, 360, primary_col=(0, 180, 255), accent_col=(46, 213, 115))
    card_cloud.save(os.path.join(OUT_DIR, "p03_cloud.png"))
    print("3/15 Created p03_cloud.png")
    
    # 4. SEVRA (Bottom Left)
    sevra_img = render_sevra(710, 496)
    card_sevra = add_neon_frame(sevra_img, 365, 255, primary_col=(222, 27, 28), accent_col=(235, 95, 45))
    card_sevra.save(os.path.join(OUT_DIR, "p04_sevra.png"))
    print("4/15 Created p04_sevra.png")
    
    # 5. VehicleGPT (Bottom Right)
    vgpt_img = render_vehiclegpt(690, 480)
    card_vgpt = add_neon_frame(vgpt_img, 350, 245, primary_col=(222, 27, 28), accent_col=(46, 213, 115))
    card_vgpt.save(os.path.join(OUT_DIR, "p05_vehiclegpt.png"))
    print("5/15 Created p05_vehiclegpt.png")
    
    # 6. Perry – Unsupervised Chatbot
    p6 = render_generic_project(
        "Perry – Unsupervised Chatbot", "Perry Bot", "AI & Unsupervised NLP",
        "Clustering & Latent Semantic Response Generator",
        ["Unsupervised conversational learning model", "Clustering & semantic context discovery", "Dynamic dialogue tree without labeled datasets"],
        color=(0, 210, 255), w=415, h=260
    )
    add_neon_frame(p6, 415, 260, primary_col=(0, 210, 255)).save(os.path.join(OUT_DIR, "p06_perry.png"))
    print("6/15 Created p06_perry.png")
    
    # 7. ICICDT 2026 – Conference Website
    p7 = render_generic_project(
        "ICICDT 2026 – Conference Website", "ICICDT 2026", "Academic Conference Portal",
        "International Conference on Devices, Circuits and Systems",
        ["Paper submission workflow & review portal", "Interactive keynote speaker schedules", "Attendee registrations & proceedings archive"],
        color=(235, 95, 45), w=360, h=248
    )
    add_neon_frame(p7, 360, 248, primary_col=(235, 95, 45)).save(os.path.join(OUT_DIR, "p07_icicdt.png"))
    print("7/15 Created p07_icicdt.png")
    
    # 8. Peri Baimmozhi – Symposium Website
    p8 = render_generic_project(
        "Peri Baimmozhi – Symposium", "Baimmozhi", "College Event Platform",
        "National Level Technical & Cultural Symposium Portal",
        ["Real-time event schedules & announcements", "Participant registration & team tracking", "Live scoring & prize announcement board"],
        color=(222, 27, 28), w=230, h=200
    )
    add_neon_frame(p8, 230, 200, primary_col=(222, 27, 28)).save(os.path.join(OUT_DIR, "p08_baimmozhi.png"))
    print("8/15 Created p08_baimmozhi.png")
    
    # 9. Glitch Yugam 2026 – Animated Event Website
    p9 = render_generic_project(
        "Glitch Yugam 2026", "Glitch Yugam", "Interactive Motion Web",
        "Cyberpunk Animated Symposium Digital Showcase",
        ["Custom WebGL & CSS canvas motion effects", "Interactive cyberpunk event challenges", "High-FPS visual transitions & particle scenes"],
        color=(0, 210, 255), w=175, h=205
    )
    add_neon_frame(p9, 175, 205, primary_col=(0, 210, 255)).save(os.path.join(OUT_DIR, "p09_glitch.png"))
    print("9/15 Created p09_glitch.png")
    
    # 10. Disaster Relief Distribution Management System
    p10 = render_generic_project(
        "Disaster Relief Management", "DRDMS", "Emergency Resource Logistics",
        "Inventory & Relief Supply Chain Platform",
        ["Real-time relief material inventory counts", "Emergency stock allocation by camp severity", "Resource dispatch GPS & volunteer coordination"],
        color=(235, 95, 45), w=215, h=206
    )
    add_neon_frame(p10, 215, 206, primary_col=(235, 95, 45)).save(os.path.join(OUT_DIR, "p10_drdms.png"))
    print("10/15 Created p10_drdms.png")
    
    # 11. OCR-Based Hackathon Project
    p11 = render_generic_project(
        "OCR Hackathon Solution", "OCR System", "Computer Vision & Text Extraction",
        "Automated Document & Receipt Parsing Engine",
        ["Optical character recognition for documents", "Multi-format image & scan extraction", "Key-value schema output with 99%+ accuracy"],
        color=(46, 213, 115), w=195, h=206
    )
    add_neon_frame(p11, 195, 206, primary_col=(46, 213, 115)).save(os.path.join(OUT_DIR, "p11_ocr.png"))
    print("11/15 Created p11_ocr.png")
    
    # 12. Civic Issue Reporter
    p12 = render_generic_project(
        "Civic Issue Reporter", "CIR", "Civic Engagement Platform",
        "Citizen Problem Reporting & Governance Portal",
        ["Citizen issue upload with photos & GPS", "Departmental review & status workflow", "Transparent resolution tracking by authorities"],
        color=(0, 210, 255), w=235, h=210
    )
    add_neon_frame(p12, 235, 210, primary_col=(0, 210, 255)).save(os.path.join(OUT_DIR, "p12_cir.png"))
    print("12/15 Created p12_cir.png")
    
    # 13. College Lost and Found Management System
    p13 = render_generic_project(
        "Lost & Found System", "CLFMS", "Campus Administration",
        "Item Verification & Custody Management",
        ["Digital logging of lost & found belongings", "Evidence & ownership verification forms", "HOD authorized item collection workflow"],
        color=(222, 27, 28), w=220, h=180
    )
    add_neon_frame(p13, 220, 180, primary_col=(222, 27, 28)).save(os.path.join(OUT_DIR, "p13_clfms.png"))
    print("13/15 Created p13_clfms.png")
    
    # 14. Buy, Sell and Exchange Marketplace
    p14 = render_generic_project(
        "Marketplace Platform", "Marketplace", "P2P Commerce & Barter",
        "Product Listing, Trading & Direct Exchange",
        ["Product listing with images & descriptions", "Buy, sell used goods, or exchange items", "Direct user chat and deal finalization"],
        color=(235, 95, 45), w=230, h=185
    )
    add_neon_frame(p14, 230, 185, primary_col=(235, 95, 45)).save(os.path.join(OUT_DIR, "p14_marketplace.png"))
    print("14/15 Created p14_marketplace.png")
    
    # 15. Jarvis – Voice-Controlled Mobile Assistant
    p15 = render_generic_project(
        "Jarvis Voice Assistant", "Jarvis AI", "Voice AI & Mobile Automation",
        "Bilingual English & Tamil Voice Automation",
        ["Flutter-based voice recognition system", "English & Tamil speech command parsing", "Automated app opening & phone device actions"],
        color=(0, 210, 255), w=225, h=180
    )
    add_neon_frame(p15, 225, 180, primary_col=(0, 210, 255)).save(os.path.join(OUT_DIR, "p15_jarvis.png"))
    print("15/15 Created p15_jarvis.png")
    
    print("\n[SUCCESS] All 15 projects rendered and saved to public/projects/!")

if __name__ == "__main__":
    generate_all()

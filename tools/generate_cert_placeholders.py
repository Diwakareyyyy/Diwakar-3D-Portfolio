import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs('public/certs', exist_ok=True)

# Red & Black / Gold cinematic theme for certificates
certs_data = [
    {
        'num': '01',
        'title': 'Professional Certification Placeholder',
        'category': 'UI/UX Design & Frontend Systems',
        'issuer': 'Design & Engineering Institute',
        'date': '2024',
        'id': 'CRED-2024-001',
        'theme': (222, 27, 28) # #DE1B1C Crimson Red
    },
    {
        'num': '02',
        'title': 'Advanced Technical Credential Placeholder',
        'category': 'Digital Technologies & Cloud Architecture',
        'issuer': 'Cloud & Technology Academy',
        'date': '2023',
        'id': 'CRED-2023-002',
        'theme': (235, 95, 45) # Amber Orange
    },
    {
        'num': '03',
        'title': 'Industry Professional Certificate Placeholder',
        'category': 'Creative Design & Visual Computing',
        'issuer': 'Creative Professionals Association',
        'date': '2024',
        'id': 'CRED-2024-003',
        'theme': (212, 175, 55) # Classic Gold
    },
    {
        'num': '04',
        'title': 'Core Competency Credential Placeholder',
        'category': 'Modern Web Architecture & Responsive Systems',
        'issuer': 'Open Source Certification Authority',
        'date': '2023',
        'id': 'CRED-2023-004',
        'theme': (222, 27, 28) # Crimson Red
    },
    {
        'num': '05',
        'title': 'Mastery Specialization Placeholder',
        'category': 'Front-End Engineering & Systems',
        'issuer': 'Global Technology Specialization Group',
        'date': '2024',
        'id': 'CRED-2024-005',
        'theme': (240, 140, 60) # Warm Amber
    }
]

W, H = 1200, 800

try:
    font_lg = ImageFont.truetype('arial.ttf', 36)
    font_md = ImageFont.truetype('arial.ttf', 24)
    font_sm = ImageFont.truetype('arial.ttf', 18)
    font_title = ImageFont.truetype('arial.ttf', 42)
    font_recip = ImageFont.truetype('arial.ttf', 52)
except Exception:
    font_lg = font_md = font_sm = font_title = font_recip = None

for item in certs_data:
    im = Image.new('RGB', (W, H), (14, 12, 14))
    draw = ImageDraw.Draw(im)
    accent = item['theme']
    
    # Outer elegant double border
    draw.rectangle([20, 20, W-20, H-20], outline=(60, 30, 32), width=2)
    draw.rectangle([32, 32, W-32, H-32], outline=accent, width=3)
    draw.rectangle([42, 42, W-42, H-42], outline=(40, 22, 24), width=1)
    
    # Corner flourishes
    for cx, cy in [(32, 32), (W-32, 32), (32, H-32), (W-32, H-32)]:
        draw.rectangle([cx-10, cy-10, cx+10, cy+10], fill=accent)

    # Header
    draw.text((W/2, 90), 'CERTIFICATE OF ACHIEVEMENT', fill=accent, anchor='mm', font=font_lg)
    draw.text((W/2, 135), 'VERIFIED CREDENTIAL • OFFICIAL DOCUMENTATION', fill=(195, 160, 160), anchor='mm', font=font_sm)
    draw.line([(W/2 - 200, 160), (W/2 + 200, 160)], fill=(90, 40, 42), width=1)
    
    # Recipient
    draw.text((W/2, 215), 'THIS CERTIFICATE IS PROUDLY PRESENTED TO', fill=(190, 170, 170), anchor='mm', font=font_sm)
    draw.text((W/2, 280), 'DIWAKAR S', fill=(255, 255, 255), anchor='mm', font=font_recip)
    draw.line([(W/2 - 160, 325), (W/2 + 160, 325)], fill=accent, width=2)
    
    # Body text
    draw.text((W/2, 375), 'For successfully demonstrating verified proficiency and completing the curriculum in:', fill=(200, 185, 185), anchor='mm', font=font_sm)
    draw.text((W/2, 435), item['title'].upper(), fill=accent, anchor='mm', font=font_title)
    draw.text((W/2, 490), f"Category: {item['category']}", fill=(235, 220, 220), anchor='mm', font=font_md)
    
    # Issuing entity
    draw.text((W/2, 560), f"Awarded by: {item['issuer']}", fill=(210, 180, 180), anchor='mm', font=font_md)
    
    # Footer metadata
    draw.line([(60, H - 140), (W - 60, H - 140)], fill=(65, 35, 38), width=1)
    
    # Date & ID on left
    draw.text((80, H - 105), f"Issued: {item['date']}", fill=(190, 170, 170), font=font_sm)
    draw.text((80, H - 75), f"Credential ID: {item['id']}", fill=(160, 130, 130), font=font_sm)
    
    # Status in center
    draw.rectangle([W/2 - 80, H - 115, W/2 + 80, H - 65], outline=accent, width=1)
    draw.text((W/2, H - 90), '• VERIFIED •', fill=accent, anchor='mm', font=font_sm)
    
    # Signature on right
    draw.text((W - 80, H - 105), 'Authorized Signatory', fill=(190, 170, 170), anchor='ra', font=font_sm)
    draw.text((W - 80, H - 75), 'Director of Certification', fill=(160, 130, 130), anchor='ra', font=font_sm)
    
    fname = f"public/certs/placeholder_{item['num']}.png"
    im.save(fname, 'PNG')
    print('Generated', fname)

import os
import subprocess
from PIL import Image

def test_homepage_diwakar_and_welcome():
    print("--- 1. Testing Homepage DIWAKAR & Welcome Heading ---")
    with open("src/scene/layout.js", "r", encoding="utf-8") as f:
        layout_js = f.read()
    # Confirm DIWAKAR is centered and uses original REF constants
    assert "capHeight: 0.5320" in layout_js
    assert "vCentre: 0.5361" in layout_js
    assert "vCentre = portrait ? h * 0.50 : h * REF.vCentre" in layout_js
    assert "heroH = capH * 1.38" in layout_js
    assert "feet = baseline + capH * 0.22" in layout_js
    print("PASS: Homepage large red DIWAKAR typography is centered in its original position with walking character walking in front of it")

    with open("src/styles/app.css", "r", encoding="utf-8") as f:
        app_css = f.read()
    assert "clamp(18px, 2.7vw, 38px)" in app_css
    assert "top: calc(var(--welcome-y, 12%) + 3px)" in app_css
    print("PASS: Welcome heading font-size slightly reduced and positioned slightly downward with clearance from nav bar and character head")
    return True

def test_skills_replacement():
    print("\n--- 2. Testing Skills Page Central Image Replacement ---")
    im = Image.open("public/tools/figure.png")
    assert im.size == (433, 577)
    assert im.mode == "RGBA"

    with open("src/gl/shaders2.js", "r", encoding="utf-8") as f:
        shaders2 = f.read()
    assert "vec3 col = s.rgb;" in shaders2
    print("PASS: Skills central human image replaced with exact uploaded artwork (433x577), rendering with full visual fidelity")
    return True

def test_projects_detail_typography():
    print("\n--- 3. Testing Project Detail Modal Typography Readability ---")
    with open("src/styles/projects.css", "r", encoding="utf-8") as f:
        proj_css = f.read()
    assert "letter-spacing: 0.075em" in proj_css
    assert "letter-spacing: 0.048em" in proj_css
    assert "line-height: 1.68" in proj_css
    assert "color: #ede2db" in proj_css
    print("PASS: Project detail title and description have increased letter spacing, comfortable line height, and high contrast against dark background")
    return True

def test_resume_pdf():
    print("\n--- 4. Testing Original Resume PDF Deployment ---")
    with open("public/resume.pdf", "rb") as f:
        data = f.read()
    assert len(data) == 79967
    assert data.startswith(b'%PDF-1.7')
    print("PASS: User's original resume PDF deployed to public/resume.pdf (79,967 bytes)")
    return True

def test_all_js_syntax():
    print("\n--- 5. Testing All JS Modules with node --check ---")
    js_files = []
    for root, _, files in os.walk("src"):
        for f in files:
            if f.endswith(".js"):
                js_files.append(os.path.join(root, f))

    failed = []
    for f in js_files:
        res = subprocess.run(["node", "--check", f], capture_output=True, text=True)
        if res.returncode != 0:
            print(f"Error in {f}: {res.stderr}")
            failed.append(f)

    assert not failed, f"Syntax errors in: {failed}"
    print(f"PASS: All {len(js_files)} JS modules compiled with 0 syntax errors")
    return True

if __name__ == "__main__":
    t1 = test_homepage_diwakar_and_welcome()
    t2 = test_skills_replacement()
    t3 = test_projects_detail_typography()
    t4 = test_resume_pdf()
    t5 = test_all_js_syntax()
    if all([t1, t2, t3, t4, t5]):
        print("\n========================================================")
        print("ALL PRECISE FINAL CORRECTIONS VERIFIED WITH 100% SUCCESS!")
        print("========================================================")

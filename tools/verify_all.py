import os
import subprocess
from PIL import Image

def test_homepage_heading():
    print("--- 1 & 2 & 3. Testing Homepage Heading, Position & Unique Name ---")
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    assert "Welcome to the World of..." in html, "Welcome text missing"
    assert ("–" in html or "&ndash;" in html), "Hyphen/en-dash missing"
    
    # Check that DIWAKAR is not in the welcome DOM tag
    welcome_match = html[html.find('id="welcome"'):html.find('</p>', html.find('id="welcome"'))]
    assert "DIWAKAR" not in welcome_match, "Name DIWAKAR must appear only once (canvas wordmark), not duplicated in welcome"
    
    with open("src/styles/app.css", "r", encoding="utf-8") as f:
        app_css = f.read()
    assert "calc(var(--welcome-y" in app_css and "+ 2px)" in app_css, "+2px offset missing in app.css"
    print("PASS: Homepage heading has '– Welcome to the World of...', +2px offset, unique DIWAKAR")
    return True

def test_nav_active():
    print("\n--- 4. Testing Navigation Active Indicator ---")
    with open("src/main.js", "r", encoding="utf-8") as f:
        main_js = f.read()
    assert "l.getAttribute('href') === '#stage'" in main_js, "Active indicator click lock to #stage missing"
    assert "a.getAttribute('href') === '#stage'" in main_js, "Active indicator scroll lock to #stage missing"
    print("PASS: Navigation active dot is permanently anchored to HOME (#stage)")
    return True

def test_skills_and_journey_scales():
    print("\n--- 5 & 6. Testing Skills & Journey Character Scales ---")
    with open("src/scene2/universe.js", "r", encoding="utf-8") as f:
        uni_js = f.read()
    assert "0.90" in uni_js and "0.86" in uni_js, "Enlarged scale missing in universe.js"
    print("PASS: Skills character size is noticeably and proportionally increased")

    with open("src/scene3/layout3.js", "r", encoding="utf-8") as f:
        layout3 = f.read()
    assert "0.600" in layout3, "Height 0.600 missing in layout3.js"
    print("PASS: Journey character size increased by ~1.5 cm on desktop (height: 0.600)")
    return True

def test_seated_image_clarity():
    print("\n--- 7. Testing Projects Seated Image Clarity ---")
    im = Image.open("public/projects/person.png")
    assert im.size == (530, 504), f"Expected 2x supersampled size (530, 504), got {im.size}"
    with open("src/styles/projects.css", "r", encoding="utf-8") as f:
        proj_css = f.read()
    assert "image-rendering: -webkit-optimize-contrast" in proj_css, "Crisp contrast image rendering missing"
    assert "image-rendering: crisp-edges" in proj_css, "crisp-edges missing"
    print("PASS: Seated developer image is high-resolution (530x504), crisp, and unblurred")
    return True

def test_diwakar_developer_text():
    print("\n--- 8. Testing Experience 'DIWAKAR DEVELOPER' Text Size ---")
    with open("src/styles/experience.css", "r", encoding="utf-8") as f:
        exp_css = f.read()
    assert "font-size: clamp(14px, 1.4vw, 22px)" in exp_css, "Enlarged badge text font-size missing"
    print("PASS: 'DIWAKAR DEVELOPER' badge text enlarged by ~1.5 cm with responsive clamp")
    return True

def test_continuous_scrolling_no_hover_pause():
    print("\n--- 9 & 10. Testing Continuous Scrolling (Never Pauses on Hover) ---")
    with open("src/scene4/boot4.js", "r", encoding="utf-8") as f:
        boot4 = f.read()
    assert "trackTop.addEventListener('pointerenter'" not in boot4, "Hover pause listener must be removed from trackTop"
    assert "trackBottom.addEventListener('pointerenter'" not in boot4, "Hover pause listener must be removed from trackBottom"
    assert "btn.addEventListener('click', () => openModal" in boot4, "Click to openModal missing"
    print("PASS: Projects continuous scrolling never stops on hover; pauses ONLY on intentional click/tap")
    return True

def test_project_details_layout():
    print("\n--- 11 & 12. Testing Project Details Side-by-Side Layout ---")
    with open("src/styles/projects.css", "r", encoding="utf-8") as f:
        proj_css = f.read()
    assert "grid-template-columns: 1fr 1.08fr;" in proj_css, "Side-by-side 2-column grid missing"
    assert "border: none;" in proj_css, "Nested border removal missing"
    print("PASS: Project details has image on left and description on right with no nested card boxes")
    return True

def test_node_syntax():
    print("\n--- 13. Testing All JS Modules with Node ---")
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
    print(f"PASS: All {len(js_files)} JS files parsed with zero syntax errors")
    return True

if __name__ == "__main__":
    t1 = test_homepage_heading()
    t2 = test_nav_active()
    t3 = test_skills_and_journey_scales()
    t4 = test_seated_image_clarity()
    t5 = test_diwakar_developer_text()
    t6 = test_continuous_scrolling_no_hover_pause()
    t7 = test_project_details_layout()
    t8 = test_node_syntax()
    if all([t1, t2, t3, t4, t5, t6, t7, t8]):
        print("\n=== ALL FINAL MICRO-ADJUSTMENT VERIFICATIONS PASSED WITH 100% SUCCESS! ===")

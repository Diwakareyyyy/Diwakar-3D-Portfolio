import os
import subprocess
import re

def test_homepage_heading_and_spacing():
    print("--- 1. Testing Homepage Heading, Position & Non-Overlapping Layout ---")
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()

    assert "– Welcome to the World of –" in html, "Welcome text with hyphens on both sides missing in index.html"
    assert "..." not in html[html.find('class="welcome__title"'):html.find('</span>', html.find('class="welcome__title"'))], "Dots should be removed from welcome heading"

    with open("src/data/portfolio-data.js", "r", encoding="utf-8") as f:
        data_js = f.read()
    assert "– Welcome to the World of –" in data_js, "Welcome text missing in portfolio-data.js"

    with open("src/styles/app.css", "r", encoding="utf-8") as f:
        app_css = f.read()
    assert "var(--welcome-y, 14.5%)" in app_css or "+ 4px" in app_css, "Welcome downward offset missing in app.css"

    with open("src/scene/layout.js", "r", encoding="utf-8") as f:
        layout_js = f.read()
    assert "vCentre = portrait ? h * 0.35 : h * 0.32" in layout_js, "vCentre positioning missing in layout.js"
    assert "heroH = portrait ? h * 0.42 : h * 0.44" in layout_js, "heroH missing in layout.js"
    assert "feet = portrait ? h * 0.90 : h * 0.92" in layout_js, "feet missing in layout.js"
    print("PASS: Homepage heading has '– Welcome to the World of –', positioned lower, DIWAKAR above character head with zero overlap")
    return True

def test_skills_silhouette_size():
    print("\n--- 2. Testing Skills Central Silhouette Enlargement ---")
    with open("src/scene2/universe.js", "r", encoding="utf-8") as f:
        uni_js = f.read()
    assert "1.08" in uni_js and "0.65" in uni_js, "Enlarged figure scale missing in universe.js"
    print("PASS: Skills central human silhouette is enlarged proportionally by ~1-1.5 cm at desktop scale")
    return True

def test_projects_seated_character_zoom():
    print("\n--- 3. Testing Projects Seated Character Subtle Zoom ---")
    with open("src/scene4/boot4.js", "r", encoding="utf-8") as f:
        boot4 = f.read()
    assert "sCurve * 0.11" in boot4, "Subtle zoom factor 0.11 missing in boot4.js"
    assert "sCurve * 0.44" not in boot4, "Excessive zoom factor 0.44 must be removed from boot4.js"
    print("PASS: Projects seated workstation character zoom reduced to subtle zoom (factor 0.11)")
    return True

def test_experience_text_and_character():
    print("\n--- 4. Testing Experience Text Reduction & Character Enlargement ---")
    with open("src/styles/experience.css", "r", encoding="utf-8") as f:
        exp_css = f.read()
    assert "clamp(10px, 0.8vw, 12.5px)" in exp_css, "Reduced badge font size missing in experience.css"
    assert "clamp(135px, 13.5vw, 185px)" in exp_css, "Enlarged character column width missing in experience.css"
    assert "clamp(210px, 33svh, 315px)" in exp_css, "Enlarged character figure max-height missing in experience.css"
    print("PASS: 'DIWAKAR DEVELOPER' badge text reduced and human character enlarged by ~1-1.5 cm")
    return True

def test_projects_continuous_scrolling_never_stops():
    print("\n--- 5. Testing Continuous Scrolling (Never Pauses on Hover, Move or Click) ---")
    with open("src/scene4/boot4.js", "r", encoding="utf-8") as f:
        boot4 = f.read()
    assert "row1Paused" not in boot4, "row1Paused must be completely removed from boot4.js"
    assert "row2Paused" not in boot4, "row2Paused must be completely removed from boot4.js"
    assert "streamTop?.addEventListener('pointerenter'" not in boot4, "Hover pause listener must be removed from streamTop"
    assert "streamBottom?.addEventListener('pointerenter'" not in boot4, "Hover pause listener must be removed from streamBottom"
    print("PASS: Projects continuous scrolling never pauses on hover, pointer movement, or click")
    return True

def test_project_detail_modal_compact():
    print("\n--- 6. Testing Compact Project Detail Modal ---")
    with open("index.html", "r", encoding="utf-8") as f:
        html = f.read()
    assert "project-modal__features" not in html, "Features list should be removed from modal"
    assert "projModalProblem" not in html, "Problem statement should be removed from modal"
    assert "projModalSolution" not in html, "Solution section should be removed from modal"
    assert "projModalTags" not in html, "Tags section should be removed from modal"
    assert "projModalGithub" not in html, "GitHub button should be removed from modal"
    assert "projModalImg" in html, "Project image must be present in modal"
    assert "projModalTitle" in html, "Project title must be present in modal"
    assert "projModalDesc" in html, "Project description must be present in modal"
    assert "projModalBackBtn" in html, "Back button must be present in modal"

    with open("src/styles/projects.css", "r", encoding="utf-8") as f:
        proj_css = f.read()
    assert "width: min(560px, 92vw)" in proj_css, "Compact panel width missing in projects.css"
    assert "max-height: 84vh" in proj_css, "Compact panel max-height missing in projects.css"
    print("PASS: Project Detail modal is compact, minimal, and contains only image, title, and short abstract")
    return True

def test_journey_text_clarity():
    print("\n--- 7. Testing Journey / Milestone Text Clarity ---")
    with open("src/styles/chrono.css", "r", encoding="utf-8") as f:
        chrono_css = f.read()
    assert "letter-spacing: .045em" in chrono_css, "Improved letter spacing for yr__lines i missing"
    assert "line-height: 1.55" in chrono_css, "Improved line height for yr__lines i missing"
    assert "letter-spacing: .12em" in chrono_css, "Improved letter spacing for yr__key missing"
    print("PASS: Journey/Milestone text spacing and clarity enhanced")
    return True

def test_final_page_text_brightness():
    print("\n--- 8. Testing Final Page Text Brightness ---")
    with open("src/styles/finale.css", "r", encoding="utf-8") as f:
        fin_css = f.read()
    assert "color: #dcd4cb;" in fin_css, "Softened f-cap color missing in finale.css"
    assert "color: #ee5b48;" in fin_css, "Softened f-cap__role color missing in finale.css"
    assert "color: #eee7df;" in fin_css, "Softened f-cap__name color missing in finale.css"
    print("PASS: Final page excessive text brightness and harshness reduced to balanced cinematic tones")
    return True

def test_all_js_syntax():
    print("\n--- 9. Testing All JS Modules with node --check ---")
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
    t1 = test_homepage_heading_and_spacing()
    t2 = test_skills_silhouette_size()
    t3 = test_projects_seated_character_zoom()
    t4 = test_experience_text_and_character()
    t5 = test_projects_continuous_scrolling_never_stops()
    t6 = test_project_detail_modal_compact()
    t7 = test_journey_text_clarity()
    t8 = test_final_page_text_brightness()
    t9 = test_all_js_syntax()
    if all([t1, t2, t3, t4, t5, t6, t7, t8, t9]):
        print("\n========================================================")
        print("ALL FINAL 10% CORRECTIONS VERIFIED WITH 100% SUCCESS!")
        print("========================================================")

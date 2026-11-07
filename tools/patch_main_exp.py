with open('src/main.js', 'r', encoding='utf-8') as f:
    code = f.read()

code = code.replace(
    "import { initExperienceSlider } from './experience/slider.js';",
    "import { initExperience } from './experience/bootExp.js';"
)

code = code.replace(
    "initExperienceSlider();",
    "initExperience();"
)

with open('src/main.js', 'w', encoding='utf-8') as f:
    f.write(code)

print("Updated main.js with initExperience!")

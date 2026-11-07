import cv2
from PIL import Image
import numpy as np

img = cv2.imread('section 5 main refrence.jpg')
h, w = img.shape[:2]

# Let's crop several areas:
# 1. Top left (y: 0 to 450, x: 0 to 500)
cv2.imwrite('tools/crop_tl.jpg', img[0:450, 0:500])

# 2. Bottom left (y: 650 to 900, x: 0 to 400)
cv2.imwrite('tools/crop_bl.jpg', img[650:900, 0:400])

# 3. Top right (y: 0 to 300, x: 1200:1600)
cv2.imwrite('tools/crop_tr.jpg', img[0:300, 1200:1600])

# 4. Bottom right (y: 650 to 900, x: 1200:1600)
cv2.imwrite('tools/crop_br.jpg', img[650:900, 1200:1600])

print("Crops written successfully")

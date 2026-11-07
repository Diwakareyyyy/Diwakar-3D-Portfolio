import os
from PIL import Image

p1 = 'public/certs/plate.jpg'
p2 = 'section 5 main refrence.jpg'
print(p1, os.path.exists(p1))
print(p2, os.path.exists(p2))

if os.path.exists(p1):
    im = Image.open(p1)
    print('plate.jpg size:', im.size)
if os.path.exists(p2):
    im2 = Image.open(p2)
    print('section 5 main refrence.jpg size:', im2.size)

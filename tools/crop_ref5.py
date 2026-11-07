from PIL import Image

# Let's inspect where text might be in section 5 main refrence.jpg
# Or check if OCR or visual difference exists between plate.jpg and section 5 main refrence.jpg
im = Image.open('section 5 main refrence.jpg')
# Crop top left (around x=0..600, y=0..350)
crop1 = im.crop((0, 0, 600, 350))
crop1.save('tools/ref5_top_left.jpg')

# Crop around title area
crop2 = im.crop((200, 100, 800, 400))
crop2.save('tools/ref5_title_area.jpg')

print('Saved crops of section 5 reference')

import cv2
import numpy as np
import json
import os

cap = cv2.VideoCapture('1000306733-Picsart-BackgroundRemover.webm')
w = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
h = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
total = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

boxes = []
idx = 0
first_frame = None

while True:
    ret, frame = cap.read()
    if not ret:
        break
    if idx == 0:
        first_frame = frame.copy()
        # Save poster
        cv2.imwrite('public/media/hero_new.jpg', frame, [cv2.IMWRITE_JPEG_QUALITY, 90])
    
    # Grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    mask = gray > 12
    if np.any(mask):
        ys, xs = np.where(mask)
        x0 = float(xs.min()) / w
        x1 = float(xs.max()) / w
        y0 = float(ys.min()) / h
        y1 = float(ys.max()) / h
    else:
        x0, y0, x1, y1 = 0.2, 0.05, 0.8, 0.95
    boxes.append([round(x0, 4), round(y0, 4), round(x1, 4), round(y1, 4)])
    idx += 1

cap.release()

print(f'Computed {len(boxes)} bounding boxes.')
print('First box:', boxes[0])
print('Middle box:', boxes[len(boxes)//2])
print('Last box:', boxes[-1])

# Save track to file
with open('public/media/hero_track.json', 'w') as f:
    json.dump({'frames': boxes, 'w': w, 'h': h, 'fps': 30, 'count': idx}, f, indent=2)

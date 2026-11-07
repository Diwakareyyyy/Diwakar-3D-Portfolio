import cv2
import numpy as np

cap = cv2.VideoCapture('1000306733-Picsart-BackgroundRemover.webm')
frames = []
idx = 0
boxes = []

while True:
    ret, frame = cap.read()
    if not ret:
        break
    # In BGR frame, where the background is removed, what is the color?
    # Let's inspect frame[0, 0]
    if idx % 30 == 0:
        corner = frame[0, 0]
        center = frame[frame.shape[0]//2, frame.shape[1]//2]
        print(f'Frame {idx}: corner BGR={corner}, center BGR={center}')
    idx += 1

cap.release()
print('Total read frames:', idx)

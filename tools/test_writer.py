import cv2
import numpy as np

# Test writing 10 frames
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter('tools/test_out.mp4', fourcc, 30.0, (720, 1280))
for i in range(10):
    f = np.zeros((1280, 720, 3), dtype=np.uint8)
    out.write(f)
out.release()
import os
print('Written test MP4 size:', os.path.getsize('tools/test_out.mp4'))

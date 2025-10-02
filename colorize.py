import cv2
import numpy as np

def apply_colorization(img):
    # Convert to grayscale if not already
    if len(img.shape) == 3 and img.shape[2] == 3:
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    else:
        gray = img

    # Apply colormap (you can try others too)
    colored = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
    return colored

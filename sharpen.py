import cv2
import numpy as np

def apply_laplacian_sharpening(image):
    # Convert to LAB and apply CLAHE to L channel
    lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
    l, a, b = cv2.split(lab)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    cl = clahe.apply(l)
    enhanced_lab = cv2.merge((cl, a, b))
    result = cv2.cvtColor(enhanced_lab, cv2.COLOR_LAB2BGR)

    # Smooth with bilateral filter to preserve edges but remove noise
    result = cv2.bilateralFilter(result, 9, 75, 75)
    return result
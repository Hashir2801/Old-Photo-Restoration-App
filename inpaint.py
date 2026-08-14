import cv2
import numpy as np

def apply_inpainting(image):
    print("[INFO] Detecting scratches/folds for inpainting...")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Detect white spots
    mask = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)[1]
    mask = cv2.dilate(mask, np.ones((5, 5), np.uint8), iterations=2)

    # Detect fold lines
    edges = cv2.Canny(gray, 30, 150)
    edges = cv2.dilate(edges, np.ones((3, 3), np.uint8), iterations=1)

    # Combine both masks
    final_mask = cv2.bitwise_or(mask, edges)

    # Apply inpainting
    inpainted = cv2.inpaint(image, final_mask, 3, cv2.INPAINT_TELEA)

    return inpainted
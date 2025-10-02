from PIL import Image, ImageChops, ImageEnhance
import numpy as np
import cv2

def apply_ela(image_path, quality=90):
    temp_filename = "temp_ela.jpg"
    Image.fromarray(cv2.cvtColor(image_path, cv2.COLOR_BGR2RGB)).save(temp_filename, "JPEG", quality=quality)

    original = Image.fromarray(cv2.cvtColor(image_path, cv2.COLOR_BGR2RGB))
    compressed = Image.open(temp_filename)

    ela_image = ImageChops.difference(original, compressed)
    extrema = ela_image.getextrema()
    max_diff = max([ex[1] for ex in extrema])
    if max_diff == 0:
        max_diff = 1
    scale = 255.0 / max_diff

    ela_image = ImageEnhance.Brightness(ela_image).enhance(scale)
    ela_np = np.array(ela_image)
    return cv2.cvtColor(ela_np, cv2.COLOR_RGB2BGR)

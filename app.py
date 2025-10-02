# app.py

import os
from utils import load_image, save_image, show_image
from enhancement import apply_histogram_equalization
from denoise import apply_median_filter, apply_gaussian_filter
from inpaint import apply_inpainting
from colorize import apply_colorization
from ela import apply_ela
from sharpen import apply_laplacian_sharpening  

def restore_photo(image_path, save_path):
    img = load_image(image_path)
    if img is None:
        print("[ERROR] Image not found. Check the filename or path.")
        return

    print("[INFO] Original image loaded.")

    # Step-by-step image restoration process
    step1 = apply_histogram_equalization(img)        # Improve contrast
    step2 = apply_median_filter(step1)               # Remove noise (salt-and-pepper)
    step3 = apply_gaussian_filter(step2)             # Smooth Texture
    ela_result = apply_ela(step3)
    step4 = apply_inpainting(ela_result)             # Remove scratches + fold lines
    final = apply_laplacian_sharpening(step4)        # Enhance sharpness & clarity

    colorized = apply_colorization(final)
    final = colorized

    save_image(final, save_path)
    print(f"[INFO] Restored image saved to: {save_path}")
    show_image("Original", img)
    show_image("Restored", final)

if __name__ == "__main__":
    original_path = os.path.join("original_images", "old_photo.jpg")  # change filename as needed
    save_path = os.path.join("restored_images", "restored_photo.jpg")
    restore_photo(original_path, save_path)

# metrics.py
from skimage.metrics import peak_signal_noise_ratio, structural_similarity
import cv2

def calculate_metrics(original, restored):
    original_gray = cv2.cvtColor(original, cv2.COLOR_BGR2GRAY)
    restored_gray = cv2.cvtColor(restored, cv2.COLOR_BGR2GRAY)

    psnr = peak_signal_noise_ratio(original_gray, restored_gray)
    ssim = structural_similarity(original_gray, restored_gray)

    return psnr, ssim

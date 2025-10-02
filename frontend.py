# frontend.py
import streamlit as st
import os
import cv2
import numpy as np
from enhancement import apply_histogram_equalization
from denoise import apply_median_filter, apply_gaussian_filter
from inpaint import apply_inpainting
from utils import save_image
from metrics import calculate_metrics

st.title("📸 Old Photo Restoration App")
st.write("Upload an old/damaged photo and see the magic!")

uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    # Read image
    file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, 1)

    st.image(img, caption="Original Image", use_container_width=True)

    st.write("Restoring image...")

    # Step-by-step restoration
    step1 = apply_histogram_equalization(img)
    step2 = apply_median_filter(step1, kernel_size=5)
    step3 = apply_gaussian_filter(step2, kernel_size=5)
    step4 = apply_inpainting(step3)
    final = step4  # You can add sharpening or colorization if desired

    # Show result
    st.image(final, caption="Restored Image", use_container_width=True)

    # Save output
    save_path = os.path.join("restored_images", uploaded_file.name)
    save_image(final, save_path)

    # Quality metrics
    psnr_val, ssim_val = calculate_metrics(img, final)
    st.markdown(f"**🔬 PSNR:** {psnr_val:.2f} dB")
    st.markdown(f"**🧠 SSIM:** {ssim_val:.4f}")

    # Download button
    is_success, im_buf_arr = cv2.imencode(".jpg", final)
    if is_success:
        st.download_button(label="📥 Download Restored Image",
                           data=im_buf_arr.tobytes(),
                           file_name="restored_" + uploaded_file.name,
                           mime="image/jpeg")

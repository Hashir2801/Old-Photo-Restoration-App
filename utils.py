import cv2
import os

def load_image(path):
    return cv2.imread(path)

def save_image(image, path):
    directory = os.path.dirname(path)
    if directory:
        os.makedirs(directory, exist_ok=True)
    return cv2.imwrite(path, image)

def show_image(window_name, image):
    # Desktop OpenCV windows are not supported on Streamlit Cloud.
    # Images should be displayed with st.image() in the Streamlit frontend.
    return None
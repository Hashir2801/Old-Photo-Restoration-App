# 📸 Old Photo Restoration App

A web-based image restoration application that enhances old or damaged
photographs using digital image processing techniques. The application
allows users to upload a photo, automatically process it, compare the
original and restored versions, view quality metrics, and download the
restored image.

## ✨ Features

-   Upload JPG, JPEG, PNG, and BMP images
-   Automatic contrast enhancement
-   Median filtering for noise reduction
-   Gaussian filtering for image smoothing
-   Inpainting for scratches and damaged areas
-   Laplacian/CLAHE-based sharpening for improved clarity
-   Side-by-side original and restored image preview
-   PSNR and SSIM quality metrics
-   Download the restored image
-   Flask-based web interface
-   Ready for deployment on Vercel

## 🛠️ Technologies Used

-   Python
-   Flask
-   OpenCV
-   NumPy
-   scikit-image
-   HTML & CSS
-   Vercel

## 🔄 Restoration Pipeline

The uploaded image is processed through the following stages:

1.  Histogram Equalization --- improves image contrast.
2.  Median Filtering --- reduces salt-and-pepper noise.
3.  Gaussian Filtering --- smooths the image.
4.  Inpainting --- attempts to repair scratches, folds, and damaged
    regions.
5.  Sharpening --- improves perceived detail and clarity.
6.  Quality Evaluation --- calculates PSNR and SSIM values.

## 📁 Project Structure

``` text
Old-Photo-Restoration-App/
├── app.py
├── enhancement.py
├── denoise.py
├── inpaint.py
├── sharpen.py
├── metrics.py
├── requirements.txt
├── vercel.json
└── README.md
```

## 🚀 Run Locally

Clone the repository and open the project directory.

Create and activate a virtual environment if desired, then install the
dependencies:

``` bash
pip install -r requirements.txt
```

Run the Flask application:

``` bash
python app.py
```

Open the following address in your browser:

``` text
http://127.0.0.1:5000
```

## ☁️ Deployment

The project includes a `vercel.json` configuration and is structured for
deployment as a Python Flask application on Vercel.

Push the project files to GitHub, import the repository into Vercel, and
deploy it.

## 📊 Quality Metrics

**PSNR (Peak Signal-to-Noise Ratio)** provides a numerical comparison
between the original and processed image.

**SSIM (Structural Similarity Index)** measures structural similarity
between the original and restored images.

These metrics are displayed after the restoration process.

## ⚠️ Note

This project uses traditional digital image processing techniques.
Results can vary depending on the type and severity of damage in the
uploaded photograph.

## 📄 License

This project is intended for educational and portfolio purposes.

import cv2
import numpy as np
from flask import Flask, request, render_template_string, send_file
from io import BytesIO
import base64

from enhancement import apply_histogram_equalization
from denoise import apply_median_filter, apply_gaussian_filter
from inpaint import apply_inpainting
from sharpen import apply_laplacian_sharpening
from metrics import calculate_metrics

app = Flask(__name__)
LAST_RESULT = None

HTML = """
<!doctype html>
<html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Old Photo Restoration</title>
<style>
body{margin:0;font-family:Arial;background:#0b1020;color:#eef2ff}.wrap{max-width:1100px;margin:auto;padding:50px 20px}
h1{font-size:42px;margin-bottom:8px}.sub{color:#aab4cf;margin-bottom:30px}.card{background:#151c30;border:1px solid #29324b;border-radius:18px;padding:25px}
form{display:flex;gap:12px;flex-wrap:wrap}input{background:#0f1526;padding:13px;border:1px solid #303b59;border-radius:10px;color:white;flex:1}
button,.download{border:0;border-radius:10px;padding:14px 22px;font-weight:bold;background:#6d7cff;color:white;text-decoration:none;cursor:pointer}
.grid{display:grid;grid-template-columns:1fr 1fr;gap:20px;margin-top:28px}.panel{background:#101729;border-radius:15px;padding:15px}
img{width:100%;border-radius:10px}.metrics{display:flex;gap:15px;margin:20px 0}.metric{background:#101729;padding:15px 20px;border-radius:12px}
.error{margin-top:18px;background:#4b2028;padding:13px;border-radius:10px}@media(max-width:700px){.grid{grid-template-columns:1fr}}
</style></head><body><div class="wrap">
<h1>📸 Old Photo Restoration</h1><div class="sub">Upload an old or damaged photo and restore it automatically.</div>
<div class="card"><form method="post" enctype="multipart/form-data">
<input type="file" name="image" accept=".jpg,.jpeg,.png,.bmp" required><button type="submit">Restore Photo</button></form>
{% if error %}<div class="error">{{ error }}</div>{% endif %}
{% if original and restored %}<div class="grid"><div class="panel"><h3>Original Image</h3><img src="data:image/jpeg;base64,{{original}}"></div>
<div class="panel"><h3>Restored Image</h3><img src="data:image/jpeg;base64,{{restored}}"></div></div>
<div class="metrics"><div class="metric"><b>PSNR</b><br>{{psnr}} dB</div><div class="metric"><b>SSIM</b><br>{{ssim}}</div></div>
<a class="download" href="/download">Download Restored Image</a>{% endif %}</div></div></body></html>
"""

def b64(img):
    ok, buf = cv2.imencode(".jpg", img)
    if not ok: raise ValueError("Image encoding failed.")
    return base64.b64encode(buf.tobytes()).decode()

def restore(img):
    img = apply_histogram_equalization(img)
    img = apply_median_filter(img, 5)
    img = apply_gaussian_filter(img, 5)
    img = apply_inpainting(img)
    return apply_laplacian_sharpening(img)

@app.route("/", methods=["GET", "POST"])
def home():
    global LAST_RESULT
    if request.method == "GET":
        return render_template_string(HTML, original=None, restored=None, error=None)
    try:
        f = request.files.get("image")
        if not f or not f.filename: raise ValueError("Please choose an image.")
        img = cv2.imdecode(np.frombuffer(f.read(), np.uint8), cv2.IMREAD_COLOR)
        if img is None: raise ValueError("Invalid image file.")
        final = restore(img)
        psnr, ssim = calculate_metrics(img, final)
        ok, buf = cv2.imencode(".jpg", final)
        if not ok: raise ValueError("Could not prepare download.")
        LAST_RESULT = buf.tobytes()
        return render_template_string(HTML, original=b64(img), restored=b64(final),
                                      psnr=f"{psnr:.2f}", ssim=f"{ssim:.4f}", error=None)
    except Exception as e:
        return render_template_string(HTML, original=None, restored=None, error=str(e))

@app.route("/download")
def download():
    if LAST_RESULT is None: return "Restore an image first.", 404
    return send_file(BytesIO(LAST_RESULT), mimetype="image/jpeg",
                     as_attachment=True, download_name="restored_photo.jpg")

if __name__ == "__main__":
    app.run(debug=True)
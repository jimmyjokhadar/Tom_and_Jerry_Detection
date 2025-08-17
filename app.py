import logging
from flask import Flask, render_template, request, jsonify
import io
import os
from PIL import Image
from model.model import TomJerryDetector

app = Flask(__name__)

detector = TomJerryDetector()

def resize(file):
    logging.info("Resizing image...")
    img_bytes = file.read()
    img = Image.open(io.BytesIO(img_bytes))

    if img.mode != 'RGB':
        img = img.convert('RGB')

    width, height = img.size
    quality = 95

    while True:
        temp_img = img.copy()

        if width > 1200 or height > 1200:
            temp_img.thumbnail((width, height), Image.Resampling.LANCZOS)

        img_io = io.BytesIO()
        temp_img.save(img_io, format='JPEG', quality=quality, optimize=True)

        img_size = img_io.tell()
        logging.info(f"Image size: {img_size} bytes")

        if img_size <= 1024 * 1024:
            img_io.seek(0)
            return img_io

        if quality > 50:
            quality -= 10
        else:
            width = int(width * 0.9)
            height = int(height * 0.9)
            quality = 85

            if width < 100 or height < 100:
                img_io.seek(0)
                return img_io

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/detect', methods=['POST'])
def detect():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]
    logging.info(f"Received image: {file.filename}")

    ext = os.path.splitext(file.filename)[1].lower()
    if ext not in ['.jpg', '.jpeg', '.png']:
        return jsonify({"error": "Unsupported file type"}), 400

    
    file_io = resize(file)

    results = detector.detect_objects(file_io.read())

    # results contains {detections, labels, scores, image(base64)}

    logging.info(f"Detections: {results['labels']}")

    return jsonify(results)

if __name__ == '__main__':
    app.run(port=8000, host='0.0.0.0', debug=True)

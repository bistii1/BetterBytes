from flask import Flask, render_template, request, jsonify
import base64
import cv2
import numpy as np
from pyzxing import BarCodeReader

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/scan_barcode', methods=['POST'])
def scan_barcode():
    # Get the image data from the frontend
    data = request.get_json()
    image_data = data['image']  # Base64 encoded image

    # Decode the base64 image
    img_data = base64.b64decode(image_data)
    np_arr = np.frombuffer(img_data, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

    # Decode the barcode
    reader = BarCodeReader()
    decoded = reader.decode(img)

    if decoded:
        # Return decoded data (e.g., product info) as a JSON response
        return jsonify({'product_info': decoded[0]})
    else:
        return jsonify({'error': 'No barcode detected'}), 400

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, render_template, request, jsonify
import base64
import cv2
import numpy as np
import requests
from pyzxing import BarCodeReader

app = Flask(__name__)

# Replace with your own USDA Food Data Central API Key
USDA_API_KEY = 'Y3juRrBZaGXrVnDp9k0UERXRMtYAuY3rKGgWA1nE'
USDA_API_URL = 'https://api.nal.usda.gov/fdc/v1/foods/search'

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
        barcode = decoded[0].get('raw', '')
        food_info = get_food_info_from_usda(barcode)
        
        if food_info:
            return jsonify({'product_info': food_info})
        else:
            return jsonify({'error': 'Product info not found in USDA database'}), 400
    else:
        return jsonify({'error': 'No barcode detected'}), 400

def get_food_info_from_usda(barcode):
    # Make a request to the USDA API
    params = {
        'api_key': USDA_API_KEY,
        'query': barcode
    }
    
    response = requests.get(USDA_API_URL, params=params)

    if response.status_code == 200:
        data = response.json()
        if 'foods' in data and data['foods']:
            food = data['foods'][0]  # Get the first result
            return {
                'name': food.get('description', 'No name available'),
                'brand': food.get('brandOwner', 'No brand available'),
                'calories': food.get('foodNutrients', [{}])[0].get('value', 'No calorie info available'),
                'ingredients': food.get('ingredients', 'No ingredients available')
            }
    return None

if __name__ == "__main__":
    app.run(debug=True, host='127.0.0.1')

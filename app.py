from flask import Flask, request, jsonify, render_template
import requests  

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get-product-info', methods=['POST'])
def get_product_info():
    data = request.json
    barcode = data.get("barcode")

    if not barcode:
        return jsonify({"error": "No barcode provided"}), 400

    try:
        api_url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        response = requests.get(api_url)

        if response.status_code == 200:
            product_data = response.json()
            product_name = product_data.get("product", {}).get("product_name", "Product name not found.")
            return jsonify({"product": product_name})

        return jsonify({"error": "Failed to fetch product info"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)

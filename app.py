from flask import Flask, request, jsonify, render_template
import requests  # Use requests to interact with Open Food Facts API

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
        print(f"Fetching product information for barcode: {barcode}")

        # Open Food Facts API URL
        api_url = f"https://world.openfoodfacts.org/api/v0/product/{barcode}.json"
        
        # Make a GET request to the Open Food Facts API
        response = requests.get(api_url)
        
        # If the response is successful (status code 200)
        if response.status_code == 200:
            product_data = response.json()

            # Check if product information is found
            if product_data.get("status") == 1:
                product_name = product_data.get("product", {}).get("product_name", "Product name not found.")
            else:
                product_name = "Product not found in Open Food Facts database."
            
            print(f"Product Info: {product_name}")
            return jsonify({"product": product_name})

        else:
            return jsonify({"error": "Failed to fetch product info"}), 500

    except Exception as e:
        print("Error occurred:", e)
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5001)  # Running on port 5001

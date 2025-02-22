import json
from flask import Flask, request, jsonify, render_template
import requests
import openai  # GPT-4 integration
import os
from openai import OpenAI

app = Flask(__name__)

openai.api_key = os.getenv("OPENAI_API_KEY")  # Ensure your API key is set

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

            # Check if product information is found
            if product_data.get("status") == 1:
                product_name = product_data.get("product", {}).get("product_name", "Product name not found.")
                product_ingredients = product_data.get("product", {}).get("ingredients_text", "")

                # Check if ingredients are found to send to GPT
                if product_ingredients:
                    # Call GPT-4 to get detailed information on the ingredients
                    gpt_response = get_gpt_info(product_ingredients)

                    return jsonify({
                        "product": product_name,
                        "gpt_info": gpt_response
                    })
                else:
                    return jsonify({
                        "product": product_name,
                        "gpt_info": "No detailed ingredient information available."
                    })
            else:
                return jsonify({"error": "Product not found in Open Food Facts database."}), 404

        return jsonify({"error": "Failed to fetch product info"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500


def get_gpt_info(ingredients):
    try:
        client = OpenAI()

        gpt_response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a food specialist. Provide a concise, list-formatted explanation of potentially harmful ingredients."},
                {
                    "role": "user",
                    "content": f"Provide an explanation of ingredients in this list that may be harmful without special characters: {ingredients}"
                }
            ]
        )
        # Access only the content of the first choice
        gpt_info = gpt_response.choices[0].message['content']

        # Return just the content as a string (no need for JSON serialization)
        return gpt_info
    
    except Exception as e:
        print("Error fetching GPT-4 information:", e)
        return "Error retrieving detailed information from GPT-4."

if __name__ == "__main__":
    app.run(debug=True, port=5001)

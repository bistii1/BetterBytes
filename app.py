from flask import Flask, request, jsonify, render_template
import openai
from openai import OpenAI
import os

app = Flask(__name__)

openai.api_key = "OPENAI_API_KEY"

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
        print("Trying to send to GPT")

        # Updated API call using the new OpenAI interface
        #"What food product has this barcode: {barcode}?"

        client = OpenAI()

        completion = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {
                        "role": "user",
                        "content": "What food product has this barcode: {barcode}?"
                    }
                ]
            )

        print(completion.choices[0].message)
                    
        #product_info = response.choices[0].message
        #print(f"Product Info: {product_info}")
        return jsonify({"product": completion.choices[0].message})

    except Exception as e:
        print("Error occurred:", e)
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)

import json
from flask import Flask, request, jsonify, render_template
import requests
import openai  # GPT-4 integration
import os
from openai import OpenAI

app = Flask(__name__)

openai.api_key = os.getenv("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")  # Ensure your API key is set

@app.route('/')
def home():
    return render_template('test.html')

@app.route('/scan')
def scanner():
    return render_template('scanner.html')

@app.route('/personalize', methods=['GET', 'POST'])
def personalize():
    if request.method == 'POST':
        user_input = request.form['user_input']  # Get the information the user submitted
        # Save the input to a file or database
        with open("personalized_data.txt", "a") as file:
            file.write(user_input + "\n")

        return render_template('personalize.html', message="Your information has been saved successfully!")

    return render_template('personalize.html', message="Click the save button to include your preferences in your result!")


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
        # Read the user's personalization if available
        user_personalization = ""
        if os.path.exists("personalized_data.txt"):
            with open("personalized_data.txt", "r") as file:
                user_personalization = file.read().strip()
        
        # Create the base content to send to GPT-4
        content = f"Provide an explanation of ingredients in this list that may be harmful without special characters: {ingredients}"

        # If user personalization exists, add it to the content
        if user_personalization:
            content += f"\n\nCreate a seperate paragraph that includes how the food relates to the user's personalization: {user_personalization}. Please remember not to include any special characters! Please bold the start of each bulleted section."

        client = OpenAI()

        gpt_response= client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a food specialist. Provide a short bulleted of potentially harmful ingredients."},
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        # Correct way to access the content
        gpt_info = gpt_response.choices[0].message.content
        print(gpt_info)

        # Convert message to dictionary
        def message_to_dict(message_obj):
            return {
                "role": message_obj.role,
                "content": message_obj.content
            }

        # Convert the message object to a dictionary
        # gpt_info = message_to_dict(gpt_info)

        # Return the dictionary as JSON
        return json.dumps(gpt_info)  # Ensure it’s JSON serializable

    except Exception as e:
        print("Error fetching GPT-4 information:", e)
        return "Error retrieving detailed information from GPT-4."

if __name__ == "__main__":
    app.run(debug=True, port=5001)
# Personalized Ingredient Scanner

## Overview
The **Personalized Ingredient Scanner** is a web-based application that helps users analyze food ingredients based on their dietary preferences. By using a barcode scanner, the app fetches ingredient data and evaluates it against a user's dietary restrictions or general health concerns. The app also includes an AI-powered nutritionist feature that provides an audio summary of ingredient analysis.

## Tech Stack
- **Backend:** Flask, OpenAI API, Open Food Facts API
- **Frontend:** JavaScript, HTML, CSS
- **Programming Languages:** Python, JavaScript

## Features
### Personalized Diet Plans
Users can create custom dietary plans, such as:
- "I want to cut out carbs"
- "I want to cut out dairy"
- Any other dietary restriction or preference

### Ingredient Scanner
- Uses barcode scanning to fetch ingredient information from the **Open Food Facts API**.
- Compares ingredients against the user's dietary restrictions.
- Identifies harmful or restricted ingredients based on the user’s plan.
- If no plan is set, it highlights common harmful ingredients.

### AI-Powered Nutritionist
- Utilizes **OpenAI’s GPT-4** to provide an AI-generated analysis of scanned food items.
- Users can receive a **spoken summary** of ingredient concerns.

## Libraries and Dependencies
```python
import json
from flask import Flask, request, jsonify, render_template
import requests
import openai  # GPT-4 integration
import os
from openai import OpenAI
```

## API Integration
### Open Food Facts API
- Used to fetch ingredient data based on the barcode of a scanned food item.
- Provides nutritional details and ingredient composition.

### OpenAI API
- GPT-4 processes ingredient lists and dietary preferences.
- AI Nutritionist feature generates human-like explanations and summaries.

## How It Works
1. **User creates a dietary plan** *(optional)*.
2. **User scans a food item** using a barcode scanner.
3. **The app fetches ingredient data** from Open Food Facts.
4. **AI compares ingredients against the user’s plan** and highlights restricted items.
5. **AI Nutritionist provides a summary**, either as text or voice.

## Setup and Installation
### Prerequisites
- Python 3.x
- Flask
- OpenAI API key

### Installation Steps
```sh
git clone https://github.com/your-repo/personalized-ingredient-scanner.git
cd personalized-ingredient-scanner
pip install -r requirements.txt
export OPENAI_API_KEY='your-api-key-here'
python app.py
```

## Future Improvements
- Add a mobile app version.
- Improve barcode scanning speed.
- Expand AI Nutritionist capabilities.
- Support additional dietary restrictions and allergens.

## Contributors
- **Your Name**
- **Other Team Members**

## License
This project is licensed under the MIT License.


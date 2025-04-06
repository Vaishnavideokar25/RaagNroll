from flask import Flask, request, jsonify
from flask_cors import CORS
import google.generativeai as genai
import os

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Configure the Gemini API
API_KEY = "AIzaSyD4awAt423V8Odheh4hRZOc7-i1qObZZzQ"  # Replace with your actual API key
genai.configure(api_key=API_KEY)

# Use the newer Gemini 1.5 Flash model
MODEL_NAME = "gemini-1.5-flash"

@app.route('/check-model', methods=['GET'])
def check_model():
    """Endpoint to check available models and the currently configured one"""
    try:
        # List all available models
        models = genai.list_models()
        available_models = [model.name for model in models]
        
        return jsonify({
            "current_model": MODEL_NAME,
            "available_models": available_models
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        user_message = data.get('message', '')
        
        if not user_message:
            return jsonify({"error": "Empty message"}), 400
        
        print(f"Using model: {MODEL_NAME}")  # Print the model being used
        
        # Create model instance with the specified model
        model = genai.GenerativeModel(MODEL_NAME)
        
        # Add context about Raagas to help Gemini provide better responses
        context = """You are RaagaBot, an expert in Indian classical music, specifically Raagas. 
        Help users understand different Raagas, their emotional qualities, 
        appropriate times to play them, and their historical significance."""
        
        # Generate response from Gemini
        response = model.generate_content(context + "\n\nUser: " + user_message)
        
        return jsonify({
            "response": response.text,
            "model_used": MODEL_NAME  # Include the model name in the response
        })
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Print the current model when starting the server
    print(f"Server starting with model: {MODEL_NAME}")
    
    # Try to list available models
    try:
        print("Checking available models...")
        models = genai.list_models()
        print("Available models:")
        for model in models:
            print(f"- {model.name}")
    except Exception as e:
        print(f"Error listing models: {str(e)}")
        
    app.run(debug=True)
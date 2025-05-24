from flask import Flask, request, jsonify, send_from_directory
import os
import requests
import json

app = Flask(__name__, static_folder='.')

def call_gemini_api(api_key, user_input):
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "contents": [
            {
                "parts": [
                    {
                        "text": user_input
                    }
                ]
            }
        ]
    }
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={api_key}"
    try:
        response = requests.post(url, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        try:
            result = response.json()
        except json.JSONDecodeError:
            return "Error: Received invalid JSON response from Gemini API."
        if "candidates" in result and len(result["candidates"]) > 0:
            content = result["candidates"][0].get("content", "")
            if isinstance(content, dict):
                parts = content.get("parts", [])
                generated_text = "".join(part.get("text", "") for part in parts)
            else:
                generated_text = str(content)
        else:
            generated_text = "No content received from API."
        return generated_text
    except requests.exceptions.RequestException as e:
        return f"Error communicating with Gemini API: {e}"

@app.route('/api/chat', methods=['POST'])
def chat():
    data = request.get_json()
    if not data or 'message' not in data:
        return jsonify({"error": "Missing 'message' in request body"}), 400

    user_message = data['message']
    api_key = os.getenv("GEMINI_API_KEY", "").strip()
    # Debug print to verify environment variable
    print(f"DEBUG: GEMINI_API_KEY environment variable value: '{api_key}'")
    if not api_key:
        return jsonify({"error": "API key is not set in environment variable GEMINI_API_KEY"}), 500

    ai_response = call_gemini_api(api_key, user_message)
    if not ai_response:
        ai_response = "No response from AI."
    return jsonify({"response": ai_response})

@app.route('/')
def serve_frontend():
    return send_from_directory('.', 'chat_frontend_for_backend.html')

if __name__ == '__main__':
    app.run(debug=True)

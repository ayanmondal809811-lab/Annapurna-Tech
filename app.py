import os
import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# ============================================================
# REPLACE WITH YOUR ACTUAL N8N PRODUCTION WEBHOOK URL
# ============================================================
N8N_WEBHOOK_URL = "https://your-n8n-instance.com/webhook/agri-data"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze():
    try:
        # Getting data from Frontend
        farmer_data = request.json
        
        # Sending data to n8n Webhook
        # Note: If n8n is not ready, this will throw an error. 
        # You can mock the response for testing.
        response = requests.post(N8N_WEBHOOK_URL, json=farmer_data, timeout=30)
        
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"error": "n8n connection failed"}), 500

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    # Render uses dynamic ports
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
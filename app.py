from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# ==========================================
# EKHANE TOMAR N8N WEBHOOK URL DITE HOBE
# ==========================================
N8N_WEBHOOK_URL = "https://your-n8n-instance.com/webhook/agri-ai"

@app.route('/')
def home():
    # Eta templates/index.html load korbe
    return render_template('index.html')

@app.route('/api/analyze', methods=['POST'])
def analyze_data():
    try:
        farmer_data = request.json
        
        # Data pathachhi n8n Webhook e
        # response = requests.post(N8N_WEBHOOK_URL, json=farmer_data)
        # ai_result = response.json()
        
        # Test korar jonno nicher mock data (n8n ready hobar aage):
        ai_result = {
            "crop_recommendation": "High-Yield Wheat",
            "risk_score": "Low (15%)",
            "sowing_time": "Next week, post light rain",
            "profit_prediction": "₹45,000 / Acre",
            "emergency_advisory": "None at present. Weather is clear.",
            "mandi_price": "₹2,200/Quintal (Kolkata Mandi)"
        }
        
        return jsonify({"status": "success", "data": ai_result})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    # Run the app
    app.run(host='0.0.0.0', port=5000, debug=True)
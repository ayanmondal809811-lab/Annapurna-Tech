import requests
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# সঠিক Production URL (test ছাড়া)
N8N_WEBHOOK_URL = "https://ayanmondal10100.app.n8n.cloud/webhook/chat-bot"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    try:
        # n8n-এ ডেটা পাঠানো হচ্ছে
        response = requests.post(N8N_WEBHOOK_URL, json={"message": user_message})
        
        # যদি n8n থেকে খালি বা ভুল রেসপন্স আসে তা হ্যান্ডেল করা
        if response.status_code == 200:
            return jsonify(response.json())
        else:
            return jsonify({"output": "Error: n8n থেকে সঠিক উত্তর পাওয়া যায়নি।"})
            
    except Exception as e:
        return jsonify({"output": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=10000)
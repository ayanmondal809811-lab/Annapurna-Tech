# app.py
from flask import Flask, render_template, request, jsonify
import requests
import uuid # unique session id এর জন্য

app = Flask(__name__)

# *** জরুরি: এখানে আপনার n8n এর PRODUCTION Webhook URL টি বসান ***
N8N_WEBHOOK_URL = "https://ayanmondal10100.app.n8n.cloud/webhook/chat-bot"

@app.route('/')
def index():
    # প্রতিটা নতুন ইউজার বা চ্যাটের জন্য একটি নতুন Session ID তৈরি করা
    session_id = str(uuid.uuid4())
    return render_template('index.html', session_id=session_id)

@app.route('/chat', methods=['POST'])
def chat():
    user_data = request.json
    user_message = user_data.get("message")
    session_id = user_data.get("sessionId")
    
    # n8n-এ ডেটা পাঠানো (message এবং sessionId)
    payload = {
        "message": user_message,
        "sessionId": session_id
    }
    
    try:
        response = requests.post(N8N_WEBHOOK_URL, json=payload)
        # n8n থেকে আসা রেজাল্ট
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({"output": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
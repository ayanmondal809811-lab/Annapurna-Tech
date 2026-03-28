from flask import Flask, render_template, request, jsonify
import requests
import uuid

app = Flask(__name__)

# n8n Webhook URL (নিশ্চিত করুন এটি Active আছে)
N8N_WEBHOOK_URL = "https://ayanmondal10100.app.n8n.cloud/webhook/chat-bot"

@app.route('/')
def index():
    session_id = str(uuid.uuid4())
    return render_template('index.html', session_id=session_id)

@app.route('/chat', methods=['POST'])
def chat():
    user_data = request.json
    user_message = user_data.get("message")
    session_id = user_data.get("sessionId")
    
    payload = {
        "message": user_message,
        "sessionId": session_id
    }
    
    try:
        # n8n-এ রিকোয়েস্ট পাঠানো
        response = requests.post(N8N_WEBHOOK_URL, json=payload, timeout=30)
        
        # যদি n8n কোনো ডাটা না পাঠায় বা এরর দেয়
        if response.status_code != 200:
            return jsonify({"output": "n8n সার্ভার রেসপন্স করছে না। অনুগ্রহ করে n8n workflow চেক করুন।"})

        data = response.json()

        # n8n ডাটা অনেক সময় লিস্ট হিসেবে পাঠায়, সেটি হ্যান্ডেল করা
        if isinstance(data, list) and len(data) > 0:
            ai_response = data[0].get("output") or data[0].get("response") or "কোনো উত্তর পাওয়া যায়নি।"
        else:
            ai_response = data.get("output") or data.get("response") or "কোনো উত্তর পাওয়া যায়নি।"
            
        return jsonify({"output": ai_response})

    except Exception as e:
        return jsonify({"output": f"Error: {str(e)}"})

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
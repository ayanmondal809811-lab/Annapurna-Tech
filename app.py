from flask import Flask, render_template, request, jsonify
import requests

app = Flask(__name__)

# n8n Webhook URL (Render-e upload korar por ekhane n8n er URL ta bosiye dibe)
N8N_WEBHOOK_URL = "https://ayanmondal10100.app.n8n.cloud/webhook/chat-bot"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    user_message = request.json.get("message")
    
    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    try:
        # n8n-e data pathano hochhe
        response = requests.post(N8N_WEBHOOK_URL, json={"message": user_message})
        data = response.json()
        
        # n8n theke asha reply return kora hochhe
        return jsonify({"reply": data.get("output", "Sorry, I couldn't understand that.")})
    except Exception as e:
        return jsonify({"reply": "Error connecting to AI server."}), 500

if __name__ == '__main__':
    app.run(debug=True)
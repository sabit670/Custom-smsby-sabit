
from flask import Flask, request, jsonify, Response
import requests
import os

app = Flask(__name__)

API_KEY = "4e48c4751d2c552693a7e777db296cd8-97a7407b-2935-442e-812f-745960507284"
BASE_URL = "https://m3gx3w.api.infobip.com"

HTML_PAGE = '''
<!DOCTYPE html>
<html lang="bn">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Custom SMS By MR SABIT</title>
  <style>
    body {
      font-family: sans-serif;
      background: linear-gradient(to right, #f3f4f6, #e0f7fa);
      margin: 0;
      padding: 0;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      min-height: 100vh;
    }
    h1 {
      font-size: 32px;
      color: #00796b;
      margin-bottom: 20px;
    }
    .form-container {
      background: #ffffff;
      padding: 30px;
      border-radius: 20px;
      box-shadow: 0 10px 20px rgba(0, 0, 0, 0.1);
      width: 90%;
      max-width: 400px;
      text-align: center;
    }
    input, textarea {
      width: 100%;
      padding: 12px;
      margin: 12px 0;
      border: 2px solid #ccc;
      border-radius: 10px;
      font-size: 16px;
    }
    button {
      padding: 12px 24px;
      background: #4ca1af;
      color: white;
      border: none;
      border-radius: 10px;
      font-size: 16px;
      cursor: pointer;
    }
    button:hover {
      background: #00796b;
    }
    #status {
      margin-top: 15px;
      font-weight: bold;
      color: #00796b;
    }
    .footer {
      margin-top: 40px;
      font-size: 14px;
      font-family: monospace;
      text-align: center;
    }
  </style>
</head>
<body>
  <h1>Custom SMS By MR SABIT</h1>
  <div class="form-container">
    <input type="text" id="number" placeholder="📞 মোবাইল নাম্বার (01XXXXXXXXX)">
    <textarea id="message" placeholder="💬 মেসেজ লিখুন..." rows="4"></textarea>
    <button onclick="sendSMS()">📤 Send SMS</button>
    <div id="status"></div>
  </div>
  <div class="footer">
    Made by Sabit | Telegram: <a href="https://t.me/sabitcommunity" target="_blank">Sabit Community</a>
  </div>
  <script>
    async function sendSMS() {
      const number = document.getElementById("number").value.trim();
      const message = document.getElementById("message").value.trim();
      const status = document.getElementById("status");
      if (!number || !message) {
        status.innerText = "⚠️ নাম্বার এবং মেসেজ দিন!";
        return;
      }
      status.innerText = "⏳ মেসেজ পাঠানো হচ্ছে...";
      try {
        const res = await fetch("/", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ number, message })
        });
        const result = await res.json();
        status.innerText = result.success ? "✅ মেসেজ সফলভাবে পাঠানো হয়েছে!" : "❌ ব্যর্থ: " + result.error;
      } catch (err) {
        status.innerText = "❌ সার্ভার সমস্যা হয়েছে।";
      }
    }
  </script>
</body>
</html>
'''

@app.route("/", methods=["GET"])
def index():
    return Response(HTML_PAGE, mimetype='text/html')

@app.route("/", methods=["POST"])
def send_sms():
    data = request.get_json()
    number = data.get("number")
    message = data.get("message")

    if not number or not message:
        return jsonify({"success": False, "error": "Missing number or message"}), 400

    payload = {
        "messages": [{
            "from": "InfoSMS",
            "destinations": [{"to": "88" + number}],
            "text": message
        }]
    }

    headers = {
        "Authorization": f"App {API_KEY}",
        "Content-Type": "application/json"
    }

    try:
        response = requests.post(f"{BASE_URL}/sms/2/text/advanced", json=payload, headers=headers)
        if response.status_code == 200:
            return jsonify({"success": True})
        else:
            return jsonify({"success": False, "error": response.text}), response.status_code
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

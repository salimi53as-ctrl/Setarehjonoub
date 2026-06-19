from flask import Flask, request
import requests

app = Flask(__name__)

BOT_TOKEN = "19108680:VLIdd-6KJY_joTrmPwsTXkIXGVh9pgFs6lM"
BASE_URL = f"https://tapi.bale.ai/bot{848341355}"

def send_message(chat_id, text):
    try:
        requests.post(BASE_URL + "/sendMessage", data={
            "chat_id": chat_id,
            "text": text
        })
    except:
        pass

@app.route("/", methods=["GET"])
def home():
    return "BOT IS RUNNING"

@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if not data or "message" not in data:
        return "ok"

    msg = data["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")

    if text == "/start":
        send_message(chat_id, "👋 ربات ستاره جنوب فعال شد")
    else:
        send_message(chat_id, "پیام دریافت شد: " + text)

    return "ok"


if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

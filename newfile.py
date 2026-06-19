import os
from flask import Flask, request
import requests

app = Flask(__name__)

# ✅ توکن از Environment Variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN is not set!")

BASE_URL = f"https://api.telegram.org/bot{BOT_TOKEN}"

# -------------------------
# ارسال پیام
# -------------------------
def send_message(chat_id, text, reply_markup=None):
    url = f"{BASE_URL}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text
    }

    if reply_markup:
        data["reply_markup"] = reply_markup

    requests.post(url, json=data)

# -------------------------
# پیام‌ها
# -------------------------
def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        keyboard = {
            "keyboard": [
                ["📊 داشبورد", "👥 بازیکنان"],
                ["ℹ️ راهنما"]
            ],
            "resize_keyboard": True
        }
        send_message(chat_id, "👋 خوش آمدی به باشگاه ستاره جنوب", keyboard)

    elif text == "📊 داشبورد":
        send_message(chat_id, "📊 داشبورد فعال است")

    elif text == "👥 بازیکنان":
        if os.path.exists("players.txt"):
            with open("players.txt", "r", encoding="utf-8") as f:
                data = f.read()
            send_message(chat_id, f"👥 بازیکنان:\n\n{data}")
        else:
            send_message(chat_id, "لیست خالی است")

    elif text == "ℹ️ راهنما":
        send_message(chat_id, "از دکمه‌ها استفاده کن")

    else:
        send_message(chat_id, "دستور ناشناخته ❌")

# -------------------------
# webhook
# -------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if data and "message" in data:
        handle_message(data["message"])

    return "ok"

# -------------------------
# داشبورد وب
# -------------------------
@app.route("/")
def home():
    return """
    <h1>⚽ Setareh Jonoub Bot</h1>
    <p>Server is running ✅</p>
    <p>Webhook active 🚀</p>
    """

# -------------------------
# run
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

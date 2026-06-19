import os
from flask import Flask, request
import requests

app = Flask(__name__)

# ⚠️ توکن را از Environment Variable بگیر (نه داخل کد)
BOT_TOKEN = os.getenv("19108680:VLIdd-6KJY_joTrmPwsTXkIXGVh9pgFs6lM")
BASE_URL = f"https://api.telegram.org/bot{848341355}"

# -------------------------
# 🧠 ارسال پیام به تلگرام
# -------------------------
def send_message(chat_id, text, reply_markup=None):
    url = f"{BASE_URL}/sendMessage"
    data = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "HTML"
    }
    if reply_markup:
        data["reply_markup"] = reply_markup

    requests.post(url, json=data)

# -------------------------
# 🤖 کنترل پیام‌ها
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
        send_message(chat_id, "سلام 👋 به ربات باشگاه ستاره جنوب خوش آمدی", keyboard)

    elif text == "📊 داشبورد":
        send_message(chat_id, "📊 داشبورد باشگاه:\n- مدیریت بازیکنان\n- اخبار\n- تمرینات")

    elif text == "👥 بازیکنان":
        if os.path.exists("players.txt"):
            with open("players.txt", "r", encoding="utf-8") as f:
                data = f.read()
            send_message(chat_id, f"👥 لیست بازیکنان:\n\n{data}")
        else:
            send_message(chat_id, "هنوز بازیکنی ثبت نشده")

    elif text == "ℹ️ راهنما":
        send_message(chat_id, "برای استفاده از ربات از دکمه‌ها استفاده کن.")

    else:
        send_message(chat_id, "دستور ناشناخته ❌")

# -------------------------
# 🌐 Webhook
# -------------------------
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if "message" in data:
        handle_message(data["message"])

    return "ok"

# -------------------------
# 🖥️ داشبورد تحت وب
# -------------------------
@app.route("/")
def dashboard():
    return """
    <h1>⚽ Setareh Jonoub Dashboard</h1>
    <p>Bot is running successfully 🚀</p>
    <p>Webhook Active ✅</p>
    """

# -------------------------
# 🚀 اجرا
# -------------------------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

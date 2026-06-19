import os
from flask import Flask, request
import requests

app = Flask(__name__)

# توکن از Environment Variable
BOT_TOKEN = os.environ.get("BOT_TOKEN")

if not BOT_TOKEN:
    raise Exception("BOT_TOKEN is not set!")

# آدرس API بله
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"


# ارسال پیام
def send_message(chat_id, text, keyboard=None):
    url = f"{BASE_URL}/sendMessage"

    data = {
        "chat_id": chat_id,
        "text": text
    }

    if keyboard:
        data["reply_markup"] = {
            "keyboard": keyboard,
            "resize_keyboard": True
        }

    requests.post(url, json=data)


# مدیریت پیام‌ها
def handle_message(message):
    chat_id = message["chat"]["id"]
    text = message.get("text", "")

    if text == "/start":
        keyboard = [
            ["📊 داشبورد", "👥 بازیکنان"],
            ["ℹ️ راهنما"]
        ]

        send_message(
            chat_id,
            "⚽ به ربات باشگاه ستاره جنوب خوش آمدید\n\nیکی از گزینه‌های زیر را انتخاب کنید:",
            keyboard
        )

    elif text == "📊 داشبورد":
        send_message(
            chat_id,
            """📊 داشبورد باشگاه ستاره جنوب

🏟️ نام باشگاه: ستاره جنوب
⚽ بخش مدیریت فعال است
👥 مدیریت بازیکنان فعال است"""
        )

    elif text == "👥 بازیکنان":

        if os.path.exists("players.txt"):
            with open("players.txt", "r", encoding="utf-8") as f:
                players = f.read()

            if players.strip():
                send_message(chat_id, "👥 لیست بازیکنان:\n\n" + players)
            else:
                send_message(chat_id, "هنوز بازیکنی ثبت نشده است")
        else:
            send_message(chat_id, "فایل بازیکنان وجود ندارد")

    elif text == "ℹ️ راهنما":
        send_message(
            chat_id,
            "برای کار با ربات از دکمه‌های پایین صفحه استفاده کنید."
        )

    else:
        send_message(
            chat_id,
            "دستور نامعتبر است ❌\n/start را ارسال کنید."
        )


# Webhook بله
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json()

    if data and "message" in data:
        handle_message(data["message"])

    return "ok", 200


# صفحه اصلی سایت
@app.route("/")
def home():
    return """
    <h1>⚽ Setareh Jonoub FC</h1>
    <h2>Bot is Running ✅</h2>
    <p>Bale Webhook Active 🚀</p>
    """


# اجرای سرور
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print("🚀 SERVER STARTING...")
    app.run(host="0.0.0.0", port=port)

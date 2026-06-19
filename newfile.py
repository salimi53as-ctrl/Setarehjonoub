from flask import Flask, request
import requests
import os

app = Flask(__name__)

# توکن ربات بله
BOT_TOKEN = "19108680:VLIdd-6KJY_joTrmPwsTXkIXGVh9pgFs6lM"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

# ذخیره موقت کاربران
users = {}


# ارسال پیام
def send_message(chat_id, text):
    requests.post(f"{BASE_URL}/sendMessage", data={
        "chat_id": chat_id,
        "text": text
    })


# Webhook بله
@app.route("/", methods=["GET", "POST"])
def webhook():

    # پاسخ به تست Render
    if request.method == "GET":
        return "Setareh Jonoub Bale Bot is Running ⚽🐉"

    # دریافت پیام از بله
    data = request.json

    if not data or "message" not in data:
        return "ok"

    msg = data["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")

    # ساخت کاربر جدید
    if chat_id not in users:
        users[chat_id] = {
            "step": 0,
            "data": {}
        }

    user = users[chat_id]

    # شروع ثبت نام
    if text == "/start":
        send_message(chat_id, "👋 سلام به آکادمی فوتبال ستاره جنوب ⚽\n\nنام و نام خانوادگی خود را وارد کنید:")
        user["step"] = 1

    elif user["step"] == 1:
        user["data"]["name"] = text
        send_message(chat_id, "👨 نام پدر را وارد کنید:")
        user["step"] = 2

    elif user["step"] == 2:
        user["data"]["father"] = text
        send_message(chat_id, "🆔 کد ملی را وارد کنید:")
        user["step"] = 3

    elif user["step"] == 3:
        user["data"]["national_id"] = text
        send_message(chat_id, "🎂 تاریخ تولد را وارد کنید:")
        user["step"] = 4

    elif user["step"] == 4:
        user["data"]["birth"] = text
        send_message(chat_id, "📞 شماره تماس را وارد کنید:")
        user["step"] = 5

    elif user["step"] == 5:
        user["data"]["phone"] = text

        send_message(
            chat_id,
            "✅ ثبت نام شما با موفقیت انجام شد:\n\n"
            f"👤 نام: {user['data']['name']}\n"
            f"👨 نام پدر: {user['data']['father']}\n"
            f"🆔 کد ملی: {user['data']['national_id']}\n"
            f"🎂 تاریخ تولد: {user['data']['birth']}\n"
            f"📞 تماس: {user['data']['phone']}"
        )

        user["step"] = 0
        user["data"] = {}

    return "ok"


# اجرای برنامه روی Render
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

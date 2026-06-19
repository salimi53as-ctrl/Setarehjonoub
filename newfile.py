from flask import Flask, request
import requests
import os

app = Flask(__name__)

BOT_TOKEN = "19108680:VLIdd-6KJY_joTrmPwsTXkIXGVh9pgFs6lM
"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

users = {}

def send_message(chat_id, text):
    try:
        requests.post(f"{BASE_URL}/sendMessage", data={
            "chat_id": chat_id,
            "text": text
        })
    except Exception as e:
        print("send error:", e)

@app.route("/", methods=["GET", "POST"])
def webhook():

    # تست سلامت سرور
    if request.method == "GET":
        return "Setareh Jonoub Bot is running ⚽🐉"

    data = request.get_json(force=True, silent=True)
    print("DEBUG DATA:", data)

    if not data:
        return "no data"

    # 🔥 حالت‌های مختلف ساختار بله
    msg = None

    if "message" in data:
        msg = data["message"]
    elif "update" in data and "message" in data["update"]:
        msg = data["update"]["message"]
    elif "body" in data:
        msg = data["body"]

    if not msg:
        return "no message"

    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")

    if chat_id not in users:
        users[chat_id] = {"step": 0, "data": {}}

    user = users[chat_id]

    if text == "/start":
        send_message(chat_id, "⚽ سلام به آکادمی ستاره جنوب\nنام و نام خانوادگی؟")
        user["step"] = 1

    elif user["step"] == 1:
        user["data"]["name"] = text
        send_message(chat_id, "👨 نام پدر؟")
        user["step"] = 2

    elif user["step"] == 2:
        user["data"]["father"] = text
        send_message(chat_id, "🆔 کد ملی؟")
        user["step"] = 3

    elif user["step"] == 3:
        user["data"]["national_id"] = text
        send_message(chat_id, "🎂 تاریخ تولد؟")
        user["step"] = 4

    elif user["step"] == 4:
        user["data"]["birth"] = text
        send_message(chat_id, "📞 شماره تماس؟")
        user["step"] = 5

    elif user["step"] == 5:
        user["data"]["phone"] = text

        send_message(chat_id,
            f"✅ ثبت شد:\n"
            f"{user['data']}"
        )

        user["step"] = 0
        user["data"] = {}

    return "ok"


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

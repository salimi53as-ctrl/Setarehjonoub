from flask import Flask, request
import requests
import os

app = Flask(__name__)

# 🔑 توکن بله
BOT_TOKEN = "19108680:VLIdd-6KJY_joTrmPwsTXkIXGVh9pgFs6lM"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

# ذخیره موقت کاربران
users = {}

# ================= SEND MESSAGE =================
def send_message(chat_id, text):
    try:
        requests.post(f"{BASE_URL}/sendMessage", data={
            "chat_id": chat_id,
            "text": text
        })
    except Exception as e:
        print("❌ SEND ERROR:", e)

# ================= HOME TEST =================
@app.route("/", methods=["GET"])
def home():
    return "⚽ Setareh Jonoub Bot is RUNNING"

# ================= WEBHOOK =================
@app.route("/webhook", methods=["POST", "GET"])
def webhook():

    # 🔥 تست اینکه درخواست واقعاً می‌رسد یا نه
    print("🔥 WEBHOOK HIT")

    # اگر از مرورگر باز شد
    if request.method == "GET":
        return "WEBHOOK OK ⚽"

    try:
        data = request.get_json(force=True, silent=True)
        print("📩 DATA RECEIVED:", data)

        if not data:
            return "no data"

        if "message" not in data:
            return "no message"

        msg = data["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "")

        print(f"👤 CHAT: {chat_id} | TEXT: {text}")

        # ساخت کاربر
        if chat_id not in users:
            users[chat_id] = {"step": 0, "data": {}}

        user = users[chat_id]

        # شروع ثبت نام
        if text == "/start":
            send_message(chat_id, "⚽ ثبت نام ستاره جنوب\nنام و نام خانوادگی؟")
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
            user["data"]["nid"] = text
            send_message(chat_id, "🎂 تاریخ تولد؟")
            user["step"] = 4

        elif user["step"] == 4:
            user["data"]["birth"] = text
            send_message(chat_id, "📞 شماره تماس؟")
            user["step"] = 5

        elif user["step"] == 5:
            user["data"]["phone"] = text

            send_message(chat_id,
                "✅ ثبت نام کامل شد:\n\n"
                f"👤 نام: {user['data']['name']}\n"
                f"👨 پدر: {user['data']['father']}\n"
                f"🆔 کد ملی: {user['data']['nid']}\n"
                f"🎂 تولد: {user['data']['birth']}\n"
                f"📞 تماس: {user['data']['phone']}"
            )

            user["step"] = 0
            user["data"] = {}

        return "ok"

    except Exception as e:
        print("❌ ERROR:", e)
        return "error"


# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    print("🚀 SERVER STARTING...")
    app.run(host="0.0.0.0", port=port, debug=False)

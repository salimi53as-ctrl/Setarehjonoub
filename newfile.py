from flask import Flask, request
import requests
app = Flask(name)
🔑 توکن ربات بله را اینجا بگذار
BOT_TOKEN = "19108680:VLIdd-6KJY_joTrmPwsTXkIXGVh9pgFs6lM"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"
ذخیره موقت کاربران
users = {}
================= SEND MESSAGE =================
def send_message(chat_id, text):
    requests.post(f"{BASE_URL}/sendMessage", data={
        "chat_id": chat_id,
        "text": text
    })
================= WEBHOOK =================
@app.route("/", methods=["POST"])
def webhook():
    data = request.json
if not data or "message" not in data:
    return "ok"

msg = data["message"]
chat_id = msg["chat"]["id"]
text = msg.get("text", "")

# ساخت کاربر اگر وجود ندارد
if chat_id not in users:
    users[chat_id] = {"step": 0, "data": {}}

user = users[chat_id]

# شروع ثبت نام
if text == "/start":
    send_message(chat_id, "👋 سلام!\nنام و نام خانوادگی را وارد کنید:")
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
        "✅ ثبت نام انجام شد:\n\n"
        f"👤 نام: {user['data']['name']}\n"
        f"👨 پدر: {user['data']['father']}\n"
        f"🆔 کد ملی: {user['data']['national_id']}\n"
        f"🎂 تولد: {user['data']['birth']}\n"
        f"📞 تماس: {user['data']['phone']}"
    )

    user["step"] = 0
    user["data"] = {}

return "ok"

================= RUN =================
if name == "main":
    app.run(host="0.0.0.0", port=10000)

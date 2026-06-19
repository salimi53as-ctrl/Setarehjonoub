from flask import Flask, request
import requests
import json
import os

app = Flask(__name__)

# ================= CONFIG =================
BOT_TOKEN = "19108680:VLIdd-6KJY_joTrmPwsTXkIXGVh9pgFs6lM"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

ADMIN_ID = "848341355"
DATA_FILE = "players.json"

# ================= LOAD/SAVE =================
def load_users():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}

def save_users(data):
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

users = load_users()

# ================= SEND MESSAGE =================
def send_message(chat_id, text, reply_markup=None):
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)

    requests.post(f"{BASE_URL}/sendMessage", data=payload)

# ================= MAIN MENU =================
def main_menu():
    return {
        "inline_keyboard": [
            [{"text": "📋 ثبت‌نام", "callback_data": "register"}],
            [{"text": "📊 وضعیت من", "callback_data": "status"}],
            [{"text": "🛠 ادمین", "callback_data": "admin"}],
        ]
    }

# ================= WEBHOOK =================
@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()

    if not data:
        return "ok"

    # ================= CALLBACK BUTTON =================
    if "callback_query" in data:
        cq = data["callback_query"]
        chat_id = str(cq["message"]["chat"]["id"])
        data_cb = cq["data"]

        if chat_id not in users:
            users[chat_id] = {"step": 0, "data": {}}

        user = users[chat_id]

        # ---------------- REGISTER ----------------
        if data_cb == "register":
            send_message(chat_id, "⚽ نام و نام خانوادگی را وارد کنید:")
            user["step"] = 1

        # ---------------- STATUS ----------------
        elif data_cb == "status":
            d = user.get("data", {})
            send_message(chat_id,
                f"📊 وضعیت شما:\n\n"
                f"👤 نام: {d.get('name','-')}\n"
                f"📞 تماس: {d.get('phone','-')}"
            )

        # ---------------- ADMIN ----------------
        elif data_cb == "admin":
            if chat_id != ADMIN_ID:
                send_message(chat_id, "⛔ دسترسی ندارید")
                return "ok"

            msg = "📋 لیست بازیکنان:\n\n"

            for i, (uid, udata) in enumerate(users.items(), start=1):
                d = udata.get("data", {})
                msg += f"{i}) {d.get('name','-')} | {d.get('phone','-')}\n"

            send_message(chat_id, msg)

        return "ok"

    # ================= TEXT MESSAGE =================
    if "message" in data:

        msg = data["message"]
        chat_id = str(msg["chat"]["id"])
        text = msg.get("text", "")

        if chat_id not in users:
            users[chat_id] = {"step": 0, "data": {}}

        user = users[chat_id]

        # /start
        if text == "/start":
            send_message(
                chat_id,
                "⚽ به باشگاه ستاره جنوب خوش آمدید 🐉\n\nاز منو انتخاب کنید:",
                main_menu()
            )
            return "ok"

        # ================= REGISTRATION STEPS =================
        if user["step"] == 1:
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
            user["step"] = 0

            send_message(chat_id,
                "✅ ثبت‌نام کامل شد ⚽\nبه ستاره جنوب خوش آمدید 🐉",
                main_menu()
            )

        save_users(users)
        return "ok"

    return "ok"

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

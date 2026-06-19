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

# ================= SEND =================
def send_message(chat_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)

    requests.post(f"{BASE_URL}/sendMessage", data=payload)

# ================= MAIN MENU =================
def main_menu():
    return {
        "inline_keyboard": [
            [{"text": "📋 ثبت‌نام بازیکن", "callback_data": "reg"}],
            [{"text": "📊 پروفایل من", "callback_data": "profile"}],
            [{"text": "🛠 پنل ادمین", "callback_data": "admin"}]
        ]
    }

# ================= REGISTRATION FLOW =================
def position_menu():
    return {
        "inline_keyboard": [
            [{"text": "🥅 دروازه‌بان", "callback_data": "pos_gk"}],
            [{"text": "🛡 دفاع", "callback_data": "pos_def"}],
            [{"text": "🎯 هافبک", "callback_data": "pos_mid"}],
            [{"text": "⚡ حمله", "callback_data": "pos_att"}]
        ]
    }

def age_menu():
    return {
        "inline_keyboard": [
            [{"text": "8-10", "callback_data": "age1"}],
            [{"text": "11-13", "callback_data": "age2"}],
            [{"text": "14-16", "callback_data": "age3"}],
            [{"text": "17-18", "callback_data": "age4"}]
        ]
    }

# ================= WEBHOOK =================
@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()
    if not data:
        return "ok"

    # ================= BUTTONS =================
    if "callback_query" in data:
        cq = data["callback_query"]
        chat_id = str(cq["message"]["chat"]["id"])
        cb = cq["data"]

        if chat_id not in users:
            users[chat_id] = {"step": 0, "data": {}}

        u = users[chat_id]

        # -------- START REG --------
        if cb == "reg":
            send_message(chat_id, "👤 نام و نام خانوادگی را وارد کنید:")
            u["step"] = 1

        # -------- POSITION --------
        elif cb.startswith("pos_"):
            pos_map = {
                "pos_gk": "دروازه‌بان",
                "pos_def": "دفاع",
                "pos_mid": "هافبک",
                "pos_att": "حمله"
            }
            u["data"]["position"] = pos_map.get(cb, "-")
            send_message(chat_id, "📅 رده سنی را انتخاب کنید:", age_menu())
            u["step"] = 3

        # -------- AGE --------
        elif cb.startswith("age"):
            age_map = {
                "age1": "8-10",
                "age2": "11-13",
                "age3": "14-16",
                "age4": "17-18"
            }
            u["data"]["age"] = age_map.get(cb, "-")

            send_message(chat_id, "📞 شماره تماس را وارد کنید:")
            u["step"] = 4

        # -------- PROFILE --------
        elif cb == "profile":
            d = u.get("data", {})
            send_message(chat_id,
                f"📊 پروفایل شما:\n\n"
                f"👤 نام: {d.get('name','-')}\n"
                f"⚽ پست: {d.get('position','-')}\n"
                f"👶 رده سنی: {d.get('age','-')}\n"
                f"📞 تماس: {d.get('phone','-')}"
            )

        # -------- ADMIN --------
        elif cb == "admin":
            if chat_id != ADMIN_ID:
                send_message(chat_id, "⛔ دسترسی ندارید")
                return "ok"

            msg = "🛠 لیست کامل بازیکنان:\n\n"

            for i, (uid, ud) in enumerate(users.items(), start=1):
                d = ud.get("data", {})
                msg += (
                    f"{i}) {d.get('name','-')} | "
                    f"{d.get('position','-')} | "
                    f"{d.get('age','-')} | "
                    f"{d.get('phone','-')}\n"
                )

            send_message(chat_id, msg)

        return "ok"

    # ================= TEXT =================
    if "message" in data:

        msg = data["message"]
        chat_id = str(msg["chat"]["id"])
        text = msg.get("text", "")

        if chat_id not in users:
            users[chat_id] = {"step": 0, "data": {}}

        u = users[chat_id]

        if text == "/start":
            send_message(chat_id,
                "⚽ باشگاه ستاره جنوب 🐉\nبه سیستم حرفه‌ای خوش آمدید",
                main_menu()
            )

        elif u["step"] == 1:
            u["data"]["name"] = text
            send_message(chat_id, "⚽ پست بازی را انتخاب کنید:", position_menu())
            u["step"] = 2

        elif u["step"] == 4:
            u["data"]["phone"] = text
            u["step"] = 0

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

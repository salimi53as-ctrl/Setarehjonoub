from flask import Flask, request
import requests
import sqlite3

app = Flask(__name__)

# 🔑 توکن بله
BOT_TOKEN = "19108680:VLIdd-6KJY_joTrmPwsTXkIXGVh9pgFs6lM"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

# 👑 ادمین
ADMIN_ID = None

# ================= DATABASE =================
conn = sqlite3.connect("players.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    father TEXT,
    national_id TEXT,
    phone TEXT,
    birth TEXT
)
""")
conn.commit()

# ================= USERS =================
users = {}

# ================= SEND MESSAGE =================
def send_message(chat_id, text):
    requests.post(f"{BASE_URL}/sendMessage", data={
        "chat_id": chat_id,
        "text": text
    })

# ================= SAVE =================
def save_player(data):
    c.execute("""
    INSERT INTO players (name,father,national_id,phone,birth)
    VALUES (?,?,?,?,?)
    """, (
        data["name"],
        data["father"],
        data["national_id"],
        data["phone"],
        data["birth"]
    ))
    conn.commit()

# ================= WEBHOOK =================
@app.route("/", methods=["POST"])
def webhook():
    global ADMIN_ID

    data = request.get_json(silent=True)
    if not data:
        return "ok"

    msg = data.get("message", {})
    chat_id = msg.get("chat", {}).get("id")
    text = msg.get("text")

    if not chat_id or text is None:
        return "ok"

    if chat_id not in users:
        users[chat_id] = {"step": 0, "data": {}}

    user = users[chat_id]

    # ================= /start =================
    if text == "/start":
        user["step"] = 1
        send_message(chat_id, "👤 نام و نام خانوادگی را وارد کنید")
        return "ok"

    # ================= /id =================
    if text == "/id":
        ADMIN_ID = chat_id
        send_message(chat_id, f"🆔 شما ادمین شدید:\n{chat_id}")
        return "ok"

    # ================= STEP 1 NAME =================
    if user["step"] == 1:
        if text.isdigit():
            send_message(chat_id, "❌ اسم نباید عدد باشد")
            return "ok"

        user["data"]["name"] = text
        user["step"] = 2
        send_message(chat_id, "👨 نام پدر؟")
        return "ok"

    # ================= STEP 2 FATHER =================
    if user["step"] == 2:
        if text.isdigit():
            send_message(chat_id, "❌ نام پدر اشتباه است")
            return "ok"

        user["data"]["father"] = text
        user["step"] = 3
        send_message(chat_id, "🆔 کد ملی؟ (10 رقم)")
        return "ok"

    # ================= STEP 3 NATIONAL ID =================
    if user["step"] == 3:
        if not text.isdigit() or len(text) != 10:
            send_message(chat_id, "❌ کد ملی باید 10 رقم باشد")
            return "ok"

        user["data"]["national_id"] = text
        user["step"] = 4
        send_message(chat_id, "📞 شماره تماس؟")
        return "ok"

    # ================= STEP 4 PHONE =================
    if user["step"] == 4:
        if not text.isdigit() or len(text) < 10:
            send_message(chat_id, "❌ شماره تماس اشتباه است")
            return "ok"

        user["data"]["phone"] = text
        user["step"] = 5
        send_message(chat_id, "🎂 تاریخ تولد؟ (مثال: 1385/05/12)")
        return "ok"

    # ================= STEP 5 BIRTH =================
    if user["step"] == 5:
        if len(text) < 8:
            send_message(chat_id, "❌ تاریخ اشتباه است")
            return "ok"

        user["data"]["birth"] = text

        save_player(user["data"])

        send_message(chat_id,
            "✅ ثبت نام کامل شد:\n\n"
            f"👤 نام: {user['data']['name']}\n"
            f"👨 پدر: {user['data']['father']}\n"
            f"🆔 کد ملی: {user['data']['national_id']}\n"
            f"📞 تماس: {user['data']['phone']}\n"
            f"🎂 تاریخ تولد: {user['data']['birth']}"
        )

        user["step"] = 0
        user["data"] = {}

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

from flask import Flask, request
import requests
import sqlite3
import re

app = Flask(__name__)

# 🔑 توکن بله
BOT_TOKEN = "19108680:VLIdd-6KJY_joTrmPwsTXkIXGVh9pgFs6lM"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

# 👑 ادمین
ADMIN_ID = 848341355


# ================= دیتابیس =================
conn = sqlite3.connect("players.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    father TEXT,
    national_id TEXT,
    birth TEXT,
    phone TEXT
)
""")
conn.commit()

# ================= کاربران =================
users = {}

# ================= اعتبارسنجی =================
def is_name(text):
    return not text.isdigit() and len(text) >= 2

def is_national_id(text):
    return text.isdigit() and len(text) == 10

def is_date(text):
    return bool(re.match(r"^\d{4}[/-]\d{1,2}[/-]\d{1,2}$", text))

def is_phone(text):
    return text.isdigit() and len(text) >= 10

# ================= ارسال پیام =================
def send_message(chat_id, text):
    requests.post(f"{BASE_URL}/sendMessage", data={
        "chat_id": chat_id,
        "text": text
    })

# ================= ذخیره =================
def save_player(data):
    c.execute("""
    INSERT INTO players (name, father, national_id, birth, phone)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["father"],
        data["national_id"],
        data["birth"],
        data["phone"]
    ))
    conn.commit()

# ================= لیست =================
def get_players():
    c.execute("SELECT name, father, national_id, birth, phone FROM players")
    rows = c.fetchall()

    if not rows:
        return "هیچ بازیکنی ثبت نشده است."

    result = ""
    for r in rows:
        result += (
            f"👤 نام: {r[0]}\n"
            f"👨 پدر: {r[1]}\n"
            f"🆔 کد ملی: {r[2]}\n"
            f"🎂 تولد: {r[3]}\n"
            f"📞 تماس: {r[4]}\n"
            "----------------------\n"
        )
    return result

# ================= webhook =================
@app.route("/", methods=["POST"])
def webhook():
    global ADMIN_ID

    data = request.json
    if not data or "message" not in data:
        return "ok"

    msg = data["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")

    if chat_id not in users:
        users[chat_id] = {"step": 0, "data": {}}

    user = users[chat_id]

    # ================= /id =================
    if text == "/id":
        ADMIN_ID = chat_id
        send_message(chat_id, f"🆔 آیدی شما ثبت شد:\n{chat_id}\n✔ شما ادمین شدید")

    # ================= start =================
    elif text == "/start":
        send_message(chat_id, "👋 سلام!\nنام و نام خانوادگی را وارد کنید:")
        user["step"] = 1

    # ================= players =================
    elif text == "/players":
        if ADMIN_ID == chat_id:
            send_message(chat_id, "📋 لیست بازیکنان:\n\n" + get_players())
        else:
            send_message(chat_id, "⛔ دسترسی ندارید")

    # ================= ثبت نام =================
    elif user["step"] == 1:
        if not is_name(text):
            send_message(chat_id, "❌ نام معتبر نیست")
        else:
            user["data"]["name"] = text
            send_message(chat_id, "👨 نام پدر؟")
            user["step"] = 2

    elif user["step"] == 2:
        if not is_name(text):
            send_message(chat_id, "❌ نام پدر معتبر نیست")
        else:
            user["data"]["father"] = text
            send_message(chat_id, "🆔 کد ملی؟ (10 رقم)")
            user["step"] = 3

    elif user["step"] == 3:
        if not is_national_id(text):
            send_message(chat_id, "❌ کد ملی باید 10 رقم باشد")
        else:
            user["data"]["national_id"] = text
            send_message(chat_id, "🎂 تاریخ تولد؟ (مثال: 1385/05/12)")
            user["step"] = 4

    elif user["step"] == 4:
        if not is_date(text):
            send_message(chat_id, "❌ فرمت تاریخ اشتباه است")
        else:
            user["data"]["birth"] = text
            send_message(chat_id, "📞 شماره تماس؟")
            user["step"] = 5

    elif user["step"] == 5:
        if not is_phone(text):
            send_message(chat_id, "❌ شماره تلفن اشتباه است")
        else:
            user["data"]["phone"] = text

            save_player(user["data"])

            send_message(chat_id,
                "✅ ثبت نام کامل شد:\n\n"
                f"👤 نام: {user['data']['name']}\n"
                f"👨 پدر: {user['data']['father']}\n"
                f"🆔 کد ملی: {user['data']['national_id']}\n"
                f"🎂 تولد: {user['data']['birth']}\n"
                f"📞 تماس: {user['data']['phone']}"
            )

            user["step"] = 0
            user["data"] = {}

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)from flask import Flask, request
import requests
import sqlite3
import re

app = Flask(__name__)

# 🔑 توکن بله
BOT_TOKEN = "YOUR_TOKEN_HERE"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

# 👑 ادمین
ADMIN_ID = None

# ================= دیتابیس =================
conn = sqlite3.connect("players.db", check_same_thread=False)
c = conn.cursor()

c.execute("""
CREATE TABLE IF NOT EXISTS players (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    father TEXT,
    national_id TEXT,
    birth TEXT,
    phone TEXT
)
""")
conn.commit()

# ================= کاربران =================
users = {}

# ================= اعتبارسنجی =================
def is_name(text):
    return not text.isdigit() and len(text) >= 2

def is_national_id(text):
    return text.isdigit() and len(text) == 10

def is_date(text):
    return bool(re.match(r"^\d{4}[/-]\d{1,2}[/-]\d{1,2}$", text))

def is_phone(text):
    return text.isdigit() and len(text) >= 10

# ================= ارسال پیام =================
def send_message(chat_id, text):
    requests.post(f"{BASE_URL}/sendMessage", data={
        "chat_id": chat_id,
        "text": text
    })

# ================= ذخیره =================
def save_player(data):
    c.execute("""
    INSERT INTO players (name, father, national_id, birth, phone)
    VALUES (?, ?, ?, ?, ?)
    """, (
        data["name"],
        data["father"],
        data["national_id"],
        data["birth"],
        data["phone"]
    ))
    conn.commit()

# ================= لیست =================
def get_players():
    c.execute("SELECT name, father, national_id, birth, phone FROM players")
    rows = c.fetchall()

    if not rows:
        return "هیچ بازیکنی ثبت نشده است."

    result = ""
    for r in rows:
        result += (
            f"👤 نام: {r[0]}\n"
            f"👨 پدر: {r[1]}\n"
            f"🆔 کد ملی: {r[2]}\n"
            f"🎂 تولد: {r[3]}\n"
            f"📞 تماس: {r[4]}\n"
            "----------------------\n"
        )
    return result

# ================= webhook =================
@app.route("/", methods=["POST"])
def webhook():
    global ADMIN_ID

    data = request.json
    if not data or "message" not in data:
        return "ok"

    msg = data["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")

    if chat_id not in users:
        users[chat_id] = {"step": 0, "data": {}}

    user = users[chat_id]

    # ================= /id =================
    if text == "/id":
        ADMIN_ID = chat_id
        send_message(chat_id, f"🆔 آیدی شما ثبت شد:\n{chat_id}\n✔ شما ادمین شدید")

    # ================= start =================
    elif text == "/start":
        send_message(chat_id, "👋 سلام!\nنام و نام خانوادگی را وارد کنید:")
        user["step"] = 1

    # ================= players =================
    elif text == "/players":
        if ADMIN_ID == chat_id:
            send_message(chat_id, "📋 لیست بازیکنان:\n\n" + get_players())
        else:
            send_message(chat_id, "⛔ دسترسی ندارید")

    # ================= ثبت نام =================
    elif user["step"] == 1:
        if not is_name(text):
            send_message(chat_id, "❌ نام معتبر نیست")
        else:
            user["data"]["name"] = text
            send_message(chat_id, "👨 نام پدر؟")
            user["step"] = 2

    elif user["step"] == 2:
        if not is_name(text):
            send_message(chat_id, "❌ نام پدر معتبر نیست")
        else:
            user["data"]["father"] = text
            send_message(chat_id, "🆔 کد ملی؟ (10 رقم)")
            user["step"] = 3

    elif user["step"] == 3:
        if not is_national_id(text):
            send_message(chat_id, "❌ کد ملی باید 10 رقم باشد")
        else:
            user["data"]["national_id"] = text
            send_message(chat_id, "🎂 تاریخ تولد؟ (مثال: 1385/05/12)")
            user["step"] = 4

    elif user["step"] == 4:
        if not is_date(text):
            send_message(chat_id, "❌ فرمت تاریخ اشتباه است")
        else:
            user["data"]["birth"] = text
            send_message(chat_id, "📞 شماره تماس؟")
            user["step"] = 5

    elif user["step"] == 5:
        if not is_phone(text):
            send_message(chat_id, "❌ شماره تلفن اشتباه است")
        else:
            user["data"]["phone"] = text

            save_player(user["data"])

            send_message(chat_id,
                "✅ ثبت نام کامل شد:\n\n"
                f"👤 نام: {user['data']['name']}\n"
                f"👨 پدر: {user['data']['father']}\n"
                f"🆔 کد ملی: {user['data']['national_id']}\n"
                f"🎂 تولد: {user['data']['birth']}\n"
                f"📞 تماس: {user['data']['phone']}"
            )

            user["step"] = 0
            user["data"] = {}

    return "ok"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

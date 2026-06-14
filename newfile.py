from flask import Flask, request
import requests
import sqlite3
import re

app = Flask(__name__)

BOT_TOKEN = "YOUR_TOKEN_HERE"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

ADMIN_ID = None

# ================= DB =================
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

users = {}

# ================= VALIDATION =================
def is_name(t):
    return t and not t.isdigit() and len(t) >= 2

def is_national_id(t):
    return t and t.isdigit() and len(t) == 10

def is_date(t):
    return bool(re.match(r"^\d{4}[/-]\d{1,2}[/-]\d{1,2}$", t))

def is_phone(t):
    return t and t.isdigit() and len(t) >= 10

# ================= SEND =================
def send_message(chat_id, text):
    requests.post(f"{BASE_URL}/sendMessage", data={
        "chat_id": chat_id,
        "text": text
    })

# ================= SAVE =================
def save_player(d):
    c.execute("""
    INSERT INTO players (name,father,national_id,birth,phone)
    VALUES (?,?,?,?,?)
    """, (d["name"], d["father"], d["national_id"], d["birth"], d["phone"]))
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

    if not chat_id or not text:
        return "ok"

    if chat_id not in users:
        users[chat_id] = {"step": 0, "data": {}}

    user = users[chat_id]

    # ================= /id =================
    if text == "/id":
        ADMIN_ID = chat_id
        send_message(chat_id, f"🆔 شما ادمین شدید:\n{chat_id}")
        return "ok"

    # ================= start =================
    if text == "/start":
        send_message(chat_id, "👤 نام و نام خانوادگی؟")
        user["step"] = 1
        return "ok"

    # ================= STEP 1 NAME =================
    if user["step"] == 1:
        if not is_name(text):
            send_message(chat_id, "❌ نام اشتباه است")
        else:
            user["data"]["name"] = text
            send_message(chat_id, "👨 نام پدر؟")
            user["step"] = 2

    # ================= STEP 2 FATHER =================
    elif user["step"] == 2:
        if not is_name(text):
            send_message(chat_id, "❌ نام پدر اشتباه است")
        else:
            user["data"]["father"] = text
            send_message(chat_id, "🆔 کد ملی؟ (10 رقم)")
            user["step"] = 3

    # ================= STEP 3 NATIONAL ID =================
    elif user["step"] == 3:
        if not is_national_id(text):
            send_message(chat_id, "❌ کد ملی باید 10 رقم باشد")
        else:
            user["data"]["national_id"] = text
            send_message(chat_id, "🎂 تاریخ تولد؟ (مثال: 1385/05/12)")
            user["step"] = 4

    # ================= STEP 4 BIRTH =================
    elif user["step"] == 4:
        if not is_date(text):
            send_message(chat_id, "❌ فرمت تاریخ اشتباه است")
        else:
            user["data"]["birth"] = text
            send_message(chat_id, "📞 شماره تماس؟")
            user["step"] = 5

    # ================= STEP 5 PHONE =================
    elif user["step"] == 5:
        if not is_phone(text):
            send_message(chat_id, "❌ شماره تماس اشتباه است")
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

BOT_TOKEN = "YOUR_TOKEN_HERE"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

ADMIN_ID = None

# ================= DB =================
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

users = {}

# ================= VALIDATION =================
def is_name(t):
    return t and not t.isdigit() and len(t) >= 2

def is_national_id(t):
    return t and t.isdigit() and len(t) == 10

def is_date(t):
    return bool(re.match(r"^\d{4}[/-]\d{1,2}[/-]\d{1,2}$", t))

def is_phone(t):
    return t and t.isdigit() and len(t) >= 10

# ================= SEND =================
def send_message(chat_id, text):
    requests.post(f"{BASE_URL}/sendMessage", data={
        "chat_id": chat_id,
        "text": text
    })

# ================= SAVE =================
def save_player(d):
    c.execute("""
    INSERT INTO players (name,father,national_id,birth,phone)
    VALUES (?,?,?,?,?)
    """, (d["name"], d["father"], d["national_id"], d["birth"], d["phone"]))
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

    if not chat_id or not text:
        return "ok"

    if chat_id not in users:
        users[chat_id] = {"step": 0, "data": {}}

    user = users[chat_id]

    # ================= /id =================
    if text == "/id":
        ADMIN_ID = chat_id
        send_message(chat_id, f"🆔 شما ادمین شدید:\n{chat_id}")
        return "ok"

    # ================= start =================
    if text == "/start":
        send_message(chat_id, "👤 نام و نام خانوادگی؟")
        user["step"] = 1
        return "ok"

    # ================= STEP 1 NAME =================
    if user["step"] == 1:
        if not is_name(text):
            send_message(chat_id, "❌ نام اشتباه است")
        else:
            user["data"]["name"] = text
            send_message(chat_id, "👨 نام پدر؟")
            user["step"] = 2

    # ================= STEP 2 FATHER =================
    elif user["step"] == 2:
        if not is_name(text):
            send_message(chat_id, "❌ نام پدر اشتباه است")
        else:
            user["data"]["father"] = text
            send_message(chat_id, "🆔 کد ملی؟ (10 رقم)")
            user["step"] = 3

    # ================= STEP 3 NATIONAL ID =================
    elif user["step"] == 3:
        if not is_national_id(text):
            send_message(chat_id, "❌ کد ملی باید 10 رقم باشد")
        else:
            user["data"]["national_id"] = text
            send_message(chat_id, "🎂 تاریخ تولد؟ (مثال: 1385/05/12)")
            user["step"] = 4

    # ================= STEP 4 BIRTH =================
    elif user["step"] == 4:
        if not is_date(text):
            send_message(chat_id, "❌ فرمت تاریخ اشتباه است")
        else:
            user["data"]["birth"] = text
            send_message(chat_id, "📞 شماره تماس؟")
            user["step"] = 5

    # ================= STEP 5 PHONE =================
    elif user["step"] == 5:
        if not is_phone(text):
            send_message(chat_id, "❌ شماره تماس اشتباه است")
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

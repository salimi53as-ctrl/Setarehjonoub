from flask import Flask, request
import requests
import sqlite3
import json
import os

app = Flask(__name__)

# ================= CONFIG =================
BOT_TOKEN = "19108680:VLIdd-6KJY_joTrmPwsTXkIXGVh9pgFs6lM"
BASE_URL = f"https://tapi.bale.ai/bot{BOT_TOKEN}"

ADMIN_ID = "848341355"
DB_FILE = "club.db"

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        chat_id TEXT,
        name TEXT,
        position TEXT,
        age TEXT,
        phone TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= SEND MESSAGE =================
def send_message(chat_id, text, reply_markup=None):
    payload = {"chat_id": chat_id, "text": text}
    if reply_markup:
        payload["reply_markup"] = json.dumps(reply_markup)

    requests.post(f"{BASE_URL}/sendMessage", data=payload)

# ================= SAVE PLAYER =================
def save_player(chat_id, name, position, age, phone):
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
    INSERT INTO players (chat_id, name, position, age, phone)
    VALUES (?, ?, ?, ?, ?)
    """, (chat_id, name, position, age, phone))

    conn.commit()
    conn.close()

# ================= GET ALL PLAYERS =================
def get_players():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("SELECT name, position, age, phone FROM players")
    rows = c.fetchall()

    conn.close()
    return rows

# ================= USERS TEMP STATE =================
users = {}

# ================= WEBHOOK =================
@app.route("/webhook", methods=["POST"])
def webhook():

    data = request.get_json()
    if not data:
        return "ok"

    # ================= MESSAGE =================
    if "message" in data:

        msg = data["message"]
        chat_id = str(msg["chat"]["id"])
        text = msg.get("text", "")

        if chat_id not in users:
            users[chat_id] = {"step": 0, "data": {}}

        u = users[chat_id]

        # ================= START =================
        if text == "/start":
            send_message(chat_id,
                "⚽ باشگاه ستاره جنوب 🐉\nثبت‌نام شروع شد\n\n👤 نام و نام خانوادگی؟"
            )
            u["step"] = 1

        elif u["step"] == 1:
            u["data"]["name"] = text
            send_message(chat_id, "⚽ پست؟ (دروازه‌بان/دفاع/هافبک/حمله)")
            u["step"] = 2

        elif u["step"] == 2:
            u["data"]["position"] = text
            send_message(chat_id, "👶 رده سنی؟")
            u["step"] = 3

        elif u["step"] == 3:
            u["data"]["age"] = text
            send_message(chat_id, "📞 شماره تماس؟")
            u["step"] = 4

        elif u["step"] == 4:
            u["data"]["phone"] = text

            # ===== SAVE TO DATABASE =====
            save_player(
                chat_id,
                u["data"]["name"],
                u["data"]["position"],
                u["data"]["age"],
                u["data"]["phone"]
            )

            send_message(chat_id,
                "✅ ثبت‌نام کامل شد ⚽\nبه ستاره جنوب خوش آمدی 🐉"
            )

            u["step"] = 0

        # ================= ADMIN =================
        elif text == "/admin":

            if chat_id != ADMIN_ID:
                send_message(chat_id, "⛔ دسترسی ندارید")
                return "ok"

            players = get_players()

            if not players:
                send_message(chat_id, "هیچ بازیکنی ثبت نشده")
                return "ok"

            msg_text = "📋 لیست بازیکنان ستاره جنوب:\n\n"

            for i, p in enumerate(players, start=1):
                msg_text += (
                    f"{i})\n"
                    f"👤 {p[0]}\n"
                    f"⚽ {p[1]}\n"
                    f"👶 {p[2]}\n"
                    f"📞 {p[3]}\n"
                    "------------------\n"
                )

            send_message(chat_id, msg_text)

        return "ok"

    return "ok"

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

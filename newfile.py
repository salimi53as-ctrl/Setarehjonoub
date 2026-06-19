from flask import Flask, request, render_template_string
import requests
import sqlite3
import os

app = Flask(__name__)

# ================= BOT TOKEN =================
BOT_TOKEN = "19108680:VLIdd-6KJY_joTrmPwsTXkIXGVh9pgFs6lM"
BASE_URL = f"https://tapi.bale.ai/bot{848341355}"

users = {}

# ================= DATABASE =================
DB = "club.db"

def init_db():
    conn = sqlite3.connect(DB)
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
    conn.close()

init_db()

def save_player(data):
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("""
        INSERT INTO players (name, father, national_id, birth, phone)
        VALUES (?, ?, ?, ?, ?)
    """, (
        data.get("name"),
        data.get("father"),
        data.get("national_id"),
        data.get("birth"),
        data.get("phone")
    ))
    conn.commit()
    conn.close()

def get_players():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    c.execute("SELECT name, father, national_id, birth, phone FROM players")
    rows = c.fetchall()
    conn.close()
    return rows

# ================= SEND MESSAGE =================
def send_message(chat_id, text):
    try:
        requests.post(f"{BASE_URL}/sendMessage", data={
            "chat_id": chat_id,
            "text": text
        })
    except:
        pass

# ================= WEBHOOK =================
@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.json

    if not data or "message" not in data:
        return "ok"

    msg = data["message"]
    chat_id = msg["chat"]["id"]
    text = msg.get("text", "")

    if chat_id not in users:
        users[chat_id] = {"step": 0, "data": {}}

    user = users[chat_id]

    if text == "/start":
        send_message(chat_id, "👋 سلام!\nنام و نام خانوادگی:")
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

        save_player(user["data"])

        send_message(chat_id,
            "✅ ثبت شد ✔️\n\n"
            f"👤 {user['data']['name']}\n"
            f"📞 {user['data']['phone']}"
        )

        user["step"] = 0
        user["data"] = {}

    return "ok"

# ================= DASHBOARD =================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>ستاره جنوب</title>
    <style>
        body {
            background: #0b1a2b;
            color: white;
            font-family: sans-serif;
            text-align: center;
        }

        h1 {
            color: gold;
        }

        table {
            margin: auto;
            width: 95%;
            border-collapse: collapse;
        }

        th, td {
            border: 1px solid #444;
            padding: 10px;
        }

        th {
            background: #1f3b5c;
            color: gold;
        }
    </style>
</head>
<body>

<h1>⚽ باشگاه ستاره جنوب 🐉</h1>
<p>داشبورد بازیکنان</p>

<table>
<tr>
    <th>نام</th>
    <th>پدر</th>
    <th>کد ملی</th>
    <th>تولد</th>
    <th>تماس</th>
</tr>

{% for p in players %}
<tr>
    <td>{{p[0]}}</td>
    <td>{{p[1]}}</td>
    <td>{{p[2]}}</td>
    <td>{{p[3]}}</td>
    <td>{{p[4]}}</td>
</tr>
{% endfor %}

</table>

</body>
</html>
"""

@app.route("/")
def home():
    return render_template_string(HTML, players=get_players())

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

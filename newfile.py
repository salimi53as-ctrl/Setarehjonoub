from flask import Flask, render_template_string
import sqlite3
import os

app = Flask(__name__)

DB_FILE = "club.db"

# ================= DATABASE =================
def init_db():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS players (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        position TEXT,
        age TEXT,
        phone TEXT
    )
    """)

    conn.commit()
    conn.close()

init_db()

# ================= GET PLAYERS =================
def get_players():
    conn = sqlite3.connect(DB_FILE)
    c = conn.cursor()
    c.execute("SELECT name, position, age, phone FROM players")
    rows = c.fetchall()
    conn.close()
    return rows

# ================= DASHBOARD HTML =================
HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>باشگاه ستاره جنوب</title>
    <style>
        body {
            font-family: sans-serif;
            background: linear-gradient(135deg, #0b1a2b, #142b44);
            color: white;
            text-align: center;
            margin: 0;
        }

        h1 {
            color: gold;
            margin-top: 20px;
        }

        table {
            margin: 30px auto;
            width: 90%;
            border-collapse: collapse;
            background: rgba(255,255,255,0.05);
            border-radius: 10px;
            overflow: hidden;
        }

        th, td {
            padding: 12px;
            border-bottom: 1px solid #333;
        }

        th {
            background: #1f3b5c;
            color: gold;
        }

        tr:hover {
            background: rgba(255,255,255,0.1);
        }

        .box {
            margin-top: 20px;
        }
    </style>
</head>
<body>

<h1>⚽ باشگاه ستاره جنوب 🐉</h1>
<p>داشبورد مدیریت بازیکنان</p>

<div class="box">
<table>
<tr>
<th>نام</th>
<th>پست</th>
<th>رده سنی</th>
<th>شماره تماس</th>
</tr>

{% for p in players %}
<tr>
<td>{{ p[0] }}</td>
<td>{{ p[1] }}</td>
<td>{{ p[2] }}</td>
<td>{{ p[3] }}</td>
</tr>
{% endfor %}

</table>
</div>

</body>
</html>
"""

# ================= ROUTE =================
@app.route("/")
def dashboard():
    players = get_players()
    return render_template_string(HTML, players=players)

# ================= RUN =================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

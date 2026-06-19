from flask import Flask, request, redirect, url_for
import sqlite3
import os

app = Flask(__name__)

DB_PATH = "data.db"


# =========================
# ساخت دیتابیس
# =========================
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS players (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age TEXT,
            position TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


# =========================
# صفحه اصلی
# =========================
@app.route("/")
def home():
    return """
    <h1>📊 باشگاه ستاره جنوب (حرفه‌ای)</h1>
    <hr>

    <a href="/players">👥 لیست بازیکنان</a><br>
    <a href="/add">➕ افزودن بازیکن</a><br>
    <a href="/health">🟢 تست سرور</a><br>
    """


# =========================
# سلامت سرور
# =========================
@app.route("/health")
def health():
    return "OK - Server is Running"


# =========================
# لیست بازیکنان
# =========================
@app.route("/players")
def players():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT * FROM players")
    rows = c.fetchall()
    conn.close()

    html = "<h2>👥 لیست بازیکنان</h2><hr>"

    for p in rows:
        html += f"""
        {p[0]}. {p[1]} | سن: {p[2]} | پست: {p[3]}
        <a href="/delete/{p[0]}">🗑 حذف</a>
        <a href="/edit/{p[0]}">✏ ویرایش</a>
        <br>
        """

    html += "<br><a href='/'>برگشت</a>"
    return html


# =========================
# افزودن بازیکن
# =========================
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        position = request.form.get("position")

        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute("INSERT INTO players (name, age, position) VALUES (?, ?, ?)",
                  (name, age, position))
        conn.commit()
        conn.close()

        return redirect(url_for("players"))

    return """
    <h2>➕ افزودن بازیکن</h2>
    <form method="post">
        نام: <input name="name"><br><br>
        سن: <input name="age"><br><br>
        پست: <input name="position"><br><br>
        <button type="submit">ثبت</button>
    </form>
    """


# =========================
# حذف بازیکن
# =========================
@app.route("/delete/<int:id>")
def delete(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM players WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for("players"))


# =========================
# ویرایش بازیکن
# =========================
@app.route("/edit/<int:id>", methods=["GET", "POST"])
def edit(id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        position = request.form.get("position")

        c.execute("""
            UPDATE players
            SET name=?, age=?, position=?
            WHERE id=?
        """, (name, age, position, id))

        conn.commit()
        conn.close()

        return redirect(url_for("players"))

    c.execute("SELECT * FROM players WHERE id=?", (id,))
    player = c.fetchone()
    conn.close()

    return f"""
    <h2>✏ ویرایش بازیکن</h2>
    <form method="post">
        نام: <input name="name" value="{player[1]}"><br><br>
        سن: <input name="age" value="{player[2]}"><br><br>
        پست: <input name="position" value="{player[3]}"><br><br>
        <button type="submit">ذخیره</button>
    </form>
    """


# =========================
# اجرا
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)

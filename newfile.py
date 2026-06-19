from flask import Flask, request, redirect, url_for
import os

app = Flask(__name__)

# =========================
# فایل بازیکنان
# =========================
if not os.path.exists("players.txt"):
    open("players.txt", "w", encoding="utf-8").close()


# =========================
# استایل حرفه‌ای
# =========================
STYLE = """
<style>
body { font-family: Arial; background:#0f172a; color:white; text-align:center; }
a { color:#38bdf8; text-decoration:none; margin:10px; display:inline-block; }
.card { background:#1e293b; padding:15px; margin:10px auto; width:60%; border-radius:10px; }
button { padding:5px 10px; border:none; border-radius:5px; cursor:pointer; }
input { padding:5px; margin:5px; }
</style>
"""


# =========================
# داشبورد
# =========================
@app.route("/")
def home():
    return STYLE + """
    <h1>📊 باشگاه ستاره جنوب</h1>

    <div class="card">
        🏟️ باشگاه: ستاره جنوب<br>
        ⚽ وضعیت: فعال<br>
        👥 سیستم مدیریت بازیکنان
    </div>

    <a href="/players">👥 بازیکنان</a>
    <a href="/add">➕ افزودن بازیکن</a>
    """


# =========================
# لیست بازیکنان + حذف
# =========================
@app.route("/players")
def players():
    with open("players.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    html = STYLE + "<h2>👥 لیست بازیکنان</h2>"

    if not lines:
        return html + "<p>⚠️ بازیکنی وجود ندارد</p><a href='/'>برگشت</a>"

    for i, line in enumerate(lines):
        name, age, position = line.strip().split(",")

        html += f"""
        <div class="card">
            {name} | سن: {age} | پست: {position}<br><br>
            <a href="/delete/{i}">🗑 حذف</a>
        </div>
        """

    html += "<a href='/'>برگشت</a>"
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

        with open("players.txt", "a", encoding="utf-8") as f:
            f.write(f"{name},{age},{position}\n")

        return redirect(url_for("players"))

    return STYLE + """
    <h2>➕ افزودن بازیکن</h2>

    <form method="post">
        <input name="name" placeholder="نام"><br>
        <input name="age" placeholder="سن"><br>
        <input name="position" placeholder="پست"><br><br>
        <button type="submit">ثبت</button>
    </form>

    <br><a href="/">برگشت</a>
    """


# =========================
# حذف بازیکن
# =========================
@app.route("/delete/<int:index>")
def delete(index):
    with open("players.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()

    if 0 <= index < len(lines):
        lines.pop(index)

    with open("players.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)

    return redirect(url_for("players"))


# =========================
# اجرای برنامه
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

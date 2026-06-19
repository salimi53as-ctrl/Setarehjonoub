from flask import Flask, request, redirect, url_for
import os

app = Flask(__name__)

# =========================
# ساخت فایل بازیکنان
# =========================
if not os.path.exists("players.txt"):
    open("players.txt", "w", encoding="utf-8").close()


# =========================
# تست سلامت سرور (خیلی مهم برای Render)
# =========================
@app.route("/health")
def health():
    return "OK - Server is Running"


@app.route("/test")
def test():
    return "TEST OK - App Works"


# =========================
# داشبورد
# =========================
@app.route("/")
def home():
    return """
    <h1>📊 باشگاه ستاره جنوب</h1>
    <hr>
    🏟️ باشگاه: ستاره جنوب <br>
    ⚽ وضعیت: فعال <br>
    👥 مدیریت بازیکنان: فعال <br><br>

    <a href="/players">👥 لیست بازیکنان</a><br>
    <a href="/add">➕ افزودن بازیکن</a><br>
    <a href="/health">🟢 تست سرور</a><br>
    <a href="/test">🧪 تست دوم</a><br>
    """


# =========================
# نمایش بازیکنان
# =========================
@app.route("/players")
def players():
    try:
        with open("players.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        if not lines:
            return "<h2>⚠️ هیچ بازیکنی ثبت نشده</h2><br><a href='/'>برگشت</a>"

        html = "<h2>👥 لیست بازیکنان</h2><hr>"

        for i, line in enumerate(lines):
            parts = line.strip().split(",")

            if len(parts) == 3:
                name, age, position = parts
                html += f"{i+1}. {name} | سن: {age} | پست: {position}<br>"

        html += "<br><a href='/'>برگشت</a>"
        return html

    except Exception as e:
        return f"<h2>❌ خطا</h2><p>{e}</p>"


# =========================
# افزودن بازیکن
# =========================
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form.get("name")
        age = request.form.get("age")
        position = request.form.get("position")

        if name and age and position:
            with open("players.txt", "a", encoding="utf-8") as f:
                f.write(f"{name},{age},{position}\n")

        return redirect(url_for("players"))

    return """
    <h2>➕ افزودن بازیکن</h2>

    <form method="post">
        نام: <input name="name"><br><br>
        سن: <input name="age"><br><br>
        پست: <input name="position"><br><br>
        <button type="submit">ثبت</button>
    </form>

    <br><a href="/">برگشت</a>
    """


# =========================
# اجرای برنامه (خیلی مهم برای Render)
# =========================
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

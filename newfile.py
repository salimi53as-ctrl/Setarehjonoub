from flask import Flask, request, redirect, url_for

app = Flask(__name__)

# =========================
# ساخت فایل اگر وجود ندارد
# =========================
try:
    open("players.txt", "x", encoding="utf-8").close()
except:
    pass


# =========================
# داشبورد
# =========================
@app.route("/")
def home():
    return """
    <h1>📊 داشبورد باشگاه ستاره جنوب</h1>
    <hr>
    🏟️ نام باشگاه: ستاره جنوب <br>
    ⚽ وضعیت: فعال <br>
    👥 مدیریت بازیکنان: فعال <br><br>

    <a href='/players'>👥 لیست بازیکنان</a><br>
    <a href='/add'>➕ افزودن بازیکن</a>
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
            return "<h2>⚠️ هیچ بازیکنی ثبت نشده</h2><a href='/'>برگشت</a>"

        html = "<h2>👥 لیست بازیکنان</h2><hr>"

        for i, line in enumerate(lines, 1):
            name, age, position = line.strip().split(",")
            html += f"{i}. {name} | سن: {age} | پست: {position}<br>"

        html += "<br><a href='/'>برگشت</a>"
        return html

    except:
        return "<h2>❌ خطا در خواندن فایل</h2>"


# =========================
# افزودن بازیکن (فرم)
# =========================
@app.route("/add", methods=["GET", "POST"])
def add():
    if request.method == "POST":
        name = request.form["name"]
        age = request.form["age"]
        position = request.form["position"]

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

    <br><a href='/'>برگشت</a>
    """


# =========================
# اجرای برنامه
# =========================
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)

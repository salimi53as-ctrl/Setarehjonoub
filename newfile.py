from flask import Flask, request, redirect, url_for, session
import sqlite3
import os

app = Flask(__name__)

# کلید امنیت Session
app.secret_key = "SETAREH_JONOUB_1388"

# اطلاعات مدیر (فعلاً ثابت)
ADMIN_USER = "admin"
ADMIN_PASS = "12345"

DB = "club.db"


# ساخت دیتابیس
def init_db():
    conn = sqlite3.connect(DB)
    c = conn.cursor()

    c.execute("""
    CREATE TABLE IF NOT EXISTS players(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        age TEXT,
        position TEXT
    )
    """)

    conn.commit()
    conn.close()


init_db()


# بررسی ورود مدیر
def login_required(func):
    def wrapper(*args, **kwargs):
        if "admin" not in session:
            return redirect(url_for("login"))
        return func(*args, **kwargs)
    wrapper.__name__ = func.__name__
    return wrapper


# صفحه اصلی
@app.route("/")
def home():
    if "admin" in session:
        return redirect("/dashboard")

    return """
    <h1>🐉⭐ باشگاه ستاره جنوب</h1>
    <h3>Setareh Jonoub Football Academy</h3>
    <hr>

    <a href="/login">
        🔐 ورود مدیریت
    </a>
    """


# ورود مدیر
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        user = request.form.get("username")
        password = request.form.get("password")

        if user == ADMIN_USER and password == ADMIN_PASS:
            session["admin"] = True
            return redirect("/dashboard")

        return """
        <h3>❌ نام کاربری یا رمز اشتباه است</h3>
        <a href="/login">تلاش دوباره</a>
        """

    return """
    <h2>🔐 ورود مدیر باشگاه</h2>

    <form method="POST">

    نام کاربری:
    <input name="username"><br><br>

    رمز عبور:
    <input type="password" name="password"><br><br>

    <button>
    ورود
    </button>

    </form>
    """

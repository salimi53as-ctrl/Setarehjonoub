import os

# =========================
# ساخت فایل بازیکنان اگر وجود ندارد
# =========================
if not os.path.exists("players.txt"):
    with open("players.txt", "w", encoding="utf-8") as f:
        f.write("")

# =========================
# داشبورد
# =========================
def dashboard():
    print("\n" + "="*40)
    print("📊 داشبورد باشگاه ستاره جنوب")
    print("="*40)
    print("🏟️ نام باشگاه: ستاره جنوب")
    print("⚽ وضعیت: فعال")
    print("👥 مدیریت بازیکنان: فعال")
    print("="*40)

# =========================
# افزودن بازیکن
# =========================
def add_player():
    name = input("نام بازیکن: ")
    age = input("سن: ")
    position = input("پست: ")

    with open("players.txt", "a", encoding="utf-8") as f:
        f.write(f"{name},{age},{position}\n")

    print("✅ بازیکن با موفقیت اضافه شد!")

# =========================
# نمایش بازیکنان
# =========================
def show_players():
    print("\n📋 لیست بازیکنان:")

    try:
        with open("players.txt", "r", encoding="utf-8") as f:
            lines = f.readlines()

        if len(lines) == 0:
            print("⚠️ هیچ بازیکنی ثبت نشده است")
            return

        for i, line in enumerate(lines, start=1):
            name, age, position = line.strip().split(",")
            print(f"{i}. {name} | سن: {age} | پست: {position}")

    except FileNotFoundError:
        print("❌ فایل بازیکنان وجود ندارد")

# =========================
# منوی اصلی
# =========================
def menu():
    while True:
        dashboard()

        print("\n1️⃣ افزودن بازیکن")
        print("2️⃣ نمایش بازیکنان")
        print("3️⃣ خروج")

        choice = input("انتخاب شما: ")

        if choice == "1":
            add_player()
        elif choice == "2":
            show_players()
        elif choice == "3":
            print("👋 خروج از برنامه")
            break
        else:
            print("❌ انتخاب نامعتبر")

# =========================
# اجرای برنامه
# =========================
menu()

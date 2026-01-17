import requests
from datetime import datetime
from zoneinfo import ZoneInfo
import os

# ===== ENV (GitHub Secrets) =====
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"].strip()
CHAT_ID = int(os.environ["TELEGRAM_CHAT_ID"])
THREAD_ID = int(os.environ["TELEGRAM_THREAD_ID"])

# ===== TIMEZONE =====
TZ = ZoneInfo("Asia/Shanghai")

# ===== PASSWORD LOGIC =====
def build_password():
    now = datetime.now(TZ)
    day = now.day
    month = now.month
    year = now.year

    top = f"{month:02d}{day:02d}"   # MMDD
    bottom = f"{year}"              # YYYY

    result_digits = []
    for t, b in zip(top[:-1], bottom[:-1]):
        result_digits.append(str(int(t) + int(b)))
    result_digits.append(str(int(top[-1]) + int(bottom[-1])))

    password = "".join(result_digits)
    return password, day, month, year

# ===== MESSAGE =====
def build_message() -> str:
    password, day, month, year = build_password()

    msg = (
        f"🔐 Пароль на актуальную дату:\n"
        f"<b>{day:02d}.{month:02d}.{year}</b>\n\n"
        f"Пароль: <b>{password}</b>"
    )

    print(
        f"[LOG] {datetime.now(TZ).strftime('%d.%m.%Y %H:%M:%S')} "
        f"→ Пароль: {password}"
    )
    return msg

# ===== SEND =====
def main():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    payload = {
        "chat_id": CHAT_ID,
        "message_thread_id": THREAD_ID,
        "text": build_message(),
        "parse_mode": "HTML",
        "disable_web_page_preview": True,
    }

    resp = requests.post(url, json=payload, timeout=10)
    print("Status:", resp.status_code)
    print("Response:", resp.text)
    resp.raise_for_status()

# ===== ENTRY =====
if __name__ == "__main__":
    main()

import requests
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+
import os

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"].strip()
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"].strip()

TZ = ZoneInfo("Europe/Minsk")

def build_message() -> str:
    now = datetime.now(TZ)

    day = now.day
    month = now.month
    year = now.year

    # МесяцДень сверху
    top = f"{month:02d}{day:02d}"  # 12 25 -> "1225"
    # Год снизу
    bottom = f"{year}"             # "2025"

    # Сложение по столбикам без переноса
    result_digits = []
    for t_digit, b_digit in zip(top[:-1], bottom[:-1]):  # все кроме последнего
        result_digits.append(str(int(t_digit) + int(b_digit)))
    # Крайний правый разряд (может быть двухзначным)
    result_digits.append(str(int(top[-1]) + int(bottom[-1])))

    result = "".join(result_digits)

    widest = max(len(top), len(bottom), len(result))
    sep = "-" * widest

    msg = (
        f"Пароль на актуальную дату: <b>{day:02d}.{month:02d}.{year}</b>\n\n"
        f"<pre>"
        f"{top.rjust(widest)}\n"
        f"+{bottom.rjust(widest)}\n"
        f"{sep}\n"
        f"{result.rjust(widest)}"
        f"</pre>\n\n"
        f"Пароль: <b>{result}</b>"
    )
    return msg

def main():
    text = build_message()

    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": text,
        "parse_mode": "HTML",
    }

    resp = requests.post(url, data=payload)
    print("Status:", resp.status_code)
    print("Response:", resp.text)
    resp.raise_for_status()

if __name__ == "__main__":
    main()

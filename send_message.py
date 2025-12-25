import requests
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+

import os

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]


TZ = ZoneInfo("Europe/Minsk")


def build_message() -> str:
    now = datetime.now(TZ)

    day = now.day
    month = now.month
    year = now.year

    day_month_num = int(f"{day:02d}{month:02d}")
    base = 2025
    password = day_month_num + base

    widest = max(len(str(day_month_num)), len(str(base)), len(str(password)))
    sep = "-" * widest

    msg = (
        f"Пароль на актуальную дату: <b>{day:02d}.{month:02d}.{year}</b>\n\n"
        f"<pre>"
        f"{str(day_month_num).rjust(widest)}\n"
        f"+{str(base).rjust(widest)}\n"
        f"{sep}\n"
        f"{str(password).rjust(widest)}"
        f"</pre>\n\n"
        f"Пароль: <b>{password}</b>"
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

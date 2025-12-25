import requests
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+
import os

# Берём токены из секретов и убираем лишние пробелы/переносы
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"].strip()
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"].strip()

TZ = ZoneInfo("Europe/Minsk")


def build_message() -> str:
    now = datetime.now(TZ)

    day = now.day
    month = now.month
    year = now.year

    # Верхняя строка: МесяцДень (MMDD)
    top = f"{month}{day:02d}"  # для 25.12 → "1225"
    # Нижняя строка: Год
    bottom = f"{year}"         # "2025"

    # Сложение столбиком без переноса
    result = ""
    for i in range(len(top)-1):
        result += str(int(top[i]) + int(bottom[i]))
    # Крайний правый разряд может быть двухзначным
    result += str(int(top[-1]) + int(bottom[-1]))

    # Определяем ширину для красивого форматирования
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

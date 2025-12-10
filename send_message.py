import os
import requests
from datetime import datetime
from zoneinfo import ZoneInfo  # доступно в Python 3.9+


# Токен бота и ID чата берём из переменных окружения (GitHub Secrets)
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"]

# Часовой пояс — Минск
TZ = ZoneInfo("Europe/Minsk")


def build_message() -> str:
    # Текущая дата/время по Минску
    now = datetime.now(TZ)

    day = now.day       # 1..31
    month = now.month   # 1..12
    year = now.year     # например, 2025

    # Форматируем день и месяц как ДДММ, например 1 марта -> "0103" -> 103
    day_month_str = f"{day:02d}{month:02d}"
    day_month_num = int(day_month_str)

    base = 2025
    password = day_month_num + base

    # Подбираем ширину для красивого выравнивания «столбиком»
    widest = max(len(str(day_month_num)), len(str(base)), len(str(password)))
    line_top = str(day_month_num).rjust(widest)
    line_mid = str(base).rjust(widest)
    line_sum = str(password).rjust(widest)
    sep = "-" * widest

    # Сообщение в HTML с блоком <pre> для моноширинного «столбика»
    msg = (
        f"Пароль на актуальную дату: <b>{day:02d}.{month:02d}.{year}</b>\n\n"
        f"<pre>"
        f"{line_top}\n"
        f"+{line_mid}\n"
        f"{sep}\n"
        f"{line_sum}"
        f"</pre>\n\n"
        f"Пароль: <b>{password}</b>"
    )

    return msg


def main():
    text = build_message()

    url = f"https://api.telegram.org/bot{8260796784:AAEKBN14VgBilXiW-2Xmgs_fKyougStIgpc}/sendMessage"
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

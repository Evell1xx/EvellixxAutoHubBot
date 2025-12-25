import requests
from datetime import datetime
from zoneinfo import ZoneInfo  # Python 3.9+
import os

# Берём токены из секретов и убираем лишние пробелы/переносы
TOKEN = os.environ["TELEGRAM_BOT_TOKEN"].strip()
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"].strip()

# Часовой пояс Минска
TZ = ZoneInfo("Europe/Minsk")

def build_message() -> str:
    now = datetime.now(TZ)

    day = now.day
    month = now.month
    year = now.year

    # Верхняя строка: МесяцДень (MMDD)
    top = f"{month:02d}{day:02d}"  # 25.12 → "1225"
    # Нижняя строка: Год
    bottom = f"{year}"              # "2025"

    # Сложение по столбикам без переноса
    result_digits = []
    for t_digit, b_digit in zip(top[:-1], bottom[:-1]):  # все кроме последнего
        result_digits.append(str(int(t_digit) + int(b_digit)))
    # Крайний правый разряд (может быть двухзначным)
    result_digits.append(str(int(top[-1]) + int(bottom[-1])))

    # Собираем итоговый пароль
    password = "".join(result_digits)

    # Ширина для красивого форматирования
    widest = max(len(top), len(bottom), len(password))
    sep = "-" * widest

    msg = (
        f"Пароль на актуальную дату: <b>{day:02d}.{month:02d}.{year}</b>\n\n"
        f"<pre>"
        f"{top.rjust(widest)}\n"
        f"+{bottom.rjust(widest)}\n"
        f"{sep}\n"
        f"{password.rjust(widest)}"
        f"</pre>\n\n"
        f"Пароль: <b>{password}</b>"
    )
    
    # Лог для GitHub Actions
    print(f"[LOG] {datetime.now(TZ).strftime('%d.%m.%Y %H:%M:%S')} → Пароль: {password}")
    
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

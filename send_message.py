import requests
from datetime import datetime
from zoneinfo import ZoneInfo  
import os

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"].strip()
CHAT_ID = os.environ["TELEGRAM_CHAT_ID"].strip()


TZ = ZoneInfo("Asia/Shanghai")

def build_password() -> str:
    now = datetime.now(TZ)
    day = now.day
    month = now.month
    year = now.year

    
    top = f"{month:02d}{day:02d}"  
    bottom = f"{year}"              

  
    result_digits = []
    for t_digit, b_digit in zip(top[:-1], bottom[:-1]):
        result_digits.append(str(int(t_digit) + int(b_digit)))
    result_digits.append(str(int(top[-1]) + int(bottom[-1])))

    password = "".join(result_digits)
    return password, day, month, year

def build_message() -> str:
    password, day, month, year = build_password()
    msg = (
        f"Пароль на актуальную дату: <b>{day:02d}.{month:02d}.{year}</b>\n\n"
        f"Пароль: <b>{password}</b>"
    )
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

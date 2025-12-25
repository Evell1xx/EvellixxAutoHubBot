import os
import requests

command = os.environ.get("BOT_COMMAND", "").lower()
token = os.environ["TELEGRAM_BOT_TOKEN"].strip()
chat_id = os.environ["TELEGRAM_CHAT_ID"].strip()

if command == "version":
    text = """На данный момент актуальная версия VoyahOS для Рест/318 - 6.11.1, вот её описание:

VOYAH OS 6.11.1

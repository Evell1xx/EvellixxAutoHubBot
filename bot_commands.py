from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

TOKEN = os.environ["TELEGRAM_BOT_TOKEN"].strip()

# Команды
async def versions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Версия бота: 1.0.0\nОбновления: 25.12.2025")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Список команд:\n/start\n/versions\n/help")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Привет! Используй /versions чтобы узнать версию.")

# Основной запуск
app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("versions", versions))
app.add_handler(CommandHandler("help", help_command))

print("Command bot is running...")
app.run_polling()

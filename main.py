
from telegram.ext import Application, CommandHandler
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text("NEET AI हिंदी बोट सक्रिय है।")

async def quiz(update, context):
    await update.message.reply_text("क्विज सिस्टम जुड़ गया है।")

app = Application.builder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("quiz", quiz))

print("Bot started...")
app.run_polling()

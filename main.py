from telegram.ext import Application, CommandHandler
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update, context):
    await update.message.reply_text(
        "NEET AI हिंदी बोट सक्रिय है।\n\nक्विज शुरू करने के लिए /quizar लिखें।"
    )

async def quiz(update, context):
    await update.message.reply_text(
        "क्विज सिस्टम जुड़ गया है।\n\nउदाहरण: /quizar कोशिका 90"
    )

app = Application.builder().token(TOKEN).build()

# सभी commands में ar जोड़ा गया
app.add_handler(CommandHandler("startar", start))
app.add_handler(CommandHandler("quizar", quiz))

print("Bot started...")
app.run_polling()

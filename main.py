import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "NEET AI हिंदी बोट सक्रिय है।\n\nक्विज शुरू करने के लिए /quizar लिखें।"
    )

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "उदाहरण: /quizar कोशिका 90"
        )
        return

    topic = context.args[0]
    count = 30

    if len(context.args) > 1:
        try:
            count = max(10, min(180, int(context.args[1])))
        except:
            count = 30

    await update.message.reply_text(
        f"विषय: {topic}\nप्रश्न: {count}\n\nNEET-स्तर के प्रश्न तैयार किए जा रहे हैं..."
    )

app = Application.builder().token(TOKEN).build()

app.add_handler(CommandHandler("startar", start))
app.add_handler(CommandHandler("quizar", quiz))

if __name__ == "__main__":
    print("Bot started...")
    app.run_polling()

import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# अपनी files import करो
from quiz import quiz
from chapter import chapter_quiz
from pdf import upload_pdf

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

# /startar
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message = (
        "NEET AI हिंदी बोट सक्रिय है।\n\n"
        "उपलब्ध Commands:\n"
        "/startar - बोट शुरू करें\n"
        "/quizar कोशिका 90 - टॉपिक क्विज\n"
        "/chapterar आनुवंशिकी 180 - अध्याय क्विज\n"
        "/uploadpdfar - PDF अपलोड करें\n"
    )
    await update.message.reply_text(message)

def main():
    if not TOKEN:
        raise ValueError(
            "TELEGRAM_BOT_TOKEN environment variable सेट नहीं है।"
        )

    app = Application.builder().token(TOKEN).build()

    # सभी commands में ar suffix
    app.add_handler(CommandHandler("startar", start))
    app.add_handler(CommandHandler("quizar", quiz))
    app.add_handler(CommandHandler("chapterar", chapter_quiz))
    app.add_handler(CommandHandler("uploadpdfar", upload_pdf))

    print("Bot started...")
    app.run_polling()

if __name__ == "__main__":
    main()

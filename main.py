import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

from quiz import quiz
from chapter import chapter_quiz
from pdf import upload_pdf

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "NEET AI हिंदी बोट सक्रिय है।\n\n"
        "/quizar कोशिका 90\n"
        "/chapterar आनुवंशिकी 180\n"
        "/uploadpdfar\n"
        "/helpar"
    )

async def helpar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "उपलब्ध Commands:\n\n"
        "/startar\n"
        "/quizar कोशिका 90\n"
        "/chapterar आनुवंशिकी 180\n"
        "/uploadpdfar\n"
        "/leaderboardar\n"
        "/resumear\n"
        "/profilear\n"
        "/helpar"
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("startar", start))
    app.add_handler(CommandHandler("helpar", helpar))
    app.add_handler(CommandHandler("quizar", quiz))
    app.add_handler(CommandHandler("chapterar", chapter_quiz))
    app.add_handler(CommandHandler("uploadpdfar", upload_pdf))

    print("Bot started...")
    app.run_polling(drop_pending_updates=True)

if __name__ == "__main__":
    main()

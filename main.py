import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes, MessageHandler, filters

from broadcast import broadcast, export_users, users_command
from database import init_db, save_user
from chapter import chapter_quiz
from diagram import diagram
from knowledge import knowledge, short_notes
from pdf import upload_pdf, upload_pdf_help
from quiz import quiz
from translator import translate_latest_pdf, translate_message

load_dotenv()

TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")


async def track_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user:
        save_user(update.effective_user)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "NEET Knowledge Bot सक्रिय है।\n\n"
        "/knowar प्रकाश संश्लेषण समझाओ\n"
        "/notesar कोशिका\n"
        "/diagramaar परागण और निषेचन\n"
        "/quizar कोशिका 30\n"
        "/chapterar आनुवंशिकी 30\n"
        "/uploadpdfar\n"
        "/translatear English\n"
        "/translatepdfar English\n"
        "/id"
    )


async def helpar(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Commands:\n\n"
        "/knowar <प्रश्न> — Hindi knowledge answer\n"
        "/notesar <topic> — Gemini-style short notes\n"
        "/diagramaar <topic> — educational SVG diagram\n"
        "/chapterar <chapter> <गिनती> — chapter quiz\n"
        "/quizar <विषय> <गिनती> — MCQ quiz\n"
        "/uploadpdfar — PDF भेजने की जानकारी\n"
        "/translatear <भाषा> — replied text translate\n"
        "/translatepdfar <भाषा> — latest PDF translate\n"
        "/id — अपना chat ID देखें\n\n"
        "Admin commands:\n"
        "/broadcast <message> या किसी message को reply करके /broadcast\n"
        "/usersar\n"
        "/exportusersar"
    )


async def show_id(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"आपका chat ID: {update.effective_chat.id}")


def main():
    if not TOKEN:
        raise RuntimeError("TELEGRAM_BOT_TOKEN configured नहीं है।")
    init_db()
    app = Application.builder().token(TOKEN).build()

    app.add_handler(MessageHandler(filters.ALL, track_user), group=-1)

    app.add_handler(CommandHandler("startar", start))
    app.add_handler(CommandHandler("helpar", helpar))
    app.add_handler(CommandHandler("id", show_id))
    app.add_handler(CommandHandler("knowar", knowledge))
    app.add_handler(CommandHandler("notesar", short_notes))
    app.add_handler(CommandHandler("diagramaar", diagram))
    app.add_handler(CommandHandler("quizar", quiz))
    app.add_handler(CommandHandler("chapterar", chapter_quiz))
    app.add_handler(CommandHandler("uploadpdfar", upload_pdf_help))
    app.add_handler(CommandHandler("translatear", translate_message))
    app.add_handler(CommandHandler("translatepdfar", translate_latest_pdf))

    app.add_handler(CommandHandler("broadcast", broadcast))
    app.add_handler(CommandHandler("usersar", users_command))
    app.add_handler(CommandHandler("exportusersar", export_users))
    app.add_handler(MessageHandler(filters.Document.ALL, upload_pdf))

    print("Knowledge bot started...")
    app.run_polling(drop_pending_updates=True)


if __name__ == "__main__":
    main()

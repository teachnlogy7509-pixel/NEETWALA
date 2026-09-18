import tempfile
from pathlib import Path

from telegram import Update
from telegram.ext import ContextTypes

from database import save_document
from gemini import generate_short_notes
from pdf_processor import detect_chapter, extract_text


def chunks(text, size=3900):
    return [text[index:index + size] for index in range(0, len(text), size)] or [""]


async def upload_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    document = update.message.document
    if not document or not (document.file_name or "").lower().endswith(".pdf"):
        return
    await update.message.reply_text("PDF download करके text और chapter identify किया जा रहा है...")
    temporary_path = Path(tempfile.gettempdir()) / f"knowledge_{update.effective_user.id}_{document.file_unique_id}.pdf"
    try:
        telegram_file = await context.bot.get_file(document.file_id)
        await telegram_file.download_to_drive(custom_path=str(temporary_path))
        text = extract_text(str(temporary_path))
        if len(text.strip()) < 20:
            await update.message.reply_text("इस PDF से selectable text नहीं मिला। शायद यह scanned/image PDF है।")
            return
        chapter = detect_chapter(text)
        save_document(update.effective_chat.id, document.file_name, chapter, text)
        await update.message.reply_text(
            f"PDF save हो गई।\nChapter: {chapter}\nExtracted characters: {len(text)}\n\nअब Gemini-style short notes बन रहे हैं..."
        )
        notes = generate_short_notes(text[:12000], chapter)
        for part in chunks(notes):
            await update.message.reply_text(part)
        if len(text) > 12000:
            await update.message.reply_text("PDF बड़ी है, इसलिए पहले 12,000 characters पर short notes बनाए गए हैं। पूरे PDF का translation: /translatepdfar English")
    except Exception as error:
        await update.message.reply_text(f"PDF process नहीं हो पाई: {error}")
    finally:
        temporary_path.unlink(missing_ok=True)


async def upload_pdf_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("PDF को Telegram में Document के रूप में भेजें। Bot text निकालेगा, chapter पहचानेगा और Gemini-style Hindi short notes बनाएगा।")

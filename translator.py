from telegram import Update
from telegram.ext import ContextTypes

from database import latest_document
from gemini import translate_text


def chunks(text, size=3900):
    return [text[index:index + size] for index in range(0, len(text), size)] or [""]


async def translate_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = " ".join(context.args).strip() or "English"
    reply = update.message.reply_to_message
    source_text = (reply.text or reply.caption) if reply else None
    if not source_text:
        await update.message.reply_text("किसी text message को reply करके लिखें: /translatear English")
        return
    await update.message.reply_text(f"Translation {target} में तैयार हो रहा है...")
    result = translate_text(source_text[:12000], target)
    for part in chunks(result):
        await update.message.reply_text(part)


async def translate_latest_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    target = " ".join(context.args).strip() or "English"
    document = latest_document(update.effective_chat.id)
    if not document:
        await update.message.reply_text("पहले एक PDF भेजें, फिर /translatepdfar English लिखें।")
        return
    await update.message.reply_text(f"{document['filename']} का translation {target} में तैयार हो रहा है...")
    text = document["extracted_text"][:12000]
    result = translate_text(text, target)
    for part in chunks(result):
        await update.message.reply_text(part)
    if len(document["extracted_text"]) > 12000:
        await update.message.reply_text("अभी पहला 12,000 characters translate किए गए हैं।")


from telegram import Update
from telegram.ext import ContextTypes

async def upload_pdf(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "PDF प्राप्त हुई। अगला चरण: टेक्स्ट एक्सट्रैक्शन और Gemini से मूल NEET-स्तर के प्रश्न जनरेशन।"
    )

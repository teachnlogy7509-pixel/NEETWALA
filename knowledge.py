from telegram import Update
from telegram.ext import ContextTypes

from gemini import ask_gemini


def chunks(text, size=3900):
    return [text[index:index + size] for index in range(0, len(text), size)] or [""]


async def knowledge(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = " ".join(context.args).strip()
    if not question:
        await update.message.reply_text("उदाहरण: /knowar प्रकाश संश्लेषण आसान भाषा में समझाओ")
        return
    await update.message.reply_text("Knowledge answer तैयार हो रहा है...")
    prompt = f"""
    तुम NEET Biology के Hindi knowledge assistant हो।
    प्रश्न: {question}
    केवल सही, सरल और NCERT-aligned Hindi में उत्तर दो।
    पहले छोटा direct answer, फिर key points, फिर एक छोटा example दो।
    यदि प्रश्न अस्पष्ट हो तो ईमानदारी से clarification मांगो।
    """
    answer = ask_gemini(prompt)
    for part in chunks(answer):
        await update.message.reply_text(part)

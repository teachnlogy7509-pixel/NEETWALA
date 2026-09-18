from telegram import Update
from telegram.ext import ContextTypes

from gemini import ask_gemini, generate_short_notes


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


async def short_notes(update: Update, context: ContextTypes.DEFAULT_TYPE):
    topic = " ".join(context.args).strip()
    reply = update.message.reply_to_message
    replied_text = (reply.text or reply.caption) if reply else None
    source = topic or replied_text
    if not source:
        await update.message.reply_text(
            "उदाहरण:\n/notesar कोशिका\n\nया किसी text message को reply करके केवल /notesar लिखें।"
        )
        return

    await update.message.reply_text("Gemini-style short notes तैयार हो रहे हैं...")
    title = topic if len(topic) < 120 else "Replied study material"
    notes = generate_short_notes(source, title)
    for part in chunks(notes):
        await update.message.reply_text(part)

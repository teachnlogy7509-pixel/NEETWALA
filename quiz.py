
from telegram import Update
from telegram.ext import ContextTypes
from bot.services.gemini import ask_gemini

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("उदाहरण: /quiz कोशिका 90")
        return

    topic = context.args[0]
    count = 30
    if len(context.args) > 1:
        try:
            count = max(10, min(180, int(context.args[1])))
        except:
            count = 30

    prompt = f"""
    केवल हिंदी में {count} मूल NEET-स्तर के जीवविज्ञान MCQ बनाओ।
    विषय: {topic}
    प्रत्येक प्रश्न में 4 विकल्प, सही उत्तर और संक्षिप्त व्याख्या दो।
    """

    text = ask_gemini(prompt)
    for i in range(0, len(text), 3900):
        await update.message.reply_text(text[i:i+3900])

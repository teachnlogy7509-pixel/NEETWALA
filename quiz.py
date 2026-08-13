from telegram import Update
from telegram.ext import ContextTypes
from gemini import ask_gemini

async def quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text(
            "उदाहरण: /quizar कोशिका 90\n\nआप 10 से 180 तक प्रश्न चुन सकते हैं।"
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
        f"विषय: {topic}\nप्रश्न: {count}\n\nNEET-स्तर के हिंदी प्रश्न तैयार किए जा रहे हैं..."
    )

    prompt = f"""
    केवल हिंदी में {count} मूल NEET-स्तर के जीवविज्ञान MCQ बनाओ।
    विषय: {topic}

    नियम:
    - 4 विकल्प (A, B, C, D)
    - सही उत्तर
    - संक्षिप्त व्याख्या
    - NCERT आधारित
    - Assertion-Reason प्रश्न भी शामिल करो
    """

    text = ask_gemini(prompt)

    for i in range(0, len(text), 3900):
        await update.message.reply_text(text[i:i+3900])

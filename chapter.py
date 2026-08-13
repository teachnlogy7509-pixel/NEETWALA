from telegram import Update
from telegram.ext import ContextTypes
from quiz_engine import generate_neet_quiz

async def chapter_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "उदाहरण: /chapterar कोशिका 180\n\nआप 10 से 180 तक प्रश्न चुन सकते हैं।"
        )
        return

    topic = context.args[0]

    try:
        count = max(10, min(180, int(context.args[1])))
    except:
        count = 90

    await update.message.reply_text(
        f"विषय: {topic}\nप्रश्न: {count}\n\nNEET-स्तर के प्रश्न तैयार किए जा रहे हैं..."
    )

    text = generate_neet_quiz(topic, count)

    for i in range(0, len(text), 3900):
        await update.message.reply_text(text[i:i+3900])

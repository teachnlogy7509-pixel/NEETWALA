
from telegram import Update
from telegram.ext import ContextTypes
from bot.services.quiz_engine import generate_neet_quiz

async def chapter_quiz(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text(
            "उदाहरण: /chapter कोशिका 180"
        )
        return

    topic = context.args[0]
    count = int(context.args[1])

    text = generate_neet_quiz(topic, count)
    for i in range(0, len(text), 3900):
        await update.message.reply_text(text[i:i+3900])

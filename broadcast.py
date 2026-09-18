import io
import os
from telegram import InputFile, Update
from telegram.error import Forbidden, TelegramError
from telegram.ext import ContextTypes

from database import list_chat_ids, mark_blocked, recent_users, user_count, users_csv


def admin_ids():
    return {int(value.strip()) for value in os.getenv("ADMIN_CHAT_IDS", "").split(",") if value.strip().lstrip("-").isdigit()}


def is_admin(update: Update):
    return bool(update.effective_user and update.effective_user.id in admin_ids())


async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.message.reply_text("यह command केवल admin के लिए है।")
        return

    source = update.message.reply_to_message
    text = " ".join(context.args).strip()
    if not source and not text:
        await update.message.reply_text("Text भेजें या किसी message को reply करके /broadcast लिखें।")
        return

    delivered = 0
    failed = 0
    for chat_id in list_chat_ids():
        try:
            if source:
                await context.bot.copy_message(chat_id=chat_id, from_chat_id=update.effective_chat.id, message_id=source.message_id)
            else:
                await context.bot.send_message(chat_id=chat_id, text=text)
            delivered += 1
        except Forbidden:
            mark_blocked(chat_id)
            failed += 1
        except TelegramError:
            failed += 1

    await update.message.reply_text(f"Broadcast पूरा हुआ। भेजे: {delivered}, असफल: {failed}")


async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.message.reply_text("यह command केवल admin के लिए है।")
        return
    rows = recent_users()
    lines = [f"Active users: {user_count()}", "", "Recent users:"]
    for row in rows:
        username = f"@{row['username']}" if row["username"] else "(no username)"
        name = " ".join(filter(None, [row["first_name"], row["last_name"]])) or "(no name)"
        lines.append(f"{name} | {username} | {row['chat_id']}")
    await update.message.reply_text("\n".join(lines))


async def export_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not is_admin(update):
        await update.message.reply_text("यह command केवल admin के लिए है।")
        return
    data = users_csv().encode("utf-8")
    await update.message.reply_document(document=InputFile(io.BytesIO(data), filename="knowledge-bot-users.csv"))

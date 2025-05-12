


from telegram import Update
from telegram.ext import (
    ApplicationBuilder, CommandHandler, ContextTypes, JobQueue
)
from datetime import time
import os

TOKEN = os.getenv("API_KEY")

QUESTION = "Quin és el teu plat preferit?"
OPTIONS = ["Pizza", "Pasta", "Sushi", "Amanida"]
registered_chats = set()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    registered_chats.add(chat_id)
    await update.message.reply_text("Aquest xat ha estat registrat per rebre enquestes.")

async def enviar_poll(context: ContextTypes.DEFAULT_TYPE):
    for chat_id in registered_chats:
        await context.bot.send_poll(
            chat_id=chat_id,
            question=QUESTION,
            options=OPTIONS,
            is_anonymous=False,
            allows_multiple_answers=False
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    job_queue: JobQueue = app.job_queue
    #job_queue.run_repeating(enviar_poll, interval=5, first=5)  # Cada 5 segons per proves
    job_queue.run_daily(enviar_poll, time=time(10, 0), days=(1, 3))  # Dimarts i dijous

    print("Bot en marxa (amb proves cada 5 segons)...")
    app.run_polling()

if __name__ == "__main__":
    main()

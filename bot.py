import schedule
import time
import asyncio
import threading
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes
import os
# Token del teu bot
TOKEN = os.getenv("API_KEY")

# Enquesta
QUESTION = "Quin és el teu plat preferit?"
OPTIONS = ["Pizza", "Pasta", "Sushi", "Amanida"]

# Xats registrats
registered_chats = set()

# Enviar enquesta a tots els xats registrats
async def enviar_poll(app):
    for chat_id in registered_chats:
        await app.bot.send_poll(
            chat_id=chat_id,
            question=QUESTION,
            options=OPTIONS,
            is_anonymous=False,
            allows_multiple_answers=False
        )

# Wrapping per fer-lo usable dins thread amb asyncio
def scheduled_poll(app):
    asyncio.run(enviar_poll(app))

# /start per registrar xat
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    registered_chats.add(chat_id)
    await update.message.reply_text("Hola! Aquest xat ha estat registrat per rebre polls cada dimecres i divendres.")

# Llança el scheduler en un fil separat
def iniciar_schedule(app):
    #schedule.every().wednesday.at("10:00").do(scheduled_poll, app)
    #schedule.every().friday.at("10:00").do(scheduled_poll, app)
    schedule.every(10).seconds.do(scheduled_poll, app)

    # def loop():
    #     while True:
    #         schedule.run_pending()
    #         time.sleep(1)
    #
    # thread = threading.Thread(target=loop, daemon=True)
    # thread.start()

# Inicia el bot
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))

    iniciar_schedule(app)

    print("Bot en marxa...")
    app.run_polling()

if __name__ == "__main__":
    main()

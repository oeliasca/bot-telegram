from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import os

async def hello(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(f'Hello {update.effective_user.first_name}')





def main() -> None:
    api_key = os.getenv('API_KEY')
    app = ApplicationBuilder().token(api_key).build()

    app.add_handler(CommandHandler("hello", hello))

    app.run_polling()


if __name__ == "__main__":
    main()
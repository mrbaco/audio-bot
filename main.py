from telegram.ext import (
    ApplicationBuilder,
    CallbackQueryHandler,
    MessageHandler,
    CommandHandler,
    filters
)
from telegram import Update
from dotenv import load_dotenv

import os, logging

from flow import (
    start_handler,
    remove_handler,
    audio_handler,
    upload_handler
)


load_dotenv('.env')

logging.basicConfig(
    # filename=f"{os.path.dirname(os.path.abspath(__file__))}/huckster_vpn_bot.log",
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

logging.getLogger("httpx").setLevel(logging.WARNING)

if __name__ == '__main__':
    application = (
        ApplicationBuilder()
            .token(os.getenv('BOT_TOKEN'))
            .concurrent_updates(True)
            .build()
    )

    application.add_handler(CommandHandler("start", start_handler))
    application.add_handler(CommandHandler("remove", remove_handler))

    application.add_handler(CallbackQueryHandler(audio_handler, pattern="^audio_.*?$"))

    application.add_handler(MessageHandler(filters.ATTACHMENT, upload_handler))

    application.run_polling(allowed_updates=Update.ALL_TYPES)

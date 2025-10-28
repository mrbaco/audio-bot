from dotenv import load_dotenv
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ContextTypes

from crud import create, read_all, read_one, remove
from database import create_database

import os


load_dotenv('.env')

async def start_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    await create_database()

    if context.args and len(context.args) != 0:
        return await audio_handler(
            update,
            context
        )

    audios = await read_all()

    keyboard = []
    
    for i in range(0, len(audios), 2):
        row = []
        for audio in audios[i:i+2]:
            button = InlineKeyboardButton(
                text=audio.file_name,
                callback_data=f'audio_{audio.id}'
            )
            row.append(button)
        keyboard.append(row)

    await update.message.reply_text(
        text='Выберите аудиозапись для прослушивания.',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

async def remove_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    if is_admin(update.effective_chat.id):
        if context.args:
            try:
                if await remove(int(context.args[0])):
                    await context.bot.send_message(
                        chat_id=update.effective_chat.id,
                        text='Аудиосообщение удалено!'
                    )

            except:
                pass

async def audio_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    audio_id = None
    args = None

    if context.args:
        args = ' '.join(context.args).split('_')
    elif update.callback_query.data:
        args = update.callback_query.data.split('_')

    if args and len(args) == 2:
        try:
            audio_id = int(args[1])
        except:
            pass

    audio = await read_one(audio_id)

    if audio:
        await context.bot.send_voice(
            chat_id=update.effective_chat.id,
            caption=audio.file_name,
            voice=audio.file_id
        )

    if hasattr(update.callback_query, 'answer'):
        await update.callback_query.answer()

async def upload_handler(
        update: Update,
        context: ContextTypes.DEFAULT_TYPE
) -> None:
    if is_admin(update.effective_chat.id):
        attachment = update.message.effective_attachment

        if not attachment:
            return

        try:
            if not await create(
                file_id=attachment.file_id,
                file_name=update.message.caption
            ):
                raise Exception()

            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Аудиосообщение добавлено!'
            )

        except Exception as e:
            print(e)
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text='Не удалось сохранить аудиосообщение!'
            )

def is_admin(chat_id: int) -> bool:
    return str(chat_id) in os.getenv('ADMIN_TELEGRAM_IDS').split(', ')

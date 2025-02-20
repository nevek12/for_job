import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from lexicon.lexicon import LEXICON_RU

logger = logging.getLogger(__name__)

# Инициализируем роутер уровня модуля
other_router = Router()


# Этот хэндлер будет срабатывать на любые сообщения,
# кроме тех, для которых есть отдельные хэндлеры
@other_router.message()
async def send_echo(message: Message):
    logger.debug('Вошли в эхо-хэндлер')
    try:
        await message.send_copy(chat_id=message.chat.id)
    except TypeError:
        await message.reply(text=LEXICON_RU['no_echo'])
    logger.debug('Выходим из эхо-хэндлера')

@other_router.callback_query()
async def send(callback: CallbackQuery, state: FSMContext):
    logger.debug(callback.json())
    logger.debug(state)
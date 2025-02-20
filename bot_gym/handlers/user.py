import logging
import copy

from aiogram import F, Router, Bot
from aiogram.exceptions import TelegramBadRequest
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from datetime import datetime

from lexicon.lexicon import LEXICON_RU, LEXICON_INL_KB, TRANSLATION, WEEKDAYS
from keyboards.keyboards import types_training_kb, days_kb, levels_kb, yes_no_kb, save_clean_kb, kb_build
from aiogram.fsm.state import default_state
from FSM.FSM import FSM, FSMWorkout
from filters.filters import AdditionalWorkoutFilter
from notion.notion import notion
from textform.textform import formatter_train

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)

# Инициализируем роутер уровня модуля
user_router = Router()


# Этот хэндлер срабатывает на команду /start
@user_router.message(CommandStart(), StateFilter(default_state))
async def process_start_command(message: Message, state: FSMContext):
    # logger.debug('Вошли в хэндлер, обрабатывающий команду /start')
    # lsst = []
    # te = cycle('0123456789')
    # for i in range(100):
    #     lsst.append(next(te))
    # await message.answer(text=''.join(lsst))
    # Отправляем сообщение пользователю
    await message.answer(text=LEXICON_RU['/start'], reply_markup=types_training_kb)
    logger.debug('Выходим из хэндлера, обрабатывающего команду /start')
    # меняем состояние
    await state.set_state(FSM.type_training)

@user_router.message(Command("clear"))
async def cmd_clear(message: Message, bot: Bot, state: FSMContext) -> None:
    try:
        # Все сообщения, начиная с текущего и до первого (message_id = 0)
        for i in range(message.message_id, 0, -1):
            await bot.delete_message(message.from_user.id, i)
    except TelegramBadRequest as ex:
        # Если сообщение не найдено (уже удалено или не существует),
        # код ошибки будет "Bad Request: message to delete not found"
        logger.debug(f"Все сообщения {message.from_user.id} удалены")
    await state.clear()
    await state.set_state(default_state)



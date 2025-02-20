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
notion_router = Router()

# выводит шаблон упражнения отправляет запрос на выбор напоминание
@notion_router.callback_query(StateFilter(FSM.save_clean), F.data == 'save')
async def process_save_data(callback: CallbackQuery, state: FSMContext, formatter_text: str):
    # отправляем пользователю что все сохранено успешно
    await callback.answer(text=LEXICON_RU['successfully'])
    # выводим шаблон программы тренировок
    await callback.message.answer(text=formatter_text)
    # запрос на напоминания
    await callback.message.answer(text=LEXICON_RU['notion'], reply_markup=yes_no_kb)
    # меняем машину состояний
    await state.set_state(FSM.notion)

    logger.debug('Все сохранилось')
# отправляем запрос на время напоминания
@notion_router.callback_query(StateFilter(FSM.notion), F.data == 'yes')
async def process_notion(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    # запрос на время напоминания
    await callback.message.answer(text=LEXICON_RU['when_notion'])
    # меняем машину состояний
    await state.set_state(FSM.timer)

# запускаем цикл напоминания
@notion_router.message(StateFilter(FSM.timer))
async def process_save_notion(message: Message, state: FSMContext, scheduler: AsyncIOScheduler):
    # берем часы и минуты от пользователя и запоминаем их в машину
    hour, minute = message.text.split(':')
    await state.update_data({'time_notion': [hour, minute]})
    # создаем напоминание
    data = await state.get_data()
    days_of_week = data['days_of_week']
    scheduler.add_job(notion, trigger='cron', args=[message, LEXICON_RU['notion_training'], state, FSM, yes_no_kb], day_of_week=','.join(days_of_week), hour=hour, minute=minute)
    scheduler.start()
    # отправляем ответ что напоминание создано
    await message.answer(text=LEXICON_RU['notion_is_created'])

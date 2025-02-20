import logging
import copy

from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
)

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
record_w_router = Router()

# запускаем запись тренировочного процесса
@record_w_router.callback_query(StateFilter(FSM.is_train), F.data == 'yes')
async def process_start_train(callback: CallbackQuery, state: FSMContext):

    await callback.answer()
    # находим день тренировки
    dt = datetime.now()
    day_of_week = WEEKDAYS[dt.weekday()]
    # находим саму тренировку
    data = await state.get_data()
    workout_dct = copy.deepcopy(data.get(day_of_week))
    # если этот день есть в тренировчной программе
    if workout_dct:
        # создаем объект итератора
        form = formatter_train(workout_dct)
        # запрос на запись повторений
        await callback.message.answer(text=LEXICON_RU['train'] + next(form))
        # закидываем в машину итератор и текущий день
        await state.update_data({'form': form, 'day_of_week': day_of_week})
        # меняем состояние машины на запись дня
        await state.set_state(FSM.writting_train)
    else:

        await callback.answer(text=LEXICON_RU['not_day_of_training'])
        # запрос в какой день тренировки будет идти запись
        await callback.message.answer(text=LEXICON_RU['choice_day_of_training'], reply_markup=kb_build(data['days_of_week'], TRANSLATION))



# продолжение записи повторений
@record_w_router.message(StateFilter(FSM.writting_train), F.text.isdigit())
async def process_continue_write_train(message: Message, state: FSMContext):

    data = await state.get_data()
    # ловим ошибку стоп итерайшен от итератора
    try:
        # запрос на запись повторения
        next_form = next(data['form'])
        await message.answer(text=LEXICON_RU['train'] + next_form)
        # записываем повторения и обновляем машину состояния
        data['repetitions'] = data.setdefault('repetitions', []) + [int(message.text)]

        await state.clear()

        await state.update_data(data)

        await state.set_state(FSM.writting_train)
    except StopIteration:

        # запрос на сохранение введенных данных
        await message.answer(text=LEXICON_RU['save_data'], reply_markup=save_clean_kb)

        # записываем повторения и обновляем машину состояния
        data['repetitions'] = data.setdefault('repetitions', []) + [int(message.text)]

        await state.clear()

        await state.update_data(data)

        # меняем машину состояния
        await state.set_state(FSM.save_train)

@record_w_router.callback_query(StateFilter(FSM.save_train), F.data == 'save')
async def process_save_train(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
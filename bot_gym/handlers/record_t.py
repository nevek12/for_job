import logging


from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.types import (
    CallbackQuery,
    Message,
)

from lexicon.lexicon import LEXICON_RU, LEXICON_INL_KB, TRANSLATION
from keyboards.keyboards import days_kb, levels_kb, yes_no_kb, save_clean_kb
from FSM.FSM import FSM, FSMWorkout
from filters.filters import AdditionalWorkoutFilter

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)

# Инициализируем роутер уровня модуля
record_t_router = Router()

# для записи нажатие на кнопки выбора типа тренировки и переводит в состояние выбора дня
@record_t_router.message(F.text.in_(['кардио-тренировка', 'тренировка на массу', 'тренировка на силу']), StateFilter(FSM.type_training))
async def process_type_training_sent(message: Message, state: FSMContext):
    # сохраняем тип тренировки
    await state.update_data(type_training=message.text, days_of_week=[])
    # отправляем запрос на выбор дня
    await message.answer(text=LEXICON_RU['choice_day'], reply_markup=days_kb)
    # меняем состояние
    await state.set_state(FSM.day_of_week)

    logger.debug(await state.get_data())

# для записи типа дня и перевода в состояние типа упражнения и количество повторений
@record_t_router.callback_query(F.data.in_([day for day in LEXICON_INL_KB][:-1]), StateFilter(FSM.day_of_week))
async def process_day_of_week_sent(callback: CallbackQuery, state: FSMContext):
    # добавляем день в FSM и сохраняем текущий день
    data = await state.get_data()
    data = data['days_of_week']
    current_day_of_week = callback.data.split('_')[-1]
    data.append(current_day_of_week)
    await state.update_data({current_day_of_week: {}, "day_of_week": current_day_of_week, "days_of_week": data})
    # выводим окошко для пользователя
    await callback.answer(text='Сохранено')
    # отправляем запрос на выбор типа упражнения
    await callback.message.answer(text=LEXICON_RU['choice_workout'])
    # меняем состояние машины на level
    await state.set_state(FSMWorkout.type_workout_count_approach)

    logger.debug(await state.get_data())

# для записи типа упражнения и перевода в состояние уровня упражнения
@record_t_router.message(StateFilter(FSMWorkout.type_workout_count_approach), F.text)
async def process_type_workout_sent(message: Message, state: FSMContext):
    # разделяем для название упражнения и количества подходов
    workout, count_approach = message.text.split(' ')
    # записываем упражнение и количество подходов
    await state.update_data({workout: {'approuch': count_approach}, 'last_workout': workout})
    # отправляем запрос на выбор уровня упражнения
    await message.answer(text=LEXICON_RU['choice_level'], reply_markup=levels_kb)

    logger.debug(await state.get_data())

# для записи уровня упражнения и перевода в состояние добавление дополнительно упражнений
@record_t_router.callback_query(F.data.in_([f"button_pressed_level_{i}" for i in range(1, 11)]))
async def process_level_sent(callback: CallbackQuery, state: FSMContext):
    # берём данные с FSM
    data = await state.get_data()

    # обновлем данные так, чтобы в дне недели сохранялась вся инфа
    # запоминаем предыдущую инфу про день тренировки
    previos_workouts_info = [{i: data.get(i)} for i in TRANSLATION if data.get(i) and i != data['day_of_week']]
    # создаем текущую информациб о дне тренировки
    workout_info = {data['day_of_week']: {**data[data['day_of_week']], **{data['last_workout']: {**data[data['last_workout']], **{'level': callback.data.split('_')[-1]}}}}}
    # присоединяем предыдущую инфу к настоящей инфе про день тренировки
    for previos_workout_info in previos_workouts_info:
        workout_info = {**workout_info, **previos_workout_info}
    # информация про текущем дня и типе тренировки
    type_training_day = {'type_training': data['type_training'], 'day_of_week': data['day_of_week'], 'days_of_week': data['days_of_week']}
    # очистка FSM
    await state.clear()
    # обновление FSM
    await state.update_data({**type_training_day, **workout_info})
    # оправляем запрос на дополнительные упражнения
    await callback.message.answer(text=LEXICON_RU['additional_workout'] + f'{TRANSLATION[data["day_of_week"]]}?', reply_markup=yes_no_kb)

    await callback.answer()

    await state.set_state(FSM.additional_workout_yes_no)

    logger.debug(await state.get_data())

# для обработки дополнительных упражнений
@record_t_router.callback_query(StateFilter(FSM.additional_workout_yes_no), AdditionalWorkoutFilter())
async def process_yes_additional_workout(callback: CallbackQuery, state: FSMContext):
    # отправляем запрос на выбор типа упражнения
    await callback.message.answer(text=LEXICON_RU['choice_workout'])

    await callback.answer()

    # меняем состояние машины на тип упражнения и кол-во подходов
    await state.set_state(FSMWorkout.type_workout_count_approach)

    logger.debug(await state.get_data())

# отказ от дополнительных упражнений отправляем запрос для дополнительного дня
@record_t_router.callback_query(StateFilter(FSM.additional_workout_yes_no), ~AdditionalWorkoutFilter())
async def process_no_additional_workout(callback: CallbackQuery, state: FSMContext):
    # отправляем запрос для добавления дополнительного дня
    await callback.message.answer(text=LEXICON_RU['additional_day'], reply_markup=yes_no_kb)

    await callback.answer(text='молодец тупорылый пользователь')

    await state.set_state(FSM.additional_day_yes_no)

# для обработки дополнительного дня переходим в состояние выбора дня
@record_t_router.callback_query(StateFilter(FSM.additional_day_yes_no), AdditionalWorkoutFilter())
async def process_yes_additional_day(callback: CallbackQuery, state: FSMContext):
    # отправляем запрос на выбор дня
    await callback.message.answer(text=LEXICON_RU['choice_day'], reply_markup=days_kb)

    await callback.answer()
    # меняем состояние
    await state.set_state(FSM.day_of_week)

    logger.debug(await state.get_data())

# отказ от выбора дня отправляем запрос на сохранение данных и меняем машину состояния
@record_t_router.callback_query(StateFilter(FSM.additional_day_yes_no), ~AdditionalWorkoutFilter())
async def process_no_additional_day(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    # отправляем запрос на сохранение или отчистку
    await callback.message.answer(text=LEXICON_RU['save_data'], reply_markup=save_clean_kb)
    # меняем состояние машины
    await state.set_state(FSM.save_clean)

    logger.debug(await state.get_data())
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder, InlineKeyboardBuilder
from lexicon.lexicon import LEXICON_KB, LEXICON_INL_KB

# ------- Создаем клавиатуру через ReplyKeyboardBuilder -------

# Создаем кнопки с типами тренировок
types_training = ['button_pressed_cardio', 'button_pressed_weight', 'button_pressed_strength']
buttons_types_training = [KeyboardButton(text=LEXICON_KB[i]) for i in types_training]

 # Инициализируем билдер для клавиатуры с кнопками типов тренировок
types_training_kb_builder = ReplyKeyboardBuilder()

# Добавляем кнопки в билдер с аргументом width=3
types_training_kb_builder.row(*buttons_types_training, width=3)

# Создаем клавиатуру с кнопками
types_training_kb: ReplyKeyboardMarkup = types_training_kb_builder.as_markup(
    one_time_keyboard=True,
    resize_keyboard=True,
    input_field_placeholder='нажми на кнопку внизу'
)

# -------------- создаем inline-клавиатуру выбора дня ------------------------------
buttons_days = [InlineKeyboardButton(text=value, callback_data=key) for key, value in LEXICON_INL_KB.items()]

days_kb_builder = InlineKeyboardBuilder()
days_kb_builder.row(*buttons_days, width=4)

days_kb: InlineKeyboardMarkup = days_kb_builder.as_markup()

# ---------------- создаем inline-клавиатуру для выбора уровня ----------------------------

buttons_levels = [InlineKeyboardButton(text=str(i), callback_data=f"button_pressed_level_{i}") for i in range(1, 11)]

levels_kb_builder = InlineKeyboardBuilder()
levels_kb_builder.row(*buttons_levels, width=5)

levels_kb: InlineKeyboardMarkup = levels_kb_builder.as_markup()

# ---------------- создаем inline-клавиатуру для ответа да нет
buttons_yes_no = [InlineKeyboardButton(text='да', callback_data='yes'), InlineKeyboardButton(text='нет', callback_data='no')]

yes_no_kb_builder = InlineKeyboardBuilder()
yes_no_kb_builder.row(*buttons_yes_no, width=2)

yes_no_kb: InlineKeyboardMarkup = yes_no_kb_builder.as_markup()

# ---------------- создаем inline-клавиатуру для ответа сохранить очистить данные ----------------------------

buttons_save_clean = [InlineKeyboardButton(text='сохранить', callback_data='save'), InlineKeyboardButton(text='очистить', callback_data='clean')]

save_clean_kb_builder = InlineKeyboardBuilder()
save_clean_kb_builder.row(*buttons_save_clean, width=2)

save_clean_kb: InlineKeyboardMarkup = save_clean_kb_builder.as_markup()

# ------------------ создаем функцию inline-клавиатуры для выбора дня тренировки --------------------------

def kb_build(days, trans):
    buttons_days = [[InlineKeyboardButton(text=trans[day], callback_data=day)] for day in days]
    return InlineKeyboardMarkup(inline_keyboard=buttons_days)


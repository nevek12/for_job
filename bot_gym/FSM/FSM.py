from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
class FSM(StatesGroup):
    # Создаем экземпляры класса State, последовательно
    # перечисляя возможные состояния, в которых будет находиться
    # бот в разные моменты взаимодействия с пользователем
    type_training = State()
    day_of_week = State()
    type_workout = State()
    additional_day_yes_no = State()
    additional_workout_yes_no = State()
    save_clean = State()
    finished_save = State()
    timer = State()
    notion = State()
    is_train = State()
    writting_train = State()
    save_train = State()

class FSMWorkout(StatesGroup):
    type_workout_count_approach = State()
    level = State()




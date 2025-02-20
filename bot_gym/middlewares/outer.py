import logging
from typing import Any, Awaitable, Callable, Dict

from datetime import datetime
from aiogram import BaseMiddleware
from FSM.FSM import FSM
from textform.textform import formatter

logger = logging.getLogger(__name__)

# Класс middleware для сохранения данных в БД
class SaveUserDataMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        state = data.get("state")
        self.pool = data.get('pool')
        if not state or event.data == 'clean':
            return await handler(event, data)
        user_state = await state.get_state()



        if user_state == FSM.save_clean and event.data == 'save':
            user_data = await state.get_data()
            user_id = event.from_user.id
            user_firstname = event.from_user.first_name
            user_lastname = event.from_user.last_name
            type_training = user_data['type_training']
            user_data.pop('type_training')
            user_data.pop('day_of_week')
            user_data.pop('days_of_week')
            user_days = user_data
            lsst_tuple = []
            data['formatter_text'] = formatter(type_training, user_days)
            for day_of_week in user_days:
                for workout, approuch_level in user_days[day_of_week].items():
                    lsst_tuple.append(f"({user_id}, '{day_of_week}', '{workout}', {user_days[day_of_week][workout]['approuch']}, {user_days[day_of_week][workout]['level']})")
            query_2 = "INSERT INTO template_workouts(user_id, day_of_week, workout, approuch, level) VALUES " + ",\n".join(lsst_tuple)
            query_1 = f"INSERT INTO users VALUES ({user_id}, '{user_firstname}', '{user_lastname}', '{type_training}');\n"
            async with self.pool.acquire() as conn:
                try:
                    with open('create_tables.sql', 'r') as sql_script:
                        query_create_table = sql_script.read()
                    await conn.execute(query_create_table)
                    await conn.execute(query_1)
                    await conn.execute(query_2)
                    logging.info(f"User data for user {user_id} saved to database.")
                except Exception as e:
                    logging.error(f"Error saving user data to database: {e}")

        return await handler(event, data)

class SaveUserTrain(BaseMiddleware):
    async def __call__(self, handler, event, data):
        self.state = data.get("state")
        self.pool = data.get('pool')
        if not self.state or event.data == 'clean':
            return await handler(event, data)
        user_state = await self.state.get_state()

        if user_state == FSM.save_train and event.data == 'save':
            user_data = await self.state.get_data()
            user_id = event.from_user.id
            type_training = user_data.pop('type_training')
            workout_date = event.message.date.strftime("%Y-%m-%d")
            current_day = user_data.pop('day_of_week')
            user_data.pop('days_of_week')
            repetitions = user_data.pop('repetitions')
            user_days = user_data
            lsst_tuple = []
            ind_rep = 0
            logger.debug(repetitions)
            for workout, approuch_level in user_days[current_day].items():
                for number_approuch in range(1, int(approuch_level['approuch']) + 1):
                    lsst_tuple.append(f"({user_id}, '{workout_date}', '{current_day}', '{workout}', {approuch_level['level']}, {number_approuch}, {repetitions[ind_rep]}, {approuch_level['approuch']})")
                    ind_rep += 1
            query_1 = "INSERT INTO record_workouts(user_id, workout_date, day_of_week, workout, level, number_approuch, repetition, approuch) VALUES " + ",\n".join(lsst_tuple)
            async with self.pool.acquire() as conn:
                try:
                    await conn.execute(query_1)
                    logging.info(f"User data for user {user_id} saved to database.")
                except Exception as e:
                    logging.error(f"Error saving user data to database: {e}")

        return await handler(event, data)
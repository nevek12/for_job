import asyncio
import logging

from aiogram import Bot, Dispatcher
from config_data.config import Config, load_config
from handlers.notion import notion_router
from handlers.other import other_router
from handlers.record_t import record_t_router
from handlers.record_w import record_w_router
from handlers.user import user_router
from aiogram.fsm.storage.memory import MemoryStorage
from database.database import create_db_pool
from middlewares.outer import SaveUserDataMiddleware, SaveUserTrain
from middlewares.inner import (
    FirstInnerMiddleware,
    SecondInnerMiddleware,
    ThirdInnerMiddleware,
)
from apscheduler.schedulers.asyncio import AsyncIOScheduler



# Настраиваем базовую конфигурацию логирования
logging.basicConfig(
    level=logging.DEBUG,
    format='[%(asctime)s] #%(levelname)-8s %(filename)s:'
           '%(lineno)d - %(name)s - %(message)s'
)

# Инициализируем логгер модуля
logger = logging.getLogger(__name__)


# Функция конфигурирования и запуска бота
async def main() -> None:

    # Загружаем конфиг в переменную config
    config: Config = load_config()

    # Инициализируем бот
    bot = Bot(token=config.tg_bot.token)
    # Инициализируем хранилище (создаем экземпляр класса MemoryStorage)
    storage = MemoryStorage()
    # Инициализируем диспатчер
    dp = Dispatcher(storage=storage)
    # Инициализация напоминания
    scheduler = AsyncIOScheduler()

    # Регистрируем роутеры в диспетчере
    dp.include_router(user_router)
    dp.include_router(record_t_router)
    dp.include_router(notion_router)
    dp.include_router(record_w_router)
    dp.include_router(other_router)

    # создаем подключение к бд
    pool = await create_db_pool(config.db.db_host, config.db.db_user, config.db.db_password, config.db.database)

    async with pool.acquire() as conn:
        try:
            with open('create_tables.sql', 'r') as sql_script:
                query_create_table = sql_script.read()
            await conn.execute(query_create_table)
            logging.debug(f"databases are created")
        except Exception as e:
            logging.error(f"Database creation error: {e}")

    # добавлем в глобальные переменные связь с бд и напоминание
    dp.workflow_data.update({'pool': pool, 'scheduler': scheduler})

    # Здесь будем регистрировать миддлвари
    notion_router.callback_query.outer_middleware(SaveUserDataMiddleware())
    record_w_router.callback_query.outer_middleware(SaveUserTrain())

    # Запускаем polling
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


asyncio.run(main())
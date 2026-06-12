"""

Телеграмм бот для изучения иностанных языков
--------------------

aiogram - телеграмм бот
python-dotenv - для хранения токенов 
SQLite - база данных
aiosqlite    - асинхронная работа с базой данных SQLite


Language Trainer Bot

"""



from os import getenv
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.routes import router


load_dotenv()
TOKEN = getenv('BOT_TOKEN')

dp = Dispatcher()

dp.include_router(router)



async def main():
    bot = Bot(token=TOKEN)
    print('Started...')
    await dp.start_polling(bot)




if __name__ == "__main__":

    asyncio.run(main())
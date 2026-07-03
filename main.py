


"""
В Мій прогресс щоб показував поточний рівень правильних та пройдених тестів.
Також треба окремо зробити кнопку та яка буде виводити повністью інформацію
про поточний мову та на якіх рівнях скільки вивченно слів та зроблено тестів.

"""



from os import getenv
import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.routes import init_db, router


load_dotenv()
TOKEN = getenv('BOT_TOKEN')

dp = Dispatcher()

dp.include_router(router)



async def main():
    await init_db()
    bot = Bot(token=TOKEN)
    print('Started...')
    await dp.start_polling(bot)




if __name__ == "__main__":

    asyncio.run(main())





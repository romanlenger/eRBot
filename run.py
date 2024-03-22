import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv, find_dotenv
from handlers import router

load_dotenv(find_dotenv())


async def main() -> None:
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w', encoding='utf-8')
    asyncio.run(main())

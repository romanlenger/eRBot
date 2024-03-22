import asyncio
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())


async def main() -> None:
    bot = Bot(token=os.getenv('TOKEN'))
    dp = Dispatcher()
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w', encoding='utf-8')
    asyncio.run(main())

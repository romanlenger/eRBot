import asyncio
from aiogram import Bot, Dispatcher


async def main() -> None:
    bot = Bot(token=os.getenv('TOKEN'))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w', encoding='utf-8')
    asyncio.run(main())

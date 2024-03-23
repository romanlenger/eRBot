import asyncio
import logging
import os
import schedule
import subprocess

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode

from dotenv import load_dotenv, find_dotenv

from app.handlers import router
from app.variables import UPDATE_SCRIPT, INTERPRET


def parser() -> None:
    script_path = UPDATE_SCRIPT
    python_interpreter = INTERPRET
    subprocess.run([python_interpreter, script_path])
    logging.info('Rates has been parsed successfully!')


async def main() -> None:
    load_dotenv(find_dotenv())
    
    bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)

    await dp.start_polling(bot)
    asyncio.create_task(autoparse())


async def autoparse():
    schedule.every().day.at("09:30").do(parser)

    while True:
        await asyncio.sleep(60)
        schedule.run_pending()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w', encoding='utf-8')

    asyncio.run(main())


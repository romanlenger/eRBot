import asyncio
import logging
import os
import subprocess
import json

from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from apscheduler.schedulers.asyncio import AsyncIOScheduler

from dotenv import load_dotenv, find_dotenv

from app.handlers import router
from app.variables import UPDATE_SCRIPT, INTERPRET, USERS_FILE


def parser() -> None:
    script_path = UPDATE_SCRIPT
    python_interpreter = INTERPRET
    subprocess.run([python_interpreter, script_path])
    logging.info('Rates has been parsed successfully!')


async def send_notification_to_users(bot: Bot) -> None:
    try:
        with open(USERS_FILE, 'r') as file:
            users_data = json.load(file)
            users_ids = [user['id'] for user in users_data]

        message = "Привіт! Наразі доступний оновлений файл з курсами валют. Можете його завантажити - /get_rates"

        for user_id in users_ids:
            try:
                await bot.send_message(user_id, message)
            except Exception as e:
                logging.error(f"An error occurred while sending a message to {user_id}: {e}")
    except Exception as e:
        logging.error(f"An error occurred while reading users file: {e}")


async def main() -> None:
    load_dotenv(find_dotenv())
    
    bot = Bot(token=os.getenv('TOKEN'), parse_mode=ParseMode.HTML)
    dp = Dispatcher()
    dp.include_router(router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(parser, "cron", hour=9)
    scheduler.add_job(send_notification_to_users, "cron", hour=9, minute=1, args=[bot])
    scheduler.start()

    await dp.start_polling(bot)
    while True:
        await asyncio.sleep(1)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w', encoding='utf-8')

    asyncio.run(main())
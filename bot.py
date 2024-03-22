from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile, Message
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv, find_dotenv

import asyncio
import logging
import time
import os
import json

import scripts.getExchangeRates as ger
from variables import RATES

dp = Dispatcher()
load_dotenv(find_dotenv())
USERS_FILE = "users.json"
PASSWORD = "your_password_here"


def save_user_data(user_data: dict) -> None:
    """
    Сохраняет данные о пользователе.
    """
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w") as f:
            json.dump([], f)

    with open(USERS_FILE, "r+") as f:
        data = json.load(f)
        user_ids = [user['id'] for user in data]
        if user_data['id'] not in user_ids:
            data.append(user_data)
            f.seek(0)
            json.dump(data, f)
        

@dp.message(Command("get_new_rates", prefix='/'))
async def get_rates(message: Message) -> None:
    user_full_name = message.from_user.full_name
    user_id = message.from_user.id

    logging.info(f'GETTING NEW FILE ---> ID: {user_id}| Name: {user_full_name}| Time: {time.asctime()}\n')

    ger.run_update_kurs()

    latest_file = ger.find_latest_excel_file(RATES)
    file_path = ger.create_new_file(latest_file)

    updated_file = ger.update_excel_file(file_path=file_path)
    new_excel_file = FSInputFile(updated_file)

    await message.answer_document(new_excel_file)


@dp.message(Command("get_rates", prefix='/'))
async def get_rates(message: Message) -> None:
    user_full_name = message.from_user.full_name
    user_id = message.from_user.id

    logging.info(f'GETTING ACTUAL FILE ---> ID: {user_id}| Name: {user_full_name}| Time: {time.asctime()}\n')

    latest_file = ger.find_latest_excel_file(RATES)
    excel_file = FSInputFile(latest_file)

    await message.answer_document(excel_file)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer("Вітаю")
    
    user_data = {
        "id": message.from_user.id,
        "full_name": message.from_user.full_name
    }
    save_user_data(user_data)


async def main() -> None:
    bot = Bot(token=os.getenv('TOKEN'))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w', encoding='utf-8')
    asyncio.run(main())





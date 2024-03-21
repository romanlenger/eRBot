from aiogram import Bot, Dispatcher
from aiogram.types import FSInputFile
from aiogram.filters import CommandStart, Command
from aiogram.types import Message
from variables import kurses, update_kurs, interpreter
from dotenv import load_dotenv, find_dotenv
import asyncio
import logging
import time
import subprocess
import os
import datetime
import shutil
import win32com.client
    
dp = Dispatcher()
load_dotenv(find_dotenv())


def run_update_kurs() -> None:
    script_path = update_kurs
    python_interpreter = interpreter
    subprocess.run([python_interpreter, script_path])


def find_latest_excel_file(folder_path: str) -> str:
    latest_date = datetime.datetime.min
    latest_file = None

    for root, dirs, files in os.walk(folder_path):
        for file_name in files:
            if file_name.endswith('.xlsx'):
                try:
                    date_str = file_name.split(' ')[3].split('.')[:2]  # Дата в названии файла после разделения по пробелу и точке
                    file_date = datetime.datetime.strptime('.'.join(date_str), "%d.%m")
                    if file_date > latest_date:
                        latest_date = file_date
                        latest_file = os.path.join(root, file_name)
                except (IndexError, ValueError) as error:
                    logging.error(error)
                    continue

    return latest_file


def create_new_file(file_path: str) -> str:
    if file_path is not None:
        today = datetime.datetime.now()
        if today.hour < 17:
            next_date = today
        else:
            next_date = today + datetime.timedelta(days=1)
        new_file_name = f"курс валют на {next_date.strftime('%d.%m.%Y')}.xlsx"

        new_file_path = os.path.join(os.path.dirname(file_path), new_file_name)

        if not os.path.exists(new_file_path):
            shutil.copy(file_path, new_file_path)
            logging.info(f"Создан новый файл: {new_file_path}")
        else:
            logging.warning('Такой файл уже существует')
    else:
        logging.error('Невозможно создать новый файл, возможно передано None')
        return None

    return new_file_path


def update_excel_file(file_path: str) -> str:
    excel = win32com.client.Dispatch("Excel.Application")
    excel.Visible = False  
    excel.DisplayAlerts = False  
    
    wb = excel.Workbooks.Open(file_path)
    wb.RefreshAll() 
    wb.Save()
    wb.Close()

    excel.Quit()

    logging.info("Запросы успешно обновлены.")
    return file_path


@dp.message(Command("get_new_rates", prefix='/'))
async def get_rates(message: Message) -> None:
    user_full_name = message.from_user.full_name
    user_id = message.from_user.id

    logging.info(f'GETTING NEW FILE ---> ID: {user_id}| Name: {user_full_name}| Time: {time.asctime()}')

    run_update_kurs()
    latest_file = find_latest_excel_file(kurses)
    file_path = create_new_file(latest_file)
    new_excel_file = FSInputFile(update_excel_file(file_path=file_path))

    await message.answer_document(new_excel_file)


@dp.message(Command("get_rates", prefix='/'))
async def get_rates(message: Message) -> None:
    user_full_name = message.from_user.full_name
    user_id = message.from_user.id

    logging.info(f'GETTING ACTUAL FILE ---> ID: {user_id}| Name: {user_full_name}| Time: {time.asctime()}')

    latest_file = find_latest_excel_file(kurses)
    excel_file = FSInputFile(latest_file)

    await message.answer_document(excel_file)


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(" Останній актуальний файл - /get_rates\n\nЗгенерувати новий файл - /get_new_rates")


async def main() -> None:
    bot = Bot(token=os.getenv('TOKEN'))
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, filename='logs.log', filemode='w', encoding='utf-8')
    asyncio.run(main())





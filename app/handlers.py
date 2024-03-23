from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.fsm.state import State, StatesGroup
from aiogram.filters import CommandStart, Command, Filter

# from .filters import LoginFilter
from dotenv import load_dotenv, find_dotenv
from .variables import USERS_FILE

import json
import os
import logging
from datetime import datetime

load_dotenv(find_dotenv())
router = Router()


class LoginState(StatesGroup):
    waiting_for_password = State()
    

class LoginFilter(Filter):
    key = 'is_login'

    def __init__(self, is_login):
        self.is_login = is_login
        
    async def __call__(self, message: Message) -> bool:
        if not os.path.exists(USERS_FILE): return False

        with open(USERS_FILE, 'r') as file:
            users = json.load(file)

        for user in users:
            if user.get('id') == int(message.from_user.id):
                return True
    

def save_user_data(user_id: int, full_name: str) -> None:
    """
    Сохраняет данные пользователя
    """
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding='utf-8') as f:
            json.dump([], f)

    with open(USERS_FILE, "r+", encoding='utf-8') as f:
        user_data = {
            "id": user_id,
            "full_name": full_name
        }
        data = json.load(f)
        user_ids = [user['id'] for user in data]
        if user_data['id'] not in user_ids:
            data.append(user_data)
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)

    logging.info("Пользователь успешно сохранен.")


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    await message.answer(f"Вітаю, {message.from_user.first_name}!\n\n /login - отримати доступ\n\n /get_rates - отримати курси валют")


"""
Обробка команд підтвердженого користувача
"""
@router.message(LoginFilter(is_login=True), Command('login'))
async def already_loggedin(message: Message):
    await message.answer('Ви вже успішно підтвердили доступ, можете отримати курси - /get_rates')


@router.message(LoginFilter(is_login=True), Command("get_rates"))
async def get_rates(message: Message):
    excel_file = FSInputFile('exchange_rates.xlsx')
    await message.answer_document(excel_file, caption=f'Актуальні курси валют на {datetime.now()}')



"""
Обробка команд непідтвердженого користувача
"""
@router.message(Command("get_rates"))
async def get_rates_denied(message: Message) -> None:
    await message.reply('Підтвердіть доступ - /login')


@router.message(Command('login'))
async def login_start(message: Message, state: FSMContext):
    await state.set_state(LoginState.waiting_for_password)
    await message.answer("Введіть пароль.")


@router.message(LoginState.waiting_for_password)
async def login_process(message: Message, state: FSMContext):
    password = message.text.strip().lower()

    if password == os.getenv('PASSWORD'):
        user_id = int(message.from_user.id)
        user_name = message.from_user.full_name
        save_user_data(user_id, user_name)

        await state.clear()
        await message.answer("Успішний вхід!\n Використайте команду /get_rates, щоб отримати акутальні курси валют.")
    else:
        await message.answer("Пароль невірний. Спробуйте ще раз.")


"""
Інші повідомлення
"""
@router.message()
async def other_cmds(message: Message) -> None:
    await message.answer_dice()



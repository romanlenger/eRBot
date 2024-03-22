from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart, Command, BaseFilter
from aiogram.fsm.state import State, StatesGroup
from dotenv import load_dotenv, find_dotenv
import json
import os
import logging
from variables import USERS_FILE

load_dotenv(find_dotenv())
router = Router()


class LoginFilter(BaseFilter):
    key = 'is_login'

    def __init__(self, is_login):
        self.is_login = is_login

    async def __call__(self, message: Message) -> bool:
        user_id = message.from_user.id
        if not user_id:
            return False  

        with open('users.json', 'r') as file:
            users = json.load(file)

        for user in users:
            if user.get('id') == user_id:
                return True 
            
        return False


class LoginState(StatesGroup):
    waiting_for_password = State()
    

def save_user_data(user_data: dict) -> None:
    """
    Сохраняет данные пользователя
    """
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, "w", encoding='utf-8') as f:
            json.dump([], f)

    with open(USERS_FILE, "r+", encoding='utf-8') as f:
        data = json.load(f)
        user_ids = [user['id'] for user in data]
        if user_data['id'] not in user_ids:
            data.append(user_data)
            f.seek(0)
            json.dump(data, f, ensure_ascii=False, indent=4)

    logging.info('Пользователь успешно сохранен.')


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Вітаю, {message.from_user.first_name}!\n /login для підтвердження доступу")


@router.message(Command('login'))
async def login_start(message: Message, state: FSMContext):
    await state.set_state(LoginState.waiting_for_password)
    await message.answer("Будь ласка, введіть пароль")


@router.message(LoginState.waiting_for_password)
async def login_password(message: Message, state: FSMContext):
    password = message.text.strip().lower()
    if password == os.getenv('PASSWORD'):
        user_data = {
            "id": message.from_user.id,
            "full_name": message.from_user.full_name
        }
        save_user_data(user_data)
        await message.answer("Успішний вхід!\n Використайте команду /get_rates, щоб отримати акутальні курси валют.")
        await state.clear()
    else:
        await message.answer("Пароль невірний. Спробуйте ще раз.")


@router.message(LoginFilter(is_login=True), Command("get_rates"))
async def get_rates(message: Message):
    # Відправляєм користувачу курси валют
    await message.reply('Ви готові отримати курси валют(тест)')
    pass


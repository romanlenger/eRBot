from aiogram import Router
from aiogram.types import Message
from aiogram.dispatcher import FSMContext
from aiogram.filters import CommandStart, Command, BoundFilter
from aiogram.dispatcher.filters.state import State, StatesGroup
from dotenv import load_dotenv, find_dotenv
import json

load_dotenv(find_dotenv())
router = Router()

class LoginFilter(BoundFilter):
    key = 'is_loginned'

    def __init__(self, is_login):
        self.is_login = is_login

    async def check(self, message: types.Message) -> bool:
        user_id = message.from_user.id
        if not user_id:
            return False  

        with open('users.json', 'r') as file:
            users = json.load(file)

        for user in users:
            if user.get('id') == user_id:
                return True 
        return False


class LoginState(State):
    waiting_for_password = State()
    

@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Вітаю, {message.from_user.name}!\nНапишіть /login для отримання доступу")


@router.message(Command('login'))
async def login_start(message: Message, state: FSMContext):
    await set_state(LoginState.waiting_for_password)
    await message.answer("Будь ласка, введіть пароль")


@router.message(state=LoginState.waiting_for_password)
async def login_password(message: Message, state: FSMContext):
    password = message.text.strip()
    if password == os.getenv('PASSWORD'):
        user_data = {
            "id": message.from_user.id,
            "full_name": message.from_user.full_name
        }
        save_user_data(user_data)
        await message.answer("Успішний вхід!")
        await state.finish()
    else:
        await message.answer("Пароль невірний. Спробуйте ще раз.")


@router.message(LoginFilter(is_loginned=True), Command("get_rates"))
async def get_rates(message: Message) -> Any:
    # Відправляєм користувачу курси валют
    pass


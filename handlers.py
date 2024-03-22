from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command, BoundFilter
from dotenv import load_dotenv, find_dotenv
import json

load_dotenv(find_dotenv())
router = Router()

class loginFilter(BoundFilter):
    key = 'is_loginned'

    def __init__(self, is_login):
        self.is_login = is_login

    async def check(self, message: types.Message) -> bool:
        pass


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Вітаю, {message.from_user.name}!")
        user_data = {
            "id": message.from_user.id,
            "full_name": message.from_user.full_name
        }
        save_user_data(user_data)


@router.message(loginFilter(True), Command("get_rates"))
async def get_rates(message: Message) -> Any:
    await message.answer('У вас є доступ до курсів валют!')


@router.message()
async def handle_password(message: Message):
    if message.text == os.getenv('PASSWORD'):

        await message.answer("Доступ надано.")
    else:
        await message.answer("Невірний пароль, спробуйте ще раз.")

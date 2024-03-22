from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv, find_dotenv
from loginfilter import isLoginned

load_dotenv(find_dotenv())
router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Вітаю, {message.from_user.name}!")


@router.message(isLoginned(True), Command("get_rates"))
async def get_rates(message: Message) -> Any:
    awai message.answer('У вас є доступ до курсу валют!')


@router.message()
async def handle_password(message: Message):
    if message.text == os.getenv('PASSWORD'):
        user_data = {
            "id": message.from_user.id,
            "full_name": message.from_user.full_name
        }
        
        save_user_data(user_data)

        await message.answer("Доступ надано.")
    else:
        await message.answer("Невірний пароль, спробуйте ще раз.")

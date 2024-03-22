from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart, Command
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
router = Router()


@router.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Вітаю, {message.from_user.name}, я щодня о 17:30 надсилаю актульні курси валют!")


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

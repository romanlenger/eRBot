from aiogram.filters import Filter
from .variables import USERS_FILE
from aiogram.types import Message
import json
import os


class LoginFilter(Filter):
    def __init__(self, is_login) -> None:
        self.is_login = is_login
        
    async def __call__(self, message: Message) -> bool:
        if os.path.exists(r'D:\DALNOBOY\exchange_rates\app\users.json'):
            with open(r'D:\DALNOBOY\exchange_rates\app\users.json', 'r') as file:
                users = json.load(file)
                for user in users:
                    if user.get('id') == int(message.from_user.id):
                        return True
        return False
            


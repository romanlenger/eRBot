from aiogram.filters import Filter
from .variables import USERS_FILE
from aiogram.types import Message
import json
import os


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
            


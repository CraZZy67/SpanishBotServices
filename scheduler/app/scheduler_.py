import requests
from aiogram import Bot

import asyncio
import os
import pycountry
from datetime import datetime, timedelta

from db.queries import get_user, update_status, get_users
from settings import Settings


class Scheduler:
    bot = Bot(token=os.getenv('TOKEN'))


    @staticmethod
    def check_user(user: int) -> bool:
        user_ = get_user(user=user)

        if user_.status != 'expiry':
            if datetime.fromisoformat(user_.expiry) > datetime.now():
                return True
            else:
                update_status(user=user, status='expiry')
                return False
        else:
            return False
    
    @staticmethod
    def get_combinations(format: str) -> dict:
        combinations = dict()

        for dialect in Settings.DIALECTS:
            combinations.update({dialect: {}})
            for level in Settings.LEVELS:
                combinations[dialect].update({level: {}})
                for translation in Settings.TRANSLEITS:
                    data = {
                        'format': format,
                        'countries': dialect,
                        'language': translation,
                        'level': level
                    }

                    response = requests.post(Settings.URL, data=data).json()

                    combinations[dialect][level].update({translation: response['answer']})
        
        return combinations
    
    @staticmethod
    def decode_info(user: tuple):
        level = 'A1-A2' if not user[5] else 'B1-C2'

        tuple_ = (
            user[0],
            user[1],
            user[2],
            user[3],
            pycountry.languages.get(alpha_2=user[4]),
            level,
            pycountry.countries.get(alpha_2=user[6]),
        )
        return tuple_
    
    @classmethod
    async def start(cls):
        while True:
            for topic in Settings.TOPICS:
                tomorrow = datetime.now() + timedelta(days=1)
                tomorrow.time = Settings.CONTENT_TIME

                diff = tomorrow - datetime.now()

                await asyncio.sleep(float(diff.hour * 60 * 60))
                combinations = cls.get_combinations(format=topic)
                
                tomorrow.time = Settings.POST_TIME
                diff = tomorrow - datetime.now()

                await asyncio.sleep(float(diff.hour * 60 * 60))
                for user in get_users():
                    user = cls.decode_info(user=user.tuple())
                    if cls.check_user(user.tuple()[1]):
                        text = combinations[user[6]][user[5]][user[4]]

                        await cls.bot.send_message(chat_id=user.tuple()[1], text=text, parse_mode='Markdown')




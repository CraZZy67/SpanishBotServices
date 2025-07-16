import requests
from aiogram import Bot
from aiogram.types import FSInputFile
from aiogram.enums.parse_mode import ParseMode

import asyncio
import os
import re
import pycountry
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta

from db.queries import get_user, update_status, get_users
from provider import Provider
from settings import Settings
from logger import main_logger


class Scheduler:
    bot = Bot(token=os.getenv('TOKEN'))
    
    @staticmethod
    def check_user(user: int) -> str:
        user_ = get_user(user=user)

        if user_[0].status != 'Expiry':
            if user_[0].expiry > datetime.now():
                return user_[0].status
            else:
                update_status(user=user_[0].user_id, status='Expiry')
                return ''
        else:
            return False

    @staticmethod
    def decode_info(user):
        main_logger.debug(f'User decode: {user.user_id}')

        level = 'A1-A2' if not user.level else 'B1-C2'

        tuple_ = (
            user.user_id,
            user.first_name,
            user.last_name,
            pycountry.languages.get(alpha_2=user.locale).name,
            level,
            pycountry.countries.get(alpha_2=user.elc.split(',')[0]).name,
        )
        return tuple_

    @classmethod
    def escape_markdown_v2(cls, text: str, keep_formatting=True):
        special_chars = r"_*[]()~`>#+-=|{}.!\\"

        if keep_formatting:
            
            formatting_patterns = [
                r'(\*{1,3})(.+?)\1',       
                r'(_{1,3})(.+?)\1',         
                r'(\|\|)(.+?)\1',         
                r'(`+)(.+?)\1',             
            ]

            placeholders = []

            def placeholder_sub(match):
                placeholders.append(match.group(0))
                return f"\u0000{len(placeholders)-1}\u0000"

            for pattern in formatting_patterns:
                text = re.sub(pattern, placeholder_sub, text)

            text = re.sub(f'([{re.escape(special_chars)}])', r'\\\1', text)

            for i, original in enumerate(placeholders):
                text = text.replace(f"\u0000{i}\u0000", original)

            return text
        else:
            return re.sub(f'([{re.escape(special_chars)}])', r'\\\1', text)
    
    @classmethod
    async def start(cls):
        while True:
            for topic in Settings.TOPICS:
                tomorrow = datetime.now(ZoneInfo("Europe/Moscow"))

                tomorrow = tomorrow.replace(hour=Settings.CONTENT_TIME.hour, minute=Settings.CONTENT_TIME.minute)

                diff = tomorrow - datetime.now(ZoneInfo("Europe/Moscow"))

                if diff.total_seconds() < 0:
                    tomorrow = datetime.now(ZoneInfo("Europe/Moscow")) + timedelta(days=1)
                    tomorrow = tomorrow.replace(hour=Settings.CONTENT_TIME.hour, minute=Settings.CONTENT_TIME.minute)
                    diff = tomorrow - datetime.now(ZoneInfo("Europe/Moscow"))

                main_logger.debug(f'Разница 1: {diff.total_seconds()}')

                await asyncio.sleep(diff.total_seconds())
                Provider.generate_combinations(format=topic)
                
                tomorrow = tomorrow.replace(hour=Settings.POST_TIME.hour, minute=Settings.POST_TIME.minute)

                diff = tomorrow - datetime.now(ZoneInfo("Europe/Moscow"))
                main_logger.debug(f'Разница 2: {diff.total_seconds()}')

                await asyncio.sleep(diff.total_seconds())
                for user in get_users():
                    user = cls.decode_info(user=user[0])
                    if cls.check_user(user[0]):
                        texts = Provider.get_text(user=user, user_status=cls.check_user(user[0]))

                        for text in texts:
                            await cls.bot.send_message(chat_id=user[0], text=text, parse_mode=ParseMode.MARKDOWN)
                    
                tomorrow = tomorrow.replace(hour=Settings.VIDEO_TIME.hour, minute=Settings.VIDEO_TIME.minute)

                diff = tomorrow - datetime.now(ZoneInfo("Europe/Moscow"))
                main_logger.debug(f'Разница 3: {diff.total_seconds()}')

                await asyncio.sleep(diff.total_seconds())

                response = requests.get(Settings.VIDEO_URL)
                for user in get_users():
                    user = cls.decode_info(user=user[0])
                    if cls.check_user(user[0]):
                        with open('video.mp4', 'wb') as file:
                            file.write(response.content)

                        await cls.bot.send_video(chat_id=user[0], video=FSInputFile(path='video.mp4', filename='video.mp4'))
                        os.remove('video.mp4')


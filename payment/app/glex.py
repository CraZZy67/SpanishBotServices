from aiogram import Bot

import os


token = os.getenv('TOKEN')

bot = Bot(token=token)
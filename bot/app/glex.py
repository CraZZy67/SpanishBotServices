from aiogram import Bot
from dotenv import load_dotenv

import os


load_dotenv(override=True)

token = os.getenv('TOKEN')

bot = Bot(token=token)
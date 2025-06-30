from aiogram import Bot
from dotenv import load_dotenv

import os


token = os.getenv('TOKEN')

bot = Bot(token=token)
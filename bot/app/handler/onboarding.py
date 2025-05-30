from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from settings import Settings
from keyboard.onboarding_kb import start_kb


onboarding_router = Router()

@onboarding_router.message(CommandStart())
async def start(message: Message):
    await message.answer(Settings.START_TEXT, reply_markup=start_kb())
